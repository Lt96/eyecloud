# -*- coding: utf-8 -*-

import os
import time
import sys
sys.path.append('/Users/yuanz/PycharmProjects/runsurface/offline_surface')

import tensorflow as tf

import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
from keras.callbacks import Callback
from util import inception_preprocess, preprocess, recompone_overlap
from model import BilinearUpsampling
from config import process_config
from trainer import DataGenerator
from keras import backend as K
from PIL import Image
import random
from writesurface import generate
import datetime
import json

class Inference():
    '''
    def __init__(self):
        self.config = process_config('./configs.json')
        self.load_model()
    '''
    def __init__(self,config_path):
        self.initialled = False
        with open(config_path, 'r', encoding='utf-8') as config_file:
            self.config = process_config(config_path)



    def initial(self):
        if not self.initialled:
            config = self.config
            with tf.variable_scope('', reuse=tf.AUTO_REUSE):
                self.load_model()



            #self.graph = tf.get_default_graph()
            self.initialled = True



    def analyze_name(self,path):
        name = os.path.split(path)[1]
        name = os.path.splitext(name)[0]
        return name

    def load_model(self):
        start = time.time()
        self.load_cornea_model()
        print('Loading cornea segmentation model with {}s'.format(time.time()-start))
        start = time.time()
        self.load_ulcer_model()
        print('Loading ulcer segmentation model with {}s'.format(time.time()-start))

    def load_cornea_model(self):
        self.cornea_model = model_from_json(open('./model/cornea/architecture.json').read(), custom_objects={'BilinearUpsampling': BilinearUpsampling})
        self.cornea_model.load_weights('./model/cornea/best_weights.h5', by_name=True)

    def load_ulcer_model(self):
        self.ulcer_model = model_from_json(open('./model/ulcer/architecture.json').read(), custom_objects={'BilinearUpsampling': BilinearUpsampling})
        self.ulcer_model.load_weights('./model/ulcer/best_weights.h5', by_name=True)

    def cv_imread(self,filepath):
        cv_img = cv2.imdecode(np.fromfile(filepath,dtype=np.uint8),-1)
        return cv_img



    def predict(self, input_path, output_pdfpath, id_):

        output_imagepath = './output'

        report = dict()
        report['patient-id'] = str(id_)
        report['report-id'] = '{}-{}'.format(
            id_,
            datetime.date.today().strftime('%Y%m%d')
        )
        start = time.time()
        # BGR -> RGB
        print('=====================')
        print(input_path)
        print('=====================')

        self.raw =self.cv_imread(input_path)
        self.raw = self.raw[:,:,::-1]
        self.cornea = self.predict_cornea()
        self.ulcer = self.predict_ulcer()
        masked = self.mask()
        id = self.analyze_name(input_path) + '.png'
        output_imagepath = os.path.join(output_imagepath, id)
        cv2.imwrite(output_imagepath, masked.astype(np.uint8))
        print('Process {} with {}s'.format(id, time.time()-start))

        report['output_image'] = output_imagepath
        report['watermark1'] = './backup/watermark1.pdf'
        report['template1'] = './pdf/template1.pdf'
        generate(report, output_pdfpath)

        return output_imagepath,report

    def predict_cornea(self):
        # resize
        if self.raw.shape[0] != self.config.cornea_height:
            raw = cv2.resize(self.raw, (self.config.cornea_width, self.config.cornea_height), interpolation=cv2.INTER_AREA)
        # preprocess
        input = np.expand_dims(raw, axis=0)
        input = inception_preprocess(input)
        # predict
        predictions = self.cornea_model.predict(input, batch_size=1, verbose=1)
        # binarized
        probResult = np.reshape(predictions[:,:,0], (self.config.cornea_height, self.config.cornea_width, 1))
        binaryResult = ((probResult>=0.5)).astype(np.uint8)*255
        binaryResult = cv2.resize(binaryResult, (self.config.ulcer_width, self.config.ulcer_height), interpolation=cv2.INTER_AREA)
        # ellipse fitting
        ret, thresh = cv2.threshold(binaryResult, 127, 255, 0)
        _, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        _ellipse = cv2.fitEllipse(contours[0])
        ellipse = np.zeros((self.config.ulcer_height, self.config.ulcer_width, 1), dtype=np.uint8)
        cv2.ellipse(ellipse, _ellipse, 255, -1)

        return ellipse

    def predict_ulcer(self):
        # resize
        if self.raw.shape[0] != self.config.ulcer_height:
            raw = cv2.resize(self.raw, (self.config.ulcer_width, self.config.ulcer_height), interpolation=cv2.INTER_AREA)
        # FOV
        cornea = np.broadcast_to(self.cornea, (self.config.ulcer_height, self.config.ulcer_width, 3))
        raw[cornea==0] = 0
        # crop
        raw = np.reshape(raw, (1, self.config.ulcer_height, self.config.ulcer_width, 3))
        datagen = DataGenerator(config=self.config, test_data=raw)
        test_img_patches, new_height, new_width = datagen._test_data()
        # predict
        predictions = self.ulcer_model.predict(test_img_patches, batch_size=self.config.batch_size, verbose=1)
        # splice
        pred_imgs = recompone_overlap(predictions, self.config, new_height, new_width)
        pred_imgs = pred_imgs[:,0:self.config.ulcer_height,0:self.config.ulcer_width,:]

        probResult=1-pred_imgs[0,:,:,0]
        binaryResult = ((probResult>=0.5)).astype(np.uint8)*255
        binaryResult = np.reshape(binaryResult, (self.config.ulcer_height, self.config.ulcer_width, 1))

        return binaryResult

    def mask(self): 
        # resize
        origin = self.raw[:,:,::-1]
        origin = cv2.resize(origin, (self.config.ulcer_width, self.config.ulcer_height), interpolation=cv2.INTER_AREA)
        # draw a mask for a cornea
        ret, thresh = cv2.threshold(self.cornea, 127, 255, 0)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.drawContours(origin, contours, -1, (0,0,255), 3)
        # draw a mask for ulcer
        ret, thresh = cv2.threshold(self.ulcer, 127, 255, 0)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        res = cv2.drawContours(img, contours, -1, (255,0,0), 3)
        
        return res

def test():
    infer = Inference('./configs.json')
    infer.initial()
    input_path = './input/9.jpg'
    #output_path = './output'
    path = infer.predict(input_path, './test1.pdf', 562)

    print(path)

if __name__ == '__main__':
    test()

