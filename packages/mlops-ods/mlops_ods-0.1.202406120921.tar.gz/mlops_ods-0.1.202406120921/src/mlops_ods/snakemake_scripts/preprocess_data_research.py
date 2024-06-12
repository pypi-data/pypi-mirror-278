import numpy as np
import pandas as pd

from mlops_ods.utils.utils_model import drop_columns, yes_no_to_numeric

df = pd.read_csv(snakemake.input[0])  # noqa: F821
df = df[~df["health"].isna()]
drop_columns(df)

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
    df["steward"].map({"1or2": 0, "3or4": 1, "4orMore": 1}).fillna(0).astype(int)
)
df["guards"] = (
    df["guards"].map({"Harmful": 0, "Unsure": 0, "Helpful": 1}).fillna(0).astype(int)
)
df["spc_common"] = df["spc_common"].fillna("n/d")
df["problems"] = df["problems"].fillna("").apply(lambda x: len(x.split(",")))
df["health"] = df["health"].map({"Poor": 0, "Fair": 1, "Good": 2}).astype(int)

df.to_csv(snakemake.output[0], index=False)  # noqa: F821
