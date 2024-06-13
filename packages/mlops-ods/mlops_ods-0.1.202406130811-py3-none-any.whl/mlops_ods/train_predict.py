import os

import catboost
import hydra
import pandas as pd
from hydra.utils import instantiate
from omegaconf import DictConfig
from sklearn import metrics

import mlops_ods.utils.utils_etl as ut_etl
import mlops_ods.utils.utils_model as ut_models
from mlops_ods.utils import utils_etl

logger = utils_etl.get_logger(__name__)
logger.propagate = False


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    path_to_data = os.path.join(os.path.dirname(os.getcwd()), cfg.settings.path_to_data)
    path_to_model = os.path.join(
        os.path.dirname(os.getcwd()),
        cfg.settings.path_to_model,
        cfg.settings.model_name,
    )
    train_mode = cfg.settings.train_mode

    mode = "train" if train_mode else "predict"
    logger.info("Start job in mode %s", mode)

    logger.info("Get data")
    file_name = cfg.settings.file_name
    ut_etl.download_kaggle_dataset_if_not_exist(path_to_data, file_name)

    df = pd.read_csv(f"{path_to_data}/{file_name}")
    df = df[~df["health"].isna()]

    logger.info("Preprocess data")
    ut_models.drop_columns(df)
    ut_models.preprocess_data(df)

    num_cols = cfg.features.numerical
    cat_cols = cfg.features.categorical
    total_cols = num_cols + cat_cols

    if train_mode:
        logger.info("Fit model")
        if cfg.settings.status == "object":
            clf = instantiate(cfg.model)
            clf.set_params(cat_features=cat_cols)
        else:
            clf = catboost.CatBoostClassifier(
                iterations=cfg.model.iterations,
                verbose=cfg.model.verbose,
                random_seed=cfg.model.random_seed,
                cat_features=cat_cols,
                thread_count=int(cfg.settings.cores) // 2,
            )
        clf.fit(df[total_cols], df["health"])
        predictions = clf.predict_proba(df[total_cols])
        roc_auc = metrics.roc_auc_score(df["health"], predictions, multi_class="ovr")
        logger.info("Roc auc score: %s", roc_auc)

        logger.info("Save model")
        ut_etl.save_model(model_path=path_to_model, model=clf)

    else:
        logger.info("Predict")
        clf = ut_etl.load_model(path_to_model)
        predictions = clf.predict_proba(df[total_cols])
        logger.info("Number of predictions: %s", len(predictions))


if __name__ == "__main__":
    main()
