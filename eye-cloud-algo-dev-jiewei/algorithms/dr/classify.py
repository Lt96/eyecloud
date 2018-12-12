# Created by Gotcha on 2018/5/1
# -*- coding: utf-8 -*-

import os
import tensorflow as tf
from tensorflow.python.framework.errors_impl import InvalidArgumentError
from tensorflow.python.platform import gfile
import re
from . import LeNet5_evaluate
import shutil


class DRDectect:
    def __init__(self, config):
        self.model_path = config['model_path']
        self.side_model_path = config['side_model_path']
        self.resized_input_tensor_name = config['resized_input_tensor_name']
        self.final_result_name = config['final_result_name']
        self.input_width = config['input_width']
        self.input_height = config['input_height']
        self.input_depth = config['input_depth']
        self.input_mean = config['input_mean']
        self.input_std = config['input_std']

    def initial(self):
        with tf.Graph().as_default() as graph:
            graph_def = tf.GraphDef()

            try:
                with open(self.model_path, 'rb') as model:
                    graph_def.ParseFromString(model.read())
                    self.resized_input_tensor, self.final_result = tf.import_graph_def(
                        graph_def,
                        name='',
                        return_elements=[
                            self.resized_input_tensor_name,
                            self.final_result_name
                        ])
            except Exception as e:
                raise e

            # Set up the image decoding sub-graph.
            self.image_data_tensor, self.decoded_image_tensor = self.decode_jpeg(
                self.input_width, self.input_height,
                self.input_depth, self.input_mean,
                self.input_std
            )

            self.graph = graph

    def classify(self, image_path):
        result = ''
        with tf.Session(graph=self.graph) as sess:
            image_tensor = gfile.FastGFile(image_path, 'rb').read()
            try:
                # Preprocess input images
                resized_input_values = sess.run(self.decoded_image_tensor,
                                                {self.image_data_tensor: image_tensor})
                # Run preprocessed images through the network.
                result_tensor = sess.run(self.final_result,
                                         {self.resized_input_tensor: resized_input_values})
            except InvalidArgumentError as e:
                raise e

            res = LeNet5_evaluate.evalutate(image_path, self.side_model_path)
            direction = ''
            type_ = ''
            if res:
                direction, _ = res

            if result_tensor[0][0] > result_tensor[0][1]:
                probability = round(result_tensor[0][0], 4)
                type_ = 'DR'
            else:
                probability = round(result_tensor[0][1], 4)
                type_ = 'NORMAL'

            return type_, probability, direction

    def decode_jpeg(self, input_width, input_height, input_depth, input_mean, input_std):
        jpeg_data = tf.placeholder(tf.string, name='DecodeJPEGInput')
        decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
        decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
        decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
        resize_shape = tf.stack([input_height, input_width])
        resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
        resized_image = tf.image.resize_bilinear(decoded_image_4d,
                                                 resize_shape_as_int)
        offset_image = tf.subtract(resized_image, input_mean)
        mul_image = tf.multiply(offset_image, 1.0 / input_std)
        return jpeg_data, mul_image
