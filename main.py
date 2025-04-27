import os
import requests
import json
import yaml
import re
import time

from function_base import fnGetDirsInDir, fnGetFilesInDir, fnGetFilesInDir2, fnGetFileTime
from function_base import fnEmpty, fnLog, fnBug, fnErr


def read_json(file):
    if(os.path.exists(file) == True):
        file_byte = open(file, 'r', encoding='utf8')
        file_info = file_byte.read()
        result = json.loads(file_info)
        file_byte.close()
    else:
        result = {}
    return result
# 读取 JSON


def read_yml(file):
    if(os.path.exists(file) == True):
        file_byte = open(file, 'r', encoding='utf8')
        file_info = file_byte.read()
        result = yaml.load(file_info, Loader=yaml.FullLoader)
        file_byte.close()
    else:
        result = {}
    return result
# 读取 YML


def for_instances(host_list, route_info):
    (title, path) = (route_info["title"], route_info["path"])
    fnLog(title)
    fnLog(path)
    name = path.replace("/", "_")
    name = name.replace("+", "_")
    for host in host_list:
        url = "%s%s" % (host, path)
        if (get_xml(url, name)):
            fnLog("抓取成功")
            break
        fnLog("---")
# 遍历 RSSHub 实例


def for_routes(route_list, host_list):
    for route_info in route_list:
        for_instances(host_list, route_info)
        print("----")
# 遍历路由


def get_xml(url, name):
    xml_file = os.path.join(os.getcwd(), "xml/%s.xml" % name)
    fnLog(url)
    try:
        r = requests.get(url, timeout=10)
        fnLog(r.status_code)
        if (r.status_code != 200):
            return False
        fnLog("r.text[:10]: %s" % r.text[:10])
        if (not r.text.startswith('<?xml')):
            return False
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(r.text)
        return True
    except Exception as e:
        fnLog("err: %s" % e)
    return False
# 抓取内容并写入文件


def main():
    global _opml, _baseUrl
    _opml = opml()
    # 配置路径
    _confg_json = os.path.join(os.getcwd(), "config.json")
    _config_yml = os.path.join(os.getcwd(), "config.yml")

    # 配置读取
    _confg_data = read_json(_confg_json)
    if not any(_confg_data):
        _confg_data = read_yml(_config_yml)
    # print(_confg_data)
    _routes = _confg_data["routes"]
    _instances = _confg_data["instances"]

    if "baseUrl" in _confg_data:
        _baseUrl = _confg_data["baseUrl"]
    try:
        if(os.environ["GITHUB_REPOSITORY"]):
            fnBug(os.environ["GITHUB_REPOSITORY"])
            _baseUrl = "https://raw.githubusercontent.com/%s/main" % os.environ["GITHUB_REPOSITORY"]
    except:
        fnLog()

    print("-----")

    for_routes(_routes, _instances)
# main


main()
