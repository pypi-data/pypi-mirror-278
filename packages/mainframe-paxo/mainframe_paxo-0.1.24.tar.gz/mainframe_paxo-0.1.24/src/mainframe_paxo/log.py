import logging

from click import echo


class ClickHandler(logging.Handler):
    """A logging handler that sends log messages to click.echo"""

    def emit(self, record):
        """Emit a log message"""
        echo(self.format(record))


# initialize logging for click echo


def init(level=logging.INFO):
    """Initialize logging for click echo"""
    # set up logging
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(ClickHandler())
    logging.captureWarnings(True)
