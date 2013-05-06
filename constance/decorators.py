from functools import wraps
from constance import config

def override_constance_settings(**settings):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old_values = {}

            for key, value in settings.items():
                old_values[key] = getattr(config, key)
                setattr(config, key, value)

            try:
                result = func(*args, **kwargs)
            finally:
                for key, value in old_values.items():
                    setattr(config, key, value)

        return wrapper
    return decorator


