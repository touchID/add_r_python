# python3 add_translation.py lib/translations/app_translations.dart lib/translations/ja_jp/ja_jp_translations.dart myNewKey '新し い文言'
# 已在 app_translations.dart 中插入: myNewKey
# 插入位置: 第 26 行
# 已在 ja_jp_translations.dart 中插入: Globalization.myNewKey
# 翻译内容: 新しい文言
# 插入位置: 第 14 行

#!/usr/bin/env python3
import re
import sys
# python3 add_translation.py <app_translations.dart路径> <ja_jp_translations.dart路径> <键名> <日文翻译内容> [注释]
# python3 add_translation.py --auto --service Google lib/translations/app_translations.dart lib/translations/ja_jp/ja_jp_translations.dart myNewKey '新しい文言'
def insert_app_translation_key(app_translations_path, key_name, comment=""):
    """在 app_translations.dart 中插入新的翻译键"""
    with open(app_translations_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到所有静态常量定义
    constants = []
    for i, line in enumerate(lines):
        match = re.match(r'^\s+static const String (\w+) = ', line)
        if match:
            constants.append((match.group(1), i, line))
    
    if not constants:
        print("错误：未找到任何静态常量定义")
        return False
    
    # 检查是否已存在
    for name, _, _ in constants:
        if name == key_name:
            print(f"警告: 键名 '{key_name}' 已存在于 app_translations.dart")
            return False
    
    # 找到插入位置（按字母顺序）
    insert_index = None
    for i, (name, line_num, line) in enumerate(constants):
        if key_name < name:
            insert_index = line_num
            break
    
    if insert_index is None:
        insert_index = constants[-1][1] + 1
    
    # 获取缩进
    first_const = constants[0]
    indent = re.match(r'^\s*', first_const[2]).group()
    
    # 构建新行
    if comment:
        comment_line = f"{indent}/// {comment}\n"
        lines.insert(insert_index, comment_line)
        insert_index += 1
    
    new_line = f'{indent}static const String {key_name} = "{key_name}";\n'
    lines.insert(insert_index, new_line)
    
    # 写回文件
    with open(app_translations_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"已在 app_translations.dart 中插入: {key_name}")
    print(f"插入位置: 第 {insert_index + 1} 行")
    
    return True

def insert_jp_translation(jp_translations_path, key_name, translation):
    """在 ja_jp_translations.dart 中插入日文翻译"""
    with open(jp_translations_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到 Map 内部的所有键值对
    entries = []
    for i, line in enumerate(lines):
        match = re.match(r'^\s+Globalization\.(\w+): ', line)
        if match:
            entries.append((match.group(1), i, line))
    
    if not entries:
        print("错误：未找到任何翻译条目")
        return False
    
    # 检查是否已存在
    for name, _, _ in entries:
        if name == key_name:
            print(f"警告: 键名 '{key_name}' 已存在于 ja_jp_translations.dart")
            return False
    
    # 找到插入位置（按字母顺序）
    insert_index = None
    for i, (name, line_num, line) in enumerate(entries):
        if key_name < name:
            insert_index = line_num
            break
    
    if insert_index is None:
        insert_index = entries[-1][1] + 1
    
    # 获取缩进
    first_entry = entries[0]
    indent = re.match(r'^\s*', first_entry[2]).group()
    
    # 构建新行
    new_line = f'{indent}Globalization.{key_name}: "{translation}",\n'
    lines.insert(insert_index, new_line)
    
    # 写回文件
    with open(jp_translations_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"已在 ja_jp_translations.dart 中插入: Globalization.{key_name}")
    print(f"翻译内容: {translation}")
    print(f"插入位置: 第 {insert_index + 1} 行")
    
    return True

def main():
    if len(sys.argv) < 5:
        print("用法: python add_translation.py <app_translations.dart路径> <ja_jp_translations.dart路径> <键名> <日文翻译内容> [注释]")
        print("示例: python add_translation.py lib/translations/app_translations.dart lib/translations/ja_jp/ja_jp_translations.dart myNewKey '新しい文言'")
        sys.exit(1)
    
    app_path = sys.argv[1]
    jp_path = sys.argv[2]
    key_name = sys.argv[3]
    translation = sys.argv[4]
    comment = sys.argv[5] if len(sys.argv) > 5 else ""
    
    try:
        success1 = insert_app_translation_key(app_path, key_name, comment)
        success2 = insert_jp_translation(jp_path, key_name, translation)
        
        if success1 and success2:
            print("\n操作完成！")
        else:
            sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()