import pickle
from importlib.resources import files
from pathlib import Path


def load_historical_expiry_dates():
    resource_path = files("volstreet").joinpath("historical_info")
    # noinspection PyTypeChecker
    file_path = Path(resource_path.joinpath("index_expiries.pkl"))
    # noinspection PyTypeChecker
    with open(file_path, "rb") as f:
        historical_expiries = pickle.load(f)

    return historical_expiries


def load_market_days():
    resource_path = files("volstreet").joinpath("historical_info")
    # noinspection PyTypeChecker
    file_path = Path(resource_path.joinpath("market_days.pkl"))
    # noinspection PyTypeChecker
    with open(file_path, "rb") as f:
        data = pickle.load(f)

    return data


# Load the historical expiry dates
historical_expiry_dates = load_historical_expiry_dates()

# Load the market days
market_days = load_market_days()

__all__ = ["historical_expiry_dates", "market_days"]
