import os
import numpy as np
from time import sleep
from typing import Optional
from volstreet import config
from threading import Thread
from functools import partial
from datetime import datetime, timedelta, time
from volstreet.config import logger
from volstreet.utils.core import (
    current_time,
    find_strike,
    time_to_expiry,
    check_for_weekend,
    calculate_ema,
    convert_exposure_to_lots,
)
from volstreet.utils.communication import notifier, log_error
from volstreet.utils.data_io import save_json_data
from volstreet.exceptions import IntrinsicValueError
from volstreet.blackscholes import simulate_price, calculate_strangle_iv
from volstreet.angel_interface.interface import (
    fetch_book,
    lookup_and_return,
    fetch_historical_prices,
)
from volstreet.angel_interface.active_session import ActiveSession
from volstreet.trade_interface import (
    Strangle,
    Straddle,
    Action,
    OptionType,
    Option,
    Index,
    Stock,
    IndiaVix,
    place_option_order_and_notify,
    execute_instructions,
    cancel_pending_orders,
)
from volstreet.strategies.helpers import (
    sleep_until_next_action,
    round_shares_to_lot_size,
    get_above_below_strangles_with_prices,
    disparity_calculator,
    most_equal_strangle,
    DeltaPosition,
    TrendPosition,
    PositionMonitor,
    load_current_strangle,
    approve_execution,
    process_stop_loss_order_statuses,
)
from volstreet.strategies.tools import execute_single_instrument
from volstreet.strategies.strategy_modifiers import exit_handler

if config.backtest_mode:
    from volstreet.backtests.proxy_functions import (
        execute_instructions,
        sleep_until_next_action,
        exit_handler,
    )


@exit_handler
def delta_hedged_strangle(
    underlying: Index | Stock,
    exposure: int | float,
    delta_threshold_pct: float = 0.04,
    target_delta: float = 0.1,
    delta_cutoff: float = 0.65,
    optimized: bool = True,
    optimize_gamma: bool = False,
    theta_time_jump_hours: float = 1,  # In hours
    delta_interval_minutes: int | float = 1,
    interrupt: bool = False,
    hedge_margin: float | None = None,  # eg 0.2
    exit_time: Optional[tuple] = (15, 29),
    use_cache: Optional[bool] = True,
    at_market: bool = False,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Delta hedged strangle",
    data_directory: Optional[str] = None,
):
    """Theta time jump is defined in hours. Delta interval is in minutes. Delta threshold is in percentage terms
    eg: 0.02 for 2%
    """

    # Setting the exposure
    if hedge_margin is None:
        base_exposure = exposure
    else:
        base_exposure = exposure / (1 + hedge_margin)

    # Entering the main function
    if time(*exit_time) < current_time().time():
        notifier(
            f"{underlying.name} {strategy_tag} not being deployed after exit time",
            notification_url,
            "INFO",
        )
        return

    # Setting the exit time
    if time_to_expiry(underlying.current_expiry, in_days=True) < 1:
        exit_time = min([tuple(exit_time), (14, 40)])
        logger.info(
            f"{underlying.name} exit time changed to {exit_time} because expiry is today"
        )

    # Setting caching
    underlying.caching = use_cache

    # Setting the initial position size
    spot_price = underlying.fetch_ltp()
    max_qty_shares = round_shares_to_lot_size(
        exposure / spot_price, underlying.lot_size
    )
    base_qty_shares = round_shares_to_lot_size(
        base_exposure / spot_price, underlying.lot_size
    )

    # Setting the delta threshold
    delta_adjustment_threshold = delta_threshold_pct * base_qty_shares
    starting_message = (
        f"{underlying.name} {strategy_tag}, "
        f"exposure: {exposure}, "
        f"max qty: {max_qty_shares}, "
        f"base qty: {base_qty_shares}, "
        f"delta threshold: {delta_adjustment_threshold}. "
    )
    notifier(starting_message, notification_url, "INFO")

    # Setting the file path
    date = current_time().strftime("%d-%m-%Y")
    if data_directory is None:
        file_path = f"{ActiveSession.obj.userId}\\{underlying.name.lower()}_delta_data\\{date}.json"
    else:
        file_path = os.path.join(data_directory, f"{date}.json")

    delta_position: DeltaPosition = DeltaPosition(
        underlying=underlying,
        base_exposure_qty=base_qty_shares,
        greek_settings={"theta_time_jump": theta_time_jump_hours / (365 * 24)},
        order_tag=strategy_tag,
        notifier_url=notification_url,
        file_path=file_path,
    )
    delta_position.set_all_options(use_cache)
    while current_time().time() < time(*exit_time):
        delta_position.update_underlying()
        delta_position.set_recommended_qty(
            target_delta, delta_cutoff, optimized, optimize_gamma
        )
        delta_position.adjust_recommended_qty()
        delta_position.enter_positions(at_market=at_market)
        delta_position.reset_trigger_flags()

        def interruption_condition():
            # Hard coded 15% of base qty shares as the threshold for interruption
            condition_1 = (
                (
                    abs(delta_position.aggregate_greeks().delta)
                    >= (0.15 * base_qty_shares)
                )
                if interrupt
                else False
            )
            condition_2 = False  # todo: Add a condition that always maximizes Theta
            return condition_1 or condition_2

        # Delta hedging begins here
        while not any(delta_position.exit_triggers.values()):
            sleep_until_next_action(
                delta_interval_minutes,
                exit_time,
                interruption_condition=interruption_condition,
            )
            try:
                delta_position.record_position_status()
            except Exception as e:
                notifier(
                    f"{underlying.name} Error while recording position status: {e}\n"
                    f"Traceback: {e.__traceback__}",
                    notification_url,
                    "ERROR",
                )
                delta_position.record_position_status = lambda: None

            if current_time().time() >= time(*exit_time):
                delta_position.exit_triggers["end_time"] = True
                break

            delta_position.update_underlying()
            aggregate_delta: float = (
                delta_position.aggregate_greeks().delta
            )  # The prices and greeks of the options are updated and cached here

            #  If aggregate delta breaches the threshold then adjust
            if abs(aggregate_delta) > delta_adjustment_threshold:
                message = (
                    f"{underlying.name} delta needs adjustment. "
                    f"Delta: {aggregate_delta}, "
                    f"Threshold: {delta_adjustment_threshold}"
                )
                logger.info(message)
                # If we are hedging with atm options
                if hedge_margin is not None:
                    delta_position.set_hedge_options()
                    hedge_option, qty_to_hedge = delta_position.recommend_delta_action(
                        delta_adjustment_threshold,
                        aggregate_delta,
                    )
                    if hedge_option:
                        # Check for breach
                        breach = delta_position.check_for_breach(
                            hedge_option.option_type, abs(qty_to_hedge), max_qty_shares
                        )

                        if not breach:
                            hedge_option.execute_order(
                                qty_to_hedge,
                                hedge_option.current_ltp,
                                strategy_tag,
                                notification_url,
                            )
                            message = (
                                f"{underlying.name} {strategy_tag} "
                                f"neutralized position with {hedge_option} "
                                f"qty: {qty_to_hedge}"
                            )
                            logger.info(message)
                            continue
                        else:
                            delta_position.exit_triggers["qty_breach_exit"] = True

                # We will end up here if we are not hedging with atm options or if there is a breach
                delta_position.exit_triggers["qty_breach_exit"] = True
                message = f"{underlying.name}. Shuffling position."
                logger.info(message)

    # Exiting the position
    message = f"{underlying.name} {strategy_tag} exit time reached."
    notifier(message, notification_url, "INFO")
    delta_position.exit_positions(at_market=at_market)


