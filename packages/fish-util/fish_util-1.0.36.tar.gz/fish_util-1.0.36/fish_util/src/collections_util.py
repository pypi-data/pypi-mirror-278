from ruamel import yaml
import time
from collections import namedtuple

from box import Box

Settings = namedtuple("Settings", ["version", "buildtime"])


# 写一个函数，实现自增版本号并更新配置文件
def update_version(settings):
    print(settings)
    version = settings["version"]
    buildtime = settings["buildtime"]
    print(f"Version: {version}")
    print(f"Build Time: {buildtime}")

    # 将字典转对象
    settings_obj = Settings(**settings)

    # 打印对象属性
    print(f"Obj Version: {settings_obj.version}")
    print(f"Obj Build Time: {settings_obj.buildtime}")

    # 将对象转字典
    settings = dict(settings_obj._asdict())

    # 使用新的配置值,将version:0.0.1的第3个小版本号加1，并更新配置文件
    version_parts = version.split(".")
    version_parts[2] = str(int(version_parts[2]) + 1)
    settings["version"] = ".".join(version_parts)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    settings["buildtime"] = timestamp

    # 打印更新后的配置数据
    print(f"New Settings: {settings}")


def main():
    print(__file__)
    settings = dict(version="0.0.1", buildtime="2021-01-01 00:00:00")
    update_version(settings)


if __name__ == "__main__":
    main()
