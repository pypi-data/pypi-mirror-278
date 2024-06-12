import json
import pickle
from pathlib import Path
from typing import Union

import click
import dvc.api
import matplotlib.pyplot as plt
import numpy as np
from catboost import CatBoostClassifier
from matplotlib.figure import Figure
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, classification_report

from .cli import cli


def conf_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Figure:
    plt.ioff()
    fig, ax = plt.subplots(figsize=(5, 5))
    ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ax=ax, colorbar=False)
    ax.xaxis.set_tick_params(rotation=90)
    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    return fig


def train(
    data: np.ndarray, target: np.ndarray, model_name: str
) -> Union[LogisticRegression, CatBoostClassifier]:
    params = dvc.api.params_show()
    model = None
    if model_name == "log_reg":
        model = LogisticRegression(**params[model_name])
        model.fit(data, target)
    elif model_name == "catboost":
        model = CatBoostClassifier(**params[model_name])
        model.fit(data, target)
    return model


def test(
    model: Union[LogisticRegression, CatBoostClassifier],
    data: np.ndarray,
    target: np.ndarray,
) -> tuple[dict, Figure]:
    predicts = model.predict(data)
    fig = conf_matrix(target, predicts)
    return classification_report(target, predicts, output_dict=True), fig


@cli.command()
@click.argument("train_frame_path", type=Path)
@click.argument("train_target_path", type=Path)
@click.argument("model_path", type=Path)
@click.argument("model_name", type=str)
def cli_train(
    train_frame_path: str,
    train_target_path: str,
    model_path: Path,
    model_name: str,
):
    train_features = np.load(train_frame_path)
    train_target = np.load(train_target_path)
    model = train(train_features, train_target, model_name)
    pickle.dump(model, model_path.open("wb"))


@cli.command()
@click.argument("test_frame_path", type=Path)
@click.argument("test_target_path", type=Path)
@click.argument("model_path", type=Path)
@click.argument("metric_path", type=Path)
@click.argument("figure_path", type=Path)
def cli_test(
    test_frame_path: str,
    test_target_path: str,
    model_path: Path,
    metric_path: Path,
    figure_path: Path,
):
    test_features = np.load(test_frame_path)
    test_target = np.load(test_target_path)
    model = pickle.load(model_path.open("rb"))
    result, fig = test(model, test_features, test_target)
    json.dump(result, metric_path.open("w"))
    plt.savefig(figure_path)
