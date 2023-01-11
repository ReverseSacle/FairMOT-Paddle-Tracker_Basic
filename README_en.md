**FairMOT_Paddle_Tracker(Single Camera)**
===
[简体中文](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README.md) | [English](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/README_en.md)

Address Navigation
---
+ [→Pytorch edtion address](https://github.com/ReverseSacle/FairMOT-Pytorch-Tracker_Basic)
+ [→FairMot author(Github)](https://github.com/ifzhang/FairMOT)

Preview
---
![MOT20-01](https://github.com/ReverseSacle/FairMOT_Paddle/blob/main/docs/MOT20-01.gif)

Preview for Interface
---
![Interface](https://user-images.githubusercontent.com/73418195/126273708-42a9aec3-a07f-4102-aaf2-3a6f5cadf2b5.png)



Enviroment Requirement
---
+ Python3
+ Paddlepaddle==2.1.0 edition
+ OpenCV-python
+ Needed requirements → All the requirements of paddle_detection
+ Test system → window10
+ The provided pkged enviroment(coda enviroment wich have all the needed libs) --> [→Google Drive](https://drive.google.com/file/d/11Wxn3kojjrbd-YL59h8dfg3eQLt0IJmn/view?usp=sharing)

Introduction
---
+ [→Summary_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Introduction_en.md)
+ [→Making_Introduction](https://github.com/ReverseSacle/FairMOT_paddle/blob/main/docs/Making_Introduction_en.md)

Provide Model file
---
**Download：** [→Google Drive](https://drive.google.com/file/d/1PRkK0G5-I9t63cT_YgCetKSpxQEecZ7-/view?usp=sharing) → need to put them in  the folder named __best_model__(root_dir)

Quickly start
---
+ ```git clone "https://github.com/ReverseSacle/FairMOT_Paddle.git"```
+ Unzip paddle-enviroment in Anaconda3/envs/ folder
+ Use pycharm,choose paddle-env enviroment.Then,create a folder named **best_model**,unzip the inference-weight in the __best_model__ folder.

About Function of Buttons
---
+ [→What the mean of the button](https://github.com/ReverseSacle/FairMOT-Paddle-Tracker_Basic/blob/main/docs/The_button_function_en.md)



About training
---
+ [→Paddle_Detection](https://github.com/PaddlePaddle/PaddleDetection) → ```git clone "https://github.com/PaddlePaddle/PaddleDetection.git" ```
+ [→Prepare datasets](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/configs/mot/README.md)
+ [→Start to train](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.1/configs/mot/fairmot)
