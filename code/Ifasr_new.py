# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib

lfasr_host = 'https://raasr.xfyun.cn/v2/api'
# 请求的接口名
api_upload = '/upload'
api_get_result = '/getResult'


class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')#bytes为一种新的类型
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):
        #print("上传部分：")
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)#结果只包含文件名，不包含路径

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        #print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)#从文件读取指定的字符数（文本模式 t）或字节数（二进制模式 b），如果未给定参数 size 或 size 为负数则读取文件所有内容。

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
        #print("upload_url:",response.request.url)
        result = json.loads(response.text)
        #print("upload resp:", result)
        return result


    def get_result(self, count):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer"
        #print("")
        #print("查询部分：")
        #print("get result参数：", param_dict)
        status = 3

        result = ''
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            # print("get_result_url:",response.request.url)
            result = json.loads(response.text)
            #print(result)
            status = result['content']['orderInfo']['status']
            print("status=",status)
            if status == 4:
                break
            time.sleep(15)
        #print("get_result resp:",result)

        data = str(result)
        final_result = ""
        if len(data.split("lattice2")) >= 2:
            data = str(data.split("lattice2")[1])
            data = data.replace("\\", "")
        # data = data.replace('"', "'")
        # data = eval(data)
        # print(data)
        #print(type(data))
            data = list(data)
            # print(data)

            for i in range(len(data) - 2):
                if data[i] == '"' and data[i + 1] == 'w' and data[i + 2] == '"':
                    for j in range(i + 5, len(data)):
                        if data[j] != '"':
                            final_result = final_result + data[j]
                        else:
                            break
            print(final_result)

        with open("D:/django-try/emd/xitong/save_txt/" + str(count) + ".txt", 'w', encoding="utf-8") as f:
            f.write(final_result)
        return final_result




# 输入讯飞开放平台的appid，secret_key和待转写的文件路径
if __name__ == '__main__':
    api = RequestApi(appid="0da4904a",
                     secret_key="5d934a0240f2f43189f2ec844cfd3008",
                     upload_file_path="D:/django-try/emd/xitong/audio/lfasr_涉政.wav")

    api.get_result(1)
