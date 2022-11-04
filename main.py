import time

import ddddocr
from lxml import etree

import requests


class WifiLogout(object):

    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)
        self.session = requests.Session()
        self.crsf = self.index()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                             Chrome/106.0.0.0 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.filename = 'verify_code_image.png'
        self.session.trust_env = False

    # 验证码识别函数
    def get_image_code(self):
        print('进入获取验证码函数')
        time.sleep(2)
        ocr = ddddocr.DdddOcr()
        try:
            with open(self.filename, 'rb') as f:
                img_bytes = f.read()
        except:
            print('打开文件失败')
        verify_code = ocr.classification(img_bytes)
        print('验证码为：', verify_code)
        time.sleep(2)
        return verify_code

    # 进入首页
    def index(self):

        url = 'https://10.10.10.3:8800'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                                     Chrome/106.0.0.0 Safari/537.36",
        }

        responses = self.session.get(url=url, headers=headers, timeout=(6, 1), verify=False)

        # 获取csrf-8800的value值
        tree = etree.HTML(responses.text)
        csrf = tree.xpath('//input [@name="_csrf-8800"]/@value')[0]
        # 获取图片的地址
        image_suffix = tree.xpath('//img [@id="loginform-verifycode-image"]/@src')[0]
        verifycode_image_url = 'https://10.10.10.3:8800' + str(image_suffix)

        # 获取验证码图片
        print("正在获取验证码图片")
        image_content = self.session.get(url=verifycode_image_url, headers=headers, timeout=(6, 1)).content
        try:
            with open('./verify_code_image.png', 'wb') as f:
                f.write(image_content)
        except Exception as e:
            print("错误信息为:", e)
        return csrf

    # 验证码校验
    def verify_code(self):
        verify_code = self.get_image_code()
        if len(verify_code) == 4:
            return verify_code
        else:
            # 验证码不是四位重新加载页面
            print('验证码识别失败,重新获取验证码o(╥﹏╥)o')
            self.crsf = self.index()
            verify_code = self.get_image_code()
            return verify_code

    # 登录函数
    def login_index(self):
        url = "https://10.10.10.3:8800/"

        data = {
            'LoginForm[username]': self.username,
            'LoginForm[password]': self.password,
            'LoginForm[verifyCode]': self.verify_code(),
            '_csrf-8800': self.crsf,
            'login-button': '',
        }
        print('登录下线网页……')
        time.sleep(2)
        respones = self.session.post(url=url, headers=self.headers, data=data, timeout=(6, 1), verify=False)
        text = respones.content
        print('登录下线网页成功……')
        time.sleep(2)

    # 下线
    def logout(self):
        # 调用登录函数
        self.login_index()
        url = 'https://10.10.10.3:8800/home/onekey'

        data = {
            '_csrf-8800': self.crsf,
        }
        print('正在进行连接用户下线……')
        response = self.session.post(url=url, headers=self.headers, data=data, timeout=(6, 1), verify=False)
        text = response.text
        print('下线成功~~~,5秒后自动关闭')
        time.sleep(5)
