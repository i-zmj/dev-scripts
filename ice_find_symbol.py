#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys

lib_dir = ''
symbol = ''
if len(sys.argv) != 3:
    lib_dir = input('请输出待搜索的静态库所在目录: ')
    symbol = input('请输出待搜索的关键字: ')
else:
    lib_dir = sys.argv[1]
    symbol = sys.argv[2]

print(f'在[{lib_dir}]文件夹中，递归搜[{symbol}]...')

if not os.path.exists(lib_dir):
    print(f'待搜索目录[{lib_dir}]不存在!')

import ice_util as util

result = set()
file_count = 0

import platform, shutil

def find_symbol(lib_dir, symbol):
    global file_count
    terminal_width = shutil.get_terminal_size().columns
    for root, dirs, files in os.walk(lib_dir):
        for file in files:
            if file.endswith(".a") or file.endswith(".lib"):
                status = f"Analysis {file}..."
                print(f"\r{status:<{terminal_width}}", end="", flush=True)
                file_count += 1
                
                cmd = ''
                if platform.system() == "Windows":
                    # 如果是Windows平台，使用内置的nm.exe
                    cmd = f'.\\tools\\nm.exe -C "{os.path.join(root, file)}" | findstr -i "{symbol}"'
                else:
                    # 如果是非Windows平台，是用系统的nm命令
                    cmd = f"nm -C {os.path.join(root, file)} | grep {symbol}"

                ret = util.subprocess_run(cmd, red_color_list=['U '], green_color_list=[' T ', ' t '])

                for line in ret.splitlines():
                    # 利用set，进行去重处理
                    result.add(f"{file} >> {line.strip()}")

find_symbol(lib_dir, symbol)

print(f"总计搜索[{file_count}]个文件。发现了[{len(result)}]个结果！")

from prettytable import PrettyTable
tb = PrettyTable()
tb.field_names = ['静态库文件名', '结果']
tb.align['静态库文件名'] = "l"
tb.align['结果'] = "l"


for line in result:
    tb.add_row(line.split(' >> '))

print(f'\n{tb}')
os.system('pause')