@exit_handler
def overnight_straddle(
    underlying: Index | Stock,
    exposure: int | float,
    call_strike_offset: Optional[float] = 0.02,
    put_strike_offset: Optional[float] = -0.02,
    take_avg_price: Optional[bool] = False,
    avg_till: Optional[tuple] = (15, 28),
    at_market: Optional[bool] = False,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Overnight straddle",
):
    """Rollover overnight short straddle to the next expiry.
    Args:
        underlying (Index | Stock): Underlying object.
        exposure (int | float): Exposure in rupees.
        call_strike_offset (float): Call strike offset in percentage terms. eg 0.02 for 2% above current price.
        put_strike_offset (float): Put strike offset in percentage terms. eg -0.02 for 2% below current price.
        take_avg_price (bool): Take average price of the index over 5m timeframes.
        avg_till (tuple): Time till which to average the price.
        at_market (bool): Whether to place market orders
        notification_url (str): Webhook URL to send notifications.
        strategy_tag (str): Tag to identify the strategy in the notification.
    """

    def is_next_day_expiry(tte: float) -> bool:
        return 1 < tte < 2

    def check_eligibility_for_overnight_straddle(effective_tte: float) -> bool:
        after_weekend = check_for_weekend(underlying.current_expiry)
        square_off_tte = (
            effective_tte - 1
        )  # Square off 1 day after because duration of the trade is 1 day

        logger.info(f"{underlying.name} current expiry tte is {effective_tte} days")

        if after_weekend:
            logger.info(f"{underlying.name} current expiry is after a weekend")
            return False

        if square_off_tte < 1:
            if is_next_day_expiry(effective_tte):
                logger.info(
                    f"{underlying.name} current expiry is next day so the trade is eligible on next expiry"
                )
                return True

            logger.info(
                f"{underlying.name} current expiry is today so the trade is not eligible"
            )
            return False

        logger.info(
            f"{underlying.name} current expiry has enough TTE to trade so the trade is eligible"
        )
        return True

    def get_expiry_to_trade_for_overnight_straddle(effective_tte: float) -> str:
        if is_next_day_expiry(effective_tte):
            return underlying.next_expiry
        return underlying.current_expiry

    # Entering main function
    quantity_in_lots = convert_exposure_to_lots(
        exposure, underlying.fetch_ltp(), underlying.lot_size, 10
    )

    effective_time_to_expiry = time_to_expiry(
        underlying.current_expiry, effective_time=True, in_days=True
    )
    eligible_for_short = check_eligibility_for_overnight_straddle(
        effective_time_to_expiry
    )

    # Taking avg price
    avg_ltp = None
    if take_avg_price:
        if current_time().time() < time(15, 00):
            notifier(
                f"{underlying.name} Cannot take avg price before 3pm. Try running the strategy after 3pm",
                notification_url,
                "ERROR",
            )
            raise Exception(
                "Cannot take avg price before 3pm. Try running the strategy after 3pm"
            )
        notifier(
            f"{underlying.name} Taking average price of the index over 5m timeframes.",
            notification_url,
            "INFO",
        )
        price_list = [underlying.fetch_ltp()]
        while current_time().time() < time(*avg_till):
            _ltp = underlying.fetch_ltp()
            price_list.append(_ltp)
            sleep(60)
        avg_ltp = np.mean(price_list)

    # Assigning vix
    vix = IndiaVix.fetch_ltp()

    # Initializing the straddle if eligible
    if eligible_for_short:
        # Assigning straddle with strike and expiry
        ltp = avg_ltp if avg_ltp else underlying.fetch_ltp()
        call_strike = find_strike(ltp, base=underlying.base, offset=call_strike_offset)
        put_strike = find_strike(ltp, base=underlying.base, offset=put_strike_offset)
        expiry_to_trade = get_expiry_to_trade_for_overnight_straddle(
            effective_time_to_expiry
        )
        sell_strangle = Strangle(
            call_strike, put_strike, underlying.name, expiry_to_trade
        )
        call_iv, put_iv, iv = sell_strangle.fetch_ivs()
        iv = iv * 100
        notifier(
            f"{underlying.name} Deploying overnight short straddle with {sell_strangle}. IV: {iv}, VIX: {vix}",
            notification_url,
            "INFO",
        )
    else:
        sell_strangle = None
        quantity_in_lots = 0
        notifier(
            f"{underlying.name} No straddle eligible for overnight short. VIX: {vix}",
            notification_url,
            "INFO",
        )

    # Loading current position
    buy_strangle, buy_quantity_in_lots = load_current_strangle(
        underlying_str=underlying.name,
        user_id=ActiveSession.obj.userId,
        file_appendix="overnight_positions",
    )

    notifier(
        f"{underlying.name} Exiting current position {buy_strangle}",
        notification_url,
        "INFO",
    )

    trade_info_dict = {
        "Date": current_time().strftime("%d-%m-%Y %H:%M:%S"),
        "Underlying": underlying.name,
    }

    call_buy_avg, put_buy_avg = np.nan, np.nan
    call_sell_avg, put_sell_avg = np.nan, np.nan

    # Placing orders
    if buy_strangle is None and sell_strangle is None:
        notifier(f"{underlying.name} No trade possible.", notification_url, "INFO")
    elif sell_strangle is None:  # only exiting current position
        execution_details = execute_instructions(
            {
                buy_strangle: {
                    "action": Action.BUY,
                    "quantity_in_lots": buy_quantity_in_lots,
                    "order_tag": strategy_tag,
                }
            },
            at_market=at_market,
        )
        call_buy_avg, put_buy_avg = execution_details[buy_strangle]

    elif buy_strangle is None:  # only entering new position
        execution_details = execute_instructions(
            {
                sell_strangle: {
                    "action": Action.SELL,
                    "quantity_in_lots": quantity_in_lots,
                    "order_tag": strategy_tag,
                }
            },
            at_market=at_market,
        )
        call_sell_avg, put_sell_avg = execution_details[sell_strangle]

    else:  # both entering and exiting positions
        if buy_strangle == sell_strangle:
            notifier(
                f"{underlying.name} Same straddle. No trade required.",
                notification_url,
                "INFO",
            )
            call_ltp, put_ltp = sell_strangle.fetch_ltp()
            call_buy_avg, put_buy_avg, call_sell_avg, put_sell_avg = (
                call_ltp,
                put_ltp,
                call_ltp,
                put_ltp,
            )
        else:
            execution_details = execute_instructions(
                {
                    buy_strangle: {
                        "action": Action.BUY,
                        "quantity_in_lots": buy_quantity_in_lots,
                        "order_tag": strategy_tag,
                    },
                    sell_strangle: {
                        "action": Action.SELL,
                        "quantity_in_lots": quantity_in_lots,
                        "order_tag": strategy_tag,
                    },
                },
                at_market=at_market,
            )
            call_buy_avg, put_buy_avg = execution_details[buy_strangle]
            call_sell_avg, put_sell_avg = execution_details[sell_strangle]

    trade_info_dict.update(
        {
            "Buy Straddle": buy_strangle,
            "Buy Call Price": call_buy_avg,
            "Buy Put Price": put_buy_avg,
            "Buy Total Price": call_buy_avg + put_buy_avg,
            "Sell Straddle": sell_strangle,
            "Sell Call Price": call_sell_avg,
            "Sell Put Price": put_sell_avg,
            "Sell Total Price": call_sell_avg + put_sell_avg,
        }
    )

    trade_data = {
        underlying.name: {
            "strangle": sell_strangle,
            "quantity": quantity_in_lots,
        }
    }
    save_json_data(
        trade_data,
        f"{ActiveSession.obj.userId}\\{underlying.name}_overnight_positions.json",
    )  # Currently overwriting the file with the new data. Can be changed to use load_combine_save_json_data
    # to append the new data to the existing data.


@exit_handler
def buy_weekly_hedge(
    underlying: Index | Stock,
    exposure: int | float,
    strike_offset: Optional[float] = 1,
    call_offset: Optional[float] = None,
    put_offset: Optional[float] = None,
    at_market: Optional[bool] = False,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Weekly hedge",
    override_expiry_day_restriction: Optional[bool] = False,
):
    """Buys next weeks strangle or straddle as a hedge. Offsets are the multipliers for the strike price.
    Example: 1.01 means 1.01 times the current price (1% above current price). If call_offset and put_offset are
    not provided, strike_offset is used for both call and put."""

    quantity_in_lots = convert_exposure_to_lots(
        exposure, underlying.fetch_ltp(), underlying.lot_size, 10
    )

    approved = approve_execution(
        underlying,
        override_expiry_day_restriction,
    )

    if not approved:
        notifier(
            f"{underlying.name} not eligible for weekly hedge since it is not expiry day",
            notification_url,
            "INFO",
        )
        return

    ltp = underlying.fetch_ltp()
    if call_offset and put_offset:
        pass
    elif strike_offset:
        call_offset = put_offset = strike_offset
    else:
        raise Exception("Either strike_offset or call_offset and put_offset required")

    call_strike = find_strike(ltp * call_offset, underlying.base)
    put_strike = find_strike(ltp * put_offset, underlying.base)
    instrument = Strangle(
        call_strike, put_strike, underlying.name, underlying.next_expiry
    )

    call_iv, put_iv, iv = instrument.fetch_ivs()
    notifier(
        f"{underlying.name} Buying weekly hedge with {instrument}. IV: {iv}",
        notification_url,
        "INFO",
    )
    execution_details = execute_instructions(
        {
            instrument: {
                "action": Action.BUY,
                "quantity_in_lots": quantity_in_lots,
                "order_tag": strategy_tag,
            }
        },
        at_market=at_market,
    )
    call_buy_avg, put_buy_avg = execution_details[instrument]

    trade_info_dict = {
        "Date": current_time().strftime("%d-%m-%Y %H:%M:%S"),
        "Underlying": underlying.name,
        "Buy Instrument": instrument,
        "Buy Call Price": call_buy_avg,
        "Buy Put Price": put_buy_avg,
        "Buy Total Price": call_buy_avg + put_buy_avg,
    }


