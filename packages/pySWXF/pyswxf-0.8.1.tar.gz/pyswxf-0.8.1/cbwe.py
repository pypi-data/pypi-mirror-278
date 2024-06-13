# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 12:24:39 2019

"""
import numpy as np
def cbwe(y1,dy1,y2,dy2):
    lg = len(y1)
    y = (y1/dy1**2+y2[0:lg]/dy2[0:lg]**2)/(1/dy1**2+1/dy2[0:lg]**2)
    dy = np.sqrt(1/(1/dy1**2 + 1/dy2[0:lg]**2))
    np.append(y,y2[lg:])
    np.append(dy,dy2[lg:])
    return y, dy
def cbwe_s(y1,dy1,y2,dy2):
    # cbwe for scalers
    y = (y1/dy1**2+y2/dy2**2)/(1/dy1**2+1/dy2**2)
    dy = np.sqrt(1/(1/dy1**2 + 1/dy2**2))
    return y,dy

   
