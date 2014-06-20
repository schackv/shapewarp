# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 10:42:03 2014

@author: schackv
"""
import os
import glob
import numpy as np
from scipy.misc import imread

DATA_DIR = os.path.join('.','data')
PATTERN = '*.csv'

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


""" A not so elegant class representing example image with landmark data"""
class image:

        
    def __init__(self,filename):
        self.image_filename = filename.replace('landmarks','image').replace('.csv','.JPG')
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
        return np.loadtxt(self.annotation_filename)
        
        
    def has_image(self):
        return os.path.exists(self.image_filename)