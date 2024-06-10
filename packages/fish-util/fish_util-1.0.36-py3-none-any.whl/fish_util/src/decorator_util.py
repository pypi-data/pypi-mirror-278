import time
import inspect
import traceback
import inspect
from functools import wraps
import fish_util.src.log_util as log_util

logger = log_util.FishLogger(__file__)
print = logger.debug


def trace_time(func):
    def wrapper(*args, **kwargs):
        # start the timer
        start_time = time.time()
        # call the decorated function
        result = func(*args, **kwargs)
        # remeasure the time
        end_time = time.time()
        # compute the elapsed time and print it
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        # return the result of the decorated function execution
        return result

    # return reference to the wrapper function
    return wrapper


def trace_args(func):
    def wrapper(*args, **kwargs):
        # print the fucntion name and arguments
        caller_frame = inspect.currentframe().f_back
        file_name = caller_frame.f_code.co_filename
        line_number = caller_frame.f_lineno
        print(
            f"Calling {func.__name__} at {file_name}:{line_number} with args: {args} kwargs: {kwargs}"
        )
        # call the function
        result = func(*args, **kwargs)
        # print the results
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


def trace_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Handle the exception
            exception_msg = traceback.format_exc()
            logger.error(f"An exception occurred: \n{exception_msg}")
            # Optionally, perform additional error handling or logging
            # Reraise the exception if needed

    return wrapper


def trace_validate(*validators):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            arg_names = list(inspect.signature(func).parameters.keys())
            # 将args和kwargs合并为一个列表，以便与validators一一对应
            all_args = list(args) + [
                kwargs.get(key)
                for key in func.__code__.co_varnames[
                    len(args) : func.__code__.co_argcount
                ]
            ]
            # 校验每个参数
            for name, validator, arg in zip(arg_names, validators, all_args):
                if not validator(arg):
                    # 获取validator的源代码
                    lambda_source = inspect.getsource(validator)
                    raise ValueError(
                        f"Invalid argument: {name}={arg}, expected: \n{lambda_source}"
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def trace_retry(max_attempts, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    time.sleep(delay)
            print(f"Function failed after {max_attempts} attempts")

        return wrapper

    return decorator
