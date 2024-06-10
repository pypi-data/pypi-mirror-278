from loguru import logger
import os
import sys

# 创建日志目录
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 日志的格式
log_format = "[{time:YYYY-MM-DD HH:mm:ss}] {level} | {file}:{line} {function} | {message}"

# 配置logger
logger.remove()  # 移除默认的logger配置
logger.add(
    sys.stdout, 
    format=log_format, 
    level="DEBUG"
)

# 为不同的日志级别设置不同的文件
levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
for level in levels:
    log_file_path = os.path.join(log_dir, f"{level.lower()}", "{time:YYYY-MM-DD}.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logger.add(
        log_file_path, 
        format=log_format, 
        level=level,
        rotation="00:00",  # 每天零点轮转
    )

print=logger.debug

# 使用示例
if __name__ == "__main__":
    logger.debug("这是一个debug信息")
    logger.info("这是一个info信息")
    logger.warning("这是一个warning信息")
    logger.error("这是一个error信息")
    logger.critical("这是一个critical信息")