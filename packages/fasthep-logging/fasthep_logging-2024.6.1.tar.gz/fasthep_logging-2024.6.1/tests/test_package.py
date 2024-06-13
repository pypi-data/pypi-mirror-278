from __future__ import annotations

import logging

import pytest

import fasthep_logging as m


def test_version() -> None:
    assert m.__version__


def test_getLogger() -> None:
    logger = m.get_logger("TESTLOGGER")
    assert logger.name == "TESTLOGGER"
    assert logger.level == m.DEFAULT_LOG_LEVEL
    assert logger.TRACE == m.TRACE  # type: ignore[attr-defined]
    assert logger.TIMING == m.TIMING  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    ("level", "func"),
    [(logging.INFO, "info"), (m.TRACE, "trace"), (m.TIMING, "timing")],
)
def test_logging(caplog: pytest.LogCaptureFixture, level: int, func: str) -> None:
    logger = m.get_logger("TESTLOGGER")
    logger.propagate = True
    caplog.set_level(level, logger="TESTLOGGER")

    getattr(logger, func)("test")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.name == "TESTLOGGER"
    assert record.levelname == logging.getLevelName(level)
    assert record.message == "test"
