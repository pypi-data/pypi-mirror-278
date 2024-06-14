import logging
import os
import uuid
import shutil
import pandas as pd
from pathlib import Path
from typing import Union, Optional, List
from tqdm import tqdm
from fastdup.vl.common.settings import Settings

Settings.IS_FASTDUP = True

import psutil
import sqlalchemy as sa
from duckdb.duckdb import IOException
from fastdup.vl.common.logging_init import get_fastdup_logger, get_vl_logger, get_timing_logger
from fastdup.vl.utils import sentry
from fastdup.fastdup_runner.run_checker import check_server_problems, check_existing_dataset
from fastdup.fastdup_runner.fastdup_runner_pipeline import run_pipeline
from fastdup.fastdup_runner.fastdup_runner_sync_db import run_sync_db
from fastdup.fastdup_runner.fastdup_runner_server.fastdup_runner_server_launcher import launch_server
from fastdup.fastdup_runner.utilities import update_pbar, switch_fastdup_log_level
from fastdup.vldbaccess import connection_manager
from fastdup.fastdup_runner.utilities import ExplorationError, GETTING_STARTED_LINK
from fastdup.pipeline.common.dataset_db_updater import PipelineFatalError

UNKNOWN_ERROR_MSG = f"""
Could not launch the Visual Layer application on your machine due to an unexpected error.
For more information, use help(fastdup) or check our documentation {GETTING_STARTED_LINK}."""

KEYBOARD_INTERRUPT_ERROR_MSG = f"""
Could not launch the Visual Layer application on your machine because operation was aborted.

If this was accidental or unexpected, please try again. 

For more information, use help(fastdup) or check our documentation {GETTING_STARTED_LINK}."""

logger = get_fastdup_logger(__name__)
APP_PATH = Path(__file__).parent.parent


def init(work_dir: Union[str, Path], input_dir: Optional[Union[str, Path, List[str], pd.DataFrame]],
         dataset_name: Optional[str], overwrite: bool) -> Union[str, Path, List[str], pd.Series]:
    work_dir = os.path.abspath(work_dir)
    Settings.PIPELINE_ROOT = Path(work_dir)
    os.makedirs(Settings.PIPELINE_ROOT, exist_ok=True)

    connection_manager.reset_pool()
    Settings.PG_URI = f"duckdb:///{Settings.PIPELINE_ROOT / 'vl.duckdb'}"

    Settings.LOCAL_FE_DIR = os.environ.get('LOCAL_FE_DIR', Path(__file__).parent / 'fastdup_runner_server' / 'frontend')

    available_ram_gb = psutil.virtual_memory().available / (1024 ** 3)
    Settings.LIMIT_NUM_IMAGES = int((100_000 * available_ram_gb) / 32)
    Settings.LIMIT_NUM_OBJECTS = int((100_000 * available_ram_gb) / 32)
    Settings.MAX_NUM_OF_IMAGES = 1_000_000
    Settings.MAX_OBJECT_COUNT = 1_000_000
    Settings.CDN_FULLPATH = 'cdn'
    Settings.ISSUES_DATA_EXISTS = True
    Settings.USER_TAGS_ENABLED = True
    Settings.ACTIONS_CART_ENABLED = True
    Settings.FILE_FILTER_ENABLED = True
    Settings.FILE_FILTER_TREE_MAX_DEPTH = 10
    Settings.FILE_FILTER_TREE_INCLUDE_FILES = False
    Settings.MIN_NUM_OF_IMAGES = 10
    Settings.LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.FATAL)
    Settings.PERSIST_EMBEDDINGS = True
    Settings.STORAGE_KEY = 'WtDmWYVGFYjRLimCFBUHZx-323r84JJ4zkquVkzi6Vc='
    Settings.DISABLE_AUTH = True
    Settings.VISUAL_SEARCH_ENABLED = False
    Settings.VECTOR_SEARCH_ENABLED = True
    get_vl_logger().setLevel(Settings.LOG_LEVEL)  # update pipeline log level
    get_timing_logger().setLevel(Settings.LOG_LEVEL)  # update timing log level

    Settings.SENTRY_OPT_OUT = False
    Settings.SENTRY_PROJ = "https://b526f209751f4bcea856a1d90e7cf891@o4504135122944000.ingest.sentry.io/4504168616427520"
    sentry.init_sentry(environment="fastdupExploration")

    # check overwrite before writing new annotations (if exist)
    if overwrite:
        overwrite_previous_run()

    if isinstance(input_dir, pd.DataFrame):
        metadata_dir: Path = Settings.PIPELINE_ROOT / 'input' / 'metadata'
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        if all([col in input_dir.columns for col in ['col_x', 'row_y', 'width', 'height']]):
            input_dir.to_parquet(metadata_dir / 'object_annotations.parquet', index=False)
        else:
            input_dir.to_parquet(metadata_dir / 'image_annotations.parquet', index=False)
    
        input_dir = input_dir['filename'].unique()

    if dataset_name is None:
        if isinstance(input_dir, (str, Path)):
            dataset_name = os.path.basename(str(input_dir))
        else:
            dataset_name = 'Dataset'

    Settings.DATASET_NAME = dataset_name

    return input_dir

