import os
import pytest


def main():
    print(__file__)
    pytest.main(["--alluredir", "./cache/allure-result", "--clean-alluredir"])
    os.system("allure serve ./cache/allure-result ")


if __name__ == "__main__":
    main()
