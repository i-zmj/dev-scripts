#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, requests

def subprocess_run(cmd, print_console=False, red_color_list=[], yellow_color_list=[], green_color_list=[]):

    # import locale
    # local_encoding = locale.getpreferredencoding()

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    result = ''
    while True:
        output = process.stdout.readline().decode("utf-8", errors="replace").strip()
        if output == '' and process.poll() is not None:
            break
        
        output = output.strip()
        for color in red_color_list:
            if color in output:
                output = f'\033[31m{output}\033[0m'
        for color in yellow_color_list:
            if color in output:
                output = f'\033[33m{output}\033[0m'
        for color in green_color_list:
            if color in output:
                output = f'\033[32m{output}\033[0m'

        if output == '':
            continue

        if print_console:
            print(output)

        result += output + '\n'
        
    return result

def fetch_index_html(url):

    # Download navicore_url
    r = requests.get(url)
    pre_content = r.content.decode('utf-8', errors='ignore').split('<pre>')[1].split('</pre>')[0]
    lines = pre_content.splitlines()

    result = []
    for line in lines:
        file = line.split('href="')[1].split('">')[0]
        infos = line.split('>')[2].split(' ')

        # 移除infos中的空值
        date = ''
        time = ''
        size = ''

        while '' in infos:
            infos.remove('')
        if len(infos) >= 1:
            date = infos[0]
        if len(infos) >= 2:
            time = infos[1]
        if len(infos) >= 3:
            size = infos[2]

        # 将字符串size转换成整数
        size_str = ''
        try:
            size = int(size)
        except Exception as e:
            size = 0
            continue

        if size > 1024 * 1024:
            size_str = "%.3f" % (size / 1024 / 1024)
            size_str += 'MB'
        elif size > 1024:
            size_str = "%.3f" % (size / 1024)
            size_str += 'KB'
        else:
            size_str = str(size) + 'B'

        item = {
            'file': file,
            'date': date,
            'time': time,
            'size': size_str
        }
        result.append(item)

    return result