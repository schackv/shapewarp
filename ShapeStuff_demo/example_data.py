# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 10:42:03 2014

@author: jsve
"""
import os
import glob
import scipy.io
import numpy as np
from scipy.misc import imread

DATA_DIR = os.path.join('.','data')
PATTERN = '*.mat'

class examples:
    """ Traverse the data examples and return a list of image objects"""
    def __init__(self):
        files = glob.glob(os.path.join(DATA_DIR,PATTERN))
        
        images = []
        for file in files:
            images.append(image(file))
        self.images = images
    
    """Return all landmarks as numpy array"""
    def landmarks(self):
        landmarks = []
        for f in self.images:
            L = f.landmarks()
            landmarks.append(np.hstack((L[:,0],L[:,1])))
        landmarks = np.vstack(landmarks)
        return landmarks

class image:

    
    def __init__(self,filename):
        self.image_filename = filename.replace('.mat','')
        self.annotation_filename = filename
    
    """
    Read an image from disk
    """
    def load(self):
        im = imread(self.image_filename)
        return im
    
    """
    Read landmarks
    """
    def landmarks(self):
        mat = scipy.io.loadmat(self.annotation_filename)
        return mat['P']
        
    def has_image(self):
        return os.path.exists(self.image_filename)