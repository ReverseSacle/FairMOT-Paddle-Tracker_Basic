import numpy as np
import paddle
import os
import cv2
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from cv2 import *

from deploy.python.infer import print_arguments, PredictConfig
from deploy.python.mot_jde_infer import JDE_Detector, MOTTimer
from deploy.python.utils import argsparser
from ppdet.modeling.mot import visualization as mot_vis




class Communicate(QObject):
    signal = pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, frequent=20):
        QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps


class VideoQt(QWidget):
    VIDEO_TYPE_OFFLINE = 0
    VIDEO_TYPE_REAL_TIME = 1
    STATUS_INIT = 0
    STATUS_PLAYING = 1
    STATUS_PAUSE = 2

    def __init__(self, video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        QWidget.__init__(self)
        self.video_address = ""
        self.video_output_address = ""
        self.choose_to_view_folder = ""
        self.couting_time = 0
        self.flag_to_video = 0
        self.flag_for_video_to_display = None
        self.video_type = video_type  # 0: offline  1: realTime
        self.auto_play = auto_play
        self.status = self.STATUS_INIT  # 0: init 1:playing 2: pause

        # timer 设置
        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.show_video_images)
        #*******************************************************************
        self.set_root_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        self.set_video_file = self.set_root_dir + '/test.avi'
        self.set_camera_id = -1
        self.set_threshold = 0.1
        self.set_use_device = 'gpu'


        self.set_use_gpu = False
        if self.set_use_device in ['gpu', 'Gpu', 'GPU']:
            self.set_use_gpu = True

        #******************************************************************

        # 初始化参数
        self.playCapture = cv2.VideoCapture()
        if self.video_output_address != "":
            self.playCapture.open(self.video_output_address)
            fps = self.playCapture.get(cv2.CAP_PROP_FPS)
            self.timer.set_fps(fps)
            self.playCapture.release()
            if self.auto_play:
                self.switch_video()

        self.threshold_value = 0.1
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 设置编码

    # 选择需要预测的视频文件
    def choose_file(self):
        self.video_address, filetype = QFileDialog.getOpenFileName(self, "请选择所需要的文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        self.flag_for_video_to_display = 0  # 打开
        print('输入路径：' + self.video_address)

    # 选择需要打开的视频文件
    def choose_file_to_view(self):
        self.choose_to_view_folder, filetype = QFileDialog.getOpenFileName(self, "请选择所需要的文件", os.getcwd(),
                                                                           "All Files(*);;Text Files(*.txt)")
        self.flag_for_video_to_display = 1  # 选择
        print('选择查看的视频路径：' + self.choose_to_view_folder)

    # 选择需要预测的视频文件的方法函数
    def open_video_file(self):
        self.choose_file()

    # 选择需要打开的视频文件的方法函数
    def open_video_for_view(self):
        self.choose_file_to_view()

    # 更新进程
    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        self.status = VideoQt.STATUS_INIT
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    # 在界面上展示图像
    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                frame = cv2.resize(frame, (1000, 1000), interpolation=cv2.INTER_AREA)
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                self.videolabel.setPixmap(temp_pixmap)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is VideoQt.VIDEO_TYPE_OFFLINE:
                    print("play finished")  # 判断本地文件播放完毕
                    self.reset()
                    self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    # 暂停与播放开关
    def switch_video(self):
        flag = 0
        if self.flag_for_video_to_display == 1:
            change_video_address = self.choose_to_view_folder
            flag = 1

        if self.flag_for_video_to_display == 0:
            change_video_address = self.video_address
            flag = 1
        try:
            print('当前视频文件：' + change_video_address)
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '提示！', '请确保有选择视频文件')
            msg_box.exec_()

        if self.flag_for_video_to_display == 0 and flag == 1:
            if self.flag_to_video == 1:
                if self.video_output_address == "" or self.video_output_address is None:
                    return
                if self.status is VideoQt.STATUS_INIT:
                    self.playCapture.open(self.video_output_address)
                    self.timer.start()
                    self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
                elif self.status is VideoQt.STATUS_PLAYING:
                    self.timer.stop()
                    if self.video_type is VideoQt.VIDEO_TYPE_REAL_TIME:
                        self.playCapture.release()
                    self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
                elif self.status is VideoQt.STATUS_PAUSE:
                    if self.video_type is VideoQt.VIDEO_TYPE_REAL_TIME:
                        self.playCapture.open(self.video_output_address)
                    self.timer.start()
                    self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

                self.status = (VideoQt.STATUS_PLAYING,
                               VideoQt.STATUS_PAUSE,
                               VideoQt.STATUS_PLAYING)[self.status]


        else:
            if self.flag_for_video_to_display == 1 and flag == 1:
                if change_video_address == "" or change_video_address is None:
                    return
                if self.status is VideoQt.STATUS_INIT:
                    self.playCapture.open(change_video_address)
                    self.timer.start()
                    self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
                elif self.status is VideoQt.STATUS_PLAYING:
                    self.timer.stop()
                    if self.video_type is VideoQt.VIDEO_TYPE_REAL_TIME:
                        self.playCapture.release()
                    self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
                elif self.status is VideoQt.STATUS_PAUSE:
                    if self.video_type is VideoQt.VIDEO_TYPE_REAL_TIME:
                        self.playCapture.open(change_video_address)
                    self.timer.start()
                    self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

                self.status = (VideoQt.STATUS_PLAYING,
                               VideoQt.STATUS_PAUSE,
                               VideoQt.STATUS_PLAYING)[self.status]
            else:
                if flag == 1:
                    msg_box = QMessageBox(QMessageBox.Warning, '提示！',  "请确保已经进行了视频预测")
                    msg_box.exec_()
                else:
                    pass

    # 获取阈值
    def onActivated(self, text):
        self.threshold_value = text
        return print(self.threshold_value)

    def open_current_device_video(self):
        try:
            # Set params
            self.couting_time += 1
            set_threshold = self.threshold_value  # 阈值
            set_camera_id = 0
            file_name = 'output_%s' % self.couting_time
            paddle.enable_static()
            parser = argsparser(self.set_root_dir,
                                None,
                                set_camera_id,
                                set_threshold,
                                self.set_use_device,
                                self.set_use_gpu)
            FLAGS = parser.parse_args()
            print_arguments(FLAGS)
            FLAGS.device = FLAGS.device.upper()
            assert FLAGS.device in ['CPU', 'GPU', 'XPU'
                                    ], "device should be CPU, GPU or XPU"

            pred_config = PredictConfig(FLAGS.model_dir)
            detector = JDE_Detector(
                pred_config,
                FLAGS.model_dir,
                device=FLAGS.device,
                run_mode=FLAGS.run_mode,
                trt_min_shape=FLAGS.trt_min_shape,
                trt_max_shape=FLAGS.trt_max_shape,
                trt_opt_shape=FLAGS.trt_opt_shape,
                trt_calib_mode=FLAGS.trt_calib_mode,
                cpu_threads=FLAGS.cpu_threads,
                enable_mkldnn=FLAGS.enable_mkldnn)

            self.video_output_address = self.set_root_dir + '/output/' + file_name + '.mp4'
            print('输出路径：' + self.video_output_address)
            self.capture = cv2.VideoCapture(set_camera_id)
            video_name = file_name + '.mp4'
            fps = 30
            frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            print('frame_count', frame_count)
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # yapf: disable
            fourcc = self.fourcc
            # yapf: enable
            if not os.path.exists(FLAGS.output_dir):
                os.makedirs(FLAGS.output_dir)
            out_path = os.path.join(FLAGS.output_dir, video_name)
            self.writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
            frame_id = 0
            timer = MOTTimer()
            results = []
            while (1):
                try:
                    ret, frame = self.capture.read()
                    if not ret:
                        break
                    timer.tic()
                    online_tlwhs, online_scores, online_ids = detector.predict(
                        [frame], FLAGS.threshold)
                    timer.toc()

                    results.append((frame_id + 1, online_tlwhs, online_scores, online_ids))
                    fps = 1. / timer.average_time
                    online_im = mot_vis.plot_tracking(
                        frame,
                        online_tlwhs,
                        online_ids,
                        online_scores,
                        frame_id=frame_id,
                        fps=fps)
                    frame_id += 1
                    print('detect frame:%d' % (frame_id))
                    im = np.array(online_im)
                    self.writer.write(im)
                    height, width = im.shape[:2]
                    if im.ndim == 3:
                        rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    elif frame.ndim == 2:
                        rgb = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
                    temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                    temp_pixmap = QPixmap.fromImage(temp_image)
                    self.videolabel.setPixmap(temp_pixmap)
                    QApplication.processEvents()
                except:
                    self.writer.release()
            self.writer.release()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '提示！', '请确保有外置摄像头')
            msg_box.exec_()


    def open_other_device_video(self):
        try:
            # Set params
            self.couting_time += 1
            set_threshold = self.threshold_value  # 阈值
            set_camera_id = 1
            file_name = 'output_%s' % self.couting_time
            paddle.enable_static()
            parser = argsparser(self.set_root_dir,
                                None,
                                set_camera_id,
                                set_threshold,
                                self.set_use_device,
                                self.set_use_gpu)
            FLAGS = parser.parse_args()
            print_arguments(FLAGS)
            FLAGS.device = FLAGS.device.upper()
            assert FLAGS.device in ['CPU', 'GPU', 'XPU'
                                    ], "device should be CPU, GPU or XPU"

            pred_config = PredictConfig(FLAGS.model_dir)
            detector = JDE_Detector(
                pred_config,
                FLAGS.model_dir,
                device=FLAGS.device,
                run_mode=FLAGS.run_mode,
                trt_min_shape=FLAGS.trt_min_shape,
                trt_max_shape=FLAGS.trt_max_shape,
                trt_opt_shape=FLAGS.trt_opt_shape,
                trt_calib_mode=FLAGS.trt_calib_mode,
                cpu_threads=FLAGS.cpu_threads,
                enable_mkldnn=FLAGS.enable_mkldnn)

            self.video_output_address = self.set_root_dir + '/output/' + file_name + '.mp4'
            print('输出路径：' + self.video_output_address)
            self.capture = cv2.VideoCapture(set_camera_id)
            video_name = file_name + '.mp4'
            fps = 30
            frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            print('frame_count', frame_count)
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # yapf: disable
            fourcc = self.fourcc
            # yapf: enable
            if not os.path.exists(FLAGS.output_dir):
                os.makedirs(FLAGS.output_dir)
            out_path = os.path.join(FLAGS.output_dir, video_name)
            self.writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
            frame_id = 0
            timer = MOTTimer()
            results = []
            while (1):
                try:
                    ret, frame = self.capture.read()
                    if not ret:
                        break
                    timer.tic()
                    online_tlwhs, online_scores, online_ids = detector.predict(
                        [frame], FLAGS.threshold)
                    timer.toc()

                    results.append((frame_id + 1, online_tlwhs, online_scores, online_ids))
                    fps = 1. / timer.average_time
                    online_im = mot_vis.plot_tracking(
                        frame,
                        online_tlwhs,
                        online_ids,
                        online_scores,
                        frame_id=frame_id,
                        fps=fps)
                    frame_id += 1
                    print('detect frame:%d' % (frame_id))
                    im = np.array(online_im)
                    self.writer.write(im)
                    height, width = im.shape[:2]
                    if im.ndim == 3:
                        rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    elif frame.ndim == 2:
                        rgb = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
                    temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                    temp_pixmap = QPixmap.fromImage(temp_image)
                    self.videolabel.setPixmap(temp_pixmap)
                    QApplication.processEvents()
                except:
                    self.writer.release()
            self.writer.release()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '提示！', '请确保有外置摄像头')
            msg_box.exec_()


    def close_video(self):  # 关闭视频
        try:
            self.writer.release()
        except:
            pass
        try:
            self.cap.release()
        except:
            pass
        cv2.destroyAllWindows()


    #视频追踪
    def predict_video(self):
        flag_predict = 0
        try:
            # Set params
            self.set_threshold = self.threshold_value  # 阈值
            if os.path.exists(self.video_address):
                set_video_file = self.video_address
                flag_predict = 1
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '提示！', "请确保有输入路径")
                msg_box.exec_()
            if flag_predict == 1:
                file_name = (set_video_file.split('.')[0]).split('/')[-1] + '_output'
                self.video_output_address = self.set_root_dir + '/output/' + file_name + '.mp4'
                print('输出路径：' + self.video_output_address)
            self.progressBar.setValue(0)
            paddle.enable_static()
            parser = argsparser(self.set_root_dir,
                                set_video_file,
                                self.set_camera_id,
                                self.set_threshold,
                                self.set_use_device,
                                self.set_use_gpu)
            FLAGS = parser.parse_args()
            print_arguments(FLAGS)
            FLAGS.device = FLAGS.device.upper()
            assert FLAGS.device in ['CPU', 'GPU', 'XPU'
                                    ], "device should be CPU, GPU or XPU"

            pred_config = PredictConfig(FLAGS.model_dir)
            detector = JDE_Detector(
                pred_config,
                FLAGS.model_dir,
                device=FLAGS.device,
                run_mode=FLAGS.run_mode,
                trt_min_shape=FLAGS.trt_min_shape,
                trt_max_shape=FLAGS.trt_max_shape,
                trt_opt_shape=FLAGS.trt_opt_shape,
                trt_calib_mode=FLAGS.trt_calib_mode,
                cpu_threads=FLAGS.cpu_threads,
                enable_mkldnn=FLAGS.enable_mkldnn)

            # predict from video file or camera video stream

            self.capture = cv2.VideoCapture(FLAGS.video_file)
            video_name = file_name + '.mp4'
            fps = 30
            frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            print('frame_count', frame_count)
            self.progressBar.setMaximum(frame_count)
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # yapf: disable
            fourcc = self.fourcc
            # yapf: enable
            if not os.path.exists(FLAGS.output_dir):
                os.makedirs(FLAGS.output_dir)
            out_path = os.path.join(FLAGS.output_dir, video_name)
            writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
            frame_id = 0
            timer = MOTTimer()
            results = []
            step = 0
            while (1):
                step += 1
                ret, frame = self.capture.read()
                if not ret:
                    break
                timer.tic()
                online_tlwhs, online_scores, online_ids = detector.predict(
                    [frame], FLAGS.threshold)
                timer.toc()

                results.append((frame_id + 1, online_tlwhs, online_scores, online_ids))
                fps = 1. / timer.average_time
                online_im = mot_vis.plot_tracking(
                    frame,
                    online_tlwhs,
                    online_ids,
                    online_scores,
                    frame_id=frame_id,
                    fps=fps)
                if FLAGS.save_images:
                    save_dir = os.path.join(FLAGS.output_dir, video_name.split('.')[-2])
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    cv2.imwrite(
                        os.path.join(save_dir, '{:05d}.jpg'.format(frame_id)),
                        online_im)
                frame_id += 1
                print('detect frame:%d' % (frame_id))
                im = np.array(online_im)
                writer.write(im)
                self.progressBar.setValue(step)
                QApplication.processEvents()
            self.flag_to_video = 1
            msg_box = QMessageBox(QMessageBox.Warning, '提示！',  "视频预测完成")
            msg_box.exec_()
            writer.release()

        except:
            pass
            #msg_box = QMessageBox(QMessageBox.Warning, '提示！',  '错误')
            #msg_box.exec_()


    # 选择并打开所选的视频文件
    def open_video_file_to_view(self):
        self.open_video_for_view()

    def closeEvent(self, event):

        reply = QtWidgets.QMessageBox.question(self, '提示！',
                                               "确定要退出程序吗?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            os._exit(0)

        else:
            pass

            # ---------------qt页面-------------------------#

    def setupUi(self, Form):
        Form.setObjectName("Form")
        # 窗口大小
        Form.resize(1200, 800)
        # 摄像区
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setStyleSheet('font-size:16px;color:white;')
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(100, 120, 800, 590))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        # 设置摄像头播放区
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.videolabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.videolabel.setAutoFillBackground(True)
        self.videolabel.setGeometry(0, 0, 800, 800)
        self.videolabel.setScaledContents(True)
        self.videolabel.setObjectName("videolabel")
        self.horizontalLayout.addWidget(self.videolabel)
        # 设置视频播放区
        # self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.videolabel2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.videolabel2.setAutoFillBackground(True)
        self.videolabel2.setGeometry(0, 0, 800, 800)
        self.videolabel2.setScaledContents(True)
        self.videolabel2.setObjectName("videolabel2")
        self.horizontalLayout.addWidget(self.videolabel2)
        # 按钮组
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(950, 200, 150, 300))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setStyleSheet('font-size:16px;color:white;')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        # 阈值选择区
        self.Thresholdlable = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Thresholdlable.setObjectName("Thresholdlable")
        self.Thresholdlable.setStyleSheet('font-size:16px;color:white;')
        self.verticalLayout.addWidget(self.Thresholdlable)
        self.Threshold = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.Threshold.setObjectName("Threshold")
        self.Threshold.setStyleSheet('background-color:slategray;font-size:16px;color:white;'
                                     'selection-background-color:gainsboro;'
                                     'selection-color:red;')
        self.Threshold.activated[str].connect(self.onActivated)
        self.verticalLayout.addWidget(self.Threshold)

        # 选择视频文件
        self.selectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.selectButton.setObjectName("selectButton")
        self.selectButton.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.selectButton.clicked.connect(self.open_video_file)
        self.verticalLayout.addWidget(self.selectButton)
        # 视频检测
        self.videoButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.videoButton.setEnabled(True)
        self.videoButton.setObjectName("videoButton")
        self.videoButton.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.videoButton.clicked.connect(self.predict_video)
        self.verticalLayout.addWidget(self.videoButton)
        # 暂停与播放键
        self.stopButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stopButton.setObjectName("startButto")
        self.stopButton.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.stopButton.clicked.connect(self.switch_video)
        self.verticalLayout.addWidget(self.stopButton)

        # 连接打开按钮
        self.openButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.openButton.setObjectName("openButton")
        self.openButton.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.openButton.setGeometry(0, 0, 32, 32)
        self.openButton.clicked.connect(self.open_current_device_video)
        self.verticalLayout.addWidget(self.openButton)

        # 外置按钮
        self.openButton2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.openButton2.setObjectName("openButton")
        self.openButton2.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.openButton2.setGeometry(0, 0, 32, 32)
        self.openButton2.clicked.connect(self.open_other_device_video)
        self.verticalLayout.addWidget(self.openButton2)

        # 打开视频文件
        self.selectButton2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.selectButton2.setObjectName("selectButton2")
        self.selectButton2.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.selectButton2.clicked.connect(self.open_video_file_to_view)
        self.verticalLayout.addWidget(self.selectButton2)

        # 关闭视频
        self.closeButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.closeButton.clicked.connect(self.close_video)
        self.verticalLayout.addWidget(self.closeButton)
        # 关闭窗口
        self.quitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.quitButton.setObjectName("quitButton")
        self.quitButton.setStyleSheet('background-color:slategray;font-size:16px;color:white;')
        self.quitButton.clicked.connect(self.closeEvent)
        self.verticalLayout.addWidget(self.quitButton)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        #进度条
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)


    def retranslateUi(self, Form):
        self._translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(self._translate("Form", "行人检测识别"))

        # self.label1.setText(self._translate("MainWindow", "行人检测系统"))
        self.videolabel.setText(self._translate("Form", " "))
        self.videolabel2.setText(self._translate("Form", "展示区"))

        self.Thresholdlable.setText(self._translate("Form", "阈值选择"))
        self.openButton.setText(self._translate("Form", "打开内置摄像头"))
        self.openButton2.setText(self._translate("Form", "打开外置摄像头"))
        self.closeButton.setText(self._translate("Form", "关闭摄像头"))
        self.Threshold.addItem(self._translate("Form", "0.1"))
        self.Threshold.addItem(self._translate("Form", "0.2"))
        self.Threshold.addItem(self._translate("Form", "0.3"))
        self.Threshold.addItem(self._translate("Form", "0.4"))
        self.Threshold.addItem(self._translate("Form", "0.5"))
        self.Threshold.addItem(self._translate("Form", "0.6"))
        self.Threshold.addItem(self._translate("Form", "0.7"))
        self.Threshold.addItem(self._translate("Form", "0.8"))
        self.Threshold.addItem(self._translate("Form", "0.9"))
        self.selectButton.setText(self._translate("Form", "选择视频文件"))
        self.selectButton2.setText(self._translate("Form", "打开视频文件"))
        self.videoButton.setText(self._translate("Form", "视频追踪"))
        self.stopButton.setText(self._translate("Form", "视频当前状态"))
        self.quitButton.setText(self._translate("Form", "退出"))


if __name__ == "__main__":
    # 初始化视屏和页面
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.setStyleSheet('background-color:black;')
    widget.setWindowOpacity(0.8)
    video = VideoQt()
    video.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
