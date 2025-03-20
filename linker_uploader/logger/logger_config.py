from loguru import logger
import  sys
import os

def setup_logger():
    logger.remove()

    logger.add(
        sys.stderr,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    log_dir = os.getcwd()
    log_path = os.path.join(log_dir, "app_{time:YYYY-MM-DD_HH-mm-ss}.log")

    logger.add(
        log_path,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    return logger

configured_logger = setup_logger()