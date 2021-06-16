from deplot.python.utils import set_thrshold,set_model_dir,set_camera_id,set_output_dir,set_video_file,set_use_device
from deploy.python.mot_infer import *

#Related Params
threshold = None
model_dir = None
camera_id = None
output_dir = None
video_file = None
use_device = None

#Set each params
set_thrshold(threshold)
set_model_dir(model_dir)
set_camera_id(camera_id)
set_output_dir(output_dir)
set_video_file(video_file)
set_use_device(use_device)

#Start to use
paddle.enable_static()
parser = argsparser()
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

# Predict from video file or camera video stream
if FLAGS.video_file is not None or FLAGS.camera_id != -1:
    predict_video(detector, FLAGS.camera_id)
else:
    print('MOT models do not support predict single image.')


