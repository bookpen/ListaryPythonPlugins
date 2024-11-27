import requests
import os
import ctypes
import json
import sys

if "script" in os.getcwd():
    os.chdir("..")
from script.utils.AuthV3Util import addAuthParams


def createRequest(en2cn=True):

    with open("Translation.json", "r") as f:
        data = json.load(f)
        APP_KEY = data["APP_KEY"]
        APP_SECRET = data["APP_SECRET"]
        en2cn_vocab_id = data["en2cn_vocab_id"]
        cn2en_vocab_id = data["cn2en_vocab_id"]
    q = sys.argv[1]
    if en2cn:
        vocab_id = en2cn_vocab_id
        lang_from = 'en'
        lang_to = 'zh-CHS'
    else:
        vocab_id = cn2en_vocab_id
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
