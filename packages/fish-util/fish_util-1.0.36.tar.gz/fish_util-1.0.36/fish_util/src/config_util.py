from ruamel import yaml
import time


class YamlLoader:
    def __init__(self, file):
        self.file = file

    def file_load(self):
        with open(self.file, "r", encoding="utf-8") as f:
            data = f.read()
        return yaml.load(data, Loader=yaml.RoundTripLoader)

    def file_dump(self, data):
        with open(self.file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, Dumper=yaml.RoundTripDumper)


# 写一个函数，实现自增版本号并更新配置文件
def update_version(file_path):
    yml = YamlLoader(file_path)
    settings = yml.file_load()
    print(f"Settings: {settings}")
    version = settings["version"]
    buildtime = settings["buildtime"]

    # 使用新的配置值,将version:0.0.1的第3个小版本号加1，并更新配置文件
    version_parts = version.split(".")
    version_parts[2] = str(int(version_parts[2]) + 1)
    settings["version"] = ".".join(version_parts)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    settings["buildtime"] = timestamp

    # 打印并保存更新后的配置数据
    yml.file_dump(settings)
    return settings


def main():
    print(__file__)
    settings = update_version("settings.yaml")
    print(f"New Settings: {settings}")


if __name__ == "__main__":
    main()
