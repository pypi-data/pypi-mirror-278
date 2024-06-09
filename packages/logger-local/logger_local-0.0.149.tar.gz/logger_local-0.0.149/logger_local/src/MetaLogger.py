import inspect
import re
import sys
from abc import ABCMeta
from functools import lru_cache
from functools import wraps
from typing import Mapping

from .LoggerLocal import Logger


class MetaLogger(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs) -> Mapping[str, object]:
        """This method is called before the class is created. It is used to create the class namespace."""
        return super().__prepare__(name, bases, **kwargs)

    def __new__(cls, name, bases, dct, **kwargs) -> type:
        # kwargs may be empty if the class is not instantiated with the metaclass
        cls.logger: Logger = None  # noqa add logger to the namespace (for typing)
        if not kwargs:
            if not bases:
                raise ValueError("Please provide a logger object to the MetaLogger metaclass")
            if any(base.__name__ == "ABC" for base in bases):
                return super().__new__(cls, name, bases, dct)
            kwargs = {"object": {'bases': bases}}
        kwargs['object']['class'] = name
        kwargs['is_meta_logger'] = True
        logger = Logger.create_logger(**kwargs)
        dct['logger'] = logger

        for key, value in dct.items():
            if callable(value) and (not key.endswith("__") or key == "__init__"):  # Exclude magic methods
                dct[key] = cls.wrap_function(value, logger)

        # Add __repr__ to the class namespace, even if explicitly defined in the class
        # because otherwise logger.start in init will fail (if __repr__ is already defined)
        def __repr__(self):
            # get init arguments
            # TODO: avoid recursive `self` repr in inheritance
            args = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
            return f"{self.__class__.__name__}({args})"

        dct["__repr__"] = __repr__
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def wrap_function(func: callable, logger: Logger) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> any:
            # Obtain the module name of the wrapped function
            function_module = getattr(func, '__module__', None) or func.__globals__.get('__name__', 'unknown_module')

            signature = inspect.signature(func)
            arg_names = [param.name for param in signature.parameters.values()]
            if len(args) + len(kwargs) == len(arg_names) + 1:  # staticmethod called with class instance
                args = args[1:]

            kwargs_updated = {**dict(zip(arg_names, args)), **kwargs.copy()}
            # if it has __wrapped__, func = func.__wrapped__  (for functools.wraps)
            real_func = func.__dict__.get("__wrapped__", func)
            filename = inspect.getfile(real_func) if not isinstance(real_func, staticmethod) else inspect.getfile(
                real_func.__func__)
            extra_kwargs = {"function_name": real_func.__name__, "class_name": real_func.__qualname__.split(".")[0],
                            "filename": filename,
                            "path": f"{function_module}.{real_func.__qualname__}"}
            kwargs_updated["extra_kwargs"] = extra_kwargs

            full_function_name = f"{function_module}.{real_func.__qualname__}"
            logger.start(full_function_name, object=kwargs_updated)
            result = None
            try:
                logger.depth = 5
                # TODO: add warning if the typing doesn't match (and not None)
                result = func(*args, **kwargs)
                logger.depth = 6
            except Exception as exception:
                # Use traceback to capture frame information
                # Use sys.exc_info() to get exception information
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # Extract the frame information from the traceback
                frame = (exc_traceback.tb_next or exc_traceback).tb_frame
                # Get the local variables
                locals_before_exception = frame.f_locals

                # use logger.exception if the caller is a test
                logger.error(full_function_name, object={"exception": exception,
                                                         "locals_before_exception": locals_before_exception,
                                                         "extra_kwargs": kwargs_updated})
                raise exception

            finally:
                logger.end(full_function_name, object={get_return_variable(func): result,
                                                       "extra_kwargs": kwargs_updated})
            return result

        return wrapper

    # TODO: add a single function wrapper


@lru_cache(maxsize=64)
def get_return_variable(func: callable) -> str:
    """returns only the first meaningful return statement of the function, if exists."""
    source_lines, _ = inspect.getsourcelines(func)
    return_pattern = re.compile(r'return\s+(?!None)([^#\n\s]+)')  # cached by re

    # Search for the pattern in the source code
    return_match = return_pattern.search('\n'.join(source_lines))

    # If a match is found, extract and return the meaningful return variable, otherwise return 'result'
    return return_match.group(1).strip() if return_match else "result"


class ABCMetaLogger(MetaLogger, ABCMeta):
    """When using abstract class, use this class to avoid conflicts with MetaLogger.
    Example:
    from abc import ABC
    class AbstractClass(ABC, metaclass=ABCMetaLogger):
        pass
    """

    def __new__(cls, name, bases, dct, **kwargs) -> type:
        cls.logger = None  # add logger to the namespace (for typing)
        return super().__new__(cls, name, bases, dct, **kwargs)
