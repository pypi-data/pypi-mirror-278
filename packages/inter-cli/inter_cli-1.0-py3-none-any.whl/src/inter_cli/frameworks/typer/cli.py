import typer
from src.inter_cli.lib.common import read_yaml
from loguru import logger
from src.inter_cli.functionalities.factory import factory
from src.inter_cli.exceptions import InvalidMLOpsConfigException


app = typer.Typer()


@app.command()
def deploy(mlops_config_path: str):
    try:
        logger.info("reading mlops_config file")
        parsed_mlops_config = read_yaml(mlops_config_path)
        version = parsed_mlops_config.get("version")
        kind = parsed_mlops_config.get("kind")
        if version is None or kind is None:
            raise InvalidMLOpsConfigException(
                "invalid MLOps config, version and kind are mandatory fields"
            )
        functionality = factory(f"{version}_{kind}")
        functionality.execute(parsed_mlops_config)
    except Exception as e:
        # logger.error(f"Could not deploy model because of: {e}")
        raise e


@app.command()
def init(version: str):
    try:
        logger.info("initializing project")
        init_functionality = factory(f"{version}_ProjectInitializer")
        init_functionality.execute()
    except Exception as e:
        logger.error(f"Could not initialize project because of: {e}")


def run() -> None:
    app()
