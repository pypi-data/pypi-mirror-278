import datetime
import logging
import os
import pathlib
import tempfile
import typing

import click

from np_aind_metadata import common, np, storage, update, utils

logger = logging.getLogger(__name__)


NPEXP_PATH_ROOT = os.getenv("NPEXP_PATH_ROOT")
now = datetime.datetime.now()


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--log-file", default=False, is_flag=True)
def cli(debug: bool, log_file: bool) -> None:
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    if debug:
        np.logger.setLevel(logging.DEBUG)
        storage.logger.setLevel(logging.DEBUG)
        update.logger.setLevel(logging.DEBUG)
        utils.logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    if log_file:
        handler = logging.FileHandler(
            now.strftime("np-aind-metadata_%Y-%m-%d-%H-%M-%S") + ".log"
        )
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        np.logger.addHandler(handler)
        storage.logger.addHandler(handler)
        update.logger.addHandler(handler)
        utils.logger.addHandler(handler)


modification_date_format_0 = "%Y-%m-%d"
modification_date_format_1 = "%Y/%m/%d"


@cli.command()
@click.argument("storage-directory", type=pathlib.Path)
@click.argument(
    "rig-name",
    type=click.Choice(["NP1", "NP2", "NP3"]),
)
@click.option(
    "--date",
    help=(
        "Rig modification date. Supported formats:"
        f" {modification_date_format_0}, {modification_date_format_1}"
    ),
    type=click.DateTime(
        formats=[
            modification_date_format_0,
            modification_date_format_1,
        ]
    ),
)
def init_rig_storage(
    storage_directory: pathlib.Path,
    rig_name: common.RigName,
    date: typing.Optional[datetime.datetime] = None,
) -> None:
    if date is None:
        modification_date = None
    else:
        modification_date = date.date()

    with tempfile.TemporaryDirectory() as temp_dir:
        rig_model = np.init_neuropixels_rig_from_np_config(
            rig_name=rig_name,
            modification_date=modification_date,
        )
        rig_model.write_standard_file(temp_dir)
        rig_model_path = pathlib.Path(temp_dir) / "rig.json"
        added_path = storage.update_item(
            storage_directory,
            rig_model_path,
            rig_name,
        )
        logger.debug("Stored rig model at: %s" % added_path)

    click.echo("Initialized rig storage for: %s" % rig_name)


@cli.command()
@click.argument("storage-directory", type=pathlib.Path)
@click.argument("--clusters", default=["B", "D", "E", "F"], type=list[str])
def init_rig_storage_behavior_clusters(
    storage_directory: pathlib.Path,
    clusters: list[str],
) -> None:
    for cluster in clusters:
        for rig_index in range(1, 7):
            rig_name = f"{cluster}{rig_index}"
            logger.debug(f"Initializing rig storage for: {rig_name}")
            with tempfile.TemporaryDirectory() as temp_dir:
                rig_model = np.init_neuropixels_rig_from_np_config(
                    rig_name=rig_name,
                    modification_date=modification_date,
                )
                rig_model.write_standard_file(temp_dir)
                rig_model_path = pathlib.Path(temp_dir) / "rig.json"
                added_path = storage.update_item(
                    storage_directory,
                    rig_model_path,
                    rig_name,
                )
                logger.debug("Stored rig model at: %s" % added_path)


# @cli.command()
# @click.argument("storage-directory", type=pathlib.Path)
# def list_rigs(storage_directory: pathlib.Path) -> None:
#     items = storage.list_items(storage_directory)
#     for item in items:
#         click.echo(item)


@cli.command()
@click.argument("storage-directory", type=pathlib.Path)
@click.argument("rig-name", type=click.Choice(["NP1", "NP2", "NP3"]))
@click.argument("rig-source", type=pathlib.Path)
def update_stored_rig(
    storage_directory: pathlib.Path, rig_name: str, rig_source: pathlib.Path
) -> None:
    added_path = storage.update_item(
        storage_directory,
        rig_source,
        rig_name,
    )
    logger.debug("Stored rig model at: %s" % added_path)
    click.echo("Updated stored rig model for: %s" % rig_name)


if __name__ == "__main__":
    cli()