@exit_handler
def biweekly_straddle(
    underlying: Index | Stock,
    exposure: int | float,
    strike_offset: Optional[float] = 1,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Biweekly straddle",
    override_expiry_day_restriction: Optional[bool] = False,
):
    """Sells the far expiry straddle."""

    quantity_in_lots = convert_exposure_to_lots(
        exposure, underlying.fetch_ltp(), underlying.lot_size, 10
    )

    approved = approve_execution(
        underlying,
        override_expiry_day_restriction,
    )

    if not approved:
        notifier(
            f"{underlying.name} not eligible for biweekly straddle since it is not expiry day",
            notification_url,
            "INFO",
        )
        return

    # Loading current position
    buy_straddle = load_current_strangle(
        underlying_str=underlying.name,
        user_id=ActiveSession.obj.userId,
        file_appendix="biweekly_position",
    )

    # Initializing new position
    ltp = underlying.fetch_ltp()
    strike = find_strike(ltp * strike_offset, underlying.base)
    expiry = underlying.far_expiry
    sell_straddle = Straddle(strike, underlying.name, expiry)
    call_iv, put_iv, iv = sell_straddle.fetch_ivs()
    notifier(
        f"{underlying.name} Deploying biweekly straddle\n"
        f"Square up position: {buy_straddle}\n"
        f"New position: {sell_straddle}\n"
        f"IV: {iv}",
        notification_url,
        "INFO",
    )

    order_instructions = {}

    if buy_straddle:
        order_instructions[buy_straddle] = {
            "action": Action.BUY,
            "quantity_in_lots": quantity_in_lots,
            "order_tag": strategy_tag,
        }

    order_instructions[sell_straddle] = {
        "action": Action.SELL,
        "quantity_in_lots": quantity_in_lots,
        "order_tag": strategy_tag,
    }

    execution_details = execute_instructions(order_instructions)
    call_sell_avg, put_sell_avg = execution_details[sell_straddle]
    call_buy_avg, put_buy_avg = execution_details.get(buy_straddle, (np.nan, np.nan))

    position_to_save = {underlying.name: {"strangle": sell_straddle}}
    save_json_data(
        position_to_save,
        f"{ActiveSession.obj.userId}\\{underlying.name}_biweekly_position.json",
    )  # Currently overwriting the file with the new data. Can use load_combine_save_json_data in the future
    # to append the new data to the existing data. (Use case: multiple indices using the same file)

    trade_info_dict = {
        "Date": current_time().strftime("%d-%m-%Y %H:%M:%S"),
        "Underlying": underlying.name,
        "Buy Straddle": buy_straddle,
        "Buy Call Price": call_buy_avg,
        "Buy Put Price": put_buy_avg,
        "Buy Total Price": call_buy_avg + put_buy_avg,
        "Sell Straddle": sell_straddle,
        "Sell Call Price": call_sell_avg,
        "Sell Put Price": put_sell_avg,
        "Sell Total Price": call_sell_avg + put_sell_avg,
    }


