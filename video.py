import os
import numpy as np
import cv2
import tensorflow as tf

from main import CWD

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

if __name__ == "__main__":
    video_path = "video_2.mp4"
    print(CWD)
    model_path = os.path.join(CWD, "weights/best.h5")
    model = tf.keras.models.load_model(model_path, compile=False)
    vs = cv2.VideoCapture(video_path)
    _, frame = vs.read()
    H, W, _ = frame.shape
    vs.release()

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter('output.avi', fourcc, 10, (W, H), True)

    cap = cv2.VideoCapture(video_path)
    idx = 0
    while True:
        ret, frame = cap.read()
        if ret == False:
            cap.release()
            out.release()
            break

        H, W, _ = frame.shape
        ori_frame = frame
        frame = cv2.resize(frame, (256, 256))
        frame = np.expand_dims(frame, axis=0)
        frame = frame / 255.0

        mask = model.predict(frame)[0]
        mask = mask > 0.5
        mask = mask.astype(np.float32)
        mask = cv2.resize(mask, (W, H))
        mask = np.expand_dims(mask, axis=-1)

        combine_frame = ori_frame * mask
        combine_frame = combine_frame.astype(np.uint8)

        cv2.imwrite(f"video1/{idx}.png", combine_frame)
        idx += 1

        out.write(combine_frame)
