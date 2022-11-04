
import time
from main import WifiLogout

username = input('请输入你的学号:')

password = input('请输入你的密码:')

user = WifiLogout(username=username, password=password)

user.logout()

