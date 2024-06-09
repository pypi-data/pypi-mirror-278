import argparse
import logging
import os
import pathlib
import sys

import coloredlogs

from .importers.strava_checkout import convert_strava_checkout
from .importers.strava_checkout import import_from_strava_checkout
from geo_activity_playground.core.activities import ActivityRepository
from geo_activity_playground.core.activities import embellish_time_series
from geo_activity_playground.core.cache_migrations import apply_cache_migrations
from geo_activity_playground.core.config import get_config
from geo_activity_playground.explorer.tile_visits import compute_tile_evolution
from geo_activity_playground.explorer.tile_visits import compute_tile_visits
from geo_activity_playground.explorer.video import explorer_video_main
from geo_activity_playground.importers.directory import import_from_directory
from geo_activity_playground.importers.strava_api import import_from_strava_api
from geo_activity_playground.webui.app import webui_main

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Utilities to work with recorded activities."
    )
    parser.set_defaults(func=lambda options: parser.print_help())
    parser.add_argument("--basedir", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument(
        "--loglevel",
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
    )

    subparsers = parser.add_subparsers(
        description="The tools are organized in subcommands.", metavar="Command"
    )

    # subparser = subparsers.add_parser(
    #     "explorer",
    #     help="Generate GeoJSON/GPX files with explored and missing explorer tiles.",
    # )
    # subparser.set_defaults(
    #     func=lambda options: main_explorer(
    #         make_time_series_source(options.basedir)
    #     )
    # )

    subparser = subparsers.add_parser(
        "explorer-video", help="Generate video with explorer timeline."
    )
    subparser.set_defaults(func=lambda options: explorer_video_main())

    subparser = subparsers.add_parser(
        "convert-strava-checkout",
        help="Converts a Strava checkout to the structure used by this program.",
    )
    subparser.set_defaults(
        func=lambda options: convert_strava_checkout(
            options.checkout_path, options.playground_path
        )
    )
    subparser.add_argument("checkout_path", type=pathlib.Path)
    subparser.add_argument("playground_path", type=pathlib.Path)

    subparser = subparsers.add_parser("serve", help="Launch webserver")
    subparser.set_defaults(
        func=lambda options: webui_main(
            make_activity_repository(options.basedir, options.skip_strava),
            host=options.host,
            port=options.port,
        )
    )
    subparser.add_argument(
        "--host", default="127.0.0.1", help="IP address to listen on"
    )
    subparser.add_argument(
        "--port", default=5000, type=int, help="the port to run listen on"
    )
    subparser.add_argument("--skip-strava", action=argparse.BooleanOptionalAction)

    subparser = subparsers.add_parser("cache", help="Cache stuff")
    subparser.set_defaults(
        func=lambda options: make_activity_repository(options.basedir, False)
    )

    options = parser.parse_args()
    coloredlogs.install(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=options.loglevel.upper(),
    )

    logging.getLogger("stravalib.protocol.ApiV3").setLevel(logging.WARNING)

    options.func(options)


def make_activity_repository(
    basedir: pathlib.Path, skip_strava: bool
) -> ActivityRepository:
    os.chdir(basedir)
    apply_cache_migrations()
    config = get_config()

    if not config.get("prefer_metadata_from_file", True):
        logger.error(
            "The config option `prefer_metadata_from_file` is deprecated. If you want to prefer extract metadata from the activity file paths, please use the new `metadata_extraction_regexes` as explained at https://martin-ueding.github.io/geo-activity-playground/getting-started/using-activity-files/#directory-structure."
        )
        sys.exit(1)

    repository = ActivityRepository()

    if pathlib.Path("Activities").exists():
        import_from_directory(
            repository,
            config.get("metadata_extraction_regexes", []),
        )
    if pathlib.Path("Strava Export").exists():
        import_from_strava_checkout(repository)
    if "strava" in config and not skip_strava:
        import_from_strava_api(repository)

    if len(repository) == 0:
        logger.error(
            f"No activities found. You need to either add activity files (GPX, FIT, …) to {basedir/'Activities'} or set up the Strava API. Starting without any activities is unfortunately not supported."
        )
        sys.exit(1)

    embellish_time_series(repository)
    compute_tile_visits(repository)
    compute_tile_evolution()
    return repository


if __name__ == "__main__":
    main()
