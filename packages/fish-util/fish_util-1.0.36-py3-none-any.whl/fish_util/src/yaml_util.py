import ruamel.yaml


class YAMLManager:
    @staticmethod
    def read_yaml(file_path):
        yaml = ruamel.yaml.YAML()
        with open(file_path, "r") as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    @staticmethod
    def write_yaml(data, file_path):
        yaml = ruamel.yaml.YAML()
        with open(file_path, "w") as outfile:
            try:
                yaml.dump(data, outfile)
            except yaml.YAMLError as exc:
                print(exc)


def main():
    import random

    random_int = random.randint(1000, 9999)
    print(f"[run main: {__file__}]")
    config_path = "config/test_config.yaml"
    # # 写入 YAML 文件
    # data = {
    #     "name": "John Doe",
    #     "job": "Developer",
    #     "skills": ["Python", "Java", "C++"],
    # }
    # YAMLManager.write_yaml(data, config_path)
    # print(f"Write YAML file: {data}")

    # 读取 YAML 文件
    config = YAMLManager.read_yaml(config_path)
    print(f"Read YAML file: {config}")

    # 更新 YAML 文件
    config["job"] = "Manager" + str(random_int)
    config["skills"].append("JavaScript" + str(random_int))
    YAMLManager.write_yaml(config, config_path)
    print(f"Update YAML file: {config}")


if __name__ == "__main__":
    main()
