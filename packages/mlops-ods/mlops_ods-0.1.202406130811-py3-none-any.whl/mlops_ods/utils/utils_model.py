import numpy as np
import pandas as pd


def yes_no_to_numeric(column: pd.Series) -> pd.Series:
    """
    Take column with two values and convert it to binary numeric: {'Yes':1, 'No':0}

    :param column: column with two values 'Yes' and 'No'
    :return: column with two values 1 and 0
    """
    return (column == "Yes") * 1


def drop_columns(df: pd.DataFrame) -> None:
    """
    Drop columns that do not need to predictions - change df inplace

    :param df: original dataframe from kaggle
    :return:
    """
    drop_cols = [
        "block_id",
        "created_at",
        "status",
        "address",
        "latitude",
        "longitude",
        "x_sp",
        "y_sp",
        "bin",
        "bbl",
        "census tract",
        "state",
        "council district",
        "boro_ct",
        "nta",
        "st_senate",
        "st_assem",
        "cncldist",
        "postcode",
        "community board",
        "borocode",
        "stump_diam",
        "spc_latin",
        "nta_name",
    ]
    df.drop(drop_cols, axis=1, inplace=True)


def preprocess_data(df: pd.DataFrame) -> None:
    """
    Preprocess some columns - change df inplace

    :param df: original dataframe from kaggle
    :return:
    """
    columns_yes_no = [
        "root_stone",
        "root_grate",
        "root_other",
        "trunk_wire",
        "trnk_light",
        "trnk_other",
        "brch_light",
        "brch_shoe",
        "brch_other",
    ]
    for col in columns_yes_no:
        df[col] = yes_no_to_numeric(df[col])

    df["curb_loc"] = (df["curb_loc"] == "OnCurb") * 1
    df["sidewalk"] = np.where(df["sidewalk"] == "Damage", 1, 0)
    df["steward"] = (
        df["steward"].map({"1or2": 1, "3or4": 2, "4orMore": 3}).fillna(0).astype(int)
    )
    df["guards"] = (
        df["guards"]
        .map({"Harmful": 1, "Unsure": 2, "Helpful": 3})
        .fillna(0)
        .astype(int)
    )
    df["spc_common"] = df["spc_common"].fillna("n/d")
    df["problems"] = df["problems"].fillna("").apply(lambda x: len(x.split(",")))
    df["health"] = (
        df["health"].map({"Poor": 0, "Fair": 1, "Good": 2}).fillna(-1).astype(int)
    )
