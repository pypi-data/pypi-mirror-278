# test

Supervisor for Windows wrote by Weber Juche.
2016.7.19


## 设计目的

在Windows下启动并控制其它命令行程序(cmdProgram)运行。
类似于Linux系统下的 Supervisor 工具。

## 打包上传PyPi方法
相关命令如下

````
$ python setup.py sdist  # 编译包
$ python setup.py sdist upload # 上传包
$ pip install --upgrade --no-cache-dir weberWinSV
````

20240611 需要升级采用 twine 上载
```
pip3 install build # 构建包的工具
pip3 install twine # 上传包的工具
pip3 install wheel # wheel格式


python setup.py sdist bdist_wheel
python -m twine upload dist/*

twine upload dist/*

twine upload --skip-existing dist/* 会上传 dist 目录下全部包
```

