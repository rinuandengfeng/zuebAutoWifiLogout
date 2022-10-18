# -*- coding:utf-8 -*-

import time

import requests

import utils


class WifiLogout(object):

    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)
        self.session = requests.Session()
        token, verify_image_suffix = self.index()
        self.token = token
        self.verify_image_suffix = verify_image_suffix
        self.headers = dict()
        self.filename = 'verify_code_image.png'
        self.session.trust_env = False

    # 字符处理
    def get_token(self, raw, value, index_front=0, index_back=10):
        token_index = raw.text.find(str(value))
        result = raw.text[token_index + int(index_front):token_index + int(index_back)]
        return result

    # 进入首页
    def index(self):
        url = 'https://10.10.10.3:8800'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                     Chrome/106.0.0.0 Safari/537.36",
        }
        responses = self.session.get(url=url, headers=headers, timeout=(6, 1), verify=False)

        # 获取csrf-8800
        token_value = '"_csrf-8800" value='
        token = self.get_token(responses, token_value, index_front=20, index_back=76)
        verify_value = '"loginform-verifycode-image" src='
        verify_image_suffix = self.get_token(responses, verify_value, index_front=50, index_back=63)
        return token, verify_image_suffix

    # 获取图片验证码的值
    def get_verify_image_code(self):
        url = 'https://10.10.10.3:8800/site/captcha'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                     Chrome/106.0.0.0 Safari/537.36",
        }
        params = {
            "v": self.verify_image_suffix
        }
        respones = self.session.get(url, params=params, headers=headers, timeout=(6, 1), verify=False)
        try:
            with open(self.filename, 'wb') as f:
                f.write(respones.content)
        except:
            print("获取验证码失败！！")
        # exit()
        verify_code = utils.get_image_code(filename=self.filename)
        return verify_code

    # 验证码校验
    def verify_code(self):
        verify_code = self.get_verify_image_code()
        if len(verify_code) == 4:
            return verify_code
        else:
            # 验证码不是四位重新加载页面
            print('验证码识别失败')
            token, verify_image_suffix = self.index()
            self.token = token
            self.verify_image_suffix = verify_image_suffix
            verify_code = self.get_verify_image_code()
            return verify_code

    # 登录函数
    def login_index(self):
        url = "https://10.10.10.3:8800/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Content-lenght': '185',
        }

        data = {
            '_csrf-8800': self.token,
            'LoginForm[username]': self.username,
            'LoginForm[password]': self.password,
            'LoginForm[verifyCode]': self.verify_code(),
            'login-button': '',
        }
        print('登录下线网页……')
        time.sleep(5)
        respones = self.session.post(url=url, headers=headers, data=data, timeout=(6, 1), verify=False)
        text = respones.content
        print('登录下线网页成功……')
        time.sleep(5)
    # 下线
    def logout(self):
        # 调用登录函数
        self.login_index()
        url = 'https://10.10.10.3:8800/home/onekey'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            "referer": 'https://10.10.10.3:8800/home',
            'Connection': 'keep-alive',
        }
        data = {
            '_csrf-8800': self.token,
        }
        print('正在进行也连接用户下线……')
        response = self.session.post(url=url, headers=headers, data=data, timeout=(6, 1), verify=False)
        text = response.text
        print('下线成功~~~,10秒后自动关闭')
        time.sleep(10)

