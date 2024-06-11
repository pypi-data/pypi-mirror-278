![Clubbi-logo](https://user-images.githubusercontent.com/32624827/160703813-03249a14-9f4f-46a4-a7c1-f46686e97459.png)

# clubbi_json

## Requisitos

- [Python 3.11](https://www.python.org/downloads/release/python-390/)
- [pipenv](https://pipenv.pypa.io/en/latest/)
- [pydantic](https://pypi.org/project/pydantic/)
- [clubbi-json](https://pypi.org/project/clubbi-json/)


## Funcionalidades

### Logger
```python
from clubbi_logger import logging

logging.logger.info("message")
logging.logger.exception(dict(message="message"))

```

### JSON Logger 
```python
from clubbi_logger import json_logging

json_logging.jlogger.warning(
    "message", 
    key=value,
    )

```
