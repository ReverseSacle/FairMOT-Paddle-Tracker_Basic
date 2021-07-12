**FairMOT_Paddle(单摄像头)**
===
[简体中文](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README.md) | [English](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README_en.md)

效果预览
---
![MOT20-01](https://github.com/ReverseSacle/FairMOT_Paddle/blob/main/docs/MOT20-01.gif)

环境要求
---
+ python3
+ paddlepaddle_develop版
+ OpenCV
+ 需要的第三方库 -> ```python setup.py install```
+ 运行的测试平台 -> window10
+ 已经配置好的conda环境--[paddle-env(暂无)]

相关介绍
---
+ [概要介绍](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Introduction_cn.md)
+ [制作介绍](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Making_Introduction_cn.md)

提供的模型文件
---
+ **下载：** [百度网盘(暂无)]() -> 默认需放置根目录的model文件夹下

快速使用
---
+ ``` git clone "https://github.com/ReverseSacle/FairMOT_Paddle.git"```

关于训练(基于paddle_detection)
---
+ [->Paddle_Detection 工具](https://github.com/PaddlePaddle/PaddleDetection) -> ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [->准备数据集](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README_cn.md)
按需要选择数据集，并非需全部下载，之后修改```configs/dataset/mot.yml```
+ [->开始训练](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/fairmot/README_cn.md)

作者
---
+ 大一在读生
 
