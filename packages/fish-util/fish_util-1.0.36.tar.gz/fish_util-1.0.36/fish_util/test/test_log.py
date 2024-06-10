from ez_fish_util.src.loguru_util import print, debug, info, warning, error, critical
from fish_util.src.loguru_util import print as print2


def test_log_debug():
    debug("This is a debug message")


def test_log_info():
    info("This is an info message")


def test_log_warning():
    warning("This is a warning message")


def test_log_error():
    error("This is an error message")


def test_log_critical():
    critical("This is a critical message")


def test_log_print():
    print("This is a print message")


if __name__ == "__main__":
    test_log_debug()
    test_log_info()
    test_log_warning()
    test_log_error()
    test_log_critical()
    test_log_print()
    print2("This is a print2 message")
