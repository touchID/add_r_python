#!/bin/bash
# 生成 Assets 模块
# 使用方法: ./generate_assets.sh <模块名称>
# 示例: ./generate_assets.sh NewFeature 或 ./generate_assets.sh new_feature

if [ -z "$1" ]; then
    echo "用法: ./generate_assets.sh <模块名称>"
    echo "示例: ./generate_assets.sh NewFeature"
    echo "或:    ./generate_assets.sh new_feature"
    exit 1
fi

MODULE_NAME="$1"

# 使用 Python 脚本生成模块，路径固定为 assets
python3 generate_module.py --type=assets "${MODULE_NAME}"

echo ""
echo "模块 ${MODULE_NAME} 已生成到 lib/module/assets/..."
