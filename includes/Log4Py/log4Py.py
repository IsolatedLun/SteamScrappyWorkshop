from includes.Log4Py.Configurer.configurer import create_config
from includes.Log4Py.utils import (create_function_log_dict,
                                   get_func_name_from_stack,
                                   is_function,
                                   prettify_params,
                                   show_res_or_err
                                   )

from datetime import datetime
from inspect import stack
from colorama import Fore, init as coloroma_int

coloroma_int()


class Logger(object):
    def __init__(self, main, config={}):
        self.run_checks(main, config)

        self.main = main
        self.config: dict = create_config(self.main, **config)

    # =============
    # Decorators
    # =============
    def watch(self, func):
        """
            Decorator function used for watching/logging functions.
        """

        def watch_wrapper(*args, **kwargs):
            result: dict = None
            to_log: dict = None
            err: Exception = None

            try:
                result = to_log = func(*args, **kwargs)
            except Exception as e:
                to_log = show_res_or_err(result, e, self.main)
                err = e

            msg: str = f'Executed func <{func.__name__}({prettify_params(*args, **kwargs)})> => {to_log}'
            if err:
                self.error(msg, create_function_log_dict(
                    func.__name__, args, kwargs, result, err))
            else:
                self.debug(msg, create_function_log_dict(
                    func.__name__, args, kwargs, result))

            return result

        return watch_wrapper

    # =============
    # Setters
    # =============
    def set_log_saver(self, target=None, args=()):
        """
            Sets the custom user function that saves logs.
        """
        if target is not None and is_function(target):
            self.config['save_func'] = target
            self.config['save_func_args'] = args
        else:
            self.warn(
                f'Save function must be a function, not "{type(target)}".')

    def set_level(self, level_name: str, color_code: int, allow_log_func_creation: bool = True, silent: bool = True):
        override = self.config['color_codes'].get(level_name, False)
        self.config['color_codes'][level_name.upper()] = color_code

        if override:
            self.alter(f'Changed level from "{override}" to {level_name}.')
        else:
            if allow_log_func_creation:
                setattr(self, level_name.lower(), self.log)

                if not silent:
                    self.alter(f'Created log function {level_name.lower()}().')
            if not silent:
                self.alter(f'Set new level {level_name}.')

    # ======================
    # Log functions
    # ======================

    def __log(self, to_log, _type, obj, in_save):
        """
            Typical log function.
            Displays log data and adds it somewhere depending on the config
        """

        func_name = get_func_name_from_stack(stack())

        def decide_type():
            """
                Checks to see if the function is a custom added one, if so the type gets set to the function's name,
                else it returns the type if it's not None, otherwise returns 'INFO'
            """

            if _type is None and not self.config['color_codes'].get(_type, False):
                return func_name.upper() if self.config['color_codes'].get(func_name.upper(), False) else 'INFO'
            return _type

        _type = decide_type()

        log_time: str = str(datetime.now())
        to_display: str = self.config['format'].format(
            time=log_time, msg=to_log, type=self.config['color_codes'][_type])

        if self.config['save_func'] and not in_save:
            if obj is None:
                obj = {}

            obj['log_message'] = to_log
            obj['log_level'] = _type
            obj['datetime'] = log_time

            self.config['save_func'](obj, *self.config['save_func_args'])

        print(to_display)

    # ======================
    # Init functions
    # ======================
    def run_checks(self, main, config):
        if getattr(main, '__name__', None) is None:
            raise ValueError('No "__main__" module found.')

        if type(config) != dict:
            raise ValueError(f'Config must be a {dict}, not "{type(config)}".')

    # =================
    # Log functions
    # =================
    def log(self, msg: str, type=None, obj=None,
            in_save=False): return self.__log(msg, type, obj, in_save)

    def debug(self, msg: str, obj=None, in_save=False): return self.__log(
        msg, 'INFO', obj, in_save)

    def alter(self, msg: str, obj=None, in_save=False): return self.__log(
        msg, 'ALTER', obj, in_save)

    def warn(self, msg: str, obj=None, in_save=False): return self.__log(
        msg, 'WARN', obj, in_save)

    def error(self, msg: str, obj=None, in_save=False): return self.__log(
        msg, 'ERR', obj, in_save)
