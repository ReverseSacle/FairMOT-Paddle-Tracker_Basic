**FairMOT_Paddle_Tracker(单摄像头)**
===
[简体中文](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README.md) | [English](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README_en.md)

效果预览
---
![MOT20-01](https://github.com/ReverseSacle/FairMOT_Paddle/blob/main/docs/MOT20-01.gif)


软件系统环境要求
---
+ 具备英伟达显卡 显存4G及其以上
+ 运行内存 8G及其以上
+ 具备window7及其以上版本的系统

快速使用(可运行的软件)
---
+ 下载：[行人检测(百度网盘(暂无))]()
+  解压压缩包后，运行.exe文件，之后请参考**相关介绍**中的软件使用指南

相关介绍
---
+ [概要介绍](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Introduction_cn.md)
+ [制作介绍](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Making_Introduction_cn.md)
+ [软件使用指南]()


源码环境要求
---
+ python3
+ OpenCV
+ 需要的第三方库 -> 基本为paddle_detection所需要的
+ 运行的测试平台 -> window10
+ 已经配置好的conda环境(所需要的全部环境的整合)--[paddle-env(百度网盘(提取码：REVE))](https://pan.baidu.com/s/1JW7pPSYcO9cclDrnSI3TRg)

源代码调试运行
---
+ ``` git clone "https://github.com/ReverseSacle/FairMOT_Paddle.git"```
+ 解压paddle-env环境到Anaconda3/envs/目录下
+ 使用pycharm，调用此paddle-env环境,再创建一个model文件夹将下面的模型权重中的xxxinference压缩包解压到此文件夹中即可使用


提供的模型权重文件
---
一个是训练好的模型权重文件，另一个是你需要的inference权重。
+ **下载：** [百度网盘(提取码：REVE)](https://pan.baidu.com/s/1tXpDy2dSk1XYtFwdOsv1pg) -> 默认需放置根目录的model文件夹下



关于训练(基于paddle_detection)
---
+ [->Paddle_Detection 工具](https://github.com/PaddlePaddle/PaddleDetection) -> ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [->准备数据集](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README_cn.md)
按需要选择数据集，并非需全部下载，之后修改```configs/dataset/mot.yml```
+ [->开始训练](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/fairmot/README_cn.md)

作者
---
+ 大一在读生
 
