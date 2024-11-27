import requests
import os
import ctypes
import json
import sys

if "script" in os.getcwd():
    os.chdir("..")
from script.utils.AuthV3Util import addAuthParams


# 您的应用ID
APP_KEY = '3819a4014cb59b13'
# 您的应用密钥
APP_SECRET = 'Ktr1OzzzhkruinoWYnQHsYkHT7PKz18S'

def createRequest(en2cn=True):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q = sys.argv[1]
    if en2cn:
        vocab_id="A15C1D79EA6E412DACD001C33E5F9463"
        lang_from = 'en'
        lang_to = 'zh-CHS'
    else:
        vocab_id = "129E9C8D4A724CB186BDCE31969B79A7"
        lang_to = 'en'
        lang_from = 'zh-CHS'
    data = {'q': q, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    response = json.loads(str(res.content, 'utf-8'))
    original = response["query"]
    result = response["translation"][0]
    msg = ["原文："+original, "译文："+result]
    msg = "\n".join(msg)
    ctypes.windll.user32.MessageBoxW(0, msg, "Translation", 1)


def doCall(url, header, params, method):
    proxies = {"http": None, "https": None}
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header,proxies=proxies)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == '__main__':
    createRequest()
