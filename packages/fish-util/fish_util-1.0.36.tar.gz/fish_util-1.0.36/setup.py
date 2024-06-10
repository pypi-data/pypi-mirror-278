from setuptools import setup, find_packages
from fish_util.src.config_util import update_version

packages = find_packages()
print(packages)

# 使用
settings = update_version("settings.yaml")
print(f"New Settings: {settings}")

name = settings["name"]
print(f"Name: {name}")

setup(
    name=settings["name"],
    version=settings["version"],
    packages=packages,
    description=settings["description"],
    long_description=open(f"../{name}/README.md").read(),
    long_description_content_type="text/markdown",
    author=settings["author"],
    author_email=settings["author_email"],
    url=settings["url"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)


def main():
    print(__file__)


if __name__ == "__main__":
    main()
