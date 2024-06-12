from functools import wraps

def enforce_pydantic_model(model_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, model_class):
                    break
            else:
                raise TypeError(f"Expected instance of {model_class.__name__}, got {type(arg)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
