# The Author of this file is @HowardZorn on GitHub
# The Maintainer of this file is @xqm32 on GitHub since 2021
# This file should be redistributed by Apache-2.0 License
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import json
import os
import re
import sys

import requests

from .HFUTEncrypt import encryptPassword
from .HFUTException import *
from .HFUTLog import log


def willLogin(what):
    def warpperA(func):
        def warpperB(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            self.logged.add(what)
            return res
        return warpperB
    return warpperA


def loginRequired(what):
    def warpperA(func):
        def warpperB(self, *args, **kwargs):
            if what in self.logged:
                return func(self, *args, **kwargs)
            else:
                raise LoginError(f"尚未登录 {what}")
        return warpperB
    return warpperA


class HFUTStudent:
    def __init__(self) -> None:
        super().__init__()
        self.session: requests.Session = None
        self.logged = set()

    @willLogin('CAS')
    def loginCAS(self, username: str, password: str) -> requests.Session:
        self.session = requests.session()
        self.session.get('https://cas.hfut.edu.cn/cas/login')
        self.session.get('https://cas.hfut.edu.cn/cas/vercode')
        # 实际上可以直接绕过验证码，这一步是为了获取 key
        self.session.get('https://cas.hfut.edu.cn/cas/checkInitVercode')
        key = self.session.cookies['LOGIN_FLAVORING']
        password = encryptPassword(key, password)
        checkUserIdenty = self.session.get(
            'https://cas.hfut.edu.cn/cas/policy/checkUserIdenty',
            params={'username': username, 'password': password},
        )
        if checkUserIdenty.json()['msg'] != 'success':
            raise LoginError(checkUserIdenty.json()['msg'])
        # 此处 execution 为 e1s1 即可
        loginCAS = self.session.post(
            'https://cas.hfut.edu.cn/cas/login',
            data={
                'username': username,
                'capcha': '',
                'execution': 'e1s1',
                '_eventId': 'submit',
                'password': password,
                'geolocation': '',
                'submit': '登录',
            },
        )

        if loginCAS.status_code == 200:
            log.info('CAS 登陆成功')
        elif loginCAS.status_code == 401:
            raise LoginError('密码错误')
        else:
            raise LoginError(f'未知错误，状态码为 {loginCAS.status_code}')
        return self.session

    @willLogin('One')
    def loginOne(self, username: str, password: str) -> requests.Session:
        self.loginCAS(username, password)

        # 通过授权获取 code
        authParams = {
            'response_type': 'code',
            'client_id': 'BsHfutEduPortal',
            'redirect_uri': 'https://one.hfut.edu.cn/home/index',
        }
        authorize = self.session.get(
            'https://cas.hfut.edu.cn/cas/oauth2.0/authorize',
            params=authParams,
        )
        # 需要两次授权
        authorize = self.session.get(
            'https://cas.hfut.edu.cn/cas/oauth2.0/authorize',
            params=authParams,
        )
        # 如果出现问题，去注释如下行
        # while not authorize.history:
        #     authorize = self.session.get(
        #         'https://cas.hfut.edu.cn/cas/oauth2.0/authorize',
        #         params=authParams,
        #     )
        code = re.findall(
            'code=(.*)', authorize.history[0].headers['Location'])[0]
        log.debug(f'code: {code}')
        log.info('获取 code 成功')

        # 获取 Token
        getTokenParams = {
            'type': 'portal',
            'redirect': f'https://one.hfut.edu.cn/home/index?code={code}',
            'code': code
        }
        getToken = self.session.get(
            'https://one.hfut.edu.cn/api/auth/oauth/getToken',
            params=getTokenParams,
        )
        token = getToken.json()['data']['access_token']
        log.debug(f'token: {token}')
        log.info('获取 token 成功')

        # 更新 Token
        self.session.get(
            'https://one.hfut.edu.cn/cas/bosssoft/checkToken',
            params={'token': token}
        )
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        log.info('One 登录成功')
        self.logged.add('One')
        return self.session

    @loginRequired('CAS')
    def dailyCheckIn(self, address: str) -> None:
        self.session.get(
            'http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/casValidate.do',
            timeout=60,
        )
        self.session.get(
            'http://stu.hfut.edu.cn/xsfw/sys/emappagelog/config/swmxsyqxxsjapp.do'
        )
        config_data = {'APPID': '5811260348942403',
                       'APPNAME': 'swmxsyqxxsjapp'}
        self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getSelRoleConfig.do',
            data={'data': json.dumps(config_data)},
        )
        self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getMenuInfo.do',
            data={'data': json.dumps(config_data)},
        )

        # 此处可以获取当前日期
        getSettingDo = self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getSetting.do',
            data={'data': '{}'},
        )
        today = getSettingDo.json()['data']['DQRQ']
        log.info(f'当前日期为 {today}')

        # 判断今日是否有数据
        judgeTodayHasDataDo = self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/judgeTodayHasData.do',
            data={'data': json.dumps({'TBSJ': today})},
        )
        log.debug(judgeTodayHasDataDo.json())
        if judgeTodayHasDataDo.json()['data'] != []:
            log.info('今日已打卡')
            return
        log.info('今日尚未打卡')

        getStuXxDo = self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getStuXx.do',
            data={'data': json.dumps({'TBSJ': today})},
        )
        if getStuXxDo.json()['code'] != '0':
            raise CheckInError(getStuXxDo.json()['msg'])
        log.info(f'获取前一次打卡信息成功')

        # 获取 studentKey
        studentKeyDo = self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/studentKey.do',
            data={'data': '{}'},
        )
        studentKey = studentKeyDo.json()['data']['studentKey']
        log.info('获取 studentKey 成功')
        log.debug(f'studentKey: {repr(studentKey)}')

        newForm = getStuXxDo.json()['data']
        newForm.update(
            {
                'DZ_SFSB': '1',
                'GCKSRQ': '',
                'GCJSRQ': '',
                'DFHTJHBSJ': '',
                'DZ_TBDZ': address,
                'BY1': '1',
                'TBSJ': today,
                'studentKey': studentKey,
            }
        )

        # setCode 获取 paramStringKey
        setCodeDo = self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/setCode.do',
            data={'data': json.dumps(newForm)},
        )
        paramStringKey = setCodeDo.json()['data']['paramStringKey']
        log.info('获取 paramStringKey 成功')
        log.debug(f'paramStringKey: {repr(paramStringKey)}')

        saveStuXxDo = self.session.post(
            'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/saveStuXx.do',
            data={'data': json.dumps({'paramStringKey': paramStringKey})},
        )
        if saveStuXxDo.json()['code'] != '0':
            raise CheckInError(saveStuXxDo.json()['msg'])
        log.info('打卡成功')


def main():
    if os.path.exists('config.json'):
        with open('config.json', encoding='UTF-8_SIG') as f:
            config = json.load(f)
        log.info(f'检测到 {config["username"]} 的配置')
    elif len(sys.argv) == 1:
        config = os.environ
    else:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('username', type=str, help='Your student ID')
        arg_parser.add_argument('password', type=str,
                                help='Password for one.hfut.edu.cn')
        arg_parser.add_argument('address', type=str, help='Check in address')
        args = arg_parser.parse_args()
        config = vars(args)

    student = HFUTStudent()
    student.loginCAS(config['username'], config['password'])
    student.dailyCheckIn(config['address'])
