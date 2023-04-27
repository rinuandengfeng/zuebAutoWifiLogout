from logs import logger
import time
import ddddocr


# 验证码识别函数
def get_verifycode_code():
    """
    :return: 返回验证码
    """
    logger.info("验证码获取中...")   
    try:
        ocr = ddddocr.DdddOcr()
    except Exception as e:
        logger.error("验证码识别模块加载失败,请检查模块是否安装正确!",e)
        waiting_exit = input("按任意键退出程序...")
        exit()
    try:
        with open('./verify_image.png', 'rb') as f:
            img_bytes = f.read()
    except:
        logger.error("验证码图片不存在")
    verify_code = ocr.classification(img_bytes)
    logger.info("验证码为:{}".format(verify_code))
    return verify_code


# def verify_code():
#         verify_code = get_verifycode_code()
#         if len(verify_code) == 4:
#             return verify_code
#         else:
#             # 验证码不是四位重新加载页面
#             logger.info("验证码校验错误重新加载页面...")
#             verify_code = get_verifycode_code()
#             return verify_code