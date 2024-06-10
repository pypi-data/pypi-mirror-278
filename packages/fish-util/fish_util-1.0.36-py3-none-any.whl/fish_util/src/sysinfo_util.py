import os
import platform
import psutil
import multiprocessing
import uuid
import arrow

import hashlib

def print_dict(d):
    for key, value in d.items():
        print(key + ":", value)

def get_info():
    device_id = get_device_id()
    current_millisecond_timestamp, current_datetime_str = get_system_time()
    cpu_count, system_version, total_memory, available_memory, battery_percent, total_disk, available_disk, local_ips = get_system_info()
    md5_value = generate_md5(device_id, current_millisecond_timestamp)

    info_dict = {
        "MD5": md5_value,
        "设备ID": device_id,
        "当前时间戳(微秒)": str(current_millisecond_timestamp),
        "当前时间": current_datetime_str,
        "CPU核心数": cpu_count,
        "系统版本": system_version,
        "总内存大小": total_memory,
        "剩余可用内存大小": available_memory,
        "剩余可用电量百分比": battery_percent,
        "总硬盘大小": total_disk,
        "剩余可用磁盘大小": available_disk,
        "局域网IP地址": local_ips
    }
    print_dict(info_dict)
    return info_dict

def generate_md5(device_id, timestamp):
    # 将a和timestamp拼接为一个字符串
    secret_key = "fishyer1314"  # 密钥
    combined_str = f"{secret_key}{device_id}{timestamp}"
    # 使用MD5算法计算哈希值
    md5_hash = hashlib.md5(combined_str.encode()).hexdigest()
    return md5_hash



def get_device_id():
    # 获取设备的唯一ID
    device_id = uuid.getnode()
    # 将ID转换为16进制字符串
    device_id_hex = hex(device_id).lstrip("0x")
    return device_id_hex


def bytes2human(n):
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n


def get_local_ips():
    local_ips = []
    for interface, addrs in psutil.net_if_addrs().items():
        if "bridge" not in interface:
            for addr in addrs:
                if addr.family == 2 and addr.address.startswith("192.168."):
                    local_ips.append(addr.address)
    return local_ips


def get_system_info():
    # 获取CPU核心数
    cpu_count = multiprocessing.cpu_count()

    # 获取系统版本
    system_version = platform.platform()

    # 获取总内存大小
    total_memory = psutil.virtual_memory().total
    total_memory_human = bytes2human(total_memory)

    # 获取剩余可用内存大小
    available_memory = psutil.virtual_memory().available
    available_memory_human = bytes2human(available_memory)

    # 获取剩余可用电量百分比
    battery_percent = (
        psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A"
    )

    # 获取总硬盘大小
    total_disk = psutil.disk_usage("/").total
    total_disk_human = bytes2human(total_disk)

    # 获取剩余可用磁盘大小
    available_disk = psutil.disk_usage("/").free
    available_disk_human = bytes2human(available_disk)

    # 获取局域网IP地址
    local_ips = get_local_ips()

    return (
        cpu_count,
        system_version,
        total_memory_human,
        available_memory_human,
        battery_percent,
        total_disk_human,
        available_disk_human,
        local_ips,
    )


def get_system_time():
    current_millisecond_timestamp = arrow.utcnow().timestamp()
    current_datetime_str = arrow.utcnow().to("local").format("YYYY-MM-DD HH:mm:ss")
    return current_millisecond_timestamp, current_datetime_str


# # 调用函数获取系统信息
# (
#     cpu_count,
#     system_version,
#     total_memory,
#     available_memory,
#     battery_percent,
#     total_disk,
#     available_disk,
#     local_ips,
# ) = get_system_info()

# # 调用函数获取设备ID
# device_id = get_device_id()

# # 调用函数获取系统时间
# current_millisecond_timestamp, current_datetime_str = get_system_time()

def main():
    print(__file__)
    get_info()


if __name__ == "__main__":
    main()