@exit_handler
def intraday_strangle(
    underlying: Index | Stock,
    exposure: int | float,
    call_strike_offset: Optional[float] = 0,
    put_strike_offset: Optional[float] = 0,
    strike_selection: Optional[str] = "equal",
    stop_loss: Optional[float | str] = "dynamic",
    call_stop_loss: Optional[float] = None,
    put_stop_loss: Optional[float] = None,
    combined_stop_loss: Optional[float] = None,
    exit_time: tuple[int, int] = (15, 29),
    sleep_time: Optional[int] = 5,
    seconds_to_avg: Optional[int] = 30,
    simulation_safe_guard: Optional[float] = 1.15,
    catch_trend: Optional[bool] = False,
    trend_qty_ratio: Optional[float] = 1,
    disparity_threshold: Optional[float] = 1000,
    place_sl_orders: Optional[bool] = False,
    move_sl_to_cost: Optional[bool] = False,
    place_orders_on_sl: Optional[bool] = False,
    convert_to_butterfly: Optional[bool] = False,
    conversion_method: Optional[str] = "pct",
    conversion_threshold_pct: Optional[float] = 0.175,
    take_profit: Optional[float] = 0,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Intraday strangle",
):
    """Intraday strangle strategy. Trades strangle with stop loss. All offsets are in percentage terms.
    Parameters
    ----------
    underlying : Index | Stock
        Underlying object
    exposure : int | float
        Exposure in rupees
    strike_selection : str, optional {'equal', 'resilient', 'atm'}
        Mode for finding the strangle, by default 'equal'
    call_strike_offset : float, optional
        Call strike offset in percentage terms, by default 0
    put_strike_offset : float, optional
        Put strike offset in percentage terms, by default 0
    stop_loss : float or string, optional
        Stop loss percentage, by default 'dynamic'
    call_stop_loss : float, optional
        Call stop loss percentage, by default None. If None then stop loss is same as stop_loss.
    put_stop_loss : float, optional
        Put stop loss percentage, by default None. If None then stop loss is same as stop_loss.
    combined_stop_loss : float, optional
        Combined stop loss percentage, by default None. If None then individual stop losses are used.
    exit_time : tuple, optional
        Exit time, by default (15, 29)
    sleep_time : int, optional
        Sleep time in seconds for updating prices, by default 5
    seconds_to_avg : int, optional
        Seconds to average prices over, by default 30
    simulation_safe_guard : float, optional
        The multiple over the simulated price that will reject stop loss, by default 1.15
    catch_trend : bool, optional
        Catch trend or not, by default False
    trend_qty_ratio : int, optional
        Ratio of trend quantity to strangle quantity, by default 1
    disparity_threshold : float, optional
        Disparity threshold for equality of strikes, by default np.inf
    place_sl_orders : bool, optional
        Place stop loss orders or not, by default False
    move_sl_to_cost : bool, optional
        Move other stop loss to cost or not, by default False
    place_orders_on_sl : bool, optional
        Place orders on stop loss or not, by default False
    convert_to_butterfly : bool, optional
        Convert to butterfly or not, by default False
    conversion_method : str, optional
        Conversion method for butterfly, by default 'breakeven'
    conversion_threshold_pct : float, optional
        Conversion threshold for butterfly if conversion method is 'pct', by default 0.175
    take_profit : float, optional
        Take profit percentage, by default 0
    notification_url : str, optional
        URL for sending notifications, by default None
    strategy_tag : str, optional
        Strategy tag for logging, by default 'Intraday strangle'
    """

    @log_error(notify=True, raise_error=True)
    def position_monitor(info_dict):
        c_avg_price = info_dict["call_avg_price"]
        p_avg_price = info_dict["put_avg_price"]
        traded_strangle = info_dict["traded_strangle"]

        # EMA parameters
        periods = max(int(seconds_to_avg / sleep_time), 1) if sleep_time >= 1 else 1
        alpha = 2 / (periods + 1)
        ema_values = {
            "call": None,
            "put": None,
            "underlying": None,
        }

        # Conversion to butterfly settings
        ctb_notification_sent = False
        ctb_message = ""
        ctb_hedge = None
        conversion_threshold_break_even = None

        def process_ctb(
            h_strangle: Strangle,
            method: str,
            threshold_break_even: float,
            threshold_pct: float,
            total_price: float,
        ) -> bool:
            hedge_total_ltp = h_strangle.fetch_total_ltp()

            if method == "breakeven":
                hedge_profit = total_price - hedge_total_ltp - underlying.base
                return hedge_profit >= threshold_break_even

            elif method == "pct":
                if (
                    total_price - (hedge_total_ltp + underlying.base)
                    < threshold_break_even
                ):
                    return False  # Ensuring that this is better than break even method
                return hedge_total_ltp <= total_price * threshold_pct

            else:
                raise ValueError(
                    f"Invalid conversion method: {method}. Valid methods are 'breakeven' and 'pct'."
                )

        if convert_to_butterfly:
            ctb_call_strike = traded_strangle.call_strike + underlying.base
            ctb_put_strike = traded_strangle.put_strike - underlying.base
            ctb_hedge = Strangle(
                ctb_call_strike, ctb_put_strike, underlying.name, expiry
            )
            c_sl = call_stop_loss if call_stop_loss is not None else stop_loss
            p_sl = put_stop_loss if put_stop_loss is not None else stop_loss
            profit_if_call_sl = p_avg_price - (c_avg_price * (c_sl - 1))
            profit_if_put_sl = c_avg_price - (p_avg_price * (p_sl - 1))

            conversion_threshold_break_even = max(profit_if_call_sl, profit_if_put_sl)

        threshold_points = (
            (take_profit * (c_avg_price + p_avg_price)) if take_profit > 0 else np.inf
        )

        last_print_time = current_time()
        last_log_time = current_time()
        last_notify_time = current_time()
        print_interval = timedelta(seconds=10)
        log_interval = timedelta(minutes=25)
        notify_interval = timedelta(minutes=180)

        while not info_dict["trade_complete"]:
            # Fetching prices
            spot_price = underlying.fetch_ltp()
            c_ltp, p_ltp = traded_strangle.fetch_ltp()
            info_dict["underlying_ltp"] = spot_price
            info_dict["call_ltp"] = c_ltp
            info_dict["put_ltp"] = p_ltp

            # Calculate EMA for each series
            for series, price in zip(
                ["call", "put", "underlying"], [c_ltp, p_ltp, spot_price]
            ):
                ema_values[series] = calculate_ema(price, ema_values[series], alpha)

            c_ltp_avg = ema_values["call"]
            p_ltp_avg = ema_values["put"]
            spot_price_avg = ema_values["underlying"]

            info_dict["call_ltp_avg"] = c_ltp_avg
            info_dict["put_ltp_avg"] = p_ltp_avg
            info_dict["underlying_ltp_avg"] = spot_price_avg

            # Combined stop loss detection
            if combined_stop_loss is not None and not np.isnan(combined_stop_loss):
                if (c_ltp_avg + p_ltp_avg) > info_dict["combined_stop_loss_price"]:
                    info_dict["exit_triggers"].update({"combined_stop_loss": True})
                    notifier(
                        f"{underlying.name} Combined stop loss triggered with "
                        f"combined price of {c_ltp_avg + p_ltp_avg}",
                        notification_url,
                        "INFO",
                    )

            # Calculate IV
            call_iv, put_iv, avg_iv = calculate_strangle_iv(
                call_price=c_ltp,
                put_price=p_ltp,
                call_strike=traded_strangle.call_strike,
                put_strike=traded_strangle.put_strike,
                spot=spot_price,
                time_left=time_to_expiry(expiry),
            )
            info_dict["call_iv"] = call_iv
            info_dict["put_iv"] = put_iv
            info_dict["avg_iv"] = avg_iv

            # Calculate mtm price
            call_exit_price = info_dict.get("call_exit_price", c_ltp)
            put_exit_price = info_dict.get("put_exit_price", p_ltp)
            mtm_price = call_exit_price + put_exit_price

            # Calculate profit
            profit_in_pts = (c_avg_price + p_avg_price) - mtm_price
            profit_in_rs = profit_in_pts * underlying.lot_size * quantity_in_lots
            info_dict["profit_in_pts"] = profit_in_pts
            info_dict["profit_in_rs"] = profit_in_rs

            if take_profit > 0:
                if profit_in_pts >= threshold_points:
                    info_dict["exit_triggers"].update({"take_profit": True})
                    notifier(
                        f"{underlying.name} Take profit triggered with profit of {profit_in_pts} points",
                        notification_url,
                        "INFO",
                    )

            # Conversion to butterfly working
            if (
                not (info_dict["call_sl"] or info_dict["put_sl"])
                and info_dict["time_left_day_start"] * 365 < 1
                and convert_to_butterfly
                and not ctb_notification_sent
                and current_time().time() < time(14, 15)
            ):
                try:
                    ctb_trigger = process_ctb(
                        ctb_hedge,
                        conversion_method,
                        conversion_threshold_break_even,
                        conversion_threshold_pct,
                        info_dict["total_avg_price"],
                    )
                    if ctb_trigger:
                        notifier(
                            f"{underlying.name} Convert to butterfly triggered\n",
                            notification_url,
                            "INFO",
                        )
                        info_dict["exit_triggers"].update(
                            {"convert_to_butterfly": True}
                        )
                        ctb_message = f"Hedged with: {ctb_hedge}\n"
                        info_dict["ctb_hedge"] = ctb_hedge
                        ctb_notification_sent = True
                except Exception as _e:
                    logger.error(f"Error in process_ctb: {_e}")

            message = (
                f"\nUnderlying: {underlying.name}\n"
                f"Time: {current_time(): %d-%m-%Y %H:%M:%S}\n"
                f"Underlying LTP: {spot_price}\n"
                f"Call Strike: {traded_strangle.call_strike}\n"
                f"Put Strike: {traded_strangle.put_strike}\n"
                f"Call Price: {c_ltp}\n"
                f"Put Price: {p_ltp}\n"
                f"MTM Price: {mtm_price}\n"
                f"Call last n avg: {c_ltp_avg}\n"
                f"Put last n avg: {p_ltp_avg}\n"
                f"IVs: {call_iv}, {put_iv}, {avg_iv}\n"
                f"Call SL: {info_dict['call_sl']}\n"
                f"Put SL: {info_dict['put_sl']}\n"
                f"Profit Pts: {info_dict['profit_in_pts']:.2f}\n"
                f"Profit: {info_dict['profit_in_rs']:.2f}\n" + ctb_message
            )
            if current_time() - last_print_time > print_interval:
                print(message)
                last_print_time = current_time()
            if current_time() - last_log_time > log_interval:
                logger.info(message)
                last_log_time = current_time()
            if current_time() - last_notify_time > notify_interval:
                notifier(message, notification_url, "INFO")
                last_notify_time = current_time()
            sleep(sleep_time)

    @log_error(raise_error=True, notify=True)
    def trend_catcher(info_dict, sl_type, qty_ratio):

        def check_trade_eligibility(option, price):
            if option.fetch_ltp() > price * 0.70:
                return True

        traded_strangle = info_dict["traded_strangle"]
        og_price = (
            info_dict["call_avg_price"]
            if sl_type == "put"
            else info_dict["put_avg_price"]
        )
        trend_option = (
            traded_strangle.call_option
            if sl_type == "put"
            else traded_strangle.put_option
        )

        qty_in_lots = max(int(quantity_in_lots * qty_ratio), 1)

        while not check_trade_eligibility(
            trend_option, og_price
        ) and current_time().time() < time(*exit_time):
            logger.info(f"Waiting for trend option to reach 70% of original price")
            sleep(sleep_time)

        # Placing the trend option order
        exec_details = execute_instructions(
            {
                trend_option: {
                    "action": Action.SELL,
                    "quantity_in_lots": qty_in_lots,
                    "order_tag": f"{strategy_tag} Trend Catcher",
                }
            }
        )
        sell_avg_price = exec_details[trend_option]

        # Setting up the stop loss on the trend option

        trend_sl_hit = False
        notifier(
            f"{underlying.name} strangle {sl_type} trend catcher starting. "
            f"Placed {qty_in_lots} lots of {trend_option} at {sell_avg_price}. "
            f"Stoploss prices: {og_price}",
            notification_url,
            "INFO",
        )

        last_print_time = current_time()
        print_interval = timedelta(seconds=10)
        while all(
            [
                current_time().time() < time(*exit_time),
                not info_dict["trade_complete"],
            ]
        ):
            option_price = trend_option.fetch_ltp()
            trend_sl_hit = option_price >= og_price
            if trend_sl_hit:
                break
            sleep(sleep_time)
            if current_time() - last_print_time > print_interval:
                last_print_time = current_time()
                logger.info(
                    f"{underlying.name} {sl_type} trend catcher running\n"
                    f"Stoploss price: {og_price}\n"
                )

        if trend_sl_hit:
            notifier(
                f"{underlying.name} strangle {sl_type} trend catcher stoploss hit.",
                notification_url,
                "INFO",
            )
            square_off = True
        else:
            notifier(
                f"{underlying.name} strangle {sl_type} trend catcher exiting.",
                notification_url,
                "INFO",
            )
            if info_dict["time_left_day_start"] * 365 < 1:  # expiry day
                square_off = False
            else:
                square_off = True

        if square_off:
            # Buying the trend option back
            exec_details = execute_instructions(
                {
                    trend_option: {
                        "action": Action.BUY,
                        "quantity_in_lots": qty_in_lots,
                        "order_tag": f"{strategy_tag} Trend Catcher",
                    }
                }
            )
            square_up_avg_price = exec_details[trend_option]
        else:
            square_up_avg_price = trend_option.fetch_ltp()

        points_captured = sell_avg_price - square_up_avg_price
        info_dict["trend_catcher_points_captured"] = points_captured

    def justify_stop_loss(info_dict, side):
        entry_spot = info_dict.get("spot_at_entry")
        current_spot = info_dict.get("underlying_ltp")
        stop_loss_price = info_dict.get(f"{side}_stop_loss_price")

        time_left_day_start = info_dict.get("time_left_day_start")
        time_left_now = time_to_expiry(expiry)
        time_delta_minutes = (time_left_day_start - time_left_now) * 525600
        time_delta_minutes = int(time_delta_minutes)
        time_delta_minutes = min(
            time_delta_minutes, 300
        )  # Hard coded number. At most 300 minutes and not more.
        try:
            simulated_option_price = simulate_price(
                strike=(
                    info_dict.get("traded_strangle").call_strike
                    if side == "call"
                    else info_dict.get("traded_strangle").put_strike
                ),
                flag=side,
                original_atm_iv=info_dict.get("atm_iv_at_entry"),
                original_spot=entry_spot,
                original_time_to_expiry=time_left_day_start,
                new_spot=current_spot,
                time_delta_minutes=time_delta_minutes,
            )
        except (Exception, IntrinsicValueError) as ex:
            error_message = (
                f"Error in justify_stop_loss for {underlying.name} {side} strangle: {ex}\n"
                f"Setting stop loss to True"
            )
            logger.error(error_message)
            notifier(error_message, notification_url, "ERROR")
            return True

        actual_price = info_dict.get(f"{side}_ltp_avg")
        unjust_increase = (
            actual_price / simulated_option_price > simulation_safe_guard
            and simulated_option_price < stop_loss_price
        )
        if unjust_increase:
            if not info_dict.get(f"{side}_sl_check_notification_sent"):
                message = (
                    f"{underlying.name} strangle {side} stop loss appears to be unjustified. "
                    f"Actual price: {actual_price}, Simulated price: {simulated_option_price}"
                )
                notifier(message, notification_url, "CRUCIAL")
                info_dict[f"{side}_sl_check_notification_sent"] = True

            # Additional check for unjustified stop loss (forcing stoploss to trigger even if unjustified only if
            # the price has increased by more than 2 times AND spot has moved by more than 0.5%)
            spot_change = (current_spot / entry_spot) - 1
            spot_moved = (
                spot_change > 0.012 if side == "call" else spot_change < -0.0035
            )  # Hard coded number
            if (
                spot_moved and (actual_price / stop_loss_price) > 1.6
            ):  # Hard coded number
                message = (
                    f"{underlying.name} strangle {side} stop loss forced to trigger due to price increase. "
                    f"Price increase from stop loss price: {actual_price / simulated_option_price}"
                )
                notifier(message, notification_url, "CRUCIAL")
                return True
            else:
                return False
        else:
            message = (
                f"{underlying.name} strangle {side} stop loss triggered. "
                f"Actual price: {actual_price}, Simulated price: {simulated_option_price}"
            )
            notifier(message, notification_url, "CRUCIAL")
            return True

    def check_for_stop_loss(info_dict, side):
        """Check for stop loss."""

        stop_loss_order_ids = info_dict.get(f"{side}_stop_loss_order_ids")

        if stop_loss_order_ids is None:  # If stop loss order ids are not provided
            ltp_avg = info_dict.get(f"{side}_ltp_avg", info_dict.get(f"{side}_ltp"))
            stop_loss_price = info_dict.get(f"{side}_stop_loss_price")
            stop_loss_triggered = ltp_avg > stop_loss_price
            if stop_loss_triggered:
                stop_loss_justified = justify_stop_loss(info_dict, side)
                if stop_loss_justified:
                    info_dict[f"{side}_sl"] = True

        else:  # If stop loss order ids are provided
            orderbook = fetch_book("orderbook")
            orders_triggered, orders_complete = process_stop_loss_order_statuses(
                orderbook,
                stop_loss_order_ids,
                context=side,
                notify_url=notification_url,
            )
            if orders_triggered:
                justify_stop_loss(info_dict, side)
                info_dict[f"{side}_sl"] = True
                if not orders_complete:
                    info_dict[f"{side}_stop_loss_order_ids"] = None

    def process_stop_loss(info_dict, sl_type):
        if (
            info_dict["call_sl"] and info_dict["put_sl"]
        ):  # Check to avoid double processing
            return

        traded_strangle = info_dict["traded_strangle"]
        other_side: str = "call" if sl_type == "put" else "put"

        # Buying the stop loss option back if it is not already bought
        if info_dict[f"{sl_type}_stop_loss_order_ids"] is None:
            option_to_buy = (
                traded_strangle.call_option
                if sl_type == "call"
                else traded_strangle.put_option
            )
            exec_details = execute_instructions(
                {
                    option_to_buy: {
                        "action": Action.BUY,
                        "quantity_in_lots": quantity_in_lots,
                        "order_tag": strategy_tag,
                    }
                }
            )
            exit_price = exec_details[option_to_buy]

        else:
            orderbook = fetch_book("orderbook")
            exit_price = (
                lookup_and_return(
                    orderbook,
                    "orderid",
                    info_dict[f"{sl_type}_stop_loss_order_ids"],
                    "averageprice",
                )
                .astype(float)
                .mean()
            )
        info_dict[f"{sl_type}_exit_price"] = exit_price

        if move_sl_to_cost:
            info_dict[f"{other_side}_stop_loss_price"] = info_dict[
                f"{other_side}_avg_price"
            ]
            if (
                info_dict[f"{other_side}_stop_loss_order_ids"] is not None
                or place_orders_on_sl
            ):
                if info_dict[f"{other_side}_stop_loss_order_ids"] is not None:
                    cancel_pending_orders(
                        info_dict[f"{other_side}_stop_loss_order_ids"], "STOPLOSS"
                    )
                option_to_repair = (
                    traded_strangle.call_option
                    if other_side == "call"
                    else traded_strangle.put_option
                )
                info_dict[f"{other_side}_stop_loss_order_ids"] = (
                    place_option_order_and_notify(
                        instrument=option_to_repair,
                        action="BUY",
                        qty_in_lots=quantity_in_lots,
                        prices=info_dict[f"{other_side}_stop_loss_price"],
                        order_tag=f"{other_side.capitalize()} stop loss {strategy_tag}",
                        webhook_url=notification_url,
                        stop_loss_order=True,
                        target_status="trigger pending",
                        return_avg_price=False,
                    )
                )

        # Starting the trend catcher
        if catch_trend:
            trend_thread = Thread(
                target=trend_catcher,
                args=(
                    info_dict,
                    sl_type,
                    trend_qty_ratio,
                ),
                name=f"{underlying.name} {sl_type} trend catcher",
            )
            trend_thread.start()
            info_dict["active_threads"].append(trend_thread)

        sleep(5)  # To ensure that the stop loss orders are reflected in the orderbook

        # Wait for exit or other stop loss to hit
        while all(
            [
                current_time().time() < time(*exit_time),
                not info_dict["exit_triggers"]["take_profit"],
            ]
        ):
            check_for_stop_loss(info_dict, other_side)
            if info_dict[f"{other_side}_sl"]:
                if info_dict[f"{other_side}_stop_loss_order_ids"] is None:
                    other_sl_option = (
                        traded_strangle.call_option
                        if other_side == "call"
                        else traded_strangle.put_option
                    )
                    notifier(
                        f"{underlying.name} strangle {other_side} stop loss hit.",
                        notification_url,
                        "CRUCIAL",
                    )
                    exec_details = execute_instructions(
                        {
                            other_sl_option: {
                                "action": Action.BUY,
                                "quantity_in_lots": quantity_in_lots,
                                "order_tag": strategy_tag,
                            }
                        }
                    )
                    other_exit_price = exec_details[other_sl_option]
                else:
                    orderbook = fetch_book("orderbook")
                    other_exit_price = (
                        lookup_and_return(
                            orderbook,
                            "orderid",
                            info_dict[f"{other_side}_stop_loss_order_ids"],
                            "averageprice",
                        )
                        .astype(float)
                        .mean()
                    )
                info_dict[f"{other_side}_exit_price"] = other_exit_price
                break
            sleep(1)

    # Entering the main function
    if time(*exit_time) < current_time().time():
        notifier(
            f"{underlying.name} intraday strangle not being deployed after exit time",
            notification_url,
            "INFO",
        )
        return
    expiry = underlying.current_expiry
    quantity_in_lots = convert_exposure_to_lots(
        exposure, underlying.fetch_ltp(), underlying.lot_size
    )

    if combined_stop_loss is None:
        # If combined stop loss is not provided, then it is set to np.nan, and
        # individual stop losses are calculated
        combined_stop_loss = np.nan
        # Setting stop loss
        stop_loss_dict = {
            "fixed": {"BANKNIFTY": 1.7, "NIFTY": 1.5},
            "dynamic": {"BANKNIFTY": 1.7, "NIFTY": 1.5},
        }

        if isinstance(stop_loss, str):
            if stop_loss == "dynamic" and time_to_expiry(expiry, in_days=True) < 1:
                stop_loss = 1.7
            else:
                stop_loss = stop_loss_dict[stop_loss].get(underlying.name, 1.6)
        else:
            stop_loss = stop_loss
    else:
        # If combined stop loss is provided, then individual stop losses are set to np.nan
        stop_loss = np.nan

    if strike_selection == "equal":
        strangle = most_equal_strangle(
            underlying=underlying,
            call_strike_offset=call_strike_offset,
            put_strike_offset=put_strike_offset,
            disparity_threshold=disparity_threshold,
            exit_time=exit_time,
            expiry=expiry,
            notification_url=notification_url,
        )
        if strangle is None:
            notifier(
                f"{underlying.name} no strangle found within disparity threshold {disparity_threshold}",
                notification_url,
                "INFO",
            )
            return
    elif strike_selection == "resilient":
        strangle = underlying.most_resilient_strangle(
            stop_loss=stop_loss, expiry=expiry
        )
    elif strike_selection == "atm":
        atm_strike = find_strike(underlying.fetch_ltp(), underlying.base)
        strangle = Strangle(atm_strike, atm_strike, underlying.name, expiry)
    else:
        raise ValueError(f"Invalid find mode: {strike_selection}")

    call_ltp, put_ltp = strangle.fetch_ltp()

    # Placing the main order
    execution_details = execute_instructions(
        {
            strangle: {
                "action": Action.SELL,
                "quantity_in_lots": quantity_in_lots,
                "order_tag": strategy_tag,
            }
        }
    )
    call_avg_price, put_avg_price = execution_details[strangle]
    total_avg_price = call_avg_price + put_avg_price

    # Calculating stop loss prices
    call_stop_loss_price = (
        call_avg_price * call_stop_loss
        if call_stop_loss
        else call_avg_price * stop_loss
    )
    put_stop_loss_price = (
        put_avg_price * put_stop_loss if put_stop_loss else put_avg_price * stop_loss
    )
    combined_stop_loss_price = total_avg_price * combined_stop_loss

    underlying_ltp = underlying.fetch_ltp()

    # Logging information and sending notification
    trade_log = {
        "Time": current_time().strftime("%d-%m-%Y %H:%M:%S"),
        "Index": underlying.name,
        "Underlying price": underlying_ltp,
        "Call strike": strangle.call_strike,
        "Put strike": strangle.put_strike,
        "Expiry": expiry,
        "Action": "SELL",
        "Call price": call_avg_price,
        "Put price": put_avg_price,
        "Total price": total_avg_price,
        "Order tag": strategy_tag,
    }

    summary_message = "\n".join(f"{k}: {v}" for k, v in trade_log.items())

    # Setting the IV information at entry

    traded_call_iv, traded_put_iv, traded_avg_iv = calculate_strangle_iv(
        call_price=call_avg_price,
        put_price=put_avg_price,
        call_strike=strangle.call_strike,
        put_strike=strangle.put_strike,
        spot=underlying_ltp,
        time_left=time_to_expiry(expiry),
    )
    try:
        atm_iv_at_entry = underlying.fetch_atm_info()["avg_iv"]
    except Exception as e:
        logger.error(f"Error in fetching ATM IV: {e}")
        atm_iv_at_entry = np.nan
    time_left_at_trade = time_to_expiry(expiry)

    # Sending the summary message
    summary_message += (
        f"\nTraded IVs: {traded_call_iv}, {traded_put_iv}, {traded_avg_iv}\n"
        f"ATM IV at entry: {atm_iv_at_entry}\n"
        f"Call SL: {call_stop_loss_price}, Put SL: {put_stop_loss_price}\n"
        f"Combined SL: {combined_stop_loss_price}\n"
    )
    notifier(summary_message, notification_url, "INFO")

    if place_sl_orders:
        call_stop_loss_order_ids = place_option_order_and_notify(
            instrument=strangle.call_option,
            action="BUY",
            qty_in_lots=quantity_in_lots,
            prices=call_stop_loss_price,
            order_tag=strategy_tag,
            webhook_url=notification_url,
            stop_loss_order=True,
            target_status="trigger pending",
            return_avg_price=False,
        )
        put_stop_loss_order_ids = place_option_order_and_notify(
            instrument=strangle.put_option,
            action="BUY",
            qty_in_lots=quantity_in_lots,
            prices=put_stop_loss_price,
            order_tag=strategy_tag,
            webhook_url=notification_url,
            stop_loss_order=True,
            target_status="trigger pending",
            return_avg_price=False,
        )
    else:
        call_stop_loss_order_ids = None
        put_stop_loss_order_ids = None

    # Setting up shared info dict
    shared_info_dict = {
        "traded_strangle": strangle,
        "spot_at_entry": underlying_ltp,
        "call_avg_price": call_avg_price,
        "put_avg_price": put_avg_price,
        "total_avg_price": total_avg_price,
        "atm_iv_at_entry": atm_iv_at_entry,
        "call_stop_loss_price": call_stop_loss_price,
        "put_stop_loss_price": put_stop_loss_price,
        "combined_stop_loss_price": combined_stop_loss_price,
        "call_stop_loss_order_ids": call_stop_loss_order_ids,
        "put_stop_loss_order_ids": put_stop_loss_order_ids,
        "time_left_day_start": time_left_at_trade,
        "call_ltp": call_ltp,
        "put_ltp": put_ltp,
        "underlying_ltp": underlying_ltp,
        "call_iv": traded_call_iv,
        "put_iv": traded_put_iv,
        "avg_iv": traded_avg_iv,
        "call_sl": False,
        "put_sl": False,
        "exit_triggers": {
            "convert_to_butterfly": False,
            "take_profit": False,
            "combined_stop_loss": False,
        },
        "trade_complete": False,
        "call_sl_check_notification_sent": False,
        "put_sl_check_notification_sent": False,
        "active_threads": [],
        "trend_catcher_points_captured": 0,
    }

    position_monitor_thread = Thread(
        target=position_monitor, args=(shared_info_dict,), name="Position monitor"
    )
    position_monitor_thread.start()
    shared_info_dict["active_threads"].append(position_monitor_thread)
    sleep(
        5
    )  # To ensure that the position monitor thread has started and orders are reflected in the orderbook

    # Wait for exit time or both stop losses to hit (Main Loop)
    while all(
        [
            current_time().time() < time(*exit_time),
            not any(shared_info_dict["exit_triggers"].values()),
        ]
    ):
        if combined_stop_loss is not None and not np.isnan(combined_stop_loss):
            pass
        else:
            check_for_stop_loss(shared_info_dict, "call")
            if shared_info_dict["call_sl"]:
                process_stop_loss(shared_info_dict, "call")
                break
            check_for_stop_loss(shared_info_dict, "put")
            if shared_info_dict["put_sl"]:
                process_stop_loss(shared_info_dict, "put")
                break
        sleep(1)

    # Out of the while loop, so exit time reached or both stop losses hit, or we are hedged

    # If we are hedged then wait till exit time
    # noinspection PyTypeChecker
    if shared_info_dict["exit_triggers"]["convert_to_butterfly"]:
        hedge_strangle = shared_info_dict["ctb_hedge"]
        execute_instructions(
            {
                hedge_strangle: {
                    "action": Action.BUY,
                    "quantity_in_lots": quantity_in_lots,
                    "order_tag": strategy_tag,
                }
            }
        )
        if place_sl_orders:
            cancel_pending_orders(
                shared_info_dict["call_stop_loss_order_ids"]
                + shared_info_dict["put_stop_loss_order_ids"]
            )
        notifier(f"{underlying.name}: Converted to butterfly", notification_url, "INFO")
        while current_time().time() < time(*exit_time):
            sleep(3)

    call_sl = shared_info_dict["call_sl"]
    put_sl = shared_info_dict["put_sl"]

    if not call_sl and not put_sl:  # Both stop losses not hit
        execution_details = execute_instructions(
            {
                strangle: {
                    "action": Action.BUY,
                    "quantity_in_lots": quantity_in_lots,
                    "order_tag": strategy_tag,
                }
            }
        )
        call_exit_avg_price, put_exit_avg_price = execution_details[strangle]

        # noinspection PyTypeChecker
        if (
            place_sl_orders
            and not shared_info_dict["exit_triggers"]["convert_to_butterfly"]
        ):
            cancel_pending_orders(
                shared_info_dict["call_stop_loss_order_ids"]
                + shared_info_dict["put_stop_loss_order_ids"]
            )
        shared_info_dict["call_exit_price"] = call_exit_avg_price
        shared_info_dict["put_exit_price"] = put_exit_avg_price

    elif (call_sl or put_sl) and not (call_sl and put_sl):  # Only one stop loss hit
        exit_option_type: str = "put" if call_sl else "call"
        exit_option = strangle.put_option if call_sl else strangle.call_option
        execution_details = execute_instructions(
            {
                exit_option: {
                    "action": Action.BUY,
                    "quantity_in_lots": quantity_in_lots,
                    "order_tag": strategy_tag,
                }
            }
        )
        non_sl_exit_price = execution_details[exit_option]
        if place_sl_orders or place_orders_on_sl:
            cancel_pending_orders(
                shared_info_dict[f"{exit_option_type}_stop_loss_order_ids"]
            )
        shared_info_dict[f"{exit_option_type}_exit_price"] = non_sl_exit_price

    else:  # Both stop losses hit
        pass

    shared_info_dict["trade_complete"] = True
    for thread in shared_info_dict["active_threads"]:
        thread.join()

    # Calculate profit
    total_exit_price = (
        shared_info_dict["call_exit_price"] + shared_info_dict["put_exit_price"]
    )
    # Exit message
    exit_message = (
        f"{underlying.name} strangle exited.\n"
        f"Time: {current_time(): %d-%m-%Y %H:%M:%S}\n"
        f"Underlying LTP: {shared_info_dict['underlying_ltp']}\n"
        f"Call Price: {shared_info_dict['call_ltp']}\n"
        f"Put Price: {shared_info_dict['put_ltp']}\n"
        f"Call SL: {shared_info_dict['call_sl']}\n"
        f"Put SL: {shared_info_dict['put_sl']}\n"
        f"Call Exit Price: {shared_info_dict['call_exit_price']}\n"
        f"Put Exit Price: {shared_info_dict['put_exit_price']}\n"
        f"Total Exit Price: {total_exit_price}\n"
        f"Total Entry Price: {total_avg_price}\n"
        f"Profit Points: {total_avg_price - total_exit_price}\n"
        f"Chase Points: {shared_info_dict['trend_catcher_points_captured']}\n"
    )
    # Exit dict
    exit_dict = {
        "Call exit price": shared_info_dict["call_exit_price"],
        "Put exit price": shared_info_dict["put_exit_price"],
        "Total exit price": total_exit_price,
        "Points captured": total_avg_price - total_exit_price,
        "Call stop loss": shared_info_dict["call_sl"],
        "Put stop loss": shared_info_dict["put_sl"],
        "Trend catcher points": shared_info_dict["trend_catcher_points_captured"],
    }

    notifier(exit_message, notification_url, "CRUCIAL")
    trade_log.update(exit_dict)

    return shared_info_dict


