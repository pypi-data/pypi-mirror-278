from dynaconf import Dynaconf

# 初始化Dynaconf对象，指定配置文件路径
# settings = Dynaconf(settings_files=["config.yaml"])
settings = Dynaconf(settings_files=["settings.yaml"])

# 读取配置文件中的数据
version = settings.version
buildtime = settings.buildtime

# 打印读取的数据
print(f"Version: {version}")
print(f"Build Time: {buildtime}")
