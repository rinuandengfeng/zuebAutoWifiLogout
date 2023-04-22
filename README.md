# zuebWifiLogout
郑州经贸学院校园网自动下线脚本

## :star: 项目介绍
该项目是一个自动下线校园网的脚本，使用python编写，使用`requests`库进行网络请求，使用`xpath`进行数据解析，使用`ddddocr`包进行验证码识别，使用`pyinstaller`进行打包。
## :warning: 声明
该项目仅供为学习使用，若不正当的使用，产生的后果一概与本人无关。

## :muscle: 模块
![python](https://img.shields.io/badge/python-3.7.13-blue)
![requests](https://img.shields.io/badge/requests-2.28.1-blue)
![ddddocr](https://img.shields.io/badge/ddddocr-1.4.7-blue)
![pyinstaller](https://img.shields.io/badge/pyinstaller-5.6.2-blue)



## :rocket: 使用方法
1. 将代码克隆到本地
    ```bash
    git clone https://github.com/rinuandengfeng/zuebAutoWifiLogout.git
    ```
2. 找到`.env`文件，修改其中的账号密码。![修改账号密码](/img/env.jpg)

3. 打开`dist/`文件夹，找到`wifi.exe`文件
![img_1.png](/img/find_wifi.jpg)

4. 可以将`dist`文件夹，中的`wifi.exe`发送桌面**快捷方式**，使用更加方便。


## :bug: BUG
该项目存在的问题，主要是`ddddocr`包的问题，具体如下：
1. 验证码识别率不高，有时需要多次运行才能识别出来。(使用的免费的验证码识别，这一点我现在也无能为力 :grimacing:)


## :rainbow: TODO
- [ ] 退出登录后可以直接登录登录上自己的账号
- [ ] 优化验证码识别率
- [ ] 优化代码结构









