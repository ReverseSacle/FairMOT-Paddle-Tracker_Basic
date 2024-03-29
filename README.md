# FairMOT_Paddle_Tracker(单摄像头)
[简体中文](https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic/blob/main/README.md) | [English](https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic/blob/main/README_en.md)

地址导航
---
+ [→Pytorch版地址](https://github.com/ReverseSacle/FairMOT-Pytorch-Tracker_Basic)
+ [→FairMot作者(Github)](https://github.com/ifzhang/FairMOT)

效果预览
---
![MOT20-01](https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic/blob/main/docs/MOT20-01.gif)

界面预览
---
![Interface](https://user-images.githubusercontent.com/73418195/126268446-f38053a6-3b1c-4c3f-98c2-afe07030a8ff.png)


软件系统环境要求
---
+ 具备英伟达显卡 显存4G及其以上
+ 运行内存 8G及其以上
+ 具备window7及其以上版本的系统

相关介绍
---
+ [→概要介绍](https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic/blob/main/docs/Introduction_cn.md)
+ [→制作介绍](https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic/blob/main/docs/Making_Introduction_cn.md)
+ [→软件使用指南](https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic/blob/main/docs/The_fuction_of_program_cn.md)


源代码环境要求
---
+ python3
+ OpenCV
+ 需要的第三方库 → 基本为paddle_detection所需要的
+ 运行的测试平台 → window10
+ 已经配置好的conda环境(所需要的全部环境的整合) --> **paddle-env下载：**[→OneDrive](https://1drv.ms/u/s!AlYD8lJlPHCIh3I2hTN2AbggBMBZ?e=VoeXM2?download=1)

源代码调试运行
---
+ ``` git clone "https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic.git"```
+ 解压paddle-env环境到Anaconda3/envs/目录下
+ 使用pycharm，调用此paddle-env环境,再在根目录中创建一个**bset_model**文件夹将下面的模型权重压缩包解压到此文件夹中即可使用


提供的模型权重文件
---
+ **下载：** [→OneDrive](https://1drv.ms/u/s!AlYD8lJlPHCIh3EfB5mefhNtDcEO?e=xt2upV?download=1) → 默认需放置根目录的best_model文件夹下



关于训练(基于paddle_detection)
---
+ [→Paddle_Detection 工具](https://github.com/PaddlePaddle/PaddleDetection) → ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [→准备数据集](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README_cn.md)
+ [→开始训练](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/fairmot/README_cn.md)

基础套件
---
+ Pyqt5 --> 界面窗口、按钮组、阈值选择、文件选择和进度条
+ Paddle --> 追踪效果
+ Opencv --> 视频和摄像头追踪，播放与暂停

参与者
---
百度Ai Studio主页
---
+ [→ASDLibb](https://aistudio.baidu.com/aistudio/personalcenter/thirdview/736371)
+ [→Chen Huilin](https://aistudio.baidu.com/aistudio/personalcenter/thirdview/787763)
 
