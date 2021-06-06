import logging
import subprocess
import pathlib

def get_logger_for_task(task):
    logger = logging.getLogger(str(task._id))
    if not logger.hasHandlers():
        fileh = logging.FileHandler(task.get_file_log(), "a")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fileh.setFormatter(formatter)
        logger.addHandler(fileh)
    logger.setLevel(logging.INFO)
    return logger


def get_last_line_of_file(file_path):
    if pathlib.Path(file_path).exists():
        return subprocess.check_output(['tail', '-1', file_path]).decode()
    return ""