@exit_handler
def quick_strangle(
    underlying: Index | Stock,
    action: str,
    iv_threshold: float,
    take_profit: float,
    scan_exit_time: tuple[int, int],
    exposure: int | float = 0,
    investment: int | float = 0,
    stop_loss: Optional[float] = None,
    trade_exit_time: tuple[int, int] = (10, 10),
    at_market: bool = False,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Quick Strangle",
):

    if not exposure and not investment:
        raise ValueError("Exposure or investment must be provided")

    DISPARITY_THRESHOLD = 0.2

    # Entering the main function
    if time(*scan_exit_time) < current_time().time():
        notifier(
            f"{underlying.name} {strategy_tag} not being deployed after exit time",
            notification_url,
            "INFO",
        )
        return

    def fetch_spot_and_basis(underlying: Index, expiry: str) -> tuple[float, float]:
        spot_price = underlying.fetch_ltp()
        current_basis = underlying.get_basis_for_expiry(
            expiry=expiry, underlying_price=spot_price
        )
        return spot_price, current_basis

    def calculate_ivs(strangle, spot_price, r, prices):
        ivs = strangle.fetch_ivs(spot=spot_price, r=r, prices=prices)
        return np.mean(ivs)

    def disparity_check(call_ltp, put_ltp):
        disparity = disparity_calculator(call_ltp, put_ltp)
        return disparity < DISPARITY_THRESHOLD

    last_log_time = current_time()

    def log_iv_status():
        nonlocal ivs, last_log_time
        if current_time() - last_log_time > timedelta(seconds=0.1):
            logger.info(f"{underlying.name} {strategy_tag} IVs: {ivs}")
            last_log_time = current_time()

    def condition_triggered() -> bool | tuple[Strangle, float, float]:
        nonlocal ivs, action, iv_threshold, strategy_tag, position
        if action == Action.BUY:
            strangle = min(ivs, key=ivs.get)
        else:
            strangle = max(ivs, key=ivs.get)
        iv = ivs[strangle]
        # noinspection PyTypeChecker
        total_price = np.sum(strangle.fetch_ltp(for_type=action.value))
        condition = iv <= iv_threshold if action == Action.BUY else iv >= iv_threshold

        if condition:
            position.position_active = True
            position.instrument = strangle
            position.initiating_price = total_price
            return True
        else:
            return False

    def profit_condition() -> bool:
        nonlocal action, total_current_price, position
        if action == Action.BUY:
            return total_current_price >= position.profit_threshold
        else:
            return total_current_price <= position.profit_threshold

    def stop_loss_condition() -> bool:
        nonlocal action, total_current_price, position

        if action == Action.BUY:
            return total_current_price <= position.stop_loss_threshold
        else:
            return total_current_price >= position.stop_loss_threshold

    strategy_tag = f"{strategy_tag} {action.upper()}"
    action = Action(action)
    expiry = underlying.current_expiry

    if stop_loss is None:
        stop_loss = np.nan

    position = PositionMonitor(underlying)

    while current_time().time() < time(*scan_exit_time):
        spot, basis = fetch_spot_and_basis(underlying, expiry)
        above_info, below_info = get_above_below_strangles_with_prices(
            underlying, spot, expiry, action.value
        )
        above_strangle, above_prices = above_info
        below_strangle, below_prices = below_info
        ivs = {}
        if disparity_check(*above_prices):
            ivs[above_strangle] = calculate_ivs(
                above_strangle, spot, basis, above_prices
            )
        if disparity_check(*below_prices):
            ivs[below_strangle] = calculate_ivs(
                below_strangle, spot, basis, below_prices
            )

        if not ivs:
            logger.info(
                f"{underlying.name} {strategy_tag} No suitable strangles found. IVs: {ivs}"
            )
            sleep(0.1)
            continue

        log_iv_status()

        if condition_triggered():
            if exposure != 0:
                quantity_in_lots = convert_exposure_to_lots(
                    exposure, underlying.fetch_ltp(), underlying.lot_size
                )
            elif investment != 0:
                # Calculation of quantity
                shares_to_buy = investment / position.initiating_price
                shares_to_buy = round_shares_to_lot_size(
                    shares_to_buy, underlying.lot_size
                )
                quantity_in_lots = shares_to_buy / underlying.lot_size
            else:
                raise ValueError("Exposure or investment must be provided")

            execution_details = execute_instructions(
                {
                    position.instrument: {
                        "action": action,
                        "quantity_in_lots": quantity_in_lots,
                        "order_tag": strategy_tag,
                    }
                },
                at_market=at_market,
            )
            call_avg_price, put_avg_price = execution_details[position.instrument]

            notifier(
                f"Entered {underlying.name} {strategy_tag} on {position.instrument} "
                f"with avg price {call_avg_price + put_avg_price}",
                notification_url,
                "INFO",
            )
            position.initiating_price = call_avg_price + put_avg_price
            break

        sleep(0.1)

    if not position.position_active:
        notifier(
            f"{underlying.name} {strategy_tag} not triggered. Exiting.",
            notification_url,
        )
        return

    if position.position_active:
        position.profit_threshold = position.initiating_price * (
            1 + (take_profit * action.num_value)
        )
        position.stop_loss_threshold = position.initiating_price * (
            1 - (stop_loss * action.num_value)
        )
        while current_time().time() < time(*trade_exit_time):
            current_call_price, current_put_price = position.instrument.fetch_ltp(
                for_type=(~action).value
            )
            total_current_price = current_call_price + current_put_price
            logger.info(
                f"{underlying.name} {strategy_tag} Current price: {total_current_price} "
                f"Target price: {position.profit_threshold} Stop loss price: {position.stop_loss_threshold}"
            )
            if profit_condition():
                notifier(
                    f"{underlying.name} {strategy_tag} profit triggered. Exiting.",
                    notification_url,
                )
                break
            if stop_loss_condition():
                notifier(
                    f"{underlying.name} {strategy_tag} stop loss triggered. Exiting.",
                    notification_url,
                )
                break

            sleep(0.1)

        # noinspection PyUnboundLocalVariable
        execution_details = execute_instructions(
            {
                position.instrument: {
                    "action": ~action,
                    "quantity_in_lots": quantity_in_lots,
                    "order_tag": strategy_tag,
                }
            },
            at_market=at_market,
        )
        call_exit_price, put_exit_price = execution_details[position.instrument]
        exit_price = call_exit_price + put_exit_price
        profit_points = (exit_price - position.initiating_price) * action.num_value
        notifier(
            f"Exited {underlying.name} {strategy_tag} with profit points {profit_points}",
            notification_url,
        )


