from lxml import etree

import requests

from logs import logger

from utils.get_image_code import get_verifycode_code

class WifiLogout(object):

    def __init__(self, username, password):
        if not username  or not password:
            logger.error("用户名或密码为空...")
            info = input("输入任意键退出程序...")
            raise Exception("用户名或密码为空...")
            
        self.username = str(username)
        self.password = str(password)
        try:
            self.session = requests.Session()
        except Exception as e:
            logger.error("没有连接网络,请连接网络之后在试...")
        self.crsf = self.index()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                             Chrome/106.0.0.0 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.session.trust_env = False

   

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
        logger.info("获取验证码图片...")
        try:
            image_content = self.session.get(url=verifycode_image_url, headers=headers, timeout=(6, 1)).content
        except Exception as e:
            logger.error("获取验证码失败",e)
        try:
            with open('./verify_image.png', 'wb') as f:
                f.write(image_content)
        except Exception as e:
            logger.error("验证码图片保存失败!",e)
        return csrf

    # 验证码校验
    def verify_code(self):
        verify_code = get_verifycode_code()
        if len(verify_code) == 4:
            return verify_code
        else:
            # 验证码不是四位重新加载页面
            logger.info("验证码校验错误重新加载页面...")
            self.crsf = self.index()
            verify_code = get_verifycode_code()
            return verify_code

    # 登录下线网站函数
    def login_index(self):
        url = "https://10.10.10.3:8800/"
        data = {
            'LoginForm[username]': self.username,
            'LoginForm[password]': self.password,
            'LoginForm[verifyCode]': self.verify_code(),
            '_csrf-8800': self.crsf,
            'login-button': '',
        }
        logger.info("登录中...")
        respones = self.session.post(url=url, headers=self.headers, data=data, timeout=(6, 1), verify=False)
        logger.info("登录成功")


        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['referer'] = 'https://10.10.10.3:8800/home'
        ## 执行下线操作
        logout_data = {
            '_csrf-8800': self.crsf,
        }
        logout_url = 'https://10.10.10.3:8800/home/onekey'
        logout_response = self.session.post(url=logout_url, headers=self.headers, data=logout_data, timeout=(6, 1),
                                            verify=False)
        tree = etree.HTML(logout_response.text)

        try:
            info = tree.xpath('//*[@id="w5-success-0"]/text()')
            logger.info(info)
            if info:
                logger.info("下线成功")
            else:
                logger.info("下线失败,请重新执行该程序o(╥﹏╥)o")
        except Exception as e:
            logger.error("下线失败",e)


    


