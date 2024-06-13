# -*- coding: utf-8 -*-
"""
multilayer_fluor_fit

file to fit fluorescence from bilayer on top of multilayer

Created on Tue Mar 14 13:50:10 2023
Code to generate multilayer sample simulation


@author: lluri
"""
import scipy.constants as scc
from pySWXF.refl_funs import reflection_matrix, standing_wave 
from pySWXF.xray_utils import eden_to_rho
from lmfit import Model
from scipy.special import erf
import numpy as np
import time
import xraydb as xdb
import scipy.constants as scc
import scipy.signal as scs 
#%% Imports and configuration section
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:40:26 2023

@author: th0lxl1
"""
#%%
def make_bilayer_model():
    Head = 'CH2'
    Tail = 'CH2'
    Methyl = 'CH2'
    rho_head = eden_to_rho(Head, 486/scc.nano**3)
    rho_tail = eden_to_rho(Tail, 323/scc.nano**3)
    bilayer_layers = [(Head,rho_head,7,3.17),            # Water                                                                          
              (Tail,rho_tail,17.23,3.17),       # Distal Acyl Chain
              (Methyl,0,2,3.17),                # Methyl Overlap Region
              (Tail,rho_tail,17.63,2.6),         # Proximal Acyl Chain
              (Head,rho_head,7,2.6)]           # Proximal Head Group
    return bilayer_layers
#%%

def sample_sim(G,D,sig_Mo,sig_Si,overlay,
               sig_Si_top,water,bilayer,
               D_Ti=108.2,sig_Ti=3.0,D_SiO2=10,sig_SiO2=3,D_SiO2_Bot=30,
               sig_SiO2_Bot=3,sig_Si_Bot=3, **kwargs):
    if water:
        layers = [('H2O',1.0,0,0)]  
        if bilayer:
            layers += make_bilayer_model()
    else:
        layers = [('N2',1.225e-3,0,0)]
    layers += [('SiO2',eden_to_rho('SiO',692e27),D_SiO2,sig_SiO2),
    ('SiO',eden_to_rho('SiO',560e27),1.5,1.5,),
    ('Si',xdb.atomic_density('Si'),overlay,sig_Si_top)]
    nstack = 20
    rMo = xdb.atomic_density('Mo')
    rSi = xdb.atomic_density('Si')
    for i in range(nstack):
        layers += [('Mo',rMo,D*G,sig_Mo),
                       ('Si',rSi,D*(1-G),sig_Si)]
    layers += [('Ti',xdb.atomic_density('Ti'),D_Ti,sig_Ti), 
                   ('SiO2',2.2,D_SiO2_Bot,sig_SiO2_Bot),
                   ('Si',xdb.atomic_density('Si'),0,sig_Si_Bot)]
    return layers

def multilayer_ref_Ti_orig(theta,I0,thoff,
                   bg,foot,G,D,sig_Mo,sig_Si,overlay,
                   sig_Si_top,water,
                   Energy,bilayer,res,D_Ti,sig_Ti,D_SiO2,sig_SiO2,
                   D_SiO2_Bot,sig_SiO2_Bot,sig_Si_Bot):
    if res == 0:
        norm = 1
        nspan = 1
        dth_span = [0]
        mul = [1]
        # print('multilayer_ref_Ti: bypassing resolution')
    else:
        nspan = 8
        dth_span = np.linspace(-2*res,2*res,nspan)
        mul = np.exp(-dth_span**2/2/res**2)
        norm = np.sum(mul)
        # print('resolution = {0:7.2f} nspan = {1:d}'.format(res,nspan))
    vals = locals()
    tic = time.time()
    result_list = []
    for i in range(nspan):
        dth = vals['dth_span'][i]
        alpha = (vals['theta'] - vals['thoff'] + dth)*scc.degree
        layers = sample_sim(G,D,sig_Mo,
                sig_Si,overlay,
                sig_Si_top,water,bilayer,
                D_Ti = D_Ti, sig_Ti = sig_Ti,
                D_SiO2 = D_SiO2,sig_SiO2=sig_SiO2,
                D_SiO2_Bot = D_SiO2_Bot, sig_SiO2_Bot = sig_SiO2_Bot,
                sig_Si_Bot = sig_Si_Bot)
        t,r,kz,_,_,_,zm = reflection_matrix(
            alpha,Energy,layers)
        Intensity = np.abs(r[:,0])**2
        frange = theta<foot
        Intensity[frange] *= theta[frange]/foot
        tres = Intensity*mul[i]/norm
        result_list.append(tres)       
    toc = time.time()
    #print(f'{toc-tic:2.1f} ',end='')
    return(I0*np.sum(np.array(result_list),0)+bg)

import numpy as np
import scipy.constants as scc
import scipy.signal as scs

def multilayer_ref_Ti(
    theta: np.ndarray,
    I0: float,
    thoff: float,
    bg: float,
    foot: float,
    G: float,
    D: float,
    sig_Mo: float,
    sig_Si: float,
    overlay: float,
    sig_Si_top: float,
    water: bool,
    Energy: float,
    bilayer: bool,
    res: float,
    D_Ti: float,
    sig_Ti: float,
    D_SiO2: float,
    sig_SiO2: float,
    D_SiO2_Bot: float,
    sig_SiO2_Bot: float,
    sig_Si_Bot: float
) -> np.ndarray:
    theta = np.array(theta)
    theta_off = theta - thoff
    
    # Recast data on uniform grid
    dth = np.min(np.diff(theta_off))
    npt = int((theta_off[-1] - theta_off[0]) / dth)
    thnew = np.linspace(theta_off[0], theta_off[-1], npt)
    
    # Simulate sample layers
    layers = sample_sim(G, D, sig_Mo, sig_Si, overlay, sig_Si_top, water, bilayer,
                        D_Ti=D_Ti, sig_Ti=sig_Ti, D_SiO2=D_SiO2, sig_SiO2=sig_SiO2,
                        D_SiO2_Bot=D_SiO2_Bot, sig_SiO2_Bot=sig_SiO2_Bot, sig_Si_Bot=sig_Si_Bot)
    alpha = thnew * scc.degree
    
    # Compute reflection matrix
    _, r, _, _, _, _, _ = reflection_matrix(alpha, Energy, layers)
    Intensity = np.abs(r[:, 0])**2
    
    # Correct for footprint
    frange = thnew < foot
    Intensity[frange] *= thnew[frange] / foot
    
    # Include resolution using convolution
    if res > 0:
        signal = np.concatenate([Intensity[::-1], Intensity, Intensity[::-1]])
        sig = res / dth
        nwin = 8 * int(sig) + 16
        win = np.exp(-0.5 * (np.arange(-nwin // 2, nwin // 2 + 1) / sig)**2)
        win /= win.sum()
        Intensity = scs.convolve(signal, win, mode='same')[npt:2*npt]
    
    # Re-interpolate data back to old angles
    Iout = np.interp(theta_off, thnew, Intensity)
    return I0 * Iout + bg


def multilayer_fluor(theta,I0,thoff,
                   bg,foot,G,D,sig_Mo,sig_Si,overlay,
                   sig_Si_top,sep,hoff,res,
                   Energy):
    water = True
    bilayer = True 
    D_bilayer = 50.86
    if res == 0:
        norm = 1
        nspan = 1
        dth_span = [0]
        mul = [1]
    else:
        nspan = 4
        dth_span = np.linspace(-1.5*res,1.5*res,nspan)
        mul = np.exp(-dth_span**2/2/res**2)
        norm = np.sum(mul)
    for i in range(nspan): 
        dth = dth_span[i]
        alpha = (theta-thoff+dth)*scc.degree 
        layers = sample_sim(G,D,sig_Mo,sig_Si,overlay,
                sig_Si_top,water,bilayer)
        t,r,kz,_,_,_,zm = reflection_matrix(alpha,Energy,layers)
        heights = np.array([sep/2,-sep/2])+hoff - D_bilayer/2
        I,E = standing_wave(heights*scc.angstrom,t,r,kz,zm)
        I = np.average(I,0)
        I /= (theta-thoff)
        I *= np.mean(theta)*I0
        if i==0:
            Itot = I*mul[i]/norm
        else:
            Itot += I*mul[i]/norm 
    Itot[(theta-thoff)<foot] *= (theta-thoff)[(theta-thoff)<foot]/foot
    Itot += bg
    print('.',end='')
    return Itot


multilayer_model_Ti = Model(multilayer_ref_Ti, independent_vars=['theta','Energy','water','bilayer'])
fluor_model = Model(multilayer_fluor, independent_vars=['theta','Energy'])

xdb.add_material('silicon_carbide', 'Si1C1', 3.21, categories=None)
SiC = xdb.find_material('silicon_carbide')
W = xdb.find_material('W')
Cr = xdb.find_material('Cr')
Si = xdb.find_material('Si')
H2O = xdb.find_material('water')
air = xdb.find_material('air')
xdb.add_material('silicon_carbide', 'Si1C1', 3.21, categories=None)
kapton = xdb.find_material('kapton')


def sample_sim_new(d_overlay, sig_overlay, G,D,sig_W,sig_SiC,
                   D_Cr, sig_Cr, sig_Si_Bot, water=False, bilayer = True, new_cell = True):
    if new_cell:
        layers = [(air.formula,air.density,0,0)]
        d_kapton = 1000 # not correct, but big
        d_water = 1000
        sig_kapton = 10 # just a random guess
        layers += [(kapton.formula, kapton.density,d_kapton, sig_kapton)]
        layers += [(H2O.formula, H2O.density,d_water, sig_kapton)]
        if bilayer:
            layers += make_bilayer_model()
    elif water:
        layers = [(H2O.formula,H2O.density,0,0)]
        if bilayer:
            layers += make_bilayer_model()
    else:
        layers = [(air.formula,air.density,0,0)]

    # now put in cap layer
    layers += [(SiC.formula,SiC.density,d_overlay,sig_overlay)]
    # put in multilayer stack
    nstack = 15
    for i in range(nstack):
        layers += [(W.formula,W.density,D*G,sig_W)]
        layers += [(SiC.formula,SiC.density,D*(1-G),sig_SiC)]
    # add chrome binding layer
    layers += [(Cr.formula,Cr.density,D_Cr,sig_Cr)]
    # add substrate
    layers += [(Si.formula,Si.density,0,sig_Si_Bot)]
    return layers


import numpy as np
import scipy.constants as scc
import scipy.signal as scs



def multilayer_ref_new(
    theta: np.ndarray,
    I0: float,
    thoff: float,
    bg: float,
    foot: float,
    G: float,
    D: float,
    d_overlay: float,
    sig_overlay: float,
    sig_W: float,
    sig_SiC: float,
    Energy: float,
    res: float,
    D_Cr: float,
    sig_Cr: float,
    sig_Si_Bot: float,
    water: bool = True,
    bilayer: bool = True,
    new_cell: bool = True
) -> np.ndarray:
    theta = np.array(theta)
    theta_off = theta - thoff
    
    # Recast data on uniform grid
    dth = np.min(np.diff(theta_off))
    npt = int((theta_off[-1] - theta_off[0]) / dth)
    thnew = np.linspace(theta_off[0], theta_off[-1], npt)
    
    # Simulate sample layers
    layers = sample_sim_new(d_overlay, sig_overlay, G, D, sig_W, sig_SiC, D_Cr, sig_Cr, sig_Si_Bot, water=water, bilayer=bilayer, new_cell=new_cell)
    alpha = thnew * scc.degree
    
    # Compute reflection matrix
    _, r, _, _, _, _, _ = reflection_matrix(alpha, Energy, layers)
    Intensity = np.abs(r[:, 0])**2
    
    # Correct for footprint
    frange = thnew < foot
    Intensity[frange] *= thnew[frange] / foot
    
    # Include resolution
    if res > 0:
        signal = np.concatenate([Intensity[::-1], Intensity, Intensity[::-1]])
        sig = res / dth
        nwin = 8 * int(sig) + 16
        win = np.exp(-0.5 * (np.arange(-nwin // 2, nwin // 2 + 1) / sig)**2)
        win /= win.sum()
        Intensity = scs.convolve(signal, win, mode='same')[npt:2*npt]
    
    # Re-interpolate data back to old angles
    Iout = np.interp(theta_off, thnew, Intensity)
    return I0 * Iout + bg


multilayer_ref_new_model = Model(multilayer_ref_new,
    independent_vars = ['theta','Energy','water','bilayer','new_cell'])
  

    