from deploy.python.mot_infer import *
from deploy.python.utils import *

#Set params
threshold = 0.6                                #阈值
video_path = './video/test.avi'                 #使用摄像头时要为None
camera_id = -1                                  #默认-1为不使用摄像头，传入视频时需为-1

#Start to run
paddle.enable_static()
parser = argsparser(new_threshold = threshold,
                    new_camera_id = camera_id,
                    new_video_path = video_path)
FLAGS = parser.parse_args()
print_arguments(FLAGS)
pred_config = PredictConfig_MOT(FLAGS.model_dir)
detector = MOT_Detector(
    pred_config,
    FLAGS.model_dir,
    use_gpu=FLAGS.use_gpu,
    run_mode=FLAGS.run_mode,
    trt_min_shape=FLAGS.trt_min_shape,
    trt_max_shape=FLAGS.trt_max_shape,
    trt_opt_shape=FLAGS.trt_opt_shape,
    trt_calib_mode=FLAGS.trt_calib_mode,
    cpu_threads=FLAGS.cpu_threads,
    enable_mkldnn=FLAGS.enable_mkldnn)

# predict from video file or camera video stream
if FLAGS.video_file is not None or FLAGS.camera_id != -1:
    predict_video(detector,
                  new_camera_id = camera_id,
                  new_video_path = video_path,
                  new_threshold = threshold)
else:
    print('MOT models do not support predict single image.')