from functools import wraps
from constance import config
from django.test import TransactionTestCase

def override_constance_settings(**settings):
    old_values = {}

    def enable():
        old_values.clear()
        for key, value in settings.items():
            old_values[key] = getattr(config, key)
            setattr(config, key, value)

    def disable():
        for key, value in old_values.items():
            setattr(config, key, value)

    def decorator(func):
        if isinstance(func, type) and issubclass(func, TransactionTestCase):
            original_pre_setup = func._pre_setup
            original_post_teardown = func._post_teardown

            def _pre_setup(self):
                enable()
                original_pre_setup(self)

            def _post_teardown(self):
                original_post_teardown(self)
                disable()

            func._pre_setup = _pre_setup
            func._post_teardown = _post_teardown
            return func


        @wraps(func)
        def wrapper(*args, **kwargs):
            enable()

            try:
                return func(*args, **kwargs)
            finally:
                disable()

        return wrapper
    return decorator


