import cv2
import paddle
import os
import numpy as np
from deploy.python.infer import print_arguments, PredictConfig
from deploy.python.mot_jde_infer import JDE_Detector, MOTTimer
from deploy.python.utils import argsparser
from ppdet.modeling.mot import visualization as mot_vis

set_root_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
set_video_file = set_root_dir + '/test.avi'
set_camera_id = -1
set_threshold = 0.5
set_use_device = 'gpu'

set_use_gpu = False
if set_use_device in ['gpu','Gpu','GPU']:
    set_use_gpu = True

paddle.enable_static()
parser = argsparser(set_root_dir,
                    set_video_file,
                    set_camera_id,
                    set_threshold,
                    set_use_device,
                    set_use_gpu)
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
if FLAGS.video_file is not None or FLAGS.camera_id != -1:
        if set_camera_id != -1:
            capture = cv2.VideoCapture(set_camera_id)
            video_name = 'mot_output.mp4'
        else:
            capture = cv2.VideoCapture(FLAGS.video_file)
            video_name = os.path.split(FLAGS.video_file)[-1]
        fps = 30
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        print('frame_count', frame_count)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # yapf: disable
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # yapf: enable
        if not os.path.exists(FLAGS.output_dir):
            os.makedirs(FLAGS.output_dir)
        out_path = os.path.join(FLAGS.output_dir, video_name)
        writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
        frame_id = 0
        timer = MOTTimer()
        results = []
        while (1):
            ret, frame = capture.read()
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
            if set_camera_id != -1:
                cv2.imshow('Tracking Detection', im)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        writer.release()
else:
    pass