#!/usr/bin/env python

#########################################################################
#file name:foreground_extraction.py
#file description:this file will include some foreground extraction function
#                 which will have the same format of input a image and return
#                 a mask image
#author:joneww
#start date:20170823
#########################################################################

import numpy as np
from skimage import morphology,color,measure,io
from scipy.misc import imsave,imread
from scipy import ndimage as nd
import log
import logging

logger = logging.getLogger("lib_logger")
#########################################################################
#func name:fground_ext_a
#func description:this foreground extraction use xyz color space and use
#                 threshold in z,then use fill holes and remove small hole
#date:20170823
#########################################################################
def fground_ext_a(image):
    '''

    :param image:input orig image
    :return: output mask image
    '''
    #change color space
    xyz_img_dat = color.rgb2xyz(image)

    #use threshold
    mask = (xyz_img_dat[:,:,2] < 0.9)
    mask = mask.astype(np.int32)

    #adjust
    filled_image = nd.morphology.binary_fill_holes(mask)
    filled_image_re = morphology.remove_small_objects(filled_image, min_size=50,connectivity=1)


    return filled_image_re
