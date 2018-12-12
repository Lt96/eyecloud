# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
from . import LeNet5_inference
import os


def evalutate(image, model_path):
    with tf.Graph().as_default() as g:
        x = tf.placeholder(tf.float32, [
            1,
            LeNet5_inference.IMAGE_SIZE,
            LeNet5_inference.IMAGE_SIZE,
            LeNet5_inference.NUM_CHANNELS],
                           name='x-input')

        y = LeNet5_inference.inference(x, False, None)

        # variable_averages = tf.train.ExponentialMovingAverage(0.99)
        # variables_to_restore = variable_averages.variables_to_restore()
        # saver = tf.train.Saver(variables_to_restore)
        saver = tf.train.Saver()

        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(model_path)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                image_raw_data = tf.gfile.FastGFile(image, 'rb').read()
                img = tf.image.decode_jpeg(image_raw_data)
                resized_img = tf.image.resize_images(img, (32, 32), tf.image.ResizeMethod.NEAREST_NEIGHBOR)
                resized_img = np.asarray(resized_img.eval(), dtype='uint8')
                image_x = resized_img.astype('float32') / 255.0
                image_x = np.array(image_x).reshape(1, 32, 32, 3)
                res = sess.run(y, feed_dict={x: image_x})
                if res[0][0] > res[0][1]:
                    return 'LEFT', str(round(res[0][0], 2))
                else:
                    return 'RIGHT', str(round(res[0][1], 2))
            else:
                return None
