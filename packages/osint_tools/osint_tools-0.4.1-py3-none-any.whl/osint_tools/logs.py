import logging.config
from osint_tools.settings import get_settings


def setup_logging(path: str = './osint_tools/logger.json') -> None:
    '''Custom logger setup.

    https://docs.python.org/3/library/logging.config.html
    '''
    import os.path
    import json
    import pathlib
    try:
        assert os.path.exists(path), f'Logging config file not found @: {path}'

        conf_file = pathlib.Path(path)
        with open(conf_file) as f_in:
            config = json.load(f_in)

        logging.config.dictConfig(config)

    except AssertionError as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(f'Unknown error loading logger::{e!s}')


setup_logging()
settings = get_settings()
logger = logging.getLogger(settings.LOGGER_NAME)
