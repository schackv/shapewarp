# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 10:33:37 2014

@author: schackv
"""

import matplotlib.pyplot as plt
import ShapeStuff.ASM as ASM
import ShapeStuff.warp as warp
import ShapeStuff.plotting as shplt
import example_data

def demo():
    """Demonstrate the shape model and warping functionality"""
    
    # Read shape data
    data = example_data.examples()
    landmarks = data.landmarks()
    print(landmarks.shape)
    
    # Plot shapes
    [shplt.plot_shape(L,'k') for L in landmarks]
    plt.show()
    
    # Active shape model (with generalized Procrustes inside)
    asm = ASM.ASM()
    asm.build(landmarks)
    
    ######## Plotting of shape model ######
    f, ax = plt.subplots(2,2)
    # Plot mean shape on top of aligned input shapes
    plt.sca(ax[0,0])
    [shplt.plot_shape(L,'k') for L in asm.AlignedShapes.T]
    shplt.plot_shape(asm.MeanShape,'r',linewidth=2.0)
    plt.title('Input shapes and mean shape')
    
    # Show covariance matrix as image
    plt.sca(ax[0,1])
    plt.imshow(asm.Covariance)
    plt.title('Covariance matrix')         
    
    # Plot the first two eigenmodes
    plt.sca(ax[1,0])
    shplt.plot_mode(asm.MeanShape,asm.PCModes[0],3)
    plt.title('Mean shape +/- 3 std of first mode')
    plt.sca(ax[1,1])
    shplt.plot_mode(asm.MeanShape,asm.PCModes[1],3)
    plt.title('Mean shape +/- 3 std of second mode')
    
    for a in ax.flatten():
        a.axis('image')
        a.invert_yaxis()
    
    plt.show()
    ######################################
    
    ######## Warping demo ################
    image = data.images[ [i.has_image() for i in data.images].index(True) ]
    W = warp.Warper(asm.MeanShape,scale=0.3)        # Warp to 0.3 of the full scale of the mean shape
    warped_image = W.warp_image(image.load(),image.landmarks())
    
    f, ax = plt.subplots(1,2)
    titles = ['Warped image','Mask']
    for idx,im in enumerate( (warped_image,W.mask)):
        plt.sca(ax[idx])
        plt.imshow(im)
        plt.axis('image')
        plt.title(titles[idx])
    plt.show()
    ######################################
    
    
    
# when executed, just run asm_demo():
if __name__ == '__main__':
    demo()