import logging
import os
import subprocess

import dill
from catboost import CatBoostClassifier


def download_kaggle_dataset_if_not_exist(
    path_to_data_folder: str, file_name_with_data: str
) -> None:
    """
    Download dataset from kaggle if it's not already exists
    in path_to_data folder with file_name name

    :param path_to_data_folder: path to folder with data
    :param file_name_with_data: name of file with data
    :return: None
    """
    # Check if the file exists in the folder
    file_path = os.path.join(path_to_data_folder, file_name_with_data)
    if not os.path.exists(file_path):
        # If not, download it
        try:
            subprocess.run(
                [
                    "kaggle",
                    "datasets",
                    "download",
                    "-d",
                    "new-york-city/ny-2015-street-tree-census-tree-data",
                    "-p",
                    path_to_data_folder,
                    "--unzip",
                ]
            )
            print(f"Downloaded {file_name_with_data} from Kaggle")
        except Exception as e:
            print(f"Error downloading {file_name_with_data}: {str(e)}")
    else:
        print(f"{file_name_with_data} already exists")


LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL", "DEBUG")
LOGGER_FORMAT = (
    "%(asctime)s %(process)d %(processName)s "
    "%(name)-12s:%(lineno)d %(levelname)-8s %(message)s"
)


def get_logger(name):
    """Get logger for name and inject stream handler"""
    log = logging.getLogger(name)
    log.setLevel(LOGGER_LEVEL)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    log.addHandler(handler)

    return log


def save_model(model_path: str, model: CatBoostClassifier) -> None:
    """
    Save model to model_path

    :param model_path: str path to model folder
    :param model: fitted model for save
    :return:
    """
    with open(model_path, "wb") as f:
        dill.dump(model, f)


def load_model(model_path: str) -> CatBoostClassifier:
    """
    Load model from model_path

    :param model_path: path to model folder
    :return:
    """
    with open(model_path, "rb") as f:
        model = dill.load(f)
        return model
