# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 08:41:22 2022

@author: lluri
"""
import xraydb as xdb
import scipy.constants as scc
import numpy as np
def eden_to_rho(material,eden):
    # converts from electron density to mass density
    atoms = xdb.chemparse(material)
    A = 0
    Z = 0
    for atom_name in atoms.keys():
        tA = xdb.atomic_mass(atom_name)
        tZ = xdb.atomic_number(atom_name)
        A += tA*atoms[atom_name]
        Z += tZ
    rho = A*eden/scc.Avogadro/1e6/Z
    return rho
def rho_to_n(material,rho,energy):
    delta, beta, _ = xdb.xray_delta_beta(material, rho, energy)
    n = 1-delta - 1j*beta
    return n
def rho_to_rhoe(material,rho,energy):
    lam = scc.h*scc.c/scc.e/energy
    k = 2*np.pi/lam
    delta, beta, _ = xdb.xray_delta_beta(material, rho, energy)
    r0 = scc.physical_constants['classical electron radius'][0]
    rhoe = delta*k**2/2/np.pi/r0
    return rhoe
