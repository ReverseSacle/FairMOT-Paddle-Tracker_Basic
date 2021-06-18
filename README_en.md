**FairMOT_Paddle(Single Camera)**
===
[简体中文](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README.md) | [English](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README_en.md)

Preview
---
![MOT20-01](https://github.com/ReverseSacle/FairMOT_Paddle/blob/main/docs/MOT20-01.gif)

Enviroment Requirement
---
+ python3
+ paddlepaddle_develop edition
+ OpenCV
+ needed requirement -> ``` python setup.py install```
+ test system -> window10

Introduction
---
+ [Summary_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Introduction_en.md)
+ [Making_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Making_Introduction_en.md)

Provide Model file
---
**Download：** [Baidu Netdisk(Coming soon)]() -> need to put it in the model folder(root_dir)

Quickly strat
---

About training
---
+ [->Paddle_Detection 工具](https://github.com/PaddlePaddle/PaddleDetection) -> ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [->Prepare datasets](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README_cn.md#%E6%95%B0%E6%8D%AE%E9%9B%86%E5%87%86%E5%A4%87)
Not need to download all datasets,just choose what you want.After that,modify ```configs/dataset/mot.yml```
+ [->Strat to train](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.1/configs/mot/fairmot)
