import pickle
from pathlib import Path

import click
import dvc.api
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from mlops_ods.config import compose_config

from .cli import cli


def train_scaler(df: pd.DataFrame) -> tuple[StandardScaler, pd.DataFrame, pd.DataFrame]:
    params = dvc.api.params_show()
    train, test = train_test_split(
        df, test_size=params["test_size"], random_state=params["random_state"]
    )

    sc = StandardScaler()
    sc.fit(train)
    return sc, train, test


def apply_scaler(scaler: StandardScaler, df: pd.DataFrame) -> pd.DataFrame:
    return scaler.transform(df)


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("scaler_path", type=Path)
@click.argument("train_features_path", type=Path)
@click.argument("test_features_path", type=Path)
def cli_train_scaler(
    input_frame_path: Path,
    scaler_path: Path,
    train_features_path: Path,
    test_features_path: Path,
):
    cfg = compose_config()
    num_cols = cfg.features.numerical

    df = pd.read_csv(input_frame_path)
    scaler, train, test = train_scaler(df[num_cols])
    pickle.dump(scaler, scaler_path.open("wb"))
    train.join(df["health"]).to_csv(train_features_path, index=False)
    test.join(df["health"]).to_csv(test_features_path, index=False)


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("scaler_path", type=Path)
@click.argument("result_frame_path", type=Path)
@click.argument("target_frame_path", type=Path)
def cli_apply_scaler(
    input_frame_path: Path,
    scaler_path: Path,
    result_frame_path: Path,
    target_frame_path: Path,
):
    cfg = compose_config()
    num_cols = cfg.features.numerical

    df = pd.read_csv(input_frame_path)
    scaler = pickle.load(scaler_path.open("rb"))
    result = apply_scaler(scaler, df[num_cols])
    np.save(result_frame_path, result)
    np.save(target_frame_path, df["health"])
