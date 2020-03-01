2020.3.1

**一、配置D3.js环境**

1.index.html

2.package.json 设置

3.执行npminstall

![image-20200301225833061](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20200301225833061.png)

执行npminstall可以自动触发NPM去下载你工程中所引用的所有依赖，包括递归的下载依赖的依赖。所有的依赖库文件会被下载到node_modules文件夹中，该文件夹位于工程文件夹中的根目录里。这些完成以后，就可以创建一个HTML文件（跟我们之前创建的那个一样），HTML文件直接从node_modules/d3/d3.js来引用D3的JavaScript库。

4.安装http-server模块

>npm install http-server –g

5.启动服务器

> http-server .

该命令可以启动一个Node.js驱动的HTTP服务器，默认端口号是8080，也可以用-p参数指定一个端口号。

![image-20200301232235732](E:\student_data\work\combine_heatmap\d3forcombination\image-20200301232235732.png)

**二、看了读取json等的例子**

有初步的想法了！