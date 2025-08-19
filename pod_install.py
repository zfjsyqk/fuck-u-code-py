# -*- coding: utf-8 -*-
# @Author: zhangfujie
# @Date:   2025-03-15 00:08:29
# @Last Modified by:   zhangfujie
# @Last Modified time: 2025-03-15 10:24:03
import subprocess
import time

POD_DIRECTORY = "/Users/zhangfujie/Desktop/xt_work/flutter_xt_projects/xt_ios/XT"

def run_pod_install():
    while True:
        try:
            print("🚀 正在执行 `pod install`...\n")

            # 运行 `pod install` 并实时打印输出
            process = subprocess.Popen(
                ["pod", "install"],
                cwd=POD_DIRECTORY,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # 逐行读取输出并打印
            for line in iter(process.stdout.readline, ""):
                print(line, end="")

            # 等待进程完成
            process.wait()

            # 如果 `pod install` 失败，检查 `returncode`
            if process.returncode != 0:
                raise Exception(f"❌ `pod install` 失败，错误代码: {process.returncode}")

            print("\n✅ `pod install` 成功！")
            break  # 退出循环
        except Exception as e:
            print(f"⚠️ 发生错误: {e}")
            print("⏳ 5 秒后重试...")
            time.sleep(60)  # 等待60秒后重试

if __name__ == "__main__":
    run_pod_install()

