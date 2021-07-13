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
+ Needed requirement -> All the requirement of paddle_detection
+ Test system -> window10
+ The provided pkged enviroment(coda enviroment wich have all the needed lib) --> [Baidu Netdisk(coming soon)]()

Introduction
---
+ [Summary_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Introduction_en.md)
+ [Making_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Making_Introduction_en.md)

Provide Model file
---
**Download：** [Baidu Netdisk(Coming soon)]() -> need to put it in the model folder(root_dir)

Quickly strat
---
+ ```git clone "https://github.com/ReverseSacle/FairMOT_Paddle.git"```

About training
---
+ [->Paddle_Detection 工具](https://github.com/PaddlePaddle/PaddleDetection) -> ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [->Prepare datasets](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README.md)
Not need to download all datasets,just choose what you want.After that,modify ```configs/dataset/mot.yml```
+ [->Strat to train](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.1/configs/mot/fairmot)
