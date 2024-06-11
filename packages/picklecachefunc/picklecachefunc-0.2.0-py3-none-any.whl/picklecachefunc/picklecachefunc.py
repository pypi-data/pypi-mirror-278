import os
import pickle
from functools import wraps

def check_cache(arg_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find the named argument in kwargs
            if arg_name in kwargs:
                file_name = kwargs[arg_name]
            else:
                raise ValueError(f"Argument '{arg_name}' not found in function call")

            # Check if the file exists
            if os.path.exists(file_name):
                # Load the object from the file
                with open(file_name, 'rb') as file:
                    result = pickle.load(file)
                print(f"Loaded result from {file_name}")
            else:
                # Execute the function and save the output to the file
                result = func(*args, **kwargs)
                with open(file_name, 'wb') as file:
                    pickle.dump(result, file)
                print(f"Saved result to {file_name}")
            return result
        return wrapper
    return decorator
