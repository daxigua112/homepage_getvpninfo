import requests
import json
import os
import time

# 机场信息输出目录
OUTPUT_DIR = ""
CONFIG_FILE = "config.json"  # 配置文件路径

def load_subscribe_list():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"配置文件 {CONFIG_FILE} 不存在")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def parse_userinfo_header(header_value):
    result = {}
    try:
        parts = header_value.split(';')
        for part in parts:
            key_value = part.strip().split('=')
            if len(key_value) == 2:
                k, v = key_value
                result[k] = int(v)
    except Exception:
        pass
    return result

def format_gb(byte_value):
    return f"{byte_value / 1073741824:.2f} GB"

def main():
    try:
        subscribe_list = load_subscribe_list()
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return

    for name, url in subscribe_list.items():
        try:
            print(f"获取 {name}...")
            response = requests.get(url, verify=False)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            userinfo = response.headers.get("Subscription-Userinfo")
            result = {}
            if userinfo:
                info = parse_userinfo_header(userinfo)
                if "upload" in info:
                    result["upload"] = format_gb(info["upload"])
                if "download" in info:
                    result["download"] = format_gb(info["download"])
                if "upload" in info and "download" in info:
                    used = info["upload"] + info["download"]
                    result["used"] = format_gb(used)
                if "total" in info:
                    result["total"] = format_gb(info["total"])
                if "expire" in info:
                    result["expire_ts"] = time.strftime("%Y-%m-%d", time.localtime(info["expire"]))

            output_path = os.path.join(OUTPUT_DIR, f"{name}.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(result, f)
            print(f"已写入 {name}.json")

        except Exception as e:
            print(f"获取 {name} 失败: {e}")

if __name__ == "__main__":
    main()