def init_db():
    migration_files = [APP_PATH / 'clustplorer-be/db.duckdb.sql', ]
    try:
        with connection_manager.get_session(autocommit=True) as session:
            for migration_file in migration_files:
                session.execute(sa.text(open(migration_file).read()))
    except IOException:
        raise ExplorationError("Database already exists, please overwrite the existing database or set a different work_dir")


def configure_dataset(dataset_id: uuid.UUID):
    Settings.DATASET_ID = dataset_id
    Settings.VISUAL_SEARCH_ENABLED_DATASET_ID = dataset_id


def cleanup() -> None:
    shutil.rmtree(Settings.PIPELINE_ROOT / 'processing', ignore_errors=True)
    shutil.rmtree(Settings.PIPELINE_ROOT / 'input', ignore_errors=True)

def delete_previous_run(previous_run_folder: str) -> None:
    artifacts = ["cdn", "input", "processing", "vl.duckdb"]
    for artifact in artifacts:
        artifact_path = Path(previous_run_folder) / artifact
        if artifact_path.exists():
            if artifact_path.is_dir():
                shutil.rmtree(artifact_path)
            else:
                os.remove(artifact_path)


def overwrite_previous_run() -> None:
    try:
        delete_previous_run(previous_run_folder=Settings.PIPELINE_ROOT)
    except PermissionError:
        logger.error(
            f"Cannot run with overwrite=True in work_dir: {Settings.PIPELINE_ROOT} due to insufficient permissions. "
            f"Please make sure you have the right permissions or set a different work_dir.")
        return

    # Reinitialize the database since it's not enough just to delete the db file to start from scratch
    # (there might be in-memory populated tables taken from the file)
    init_db()


def do_visual_layer(work_dir: Union[str, Path],
                    input_dir: Optional[Union[str, Path, List[str]]] = None,
                    dataset_name: Optional[str] = None,
                    overwrite: bool = False,
                    run_server: bool = True) -> None:
    fastdup_log_level = switch_fastdup_log_level(logging.FATAL)  # this solution is super ugly and should be replaced ASAP

    input_dir = init(work_dir, input_dir, dataset_name, overwrite)
    dataset_id = check_existing_dataset()

    try:
        if dataset_id:
            if input_dir is not None or dataset_name is not None:
                logger.warning(
                    f"** WARNING **: Dataset already exists in this work_dir so input_dir and dataset_name will be ignored."
                    f" If you want to run with a different dataset, please set overwrite=True or set a different work_dir.")
            configure_dataset(dataset_id)
        else:
            if input_dir is None:
                logger.error("input_dir is required for the first run")
                return
            pbar = tqdm(total=3)
            configure_dataset(uuid.uuid4())
            init_db()
            run_pipeline(input_dir, pbar)
            run_sync_db()
            cleanup()
            update_pbar(pbar, 'Done')

        if run_server:
            check_server_problems()
            launch_server()
    except KeyboardInterrupt as e:
        raise KeyboardInterrupt(KEYBOARD_INTERRUPT_ERROR_MSG) from None
    except ExplorationError as e:
        raise e
    except PipelineFatalError as e:
        if isinstance(e.__cause__, KeyboardInterrupt):
            raise KeyboardInterrupt(KEYBOARD_INTERRUPT_ERROR_MSG) from None
        else:
            raise ExplorationError(e) from e
    except Exception as e:
        if isinstance(e.__cause__, KeyboardInterrupt):
            raise KeyboardInterrupt(KEYBOARD_INTERRUPT_ERROR_MSG) from None
        else:
            raise ExplorationError(UNKNOWN_ERROR_MSG) from e
    finally:
        switch_fastdup_log_level(fastdup_log_level)  # this solution is super ugly and should be replaced ASAP
