# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 09:47:57 2018

@author: th0lxl1
"""

from numpy import sqrt, tile, transpose,  sin, exp, zeros
from numpy import linspace
from numpy import sum as nsum
from numpy import abs as nabs
import xraydb as xdb
import numpy as np
import scipy.constants as scc


def mlayer_rough(alpha,k0,n_r,zm0,sig):        
    """        
    mlayer(alpha,n,z,sig)
    Updated LBL May 30, 2022 
    from M. Tolan
    X-Ray Scattering from Soft-Matter Thin Films
    Chapter 2, p12 and following

    multi-layer parratt model with roughness
    
    We model the surface as a number of interfaces.  To  avoid confusion, 
    the electron densities are put in as electron density differences.  
    
    Variables:
    alpha --- The incident angle in radians
    k0    --- The magnitude of the wavevector of the light
    n     --- The  indices of refraction 
    z     --- The positions of the interfaces 
    sig   --- The roughness of each interface

    Translated to python August 20, 2018, Laurence Lurio 
    
    Note that R[:,0] is the top layer reflectivity and that T[:,0]
    is meaningless (just equal to 1) T[:,1] is the transmission from
    the first layer to the second layer
    
    O is the top interface
    
    Note index of refraction must be 1 - delta + i beta
    
    Note: T and R stand for the electric fields, not the
    coefficients.  Their form contains the z dependence, e.g
    R exp(+ikz)  and T exp(-ikz), with z a negative number going
    into the material
    """
    la = alpha.shape[0]
    ln = n_r.shape[0] # ln is the number of layers
    # need to subtract off the first index, as Tolan formalism assumes 
    # you are coming in from vacuum
    nr2d = n_r**2-n_r[0]**2
    nr2d = tile(nr2d,(la,1))
    nr2d = nr2d.astype(complex)
    zm = tile(zm0,(la,1))
    sig = tile(sig,(la,1))
    alpha = transpose(tile(alpha,(ln,1)))
    R = zeros((la,ln),dtype=complex)
    T = zeros((la,ln),dtype=complex)
    X = zeros((la,ln),dtype=complex)
    kz=k0*sqrt(sin(alpha)**2 + nr2d)
    rr=(kz[:,0:-1]-kz[:,1:])/(kz[:,0:-1]+kz[:,1:]) # eq. 2.17
    # Here is where the roughness factors in
    rr=rr*exp(-nabs(2*kz[:,0:-1]*kz[:,1:]*sig*sig))
    # tp=tp*exp(nabs((kz[:,0:-1]-kz[:,1:])**2*sig*sig/2))
    tp = 1-rr
    # append 0 and 1 for the reflection and transmission coefficient of the last layer
    
    for jl in range(ln-2,-1,-1):
        # since rr only describes the interfaces, not the layers,
        # the number of rr's is 1 less than the number of kz's
        X[:,jl]=rr[:,jl]+X[:,jl+1]*exp(2j*kz[:,jl+1]*zm[:,jl])
        X[:,jl]=X[:,jl]*exp(-2j*kz[:,jl]*zm[:,jl])
        X[:,jl]=X[:,jl]/(1+rr[:,jl]*X[:,jl+1]*exp(2j*kz[:,jl+1]*zm[:,jl]))
    T[:,0]=1.0
    R[:,0]=X[:,0]
    for jl in range(0,ln-1):
        R[:,jl+1]=(R[:,jl]*exp(-1j*(kz[:,jl+1]-kz[:,jl])*zm[:,jl])
                   -T[:,jl]*rr[:,jl]*exp(-1j*(kz[:,jl+1]+kz[:,jl])*zm[:,jl]))
        R[:,jl+1]=R[:,jl+1]/tp[:,jl]
        T[:,jl+1]=(T[:,jl]*exp(1j*(kz[:,jl+1]-kz[:,jl])*zm[:,jl])
                   -R[:,jl]*rr[:,jl]*exp(1j*(kz[:,jl+1]+kz[:,jl])*zm[:,jl]))
        T[:,jl+1]=T[:,jl+1]/tp[:,jl]
    return([T,R,kz,X,rr,tp,zm0])

def mlayer_conv(alpha,k0,n,z,sig,res,npt):
    dX = linspace(-res, res, num=npt)
    yout=[]
    mu=res/2.35
    norm = nsum(exp(-(dX/mu)**2))
    yout=0
    for delx in dX:
        _,R,_,_,_,_ = mlayer_rough(abs(alpha+delx),k0,n,z,sig)
        yout = yout+exp(-(delx/mu)**2)*abs(R[:,0])**2/norm
    return(yout)

def reflection_matrix(alpha,E,layers):
    '''
    reflection_matrix(alpha,E,layers)

    Parameters
    ----------
    alpha : numpy array float 
        incident angles (in radians).
    E : float
        incident energy (eV).
    layers : array of layers 
        each layer has a material (e.g. 'H2O') and density (g/cc) a thickness
        and a roughness.  
    The sig and thickness for the zeroth layer are thrown away as they have no meaning.

    Returns
    ----------
    T : numpy array (n_alpha, n_layer)
        Transmission matrix returned by mlayer or mlayer_rough
    R : numpy array (n_alpha, n_layer)
        Reflectivity matrix returned by mlayer or mlayer_rough.
    kz : numpy array (n_alpha, n_layer)
        wavevector matrix returned by mlayer or mlayer_rough. (units of inv meters)
    '''   
    k0 = 2*np.pi*E*scc.e/scc.h/scc.c
    nl  = len(layers)
    n_r = np.zeros(nl,complex)
    h_i = np.zeros(nl-1)
    sig_i = np.zeros(nl-1)
    z = 0
    for  i, (material, density, thick, rough)   in enumerate(layers):
        delta,beta,att = xdb.xray_delta_beta(material,density,E)
        n_r[i] = 1-delta+1j*beta 
        if i>0:
            h_i[i-1] = z
            z -= thick*scc.angstrom;
            sig_i[i-1] = rough*scc.angstrom
    T,R,kz,X,rr,tp,zd  = mlayer_rough(alpha,k0,n_r,h_i,sig_i)
    return T,R,kz,X,rr,tp,zd


def standing_wave(z,T,R,kz,h_i):
    '''
    standing_wave(T,R,kz,z)
    
    Function to calculate the electric field standing wave 
    
    Parameters
    ----------
    z : numpy array (1d)
        heights relative to top surface at which to calculate
            the standing wave.
    T : numpy array (n_alpha, n_layer)
        Transmission matrix returned by mlayer or mlayer_rough
    R : numpy array (n_alpha, n_layer)
        Reflectivity matrix returned by mlayer or mlayer_rough.
    kz : numpy array (n_alpha, n_layer)
        wavevector matrix returned by mlayer or mlayer_rough.
    h_i : numpy array (n_layer-1)
        array of interface height positions

            
    Here n_alpha is the number of angles input to mlayer and n_layer the
    number of layers input to mlayer.

    Returns
    -------
    I : numpy array (n_z,n_alpha)
        Standing wave intensity.
    E : numpy array (n_z,n_alpha)
        Electric field intensity.

    '''
    n_alpha,n_layer = np.shape(T)
    n_z = len(z)
    E = np.zeros((n_z,n_alpha))+0j   
    for i in range(n_layer):
        if i == 0:
            wz = z >= h_i[i]
        elif i == n_layer-1:
            wz = z < h_i[i-1]
        else :
            wz = (z < h_i[i-1])*(z >= h_i[i])
        # only do calculation for subset of z values
        tz = z[wz]
        n_tz = len(tz)
        T_full = np.broadcast_to(T[:,i],(n_tz,n_alpha))
        R_full = np.broadcast_to(R[:,i],(n_tz,n_alpha))
        kz_full = np.broadcast_to(kz[:,i],(n_tz,n_alpha))
        z_full = np.transpose(np.broadcast_to(tz,(n_alpha,n_tz)),(1,0))
        
        E[wz,:] = np.exp(-1j*kz_full*z_full)*T_full
        E[wz,:] += np.exp(1j*kz_full*z_full)*R_full
    # expand all the arrays to the same size for multiplying   
    I = np.abs(E)**2
    return I,E


    
    
