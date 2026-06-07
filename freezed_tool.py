#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import yaml
import subprocess

def main():
    print("🔍 扫描 freezed 文件中...")

    # 找到所有需要忽略的源文件
    files = []
    for f in glob.glob("lib/**/*.dart", recursive=True):
        if ".freezed.dart" in f:
            continue
        if os.path.exists(f.replace(".dart", ".freezed.dart")):
            files.append(f.replace("\\", "/"))

    files = sorted(list(set(files)))
    print(f"✅ 找到 {len(files)} 个文件，即将忽略")

    # 生成 build.yaml
    config = {
        "targets": {
            "$default": {
                "sources": {
                    "exclude": files
                }
            }
        }
    }

    with open("build.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print("✅ build.yaml 生成成功")
    print("🚀 开始构建...\n")

    # 执行构建
    try:
        subprocess.run([
            "flutter", "pub", "run", "build_runner", "build",
            "--delete-conflicting-outputs"
        ], check=True)
    finally:
        # ✅ 构建完自动删除 build.yaml
        if os.path.exists("build.yaml"):
            os.remove("build.yaml")
            print("\n🗑️ 已自动删除 build.yaml")

    print("\n🎉 全部完成！")

if __name__ == '__main__':
    main()