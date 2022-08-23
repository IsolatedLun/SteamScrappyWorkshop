from includes.Log4Py.Configurer.const import (
    LOGGING_COLOR_CODES, LOGGING_FORMAT, LOGGING_DIR, LOGGING_MESSAGE_FORMAT)
from includes.Log4Py.utils import (
    default_log_saver, prop_or_default, get_path_file_name)

from typing import Callable
from types import ModuleType


def create_config(
    main: ModuleType,
    color_codes: dict = None,
    save_func: Callable = None,
    save_func_args: tuple = None,
    log_path: str = None
):

    log_path = prop_or_default(
        log_path, f'{get_path_file_name(main.__file__)}.log.txt')
    return {
        'color_codes': prop_or_default(color_codes, LOGGING_COLOR_CODES),
        'log_path': log_path,
        'format': LOGGING_FORMAT,
        'message_format': LOGGING_MESSAGE_FORMAT,

        'save_func': prop_or_default(save_func, default_log_saver),
        'save_func_args': prop_or_default(save_func_args, (LOGGING_DIR, log_path))
    }
