# The Author of this file is @HowardZorn on GitHub
# This file should be redistributed by Apache-2.0 License
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import base64
import json
import os
import sys

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .HFUTException import *
from .HFUTLog import log


class HFUTStudent:
    def __init__(self) -> None:
        super().__init__()
        self.session = requests.session()

    def login(self, username: str, password: str) -> None:
        # 加密方法在页面源代码中
        def encryptPassword(key, aes_str):
            aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
            padPKCS7 = pad(aes_str.encode('utf-8'), AES.block_size,
                           style='pkcs7')
            encryptAes = aes.encrypt(padPKCS7)
            encryptedText = str(base64.encodebytes(
                encryptAes), encoding='utf-8')
            encryptedTextStr = encryptedText.replace("\n", "")
            return encryptedTextStr

        self.session.get("https://cas.hfut.edu.cn/cas/login")
        self.session.get("https://cas.hfut.edu.cn/cas/vercode")
        # 实际上可以直接绕过验证码，这一步是为了获取 key
        self.session.get("https://cas.hfut.edu.cn/cas/checkInitVercode")
        key = self.session.cookies["LOGIN_FLAVORING"]
        password = encryptPassword(key, password)
        checkUserIdenty = self.session.get(
            "https://cas.hfut.edu.cn/cas/policy/checkUserIdenty",
            params={"username": username, "password": password},
        )
        if checkUserIdenty.json()["msg"] != "success":
            raise LoginError(checkUserIdenty.json()["msg"])

        # 此处 execution 为 e1s1 即可
        loginCAS = self.session.post(
            "https://cas.hfut.edu.cn/cas/login",
            data={
                "username": username,
                "capcha": "",
                "execution": "e1s1",
                "_eventId": "submit",
                "password": password,
                "geolocation": "",
                "submit": "登录",
            },
        )

        if loginCAS.status_code == 200:
            log.info("登陆成功")
        elif loginCAS.status_code == 401:
            raise LoginError("密码错误")
        else:
            raise LoginError(f"未知错误，状态码为 {loginCAS.status_code}")

    # @retry(retry=retry_if_exception_type(ConnectionError), stop=stop_after_attempt(3), wait=wait_fixed(30))
    def dailyCheckIn(self, address: str) -> bool:
        self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/casValidate.do"
        )
        self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/emappagelog/config/swmxsyqxxsjapp.do"
        )
        config_data = {"APPID": "5811260348942403",
                       "APPNAME": "swmxsyqxxsjapp"}
        self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getSelRoleConfig.do",
            data={"data": json.dumps(config_data)},
        )
        self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getMenuInfo.do",
            data={"data": json.dumps(config_data)},
        )

        # 此处可以获取当前日期
        getSettingDo = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getSetting.do",
            data={"data": "{}"},
        )
        today = getSettingDo.json()["data"]["DQRQ"]

        getStuXxDo = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getStuXx.do",
            data={"data": json.dumps({"TBSJ": today})},
        )
        if getStuXxDo.json()["code"] != "0":
            raise CheckInError(getStuXxDo.json()["msg"])

        # 获取 studentKey
        studentKeyDo = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/studentKey.do",
            data={"data": "{}"},
        )
        studentKey = studentKeyDo.json()["data"]["studentKey"]
        log.info("获取 studentKey 成功")
        log.debug(f"studentKey: {repr(studentKey)}")

        newForm = getStuXxDo.json()["data"]
        newForm.update(
            {
                "DZ_SFSB": "1",
                "GCKSRQ": "",
                "GCJSRQ": "",
                "DFHTJHBSJ": "",
                "DZ_TBDZ": address,
                "BY1": "1",
                "TBSJ": today,
                "studentKey": studentKey,
            }
        )

        # setCode 获取 paramStringKey
        setCodeDo = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/setCode.do",
            data={"data": json.dumps(newForm)},
        )
        paramStringKey = setCodeDo.json()["data"]["paramStringKey"]
        log.info("获取 paramStringKey 成功")
        log.debug(f"paramStringKey: {repr(paramStringKey)}")

        saveStuXxDo = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/saveStuXx.do",
            data={"data": json.dumps({"paramStringKey": paramStringKey})},
        )
        if saveStuXxDo.json()["code"] != "0":
            raise CheckInError(saveStuXxDo.json()["msg"])
        log.info("打卡成功")


def main():
    if os.path.exists('config.json'):
        with open('config.json', encoding="UTF-8_SIG") as f:
            cnofig = json.load(f)
    elif len(sys.argv) == 1:
        cnofig = os.environ
    else:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("username", type=str, help="Your student ID")
        arg_parser.add_argument("password", type=str,
                                help="Password for one.hfut.edu.cn")
        arg_parser.add_argument("address", type=str, help="Check in address")
        args = arg_parser.parse_args()
        cnofig = vars(args)

    student = HFUTStudent()
    student.login(cnofig["username"], cnofig["password"])
    student.dailyCheckIn(cnofig['address'])