@exit_handler
def trend_v2(
    underlying: Index | Stock,
    exposure: int | float,
    exit_time: tuple[int, int] = (15, 27),
    threshold_movement: Optional[float] = None,
    beta: Optional[float] = 0.8,
    stop_loss: Optional[float] = 0.003,
    hedge_offset: Optional[float | bool] = 0.004,
    optimized: bool = False,
    target_delta: float = 0.65,
    theta_time_jump_hours: int = 6,  # In hours
    max_entries: Optional[int] = 3,
    at_market: bool = False,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Trend",
    data_directory: Optional[str] = None,
):
    # Entering the main function
    if time(*exit_time) < current_time().time():
        notifier(
            f"{underlying.name} {strategy_tag} not being deployed after exit time",
            notification_url,
            "INFO",
        )
        return

    # Quantity
    spot_price = underlying.fetch_ltp()
    quantity_in_shares = round_shares_to_lot_size(
        exposure / spot_price, underlying.lot_size
    )

    # Fetching open price
    if current_time().time() > time(9, 18):
        try:
            open_time = current_time().replace(hour=9, minute=16, second=0)
            open_price_data = fetch_historical_prices(
                underlying.token, "ONE_MINUTE", open_time, open_time
            )
            open_price = open_price_data[0][1]
        except Exception as e:
            notifier(
                f"Error in fetching historical prices: {e}",
                notification_url,
                "INFO",
            )
            open_price = underlying.fetch_ltp()
    else:
        while current_time().time() < time(9, 16):
            sleep(1)
        open_price = underlying.fetch_ltp()

    # Threshold movement and price boundaries
    threshold_movement = threshold_movement or (IndiaVix.fetch_ltp() * (beta or 1)) / 48
    price_boundaries = [
        open_price * (1 + ((-1) ** i) * threshold_movement / 100) for i in range(2)
    ]

    # Exit time
    exit_time_object = time(*exit_time)
    scan_end_time = (
        datetime.combine(current_time().date(), exit_time_object)
        - timedelta(minutes=10)
    ).time()

    # Setting the file path
    date = current_time().strftime("%Y-%m-%d")
    if data_directory is None:
        file_path = f"{ActiveSession.obj.userId}\\{underlying.name.lower()}_trend_data\\{date}.json"
    else:
        file_path = os.path.join(data_directory, f"{date}.json")

    # Initializing the trend position manager
    greek_settings = {"theta_time_jump": theta_time_jump_hours / (365 * 24)}
    trend_position = TrendPosition(
        underlying=underlying,
        base_exposure_qty=quantity_in_shares,
        greek_settings=greek_settings,
        notifier_url=notification_url,
        order_tag=strategy_tag,
        file_path=file_path,
    )
    trend_position.set_all_options(options_with_cache=True)

    notifier(
        f"{underlying.name} trend following starting with {threshold_movement:0.2f} threshold movement\n"
        f"Current Price: {open_price}\nUpper limit: {price_boundaries[0]:0.2f}\n"
        f"Lower limit: {price_boundaries[1]:0.2f}.",
        notification_url,
        "INFO",
    )
    entries = 0
    movement = 0
    while entries < max_entries and current_time().time() < exit_time_object:

        # Scan for entry condition
        notifier(
            f"{underlying.name} trender {entries+1} scanning for entry condition.",
            notification_url,
            "INFO",
        )
        while current_time().time() < scan_end_time:
            ltp = underlying.fetch_ltp()
            movement = (ltp - open_price) / open_price * 100
            if abs(movement) > threshold_movement:
                break
            sleep_until_next_action(1, exit_time)

        if current_time().time() >= scan_end_time:
            notifier(
                f"{underlying.name} trender {entries+1} exiting due to time.",
                notification_url,
                "CRUCIAL",
            )
            break

        # Entry condition met taking position
        price = underlying.fetch_ltp()
        action: Action = Action.BUY if movement > 0 else Action.SELL
        stop_loss_price = price * (
            (1 - stop_loss) if action == Action.BUY else (1 + stop_loss)
        )
        notifier(
            f"{underlying.name} {action} trender triggered with {movement:0.2f} movement. "
            f"{underlying.name} at {price}. "
            f"Stop loss at {stop_loss_price}.",
            notification_url,
            "INFO",
        )

        # Set quantities and enter the position
        trend_position.set_recommended_qty(
            optimized=optimized,
            target_delta=target_delta,
            trend_direction=action,
            hedge_offset=hedge_offset,
        )
        trend_position.enter_positions(at_market=at_market)

        notifier(
            f"{underlying.name} {action} trender {entries+1} entered.",
            notification_url,
            "INFO",
        )

        # Monitoring begins
        stop_loss_hit = False
        early_exit = False
        # 15% of the quantity will be the delta threshold
        exit_threshold = 0.15 * quantity_in_shares
        while current_time().time() < exit_time_object:
            sleep_until_next_action(1, exit_time)
            trend_position.record_position_status()
            ltp = underlying.fetch_ltp()
            movement = (ltp - open_price) / open_price * 100
            stop_loss_hit = (
                (ltp < stop_loss_price)
                if action == Action.BUY
                else (ltp > stop_loss_price)
            )
            if stop_loss_hit:
                break
            if abs(trend_position.aggregate_greeks().delta) < exit_threshold:
                notifier(
                    f"{underlying.name} trender {entries+1} delta threshold hit.",
                    notification_url,
                    "INFO",
                )
                early_exit = True
                break

        # Exit condition met exiting position (stop loss or time)
        stop_loss_message = f"Trender stop loss hit. " if stop_loss_hit else ""
        notifier(
            f"{stop_loss_message}{underlying.name} trender {entries+1} exiting.",
            notification_url,
            "CRUCIAL",
        )
        trend_position.exit_positions(at_market=at_market)
        notifier(
            f"{underlying.name} {action} trender {entries+1} exited.",
            notification_url,
            "INFO",
        )
        entries += 1
        if early_exit:
            break


