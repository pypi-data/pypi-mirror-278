import os
import json
import numpy as np
import pandas as pd
from volstreet import config
from volstreet.backtests.tools import nav_drawdown_analyser


def consolidate_backtest(path: str) -> pd.DataFrame:
    df = pd.DataFrame()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            day_df = pd.read_csv(os.path.join(path, file))
            df = pd.concat([df, day_df])
    df["quantity"] = np.where(
        df["action"] == "BUY", 1 * df["quantity"], -1 * df["quantity"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df = df.iloc[:, 1:]
    return df


def describe_backtest(dataframe: pd.DataFrame) -> pd.DataFrame:
    # -1 because we are selling the strangle
    all_days = dataframe.groupby(dataframe.index.date).agg(
        {"quantity": "sum", "value": ["sum", lambda x: x.abs().sum()]}
    )
    config.logger.info(f"Total number of days: {len(all_days)}")
    all_days.columns = ["quantity", "profit", "turnover"]
    all_days["exposure"] = 10000000
    all_days["profit"] *= -1
    all_days["profit_percentage"] = (all_days["profit"] / all_days["exposure"]) * 100
    invalid_days = all_days.query("quantity != 0").index
    all_days = all_days[all_days["quantity"] == 0].drop(columns="quantity")
    config.logger.info(
        f"Number of valid days: {len(all_days)}. Invalid days: {invalid_days}"
    )
    config.logger.info(
        f"Profit Margin: {(all_days.profit.sum() / all_days.turnover.sum()) * 100: 0.2f}%"
    )
    all_days = nav_drawdown_analyser(
        all_days, column_to_convert="profit_percentage", profit_in_pct=True
    )
    return all_days


def get_condensed_position_details(folder_name):
    json_data = []
    for file in os.listdir(folder_name):
        if file.endswith(".json") and "parameters" not in file:
            with open(f"{folder_name}\\{file}", "r") as f:
                data = json.load(f)
                json_data.extend(data)
    df = pd.DataFrame(json_data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df


def reconcile_position_pnl_with_summary(
    position_dataframe: pd.DataFrame, summary_dataframe: pd.DataFrame
):
    eod_profit = position_dataframe.pivot_table(
        index=position_dataframe.index.date, values=["mtm"], aggfunc="last"
    )
    combined = eod_profit.merge(
        summary_dataframe[["profit"]], left_index=True, right_index=True
    )
    combined = combined.round(2)
    combined["difference"] = combined["mtm"] - combined["profit"]

    return combined["difference"].sum() == 0, combined
