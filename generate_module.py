#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据模板生成新的 Flutter 模块文件

用法:
    python generate_module.py --type=<类型> <模块名称>
    类型: my_page, order, assets, feed
    示例: python generate_module.py --type=my_page NewFeature
    示例: python generate_module.py --type=my_page new_feature

生成的文件:
    - lib/module/<module_path>/<module_name>_binding.dart
    - lib/module/<module_path>/<module_name>_page.dart
    - lib/module/<module_path>/<module_name>_state.dart
    - lib/module/<module_path>/<module_name>_view_mode.dart
    - lib/data/provider/service/<module_name>_service.dart
    - lib/data/provider/use_case/<module_name>_api_use_case.dart
"""

import os
import sys
import re
import argparse

def is_camel_case(s):
    """判断是否为驼峰命名（首字母大写）"""
    return len(s) > 0 and s[0].isupper() and '_' not in s

def is_snake_case(s):
    """判断是否为蛇形命名（全小写，下划线分隔）"""
    return len(s) > 0 and s == s.lower() and '_' in s

def to_pascal_case(snake_str):
    """将蛇形命名转换为帕斯卡命名（首字母大写）"""
    components = snake_str.replace('-', '_').split('_')
    return ''.join(x.capitalize() for x in components)

def to_snake_case(pascal_str):
    """将帕斯卡命名转换为蛇形命名（全小写，下划线分隔）"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', pascal_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def create_directory(path):
    """创建目录（如果不存在）"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"创建目录: {path}")

def create_file(filepath, content):
    """创建文件（使用 CRLF 换行符）"""
    dir_path = os.path.dirname(filepath)
    if dir_path:
        create_directory(dir_path)
    
    # 将 LF 替换为 CRLF
    content = content.replace('\n', '\r\n')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"创建文件: {filepath}")

def generate_binding(module_name_pascal, module_name_snake, module_path):
    """生成 binding 文件"""
    content = f'''import 'package:get/get.dart';
import 'package:shisankeisei/data/provider/service/{module_name_snake}_service.dart';
import 'package:shisankeisei/module/{module_path}/{module_name_snake}/{module_name_snake}_view_mode.dart';

/// [author] user
///
/// [describe] {module_name_pascal}:画面
///
/// [date] 2025/07/11
class {module_name_pascal}Binding extends Bindings {{
  @override
  void dependencies() {{
    Get.lazyPut(() => {module_name_pascal}ViewMode());
    Get.lazyPut(() => {module_name_pascal}Service());
  }}
}}
'''
    filepath = f'lib/module/{module_path}/{module_name_snake}/{module_name_snake}_binding.dart'
    create_file(filepath, content)

def generate_page(module_name_pascal, module_name_snake, module_path):
    """生成 page 文件"""
    content = f'''import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:shisankeisei/base/mvvm/view/base_stateful_page.dart';
import 'package:shisankeisei/theme/app_styles.dart';
import 'package:shisankeisei/theme/app_text_theme.dart';
import 'package:shisankeisei/theme/color/theme_colors.dart';
import 'package:shisankeisei/translations/app_translations.dart';

import '{module_name_snake}_view_mode.dart';

/// [author] user
///
/// [describe] {module_name_pascal}
///
/// [date] 2025/07/11
class {module_name_pascal}Page extends BaseStatefulPage {{
  const {module_name_pascal}Page({{super.key}});

  @override
  BaseState createState() {{
    return {module_name_pascal}State();
  }}
}}

class {module_name_pascal}State extends BaseState<{module_name_pascal}ViewMode, {module_name_pascal}Page> {{
  @override
  bool get canPop => false;

  @override
  String titleString() {{
    return 'Globalization.{module_name_snake}.tr'.tr;
  }}

  @override
  bool isCenterTitle() => true;

  @override
  Widget buildContent(BuildContext context) {{
    return LayoutBuilder(builder: (context, BoxConstraints constraints) {{
      return _createContent(context, constraints);
    }});
  }}

  Widget _createContent(BuildContext context, BoxConstraints constraints) {{
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: const Center(
        child: Text('{module_name_pascal}'),
      ),
    );
  }}
}}
'''
    filepath = f'lib/module/{module_path}/{module_name_snake}/{module_name_snake}_page.dart'
    create_file(filepath, content)

def generate_state(module_name_pascal, module_name_snake, module_path):
    """生成 state 文件"""
    content = f'''import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:get/get_rx/src/rx_types/rx_types.dart';
import 'package:shisankeisei/base/mvvm/view_mode/base_action.dart';
import 'package:shisankeisei/base/net/base_api_use_case.dart';
import 'package:shisankeisei/data/provider/use_case/{module_name_snake}_api_use_case.dart';

part '{module_name_snake}_state.freezed.dart';

/// [author] user
///
/// [describe] {module_name_pascal}:画面
///
/// [date] 2025/07/11
class {module_name_pascal}State {{
  late final Rx<ResponseEntity> rx{module_name_pascal};

  {module_name_pascal}State() {{
    rx{module_name_pascal} = ResponseEntity().obs;
  }}
}}

@Freezed(copyWith: false, when: FreezedWhenOptions.none, map: FreezedMapOptions.none)
sealed class {module_name_pascal}Actions extends BaseAction {{
  const factory {module_name_pascal}Actions.fetch{module_name_pascal}({{{module_name_pascal}Request? request}}) = Fetch{module_name_pascal};
}}
'''
    filepath = f'lib/module/{module_path}/{module_name_snake}/{module_name_snake}_state.dart'
    create_file(filepath, content)

def generate_view_mode(module_name_pascal, module_name_snake, module_path):
    """生成 view_mode 文件"""
    content = f'''import 'package:get/get.dart';
import 'package:shisankeisei/base/mvvm/view_mode/multi_net_data.dart';
import 'package:shisankeisei/base/mvvm/view_mode/session_change_mixin.dart';
import 'package:shisankeisei/base/mvvm/view_mode/view_mode.dart';
import 'package:shisankeisei/base/net/base_api_use_case.dart';
import 'package:shisankeisei/data/provider/service/{module_name_snake}_service.dart';
import 'package:shisankeisei/data/provider/use_case/{module_name_snake}_api_use_case.dart';
import 'package:shisankeisei/module/my_page/my_page_base/myPageSessionChangeMixin.dart';
import 'package:shisankeisei/utils/master_code_util.dart';

import '{module_name_snake}_state.dart';

/// [author] user
///
/// [describe] {module_name_pascal}:画面
///
/// [date] 2025/07/11
class {module_name_pascal}ViewMode extends ViewMode<{module_name_pascal}Actions, {module_name_pascal}Service> {{
  final {module_name_pascal}State {module_name_snake}State = {module_name_pascal}State();

  @override
  void onInit() {{
    super.onInit();
  }}

  @override
  dispatch({module_name_pascal}Actions action) {{
    return switch (action) {{
      Fetch{module_name_pascal} {module_name_snake} => request(api.get{module_name_pascal}({module_name_snake}.request), action: action, handleLoading: true),
    }};
  }}

  @override
  void onValue(MultiNetData netData, {module_name_pascal}Actions action) {{
    switch (action) {{
      case Fetch{module_name_pascal}(request: final {module_name_snake}Request):
        if ((netData[0] as ResponseEntity).result == APIResult.success) {{
          {module_name_snake}Request?.callback?.call();
        }}
        break;
    }}
  }}
}}
'''
    filepath = f'lib/module/{module_path}/{module_name_snake}/{module_name_snake}_view_mode.dart'
    create_file(filepath, content)

def generate_service(module_name_pascal, module_name_snake):
    """生成 service 文件"""
    content = f'''import 'package:shisankeisei/base/net/base_api_use_case.dart';
import 'package:shisankeisei/base/service/base_service.dart';
import 'package:shisankeisei/data/provider/use_case/{module_name_snake}_api_use_case.dart';

/// [author] user
///
/// [describe] {module_name_pascal}:画面
///
/// [date] 2025/07/11
class {module_name_pascal}Service extends BaseService {{
  Future<ResponseEntity<ResponseEntity>> get{module_name_pascal}({module_name_pascal}Request? request) {{
    return getNewDataFromNet({module_name_pascal}ApiUseCase(), request, method: HttpMethod.post);
  }}
}}
'''
    filepath = f'lib/data/provider/service/{module_name_snake}_service.dart'
    create_file(filepath, content)

def generate_api_use_case(module_name_pascal, module_name_snake):
    """生成 api_use_case 文件"""
    content = f'''import 'package:shisankeisei/base/net/base_api_use_case.dart';

/// [author] user
///
/// [describe] {module_name_pascal}:画面
///
/// [date] 2025/07/11
class {module_name_pascal}ApiUseCase extends BaseAPIUseCase<ResponseEntity, {module_name_pascal}Request> {{
  @override
  String getPath({module_name_pascal}Request? request) {{
    return "/v1/{module_name_snake.replace('_', '-')}";
  }}
}}

/// [describe] {module_name_pascal}:リクエストパラメータ
///
/// [date] 2025/07/11
class {module_name_pascal}Request implements IRequest {{
  {module_name_pascal}Request({{
    this.callback,
  }});

  // コールバック
  final Function? callback;

  @override
  Map<String, dynamic>? getParameters() {{
    return {{}};
  }}
}}
'''
    filepath = f'lib/data/provider/use_case/{module_name_snake}_api_use_case.dart'
    create_file(filepath, content)

def main():
    parser = argparse.ArgumentParser(description='生成 Flutter 模块')
    parser.add_argument('--type', required=True, choices=['my_page', 'order', 'assets', 'feed'],
                        help='模块类型: my_page, order, assets, feed')
    parser.add_argument('module_name', help='模块名称（支持驼峰或蛇形命名）')
    args = parser.parse_args()

    module_type = args.type
    input_name = args.module_name
    
    # 根据输入判断命名风格
    if is_camel_case(input_name):
        # 驼峰命名 -> 帕斯卡命名
        module_name_pascal = input_name
        module_name_snake = to_snake_case(input_name)
        print(f"检测到驼峰命名格式")
    elif is_snake_case(input_name):
        # 蛇形命名
        module_name_snake = input_name
        module_name_pascal = to_pascal_case(input_name)
        print(f"检测到蛇形命名格式")
    else:
        # 单单词或其他格式，默认转为帕斯卡命名
        module_name_pascal = input_name.capitalize()
        module_name_snake = input_name.lower()
        print(f"检测到单单词格式")
    
    # 根据类型确定模块路径
    if module_type == 'my_page':
        module_path = f'my_page'
        full_module_name_pascal = f'MyPage{module_name_pascal}'
        full_module_name_snake = f'my_page_{module_name_snake}'
    elif module_type == 'order':
        module_path = f'order/invest_order'
        full_module_name_pascal = f'InvestOrder{module_name_pascal}'
        full_module_name_snake = f'invest_order_{module_name_snake}'
    elif module_type == 'assets':
        module_path = f'assets'
        full_module_name_pascal = f'Assets{module_name_pascal}'
        full_module_name_snake = f'assets_{module_name_snake}'
    elif module_type == 'feed':
        module_path = f'feed'
        full_module_name_pascal = f'Feed{module_name_pascal}'
        full_module_name_snake = f'feed_{module_name_snake}'
    else:
        print(f"未知模块类型: {module_type}")
        sys.exit(1)
    
    print(f"\\n=== 生成模块 ===")
    print(f"类型: {module_type}")
    print(f"模块名称(帕斯卡): {full_module_name_pascal}")
    print(f"模块名称(蛇形): {full_module_name_snake}")
    print(f"模块路径: {module_path}")
    
    # 创建模块目录
    module_dir = f'lib/module/{module_path}/{full_module_name_snake}'
    create_directory(module_dir)
    
    # 生成文件
    print("\\n生成文件:")
    
    # 使用完整的模块名称生成文件
    generate_binding(full_module_name_pascal, full_module_name_snake, module_path)
    generate_page(full_module_name_pascal, full_module_name_snake, module_path)
    generate_state(full_module_name_pascal, full_module_name_snake, module_path)
    generate_view_mode(full_module_name_pascal, full_module_name_snake, module_path)
    generate_service(full_module_name_pascal, full_module_name_snake)
    generate_api_use_case(full_module_name_pascal, full_module_name_snake)
    
    print(f"\\n=== 模块生成完成! ===")
    print(f"生成的文件:")
    print(f"  lib/module/{module_path}/{full_module_name_snake}/")
    print(f"    - {full_module_name_snake}_binding.dart")
    print(f"    - {full_module_name_snake}_page.dart")
    print(f"    - {full_module_name_snake}_state.dart")
    print(f"    - {full_module_name_snake}_view_mode.dart")
    print(f"  lib/data/provider/service/{full_module_name_snake}_service.dart")
    print(f"  lib/data/provider/use_case/{full_module_name_snake}_api_use_case.dart")
    print(f"\\n注意: 需要运行 flutter pub run build_runner build 生成 freezed 文件")

if __name__ == '__main__':
    main()
