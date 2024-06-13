import functools
import traceback
from inspect import signature
from time import sleep
from volstreet import config
from volstreet.utils import (
    notifier,
    current_time,
)
from volstreet.strategies.monitoring import exit_positions, notify_pnl


def exit_handler(strategy):
    @functools.wraps(strategy)
    def wrapper(*args, **kwargs):
        execution_time = current_time()
        sig = signature(strategy)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        strategy_tag = bound.arguments.get("strategy_tag")
        underlying = bound.arguments.get("underlying")
        underlying = underlying.name
        notification_url = bound.arguments.get("notification_url")
        exposure = bound.arguments.get("exposure")
        try:
            return strategy(*args, **kwargs)
        except Exception as e:
            user_prefix = config.ERROR_NOTIFICATION_SETTINGS.get("user")
            user_prefix = f"{user_prefix} - " if user_prefix else ""
            sleep(5)  # Sleep for 5 seconds to allow the orders to be filled
            notifier(
                f"{user_prefix}"
                f"Error in strategy {strategy.__name__}: {e}\nTraceback:{traceback.format_exc()}\n\n"
                f"Exiting existing positions...",
                webhook_url=config.ERROR_NOTIFICATION_SETTINGS["url"],
                level="ERROR",
                send_whatsapp=True,
            )
            exit_positions(underlying, strategy_tag, execution_time)
        finally:
            sleep(5)  # Sleep for 5 seconds to allow the orders to be filled
            notify_pnl(
                underlying,
                strategy_tag,
                execution_time,
                exposure,
                notification_url,
            )

    return wrapper
