import pandas as pd
from datetime import datetime
import pickle
import numpy as np
from volstreet.config import logger
from volstreet.historical_info import historical_expiry_dates
from volstreet.backtests.database import DataBaseConnection


class UnderlyingInfo:
    def __init__(self, name):
        self.name = name.upper()
        self.base = self._get_base()
        self.expiry_dates = filter_expiry_dates_for_index(self.name)

    def _get_base(self):
        if self.name in ["NIFTY", "FINNIFTY"]:
            return 50
        elif self.name in ["BANKNIFTY", "SENSEX", "BANKEX"]:
            return 100
        elif self.name == "MIDCPNIFTY":
            return 25
        else:
            raise ValueError("Invalid index name")


def filter_expiry_dates_for_index(underlying: str) -> pd.DatetimeIndex:
    index_expiry_dates = historical_expiry_dates[underlying.upper()]
    return pd.DatetimeIndex(sorted(index_expiry_dates))


def fetch_historical_expiry(
    underlying: str,
    date_time: str | datetime,
    threshold_days: int = 0,
    n_exp: int = 1,
) -> pd.DatetimeIndex | pd.Timestamp | None:
    if isinstance(date_time, str):
        date_time = pd.to_datetime(date_time)

    filtered_dates = filter_expiry_dates_for_index(underlying)
    filtered_dates = filtered_dates.sort_values()
    delta_days = (filtered_dates - date_time.replace(hour=00, minute=00)).days
    filtered_dates = filtered_dates[delta_days >= threshold_days]
    nearest_exp_dates = [*sorted(filtered_dates)]
    if n_exp == 1:
        return nearest_exp_dates[0] if len(nearest_exp_dates) != 0 else None
    if len(nearest_exp_dates) < n_exp:
        logger.warning(f"Insufficient expiry dates for {underlying} on {date_time}")
        while len(nearest_exp_dates) < n_exp:
            nearest_exp_dates.append(np.nan)
    return pd.DatetimeIndex(nearest_exp_dates[:n_exp])
