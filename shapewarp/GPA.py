# -*- coding: utf-8 -*-

""" 
Generalized Procrustes Analysis

@author: schackv
"""

import numpy as np
    

""" 
Perform the generalized Procrustes analysis using the given landmarks.
Landmarks are expected to be a numpy N x 2*p array where p is the number of landmarks
and N the number of observation. x coordinates are before y coordinates in each row.
"""
def generalized_procrustes_2d(landmarks,ctr=False):
    N, p = landmarks.shape
    k = p/2
    
    # Convert to complex numbers and center
    C = np.matrix(landmarks[:,:k] + 1j*landmarks[:,-k:]).T
    C = C - np.mean(C,axis=0)
    
    # Handle scale
    beta = np.real(np.sqrt(np.diag(C.H*C) ) )
    mbeta = np.mean(beta)  # Average scale
    C = C * np.diagflat(1/beta)
    assert(len(beta)==N)
        
    # Solve eigenvalue problem
    eigvals, eigvecs = np.linalg.eig(C*C.H)
    idx = np.argsort(-np.abs(eigvals))
    m = np.matrix(eigvecs[:,idx[0]])     # Eigenvector for largest magnitude eigenvalue
    
    # Full Procrustes fit
    f = m.H * C
    assert(f.size==N)
    C = np.multiply(C,f.conj())
    mf = np.sum(f)/N
    mf = mbeta * mf.conj()/np.abs(mf)
    
    # Align to average rotation and scale
    if ctr==True:
        mf /= np.linalg.norm(mf)
    
    m *= mf.conj()  
    C *= mf.conj()
        
    # Convert back to real values
    m = np.vstack((np.real(m),np.imag(m)))
    Xnew = np.vstack((np.real(C),np.imag(C)))

    # Covariance calculation
    X = Xnew - m    # Remove mean before covariance calculation
    S = X*X.T/N
    assert(S.shape[0]==p)
    
    return m, S, Xnew
            

    
#    def __init__(self):
#        
    
