# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 14:22:40 2014

@author: schackv
"""

import numpy as np
import scipy.spatial
from matplotlib.path import Path
import scipy.ndimage as ndimage

class Warper:

    def __init__(self, shape, scale=1):
        """ 
        Initalize a Warper with a reference shape with coordinates in the 
        numpy array 'shape'
        """
        xy = shape.copy() * scale
        self.scale = scale
        
        xy = self.shape_to_xy(xy)
            
        xy = xy - np.min(xy,axis=0)
        dt = scipy.spatial.Delaunay(xy)
        
        # Define a grid
        cols = int(np.ceil(np.max(xy[:,0])))
        rows = int(np.ceil(np.max(xy[:,1])))
        xx, yy = np.meshgrid(range(cols),range(rows))

        xy_grid = np.vstack((xx.flatten(),yy.flatten())).T        
        
        # Define a mask 
        mask = Path(xy).contains_points(xy_grid)
        self.mask = mask.reshape(xx.shape)
        xy_grid = xy_grid[mask==True,:] # Remove pts not inside mask
        
        # Calculate barycentric coordinates for all points inside mask
        simplex_ids = dt.find_simplex(xy_grid)
        bary_coords = points_to_bary(dt,simplex_ids,xy_grid)
        
        self.tri = dt.simplices
        self.warp_template = np.hstack((simplex_ids[:,np.newaxis],bary_coords))
        

    def warp_image(self, im, P):
        """Warp an image from the coordinates P in im to the mean shape associated
        with the current instance of this Warper 
        """
        P = self.shape_to_xy(P)
                
        # Transform template barycentric coordinates to im's image coordinates
        tri_x = P[self.tri[self.warp_template[:,0].astype(int),:],0]
        tri_y = P[self.tri[self.warp_template[:,0].astype(int),:],1]
        
        pt_x  = np.sum(tri_x * self.warp_template[:,1:],axis=1)
        pt_y  = np.sum(tri_y * self.warp_template[:,1:],axis=1)
        cartesian_xy = np.hstack((pt_x[:,np.newaxis], pt_y[:,np.newaxis]))
        
        # Interpolate image values at these coordinates
        xx, yy = np.meshgrid(range(im.shape[0]),range(im.shape[1]))
        warped_channels = []
        for d in range(im.shape[2]):
            values = ndimage.map_coordinates(im[:,:,d].astype(float)/np.iinfo(im.dtype).max,np.fliplr(cartesian_xy).T,cval=np.nan)
            values[values>1]=1
            values[values<0]=0
            channel = np.empty(self.mask.shape)*np.NaN
            channel[self.mask==True]=values
            warped_channels.append(channel)     # Build image
            
        warped_image = np.dstack(warped_channels)
        return warped_image
        

    def shape_to_xy(self,xy):
        if not (xy.ndim==2) & (xy.shape[1]==2):
            k = len(xy)/2
            xy = np.hstack( (xy[:k],xy[-k:]) )
        return xy


def MeanShapeTriangulation(self):
    """Get the interior triangulation of the mean shape

    Returns    xy, tri
    where xy are the coordinates of the points
    and tri is a p x 3 array of indices into xy defining the
    interior triangulation of xy
    """
    x = self.MeanShape[:self.k]
    y = self.MeanShape[-self.k:]
    xy = np.hstack((x,y))
    dt = scipy.spatial.Delaunay(xy)
    
    tri = simplices_in_polygon(xy,dt.simplices)
    
    return xy, tri
    #        import matplotlib.pyplot as plt
    #        plt.triplot(xy[:,0],xy[:,1],dt.simplices.copy())
    #        plt.triplot(xy[:,0],xy[:,1],tri,'r-',hold=True)
    #        plt.axis('image')
    #        plt.show()
    #        plt.show()
    
    
    
def simplices_in_polygon(poly_xy,simplices):
    """Given a list of simplices indexing into poly, return the simplices
    inside the polygon.
    poly_xy should be a N x 2 numpy array
    """    
    from matplotlib.path import Path
    
    simp_means = [np.mean(poly_xy[s,:],axis=0) for s in simplices]
    is_inside = Path(poly_xy).contains_points(simp_means)
    interior_simplices = simplices[is_inside,:]
    return interior_simplices


def points_to_bary(tri,tetrahedra,targets):
    """Convert xy coordinates to barycentric coordinates within the triangle in which
    it resides
    """        
    X = tri.transform[tetrahedra,:2]
    Y = targets - tri.transform[tetrahedra,2]
    b = np.einsum('ijk,ik->ij', X, Y)
    bcoords = np.c_[b, 1 - b.sum(axis=1)]
    return bcoords