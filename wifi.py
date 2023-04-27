
import os
from dotenv import load_dotenv
from main import WifiLogout

#加载env文件
load_dotenv()

username = os.getenv("name")

password = os.getenv('password')

user = WifiLogout(username=username, password=password)

user.start()
a = input("请点×关闭窗口")