@exit_handler
def reentry_straddle(
    underlying: Index | Stock,
    exposure: int | float,
    strike_offset: float = 0,
    call_stop_loss: Optional[float] = None,
    put_stop_loss: Optional[float] = None,
    stop_loss: Optional[float] = 0.5,
    call_reentries: int = None,
    put_reentries: int = None,
    reentries: int = 1,
    exit_time: tuple[int, int] = (15, 29),
    at_market: bool = False,
    notification_url: Optional[str] = None,
    strategy_tag: Optional[str] = "Reentry_straddle",
    data_directory: Optional[str] = None,
):

    if time(*exit_time) < current_time().time():
        notifier(
            f"{underlying.name} {strategy_tag} not being deployed after exit time",
            notification_url,
            "INFO",
        )
        return

    spot_price = underlying.fetch_ltp()

    call_stop_loss = call_stop_loss or stop_loss
    put_stop_loss = put_stop_loss or stop_loss

    strangle = most_equal_strangle(
        underlying, strike_offset, -strike_offset, range_of_strikes=1
    )

    quantity_in_lots = convert_exposure_to_lots(
        exposure, spot_price, underlying.lot_size
    )

    execute_order = partial(
        execute_single_instrument,
        at_market=at_market,
        order_tag=strategy_tag,
        quantity_in_lots=quantity_in_lots,
    )

    notifier(
        f"{underlying.name} {strategy_tag} starting with straddle {strangle} and prices {strangle.fetch_ltp()}",
        notification_url,
        "INFO",
    )

    # Placing the main order
    call_avg_price, put_avg_price = execute_order(
        instrument=strangle, action=Action.SELL
    )
    call_sl_price = call_avg_price * (1 + call_stop_loss)
    put_sl_price = put_avg_price * (1 + put_stop_loss)

    # A tuple of (in_trade, reattempts)
    call_reentries = call_reentries or reentries
    put_reentries = put_reentries or reentries
    status_dict = {
        strangle.call_option: (True, call_reentries),
        strangle.put_option: (True, put_reentries),
    }

    def check_for_stoploss_hit(opt: Option, sl_price: float):
        if opt.fetch_ltp() >= sl_price:
            return True
        return False

    def check_for_reentry_condition(opt: Option, check_price: float):
        if opt.fetch_ltp() <= check_price:
            return True
        return False

    while current_time().time() < time(*exit_time):
        if all(
            [not status[0] for status in status_dict.values()]
            + [not status[1] for status in status_dict.values()]
        ):
            notifier(
                f"{underlying.name} {strategy_tag} all positions exited.",
                notification_url,
                "INFO",
            )
            return

        sleep_until_next_action(1, exit_time)

        for option in status_dict:
            # If its active check for sl, if not check for reentry
            if status_dict[option][0]:
                stoploss_price = (
                    call_sl_price
                    if option.option_type == OptionType.CALL
                    else put_sl_price
                )
                sl_hit = check_for_stoploss_hit(option, stoploss_price)
                if sl_hit:
                    option_exit_price = execute_order(
                        instrument=option, action=Action.BUY, square_off_order=True
                    )
                    status_dict[option] = (False, status_dict[option][1])
                    notifier(
                        f"{underlying.name} {strategy_tag} {option} stop loss hit. "
                        f"Exit price: {option_exit_price}",
                        notification_url,
                        "INFO",
                    )
            # If its inactive but has reattempts left, check for reentry
            elif status_dict[option][1] > 0:
                reentry_price = (
                    call_avg_price
                    if option.option_type == OptionType.CALL
                    else put_avg_price
                )
                reentry_hit = check_for_reentry_condition(option, reentry_price)
                if reentry_hit:
                    option_entry_price = execute_order(
                        instrument=option, action=Action.SELL
                    )
                    status_dict[option] = (True, status_dict[option][1] - 1)
                    notifier(
                        f"{underlying.name} {strategy_tag} {option} reentry condition met. "
                        f"Reentry price: {option_entry_price}",
                        notification_url,
                        "INFO",
                    )
            else:
                pass

    # Exit open positions if any
    notifier(f"{underlying.name} {strategy_tag} exiting.", notification_url, "INFO")
    for option in status_dict:
        if status_dict[option][0]:
            execute_order(instrument=option, action=Action.BUY, square_off_order=True)
