import logging
import sys


def has_level_handler(logger: logging.Logger) -> bool:
    """Check if there is a handler in the logging chain that will handle the given logger's effective level."""
    level = logger.getEffectiveLevel()
    current = logger

    while current:
        if any(handler.level <= level for handler in current.handlers):
            return True

        if not current.propagate:
            break

        current = current.parent

    return False


default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))


def create_logger(app) -> logging.Logger:
    logger = logging.getLogger(app.name)

    if app.debug and not logger.level:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(app.log_level)

    if not has_level_handler(logger):
        logger.addHandler(default_handler)
        logger.propagate = True

    return logger