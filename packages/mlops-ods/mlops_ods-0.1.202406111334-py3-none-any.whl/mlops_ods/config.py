from pathlib import Path

from hydra import compose, initialize
from omegaconf import DictConfig


def compose_config(
    overrides: list[str] | None = None,
    config_path: Path = Path("conf"),
    config_name: str = "config",
) -> DictConfig:
    """
    Hydra config

    :param overrides: list of overrides for config file
    :param config_path: the path of the config
    :param config_name: the name of the config
           (usually the file name without the .yaml extension)
    :return: the composed config
    """
    with initialize(version_base=None, config_path=str(config_path)):
        hydra_config = compose(config_name=config_name, overrides=overrides)
        return hydra_config
