# 图片识别函数
import time

import ddddocr


def get_image_code(filename):
    print('进入获取验证码函数')
    time.sleep(5)
    ocr = ddddocr.DdddOcr()
    try:
        with open(filename, 'rb') as f:
            img_bytes = f.read()
    except:
        print('打开文件失败')
    verify_code = ocr.classification(img_bytes)
    print('验证码为：', verify_code)
    time.sleep(5)
    return verify_code
