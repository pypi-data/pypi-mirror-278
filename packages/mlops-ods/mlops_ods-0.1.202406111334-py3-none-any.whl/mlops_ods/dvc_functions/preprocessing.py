from pathlib import Path

import click
import pandas as pd

from mlops_ods.utils.utils_model import drop_columns, preprocess_data

from .cli import cli


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("output_frame_path", type=Path)
def cli_preprocessing(input_frame_path: Path, output_frame_path: Path):
    df = pd.read_csv(input_frame_path)
    df = df[~df["health"].isna()]
    drop_columns(df)
    preprocess_data(df)
    df.to_csv(output_frame_path, index=False)
