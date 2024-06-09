import logging, os, sys
from contextlib import contextmanager


@contextmanager
def suppress_std():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull

        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class Formatter(logging.Formatter):
    grey = "\x1b[38;20m"
    cyan = "\x1b[36;20m"
    purple = "\x1b[35;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    RESET = "\x1b[0m"
    # format = "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    # format = "[%(name)s](%(levelname)s) | %(asctime)s -> %(message)s"
    COLORS = {
        logging.DEBUG: purple,
        logging.INFO: cyan,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red,
    }
    # FORMATS = {
    #     logging.DEBUG: f"{purple}{format}{RESET}",
    #     logging.INFO: f"{cyan}{format}{RESET}",
    #     logging.WARNING: f"{yellow}{format}{RESET}",
    #     logging.ERROR: f"{red}{format}{RESET}",
    #     logging.CRITICAL: f"{bold_red}{format}{RESET}",
    # }

    def __init__(self, fmt, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.RESET)
        hyperlink = f"\x1b]8;;file://{record.pathname}\a{record.filename}:{record.lineno}\x1b]8;;\a"
        record.msg = f"{log_color}{record.msg}{self.RESET} ({hyperlink})"

        # formatted_message = f"[{record.name}]({record.levelname}) | {self.formatTime(record, '%H:%M:%S')} -> {record.msg}"

        return f"{log_color}[{record.name}]({record.levelname}){self.RESET} | {self.formatTime(record, self.datefmt)} -> {record.msg}"


def mklog(name, level=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.handlers.clear()

    # for handler in logger.handlers:
    #     logger.removeHandler(handler)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(
        Formatter(
            "[%(name)s](%(levelname)s) | %(asctime)s -> %(message)s",
            datefmt="%H:%M:%S",
        )
    )

    logger.addHandler(ch)

    # Disable log propagation
    logger.propagate = False

    return logger


def getLogger(name=None, level=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    for h in logger.handlers[:]:
        logger.removeHandler(h)
        h.close()

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(
            Formatter(
                "[%(name)s](%(levelname)s) | %(asctime)s -> %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(ch)

        # Disable log propagation to prevent duplicate logs
        logger.propagate = False

    return logger
