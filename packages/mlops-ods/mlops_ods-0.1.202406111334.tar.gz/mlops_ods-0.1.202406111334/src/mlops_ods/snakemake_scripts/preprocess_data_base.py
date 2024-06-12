import pandas as pd

from mlops_ods.utils.utils_model import drop_columns, preprocess_data

df = pd.read_csv(snakemake.input[0])  # noqa: F821
df = df[~df["health"].isna()]
drop_columns(df)
preprocess_data(df)
df.to_csv(snakemake.output[0], index=False)  # noqa: F821
