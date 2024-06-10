from pathlib import Path
from loguru import logger

def valid_output_path(folder: str) -> bool:
    if not Path(folder).exists():
        logger.error(f'The output folder does not exist: {folder}')
        return False
    return True
