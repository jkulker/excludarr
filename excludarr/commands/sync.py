import typer

from loguru import logger

from excludarr.utils.config import Config
from excludarr.core import SyncActions

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    radarr: bool = typer.Option(False, "-r", "--radarr", help="Sync Radarr."),
    sonarr: bool = typer.Option(False, "-s", "--sonarr", help="Sync Sonarr."),
    progress: bool = typer.Option(
        False, "--progress", help="Track the progress using a progressbar."
    ),
):
    logger.debug("Got sync as subcommand")
    logger.debug(f"Got CLI values for -r, --radarr option: {radarr}")
    logger.debug(f"Got CLI values for -s, --sonarr option: {sonarr}")
    logger.debug(f"Got CLI values for --progress option: {progress}")

    logger.debug("Reading configuration file")
    config = Config()

    sync = SyncActions(
        radarr,
        sonarr,
        config.database_path,
        config.locale,
        config.radarr_url,
        config.radarr_api_key,
        config.radarr_verify_ssl,
        config.sonarr_url,
        config.sonarr_api_key,
        config.sonarr_verify_ssl,
    )
    sync.sync_movies()
    sync.sync_series()


if __name__ == "__main__":
    app()
