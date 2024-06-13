from __future__ import annotations

from time import sleep

from codetiming import Timer

from fasthep_logging import TIMING
from fasthep_logging import get_logger as flogger

logger = flogger("console_log", TIMING)

logger.info("This is an info message")
logger.warning("This is a warning message")
logger.debug("This is a debug message")
logger.timing("This is a timing message")
logger.trace("This is a trace message")

# example with codetiming

with Timer(
    text="Elapsed time: {:.2f} seconds for sleeping 2 seconds",
    logger=logger.timing,
):
    sleep(2)
