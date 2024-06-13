# fasthep-logging

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Gitter][gitter-badge]][gitter-link]

The FAST-HEP logging package adds two new log levels to the standard Python
logging:

- `TRACE` is the most verbose level, and is used for debugging purposes.
- `TIMING` is used to log timing information. Log level is between `DEBUG` and
  `WARNING`.

In addition, this package sets a logging standard for FAST-HEP projects:

- per-log-level formatting
- log file support

## Example

```python
from fasthep_logging import get_logger, TRACE

log = get_logger("FASTHEP::Carpenter")
log.setLevel(TRACE)

...

log.debug("This is a debug message %s", msg)
log.trace("This is a verbosity level higher than DEBUG")


from codetiming import Timer

with Timer(
    text=f"Processing data took {{:.3f}}s for {file_path}",
    logger=log.timing,  # type: ignore[attr-defined]
):
    process_data(file_path)
```

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/FAST-HEP/fasthep-logging/workflows/CI/badge.svg
[actions-link]:             https://github.com/FAST-HEP/fasthep-logging/actions
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/orgs/FAST-HEP/discussions
[gitter-badge]:             https://badges.gitter.im/FAST-HEP/community.svg
[gitter-link]:              https://gitter.im/FAST-HEP/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[pypi-link]:                https://pypi.org/project/fasthep-logging/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/fasthep-logging
[pypi-version]:             https://badge.fury.io/py/fasthep-logging.svg
[rtd-badge]:                https://readthedocs.org/projects/fasthep-logging/badge/?version=latest
[rtd-link]:                 https://fasthep-logging.readthedocs.io/en/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
<!-- prettier-ignore-end -->
