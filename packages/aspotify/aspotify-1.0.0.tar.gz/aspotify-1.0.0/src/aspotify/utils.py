import logging
import pathlib


def setup_logger(name: str, filename: str) -> logging.Logger:
    """
    Configures and returns a logger with the specified name and filename.

    Parameters
    ----------
    name : str
        The name of the logger.

    filename : str
        The name of the log file (without the directory path).

    Returns
    -------
    Logger
        A configured logger instance.

    Example
    -------
    >>> logger = setup_logger("API:", "api.log")
    >>> logger.info("This is an informational message.")

    Directory
    ---------
    ~/.spotify/log/
    """
    logging.basicConfig(
        filename=pathlib.Path.home() / f".spotify/log/{filename}",
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)
