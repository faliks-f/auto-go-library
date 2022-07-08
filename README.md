# Auto-Go-Library

#### 注意：此项目只能在linux系统上运行，在Windows系统上运行一段时间后会停止运行，这与系统的底层api实现有关

我自动去图书馆,通过电脑端微信客户端进行抓包

抓包教程：[Chalres安装证书抓https包](https://blog.csdn.net/m0_46225184/article/details/125416873)
[网络数据包分析](https://blog.csdn.net/m0_46225184/article/details/125530140?csdn_share_tail=%7B%22type%22%3A%22blog%22%2C%22rType%22%3A%22article%22%2C%22rId%22%3A%22125530140%22%2C%22source%22%3A%22m0_46225184%22%7D&ctrtid=6gpa9)

安装依赖
```shell
pip install -r requirements.txt
```

启动服务
```shell
#直接启动
python3 main.py
#建议使用screen命令启动
screen -S go-library python3 main.py
```

单次运行测试
```shell
python3 main.py --run-once True
```