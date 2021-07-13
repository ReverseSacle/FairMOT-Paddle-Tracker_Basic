**FairMOT_Paddle_Tracker(Single Camera)**
===
[简体中文](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README.md) | [English](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README_en.md)

Preview
---
![MOT20-01](https://github.com/ReverseSacle/FairMOT_Paddle/blob/main/docs/MOT20-01.gif)

Enviroment Requirement
---
+ Python3
+ Paddlepaddle==2.1.0 edition
+ OpenCV-python
+ Needed requirement -> All the requirements of paddle_detection
+ Test system -> window10
+ The provided pkged enviroment(coda enviroment wich have all the needed libs) --> [Google Drive](https://drive.google.com/file/d/1zFbvtcSQwsg6Pmuoo0-q1k9-RclSbNE1/view?usp=sharing)

Introduction
---
+ [Summary_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Introduction_en.md)
+ [Making_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Making_Introduction_en.md)

Provide Model file
---
**Download：** [Google Drive](https://pan.baidu.com/s/1tXpDy2dSk1XYtFwdOsv1pg) -> need to put it in the folder named model(root_dir)

Quickly start
---
+ ```git clone "https://github.com/ReverseSacle/FairMOT_Paddle.git"```

About training
---
+ [->Paddle_Detection 工具](https://github.com/PaddlePaddle/PaddleDetection) -> ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [->Prepare datasets](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README.md)
Not need to download all datasets,just choose what you want.After that,modify ```configs/dataset/mot.yml```
+ [->Strat to train](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.1/configs/mot/fairmot)
