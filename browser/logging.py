import logging
import os
import sys
from concurrent_log_handler import ConcurrentRotatingFileHandler
from browser.settings import LogSettings
from typing import Optional


def configure_logging(
    name: Optional[str] = None,
    log_level: int = LogSettings.level,
    log_dir: Optional[str] = LogSettings.log_dir,
    log_file_prefix: Optional[str] = LogSettings.log_file_prefix,
    backup_count: int = LogSettings.backup_count,
    encoding: str = LogSettings.encoding,
) -> logging.Logger:
    """
    A logger that supports log rotation and console output, using the ConcurrentRotatingFileHandler handler.

    :param name: The name of the logger, default is None, using the root logger.
    :param log_level: The log level, default is logging.DEBUG.
    :param log_dir: The log file directory, default is './log_files'.
    :param log_file_prefix: The log file prefix, default is 'app'.
    :param backup_count: The number of backup files to keep, default is 7.
    :param encoding: The log file encoding, default is 'utf-8'.
    :return: The configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create log directory
        if log_dir:
            log_dir = os.path.abspath(log_dir)
            os.makedirs(log_dir, exist_ok=True)

        # Configure concurrent log rotation handler
        if log_file_prefix:
            log_file_name = f"{log_file_prefix}.log"
            log_file_path = os.path.join(log_dir, log_file_name)
            rotating_file_handler = ConcurrentRotatingFileHandler(
                filename=log_file_path,
                # Set max file size to 10 MB
                maxBytes=10 * 1024 * 1024,
                backupCount=backup_count,
                encoding=encoding,
            )
            rotating_file_handler.setFormatter(formatter)
            logger.addHandler(rotating_file_handler)

        # Configure console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
