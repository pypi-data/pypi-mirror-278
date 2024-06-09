"""Decorators for ComponentService"""


def initialize_check(initialize_must_be_run=True):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            cls = self.__class__.__name__
            if initialize_must_be_run and not self._executed_initialize:
                raise AttributeError(
                    f"Method '{cls}.initialize' must be run before calling '{cls}.{method.__name__}()'."
                )
            elif not initialize_must_be_run and self._executed_initialize:
                raise AttributeError(
                    f"Method '{cls}.initialize' has already been run. '{cls}.{method.__name__}()' can only be run before calling `initialize`."
                )
            return method(self, *args, **kwargs)

        return wrapper

    return decorator
