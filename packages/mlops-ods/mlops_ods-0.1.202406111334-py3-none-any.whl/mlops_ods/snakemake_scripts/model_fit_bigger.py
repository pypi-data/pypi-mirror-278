import pandas as pd
from catboost import CatBoostClassifier

from mlops_ods.config import compose_config
from mlops_ods.utils.utils_etl import save_model

df = pd.read_csv(snakemake.input[0])  # noqa: F821
cfg = compose_config(overrides=["model=slow"])
num_cols = cfg.features.numerical
cat_cols = cfg.features.categorical
total_cols = num_cols + cat_cols
clf = CatBoostClassifier(
    iterations=cfg.model.iterations,
    verbose=cfg.model.verbose,
    random_seed=cfg.model.random_seed,
    cat_features=cat_cols,
)
clf.fit(df[total_cols], df["health"])
save_model(model_path=snakemake.output[0], model=clf)  # noqa: F821
