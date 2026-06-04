#!/usr/bin/env python3
# python3 add_asset.py lib/generated/assets/r.dart assets/images/order/icon_order_cpu.svg

import re
import sys
import os

def generate_variable_name(asset_path):
    """从素材路径生成变量名（采用驼峰命名法）"""
    # 标准化路径，处理绝对路径和相对路径
    path = os.path.normpath(asset_path)
    
    # 尝试移除 'assets/images/' 前缀（处理相对路径）
    if path.startswith('assets/images/'):
        path = path[len('assets/images/'):]
    else:
        # 处理绝对路径：查找 'assets/images/' 在路径中的位置
        idx = path.find('assets/images/')
        if idx != -1:
            path = path[idx + len('assets/images/'):]
    
    # 将路径分隔符替换为下划线（兼容 Windows 和 Unix）
    path = path.replace(os.sep, '_')
    
    # 移除文件扩展名
    path = re.sub(r'\.\w+$', '', path)
    
    # 将连字符替换为下划线
    path = path.replace('-', '_')
    
    # 转换为小写并移除多余的下划线
    parts = path.lower().split('_')
    parts = [p for p in parts if p]
    
    # 构建驼峰命名：首字母小写，后续单词首字母大写
    if not parts:
        return ''
    
    # 第一个单词小写，后续单词首字母大写
    camel_case = parts[0] + ''.join(p.capitalize() for p in parts[1:])
    
    return camel_case

def get_relative_asset_path(asset_path):
    """获取素材的相对路径（相对于项目根目录）"""
    # 标准化路径
    path = os.path.normpath(asset_path)
    
    # 尝试提取 'assets/images/' 及其后面的部分
    if path.startswith('assets/images/'):
        return path
    else:
        idx = path.find('assets/images/')
        if idx != -1:
            return path[idx:]
    
    # 如果找不到 assets/images 前缀，返回原始路径
    return asset_path

def insert_asset(r_dart_path, asset_path):
    """将素材插入到 r.dart 文件的正确位置"""
    # 获取相对路径（用于插入到 r.dart 中）
    relative_path = get_relative_asset_path(asset_path)
    
    # 生成变量名
    var_name = generate_variable_name(asset_path)
    
    # 读取 r.dart 文件内容
    with open(r_dart_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到类内部的所有静态常量定义
    # 格式: static const String xxx = 'xxx';
    constants = []
    for i, line in enumerate(lines):
        match = re.match(r'^\s+static const String (\w+) = ', line)
        if match:
            constants.append((match.group(1), i, line))
    
    if not constants:
        print("错误：未找到任何静态常量定义")
        return False
    
    # 找到插入位置
    insert_index = None
    for i, (name, line_num, line) in enumerate(constants):
        if var_name < name:
            insert_index = line_num
            break
    
    # 如果比所有变量名都大，插入到最后一个常量之后
    if insert_index is None:
        insert_index = constants[-1][1] + 1
    
    # 构建新行（保持与其他行相同的缩进）
    first_const = constants[0]
    indent = re.match(r'^\s*', first_const[2]).group()
    new_line = f"{indent}static const String {var_name} = '{relative_path}';\n"
    
    # 插入新行
    lines.insert(insert_index, new_line)
    
    # 写回文件
    with open(r_dart_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"已成功插入素材: {var_name}")
    print(f"路径: {relative_path}")
    print(f"插入位置: 第 {insert_index + 1} 行")
    
    return True

def main():
    if len(sys.argv) != 3:
        print("用法: python add_asset.py <r.dart路径> <素材路径>")
        print("示例: python add_asset.py lib/generated/assets/r.dart assets/images/order/icon_order_cpu.svg")
        sys.exit(1)
    
    r_dart_path = sys.argv[1]
    asset_path = sys.argv[2]
    
    try:
        success = insert_asset(r_dart_path, asset_path)
        if success:
            print("\n操作完成！")
        else:
            sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()