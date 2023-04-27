
from logs import logger

def get_response(url,headers,session):
    """
    :param url: 请求的url
    :param headers: 请求头
    :return: 返回响应
    get请求获取响应
    """
    if  url and headers:
        try:
            response = session.get(url=url,headers=headers, timeout=(6, 1), verify=False)
        except Exception as e:
            logger.error("请求失败",e)
            waiting_exit = input("按任意键退出程序...")
            exit()
    else:
        raise Exception("url或headers参数错误")
    return response


def post_requests(url,headers,session,data):
    """
    :param url: 请求的url
    :param headers: 请求头
    :return: 返回响应
    post请求获取响应
    """
    
    
    if url and headers:
        try:
            response = session.post(url=url,headers=headers, data = data,timeout=(6, 1), verify=False,)
        except Exception as e:
            logger.error("请求失败",e)
            waiting_exit = input("按任意键退出程序...")
            exit()
    else:
        raise Exception("url或headers参数错误")
    return response


def get_image(url,headers,session):
    """
    :param url: 请求的url
    :param headers: 请求头
    :return: 返回响应
    获取验证码图片，并写入文件中
    """
    if url and headers and session:
        logger.info("获取验证码图片...")
        try:
            image_content = session.get(url=url,headers=headers, timeout=(6, 1), verify=False).content

            with open('./verify_image.png', 'wb') as f:
                f.write(image_content)
        except Exception as e:
            logger.error("获取验证码失败...",e)
            waiting_exit = input("按任意键退出程序...")
            exit()
    else:
        raise Exception("url或headers参数错误")
