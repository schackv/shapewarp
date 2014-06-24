# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:18:20 2014

@author: schackv
"""

from . import GPA
import numpy as np


class ASM:
    
    """
    Build an active shape model from the landmarks given.
    Landmarks are expected to be a numpy N x 2*p array 
    where p is the number of landmarks.
    """
    def build(self,landmarks):
                
        # Do Generalized Procrustes analysis
        mu, S, Xnew = GPA.generalized_procrustes_2d(landmarks)
       
        self.k = len(mu)/2      # Number of points
        self.MeanShape = np.array(mu)
        self.Covariance = np.array(S)
        self.AlignedShapes = np.array(Xnew)
        
        # PCA on shapes
        eigvals, eigvecs = np.linalg.eig(S)
        eigvals = np.abs(eigvals)
        eigvecs = np.abs(eigvecs)
        idx = np.argsort(-eigvals)   # Ensure descending sort
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:,idx]
        
        self.Scores = np.array(Xnew.T * eigvecs)
        self.MeanScores = np.array(mu.T * eigvecs)
        self.VarianceExplained = np.array(np.cumsum(eigvals/np.sum(eigvals)))
        
        # Build modes for up to 95% variance
        npcs,_ = index_of_true(self.VarianceExplained>0.95)
        npcs += 1

        M = []
        for i in range(0,npcs-1):
            M.append(np.array(np.sqrt(eigvals[i]) * eigvecs[:,i]))
        self.PCModes = M
        
    


        
def index_of_true(arr):
    for index, item in enumerate(arr):
        if item == True:
            return index, item
            

    