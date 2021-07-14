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
One is the weight(best_model) and the other is the inference weight which you need.  
**Download：** [Google Drive](https://drive.google.com/file/d/14iXPzddTOLkW-eH6eLzWKK2I6hC87asN/view?usp=sharing) -> need to put them in  the folder named __best_model__(root_dir)

Quickly start
---
+ ```git clone "https://github.com/ReverseSacle/FairMOT_Paddle.git"```
+ Unzip paddle-enviroment in Anaconda3/envs/ folder
+ Use pycharm,choose paddle-env enviroment.Then,create a folder named model,put the inference-weight in the __best_model__ folder.



About training
---
+ [->Paddle_Detection](https://github.com/PaddlePaddle/PaddleDetection) -> ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [->Prepare datasets](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README.md)
Not need to download all datasets,just choose what you want.After that,modify ```configs/dataset/mot.yml```
+ [->Start to train](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.1/configs/mot/fairmot)
