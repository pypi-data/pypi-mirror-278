# Model for gold fluorescence
from lmfit import Model, models, create_params, Parameters
from matplotlib import pyplot as plt
import numpy as np
import scipy.constants as scc
import importlib.resources
from lmfit import Parameters
import xraydb as xdb
from pySWXF import fluor_fit, refl_funs
from pySWXF.fluor_fit import multilayer_ref_new_model, multilayer_model_Ti
from pySWXF import spec_utils, AuI_funs
import re
import pandas as pd
from scipy.interpolate import RectBivariateSpline
from typing import Dict, Any, List, Tuple, Optional
import sys
import logging

logger = logging.getLogger(__name__)


g1 = models.GaussianModel(prefix='g1')
g2 = models.GaussianModel(prefix='g2')
q1 = models.QuadraticModel() 
peak_model = g1+g2+q1

# code to fit reflectivity and find offset

MULTILAYER_FIT_NEW = 'NM_clean_NIU_NOKW_Mar26_24_fit4.json'
MULTILAYER_FIT_OLD = 'niu_multilayer_fit_params_3_LBL.json'

def water_refract(th,Beam_Energy):
        alphac_water = np.sqrt(2*xdb.xray_delta_beta('H2O',1.00,Beam_Energy)[0])
        thc_water = alphac_water/scc.degree
        return np.sqrt(th**2  - thc_water**2)


def get_params(fitflag):
    if fitflag == 'NN':
        parfilename = MULTILAYER_FIT_NEW
    elif fitflag == 'OO':
        parfilename = MULTILAYER_FIT_OLD
    elif fitflag == 'NO':
        parfilename = MULTILAYER_FIT_OLD
    else:
        print(f'get_params Not configured for flag {fitflag}')
        sys.exit()
    with importlib.resources.open_text('pySWXF', parfilename) as f:
        params = Parameters()
        params.load(f)
    return(params)

def get_offset_fit(th, I, dI, dinfo, scanno,  varylist = None, startlist = None, showfit=True):
    """
    Fit the offset in the reflection data for different experimental setups.

    Parameters:
    -----------
    th : array-like
        The angular positions of the measurements.
    I : array-like
        The measured reflected intensity.
    dI : array-like
        The uncertainties in the measured intensities (not used in the function, but included for completeness).
    showfit : bool, optional
        Whether to display the fit plot. Default is True.
    verbose : bool, optional
        Whether to print detailed information during execution. Default is True.

    Returns:
    --------
    thoff : float
        The angular offset resulting from the fit.
    result : lmfit.model.ModelResult
        The result of the fit, containing the best-fit parameters and statistics.
    """
    
    params = get_params(dinfo['fitflag'])
    
    if dinfo['fitflag'] == 'NN':
        logger.info(f'Using flag {dinfo["fitflag"]}: New cell, New multilayer')
        th_refrac = AuI_funs.water_refract(th, Beam_Energy)
        fitfun = AuI_funs.multilayer_ref_new_model
    elif dinfo['fitflag'] == 'OO':
        logger.info(f'Using flag {dinfo["fitflag"]}: Old cell, Old multilayer')
        logger.info('Side entry sample cell: No refraction correction.')
        th_refrac = th
        fitfun = AuI_funs.multilayer_model_Ti
    elif dinfo['fitflag'] == 'NO':
        logger.info(f'Using flag {dinfo["fitflag"]}: New cell, Old multilayer')
        logger.info('Top entry sample cell: Using refraction correction.')
        th_refrac = AuI_funs.water_refract(th, Beam_Energy)
        fitfun = AuI_funs.multilayer_model_Ti
    else:
        logger.info(f'Not configured for flag {dinfo["fitflag"]}')
        sys.exit()
    
    for key in params.keys():
        params[key].vary = False

    params['I0'].vary = True
    params['I0'].max = 1e9
    params['I0'].min = 100
    params['I0'].value = np.max(I) * 3.5
    params['thoff'].vary = True
    params['thoff'].min = -0.1
    params['thoff'].max = 0.1
    params['res'].value = 0.001

    if varylist is not None:
        for item in varylist:
            params[item].vary = True
    if startlist is not None:
        for item in startlist:
            params[item[0]].value = item[1]
    logger.info('Fitting amplitude and offset')

    if (dinfo['fitflag'] == 'NN'):
        presim = fitfun.eval(params=params, theta=th_refrac, 
                            Energy=dinfo['Energy'], water=True,
                            bilayer=True, new_cell=False)
    elif (dinfo['fitflag'] == 'NO') or (dinfo['fitflag'] == 'OO'):
        presim = fitfun.eval(params=params, theta=th_refrac, 
                            Energy=dinfo['Energy'], water=True,
                            bilayer=True)
    cen_sim = np.sum(presim * th) / np.sum(presim)
    cen_dat = np.sum(I * th) / np.sum(I)
    params['thoff'].value = cen_dat - cen_sim

    if (dinfo['fitflag'] == 'NN'):
        result = fitfun.fit(I, theta=th_refrac, params=params, 
                        Energy=dinfo['Energy'], water=True, bilayer=True,
                        new_cell=False, weights=I * 0 + 1)
    elif (dinfo['fitflag'] == 'NO') or (dinfo['fitflag'] == 'OO'):
        result = fitfun.fit(I, theta=th_refrac, params=params,Energy=dinfo['Energy'], water=True, bilayer=True, weights=I * 0 + 1)
    thoff = result.params['thoff'].value
    
    th_peak = th[np.argmax(I)]
    
    if showfit:    
        ysim = result.eval(theta=th_refrac, Energy=dinfo['Energy'],
                           water=True, bilayer=True, new_cell=False)
        plt.plot(th, I, label='data')
        plt.plot(th, ysim, '-k', label='fit')
        plt.locator_params(axis='x', nbins=20)
        plt.grid()
        plt.xlabel('th (deg)')
        plt.ylabel('Reflected Intensity')
        plt.title(f'{dinfo["spec_filename_stub"]:s} scan {scanno:d}')
        plt.legend()
        logger.info(f'Angular offset = {thoff:.3f}') 
    return thoff, th_peak, result

def setup_fit(dinfo,mca_sum,debug=False):
    """
    Set up the fitting function and initial parameters based on the fluorophore.

    Parameters:
    - dinfo (dict): Dictionary containing experimental information.

    Returns:
    - fit_fun (Model): Combined lmfit model.
    - pars (Parameters): Initial parameters for the model.
    - data_range (array-like): Range of data to fit.
    - amplitude_names (list): List of amplitude parameter names.
    """
    if (dinfo['fluorophore'] == 'Br') and  (dinfo['run_date'] == 'Nov23'):
        print('setup_fit November Br data ') if debug else None
        return setup_fit_br_nov23(dinfo,mca_sum)
    elif (dinfo['fluorophore'] == 'gold') and  (dinfo['run_date'] == 'Nov23'):
        print('setup_fit November gold data ') if debug else None
        return setup_fit_gold(dinfo,mca_sum)
    elif (dinfo['fluorophore'] == 'Br') and (dinfo['run_date'] == 'Feb24'):
        print('setup_fit February  Br data ') if debug else None
        return setup_fit_br_feb24(dinfo,mca_sum)
    elif (dinfo['fluorophore'] == 'Br') and (dinfo['run_date'] == 'Mar23'):
        print('setup_fit March  Br data ') if debug else None
        return setup_fit_br_mar23(dinfo,mca_sum) 
    elif (dinfo['fluorophore'] == 'gold') and (dinfo['run_date'] == 'Mar23'):
        print('setup_fit March gold data ') if debug else None
        return setup_fit_gold_Mar23(dinfo,mca_sum)

def setup_fit_br_nov23(dinfo,mca_sum):
    quad_mod = models.QuadraticModel()
    gaus_mod = models.GaussianModel()
    fit_fun = quad_mod + gaus_mod
    pars = Parameters()
    pars.add('amplitude', value=150000, min=0)
    pars.add('center', value=13400)
    pars.add('sigma', value=115, vary=False)
    pars.add('a', value=0)
    pars.add('b', value=0)
    pars.add('c', value=5000)
    data_range = (dinfo['E'] > 13359 - 756.3) & (dinfo['E'] < 13359 + 302.6)
    amplitude_names = ["amplitude"]
    return fit_fun, pars, data_range, amplitude_names

def setup_fit_gold(dinfo,mca_sum):
    g1 = models.GaussianModel(prefix='g1_')
    g2 = models.GaussianModel(prefix='g2_')
    q1 = models.QuadraticModel()
    fit_fun = g1 + g2 + q1
    pars = Parameters()
    pars.add('g1_center', value=13400, vary=False)
    pars.add('g2_center', value=13771, vary=False)
    pars.add('g1_sigma', value=114.8, vary=False)
    pars.add('g2_sigma', value=114.8, vary=False)
    pars.add('g1_amplitude', value=2e5)
    pars.add('g2_amplitude', value=4e4)
    pars.add('a', value=0)
    pars.add('b', value=-7.5)
    pars.add('c', value=5000)
    data_range = (dinfo['E'] > 13000) & (dinfo['E'] < 14100)
    amplitude_names = ["g1_amplitude", "g2_amplitude"]
    return fit_fun, pars, data_range, amplitude_names

def setup_fit_gold_Mar23(dinfo,mca_sum):
    g1 = models.GaussianModel(prefix='g1_')
    g2 = models.GaussianModel(prefix='g2_')
    q1 = models.QuadraticModel()
    fit_fun = g1 + g2 + q1
    pars = Parameters()
    pars.add('g1_center', value=9713, vary=True)
    pars.add('g2_center', value=11443, vary=True)
    pars.add('g1_sigma', value=114.8, vary=True)
    pars.add('g2_sigma', value=114.8, vary=True)
    pars.add('g1_amplitude', value=2e5)
    pars.add('g2_amplitude', value=2e5)
    pars.add('a', value=0)
    pars.add('b', value=-7.5)
    pars.add('c', value=5000)
    data_range = (dinfo['E'] > 9300) & (dinfo['E'] < 12500)
    amplitude_names = ["g1_amplitude", "g2_amplitude"]
    return fit_fun, pars, data_range, amplitude_names

def setup_fit_br_feb24(dinfo,mca_sum):
    data_range = (dinfo['E'] > 11000) & (dinfo['E'] < 12500)
    mx = np.max(mca_sum[data_range])
    RR = mx/300
    g1 = models.GaussianModel(prefix='g1_')
    g2 = models.GaussianModel(prefix='g2_')
    q1 = models.QuadraticModel()
    fit_fun = g1 + g2 + q1
    pars = Parameters()
    pars.add('g1_center', value=11920, vary=True)
    pars.add('g2_center', value=11490, vary=True)
    pars.add('g1_sigma', value=114.8, vary=False)
    pars.add('g2_sigma', value=114.8, vary=False)
    pars.add('g1_amplitude', value=3876*RR)
    pars.add('g2_amplitude', value=51770*RR)
    pars.add('a', value=8.897e-06*RR)
    pars.add('b', value=-0.211*RR)
    pars.add('c', value=1268*RR)
    amplitude_names = ["g1_amplitude"]
    return fit_fun, pars, data_range, amplitude_names


def setup_fit_br_mar23(dinfo,mca_sum):
    data_range = (dinfo['E'] > 11000) & (dinfo['E'] < 12500)
    mx = np.max(mca_sum[data_range])
    RR = mx/300
    g1 = models.GaussianModel(prefix='g1_')
    g2 = models.GaussianModel(prefix='g2_')
    q1 = models.QuadraticModel()
    fit_fun = g1 + g2 + q1
    pars = Parameters()
    pars.add('g1_center', value=11920, vary=True)
    pars.add('g2_center', value=11490, vary=True)
    pars.add('g1_sigma', value=114.8, vary=False)
    pars.add('g2_sigma', value=114.8, vary=False)
    pars.add('g1_amplitude', value=3876*RR)
    pars.add('g2_amplitude', value=51770*RR)
    pars.add('a', value=8.897e-06*RR)
    pars.add('b', value=-0.211*RR)
    pars.add('c', value=1268*RR)
    amplitude_names = ["g1_amplitude"]
    return fit_fun, pars, data_range, amplitude_names

def get_fluor_amplitude(mca_instance, dinfo, start_pars=None):
    """
    Get the fluorescence amplitude from the data.

    Parameters:
    - mca_data (array-like): MCA data to fit.
    - dinfo (dict): Dictionary containing experimental information.
    - start_pars (Parameters, optional): Starting parameters for the fit.

    Returns:
    - peak_counts (float): Sum of peak counts.
    - peak_errs (float): Sum of peak errors.
    """
    fit_fun, pars, data_range, amplitude_names = setup_fit(dinfo,mca_instance)
    if start_pars is not None:
        pars = start_pars
        for amplitude_name in amplitude_names:
            pars[amplitude_name].max = pars[amplitude_name].value * 4
            pars[amplitude_name].min = 0
    dE = dinfo['E'][1] - dinfo['E'][0]
    X = dinfo['E'][data_range]
    this_result = fit_fun.fit(mca_instance[data_range] / dE, x=X, params=pars)
    peak_counts = sum(this_result.params[amplitude_name].value for amplitude_name in amplitude_names)
    peak_errs = np.sqrt(sum(
        (this_result.params[amplitude_name].stderr if isinstance(this_result.params[amplitude_name].stderr, float) else np.inf)**2
        for amplitude_name in amplitude_names
    ))
    return peak_counts, peak_errs

def get_start_pars(mca_data, dinfo):
    """
    Get the starting parameters for the fit.

    Parameters:
    - mca_data (array-like): MCA data to fit.
    - dinfo (dict): Dictionary containing experimental information.

    Returns:
    - pars (Parameters): Fitted parameters.
    - this_result (ModelResult): Result of the initial fit.
    - amplitude_names (list): List of amplitude parameter names.
    """
    mca_sum = np.sum(mca_data, 0)
    fit_fun, pars, data_range, amplitude_names = setup_fit(dinfo, mca_sum)
    dE = dinfo['E'][1] - dinfo['E'][0]
    X = dinfo['E'][data_range] 
    npt = mca_data.shape[0]
    this_result = fit_fun.fit(mca_sum[data_range] / dE, x=X, params=pars)
    pars = this_result.params
    for amplitude_name in amplitude_names:
        pars[amplitude_name].value /= npt
    return pars, this_result, amplitude_names

def show_fluor_fit(result, dinfo, amplitude_names, label=True):
    """
    Show the fit result for fluorescence data.

    Parameters:
    - result (ModelResult): Result of the fit.
    - dinfo (dict): Dictionary containing experimental information.
    """
    result.fit()
    result.plot_fit()
    E = result.userkws['x']
    ysim0 = result.eval()
    par0 = result.params
    for amplitude_name in amplitude_names:
        par0[amplitude_name].value = 0
    ysim1 = result.eval(params=par0)
    plt.plot(E, ysim0 - ysim1, '--g', label='Fluorescence Intensity')
    plt.legend()
    plt.ylabel('Counts/Second')
    plt.xlabel('Energy (eV)')
    plt.title(f'Fit to Fluorescence Peak {dinfo["fluorophore"]}')
    if label:
        spec_utils.K_label('Br', height=.8)
        spec_utils.L_label('Au', height=.5)


def get_fluorescence_data(mca_data, dinfo, norm=None, plot_fit=False):
    """
    Get fluorescence data and fit results.

    Parameters:
    - mca_data (array-like): MCA data to fit.
    - dinfo (dict): Dictionary containing experimental information.
    - norm (array-like, optional): Normalization factor.
    - plot_fit (bool, optional): Whether to plot the fit.

    Returns:
    - mca_amplitudes (array-like): MCA amplitudes.
    - mca_errors (array-like): MCA errors.
    """
    nscanpoints = mca_data.shape[0]
    mca_amplitudes = np.empty(nscanpoints)
    mca_errors = np.empty(nscanpoints)
    start_pars, start_result, amplitude_names = get_start_pars(mca_data, dinfo)
    if plot_fit:
        show_fluor_fit(start_result, dinfo, amplitude_names)
    for ii in range(nscanpoints):
        A, dA = get_fluor_amplitude(mca_data[ii, :], dinfo, start_pars=start_pars)
        mca_amplitudes[ii] = A
        mca_errors[ii] = dA
    if norm is not None:
        norm_factor = norm / np.average(norm)
        mca_amplitudes *= norm_factor
        mca_errors *= norm_factor
    return mca_amplitudes, mca_errors, start_pars

def plot_fluorescence(angles, mca_amplitudes, mca_errors, dinfo, fluorescence_scan_number, nflist=None):
    """
    Plot fluorescence data.

    Parameters:
    - angles (array-like): Angles of the measurement.
    - mca_amplitudes (array-like): MCA amplitudes.
    - mca_errors (array-like): MCA errors.
    - dinfo (dict): Dictionary containing experimental information.
    - fluorescence_scan_number (int): The scan number for fluorescence.
    - nflist (str, optional): List of scan numbers.
    """
    plt.errorbar(angles, mca_amplitudes, mca_errors, fmt='-ks')
    plt.xlabel('theta (deg)')
    plt.ylabel('fluorescence intensity (cps)')
    scanstring = nflist if nflist is not None else f'{fluorescence_scan_number}'
    plt.title(f"file: {dinfo['vortex_filename_stub']} scan: {scanstring}, {dinfo['fluorophore']}")
    plt.ylim(0.7 * np.min(mca_amplitudes), 1.3 * np.max(mca_amplitudes))




def fluor_multifit(N_align: List[int], N_fluor: List[int], dinfo: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, str, float, Any]:
    """
    Perform multi-fit for fluorescence data.

    Parameters:
    - N_align (list): List of alignment scan numbers.
    - N_fluor (list): List of fluorescence scan numbers.
    - dinfo (dict): Dictionary containing experimental information.

    Returns:
    - angles_0 (array-like): Final angles.
    - mca_amplitudes_0 (array-like): Final MCA amplitudes.
    - mca_errors_0 (array-like): Final MCA errors.
    - nflist (str): List of fluorescence scan numbers.
    - thoff (float): Offset angle from first fit.
    - result_reflectivity: Result of the reflectivity fit.
    """
    def get_reflectivity_data(align_scan_number: int, dinfo: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        data, _ = spec_utils.readscan(dinfo["align_filename"], align_scan_number)
        if dinfo['run_date'] == 'Mar23':
            return spec_utils.get_DND_refl(data)
        elif dinfo['run_date'] in ['Feb24', 'Nov23']:
            return spec_utils.get_CLS_refl(data)
        else:
            raise ValueError(f"Unknown run date: {dinfo['run_date']}")

    nflist = ", ".join(map(str, N_fluor))
    last_align_scan_number = -1
    angles_0 = mca_amplitudes_0 = mca_errors_0 = thoff = result_reflectivity = None

    for ii, (align_scan_number, fluorescence_scan_number) in enumerate(zip(N_align, N_fluor)):
        logger.info(f'Working on dataset {ii + 1}: align scan {align_scan_number}, fluor scan {fluorescence_scan_number}')

        if align_scan_number != last_align_scan_number:
            logger.info('Fitting alignment scan for angle offset')
            try:
                th, I, exposure_time, norm = get_reflectivity_data(align_scan_number, dinfo)
            except ValueError as e:
                logger.error(f"Error in getting reflectivity data: {e}")
                continue

            rr = (th > 0.4) & (th < 0.6)
            dI = np.sqrt(I)
            theta_offset, theta_peak, result = get_offset_fit(th[rr], I[rr], dI[rr], dinfo, align_scan_number, showfit=False)
            logger.info(f'scan: {align_scan_number} theta_offset = {theta_offset:.6f} at {theta_peak:.6f}')
        else:
            logger.info('Repeated alignment scan. No fit required')

        last_align_scan_number = align_scan_number

        mca_data, mca_sum, ndset, angles, npt, exposure_time, norm = spec_utils.get_fluor_data(dinfo, fluorescence_scan_number)
        mca_amplitudes, mca_errors, start_pars = get_fluorescence_data(mca_data / exposure_time, dinfo, norm=None, plot_fit=False)

        if ii == 0:
            thpeak = theta_peak,
            thoff = theta_offset
            mca_amplitudes_0 = mca_amplitudes
            mca_errors_0 = mca_errors
            angles_0 = angles
            result_reflectivity = result
            I_0 = I 
            dI_0 = dI
        else:
            adjusted_angles = angles + thoff - theta_offset
            interpolated_amplitudes = np.interp(angles, adjusted_angles, mca_amplitudes)
            interpolated_errors = np.interp(angles, adjusted_angles, mca_errors)
            mca_amplitudes_0, mca_errors_0 = spec_utils.cbwe_s(mca_amplitudes_0, mca_errors_0, interpolated_amplitudes, interpolated_errors)

        nnorm = norm / np.mean(norm)

    return angles_0, mca_amplitudes_0 / nnorm, mca_errors_0 / nnorm, I_0, dI_0,exposure_time,  nflist, thoff, thpeak,  result_reflectivity



def get_Zlist(N,D):
    # D = bilayer thickness
    # N slabs in bilayer
    edgelist = np.linspace(0,D,N+1)        # positions of interfaces of slabs
    Zlist = (edgelist[0:-1]+edgelist[1:])/2   # positions of centers of slabs
    return Zlist, edgelist

def multilayer_fluor_lay_N(theta,Avec,Imap,zmax):
    ''' multilayer_fluor_lay_N(theta,I0,thoff,bg,Avec)
    breaks up bilayer into N slabs wit N the dimension of Avec
    The A's are the amplitudes of the slabs
    '''
    # need to add feature to convolute with angular resolution
    alpha = theta*scc.degree
    Zlist, edgelist = get_Zlist(np.size(Avec), zmax)
    Ifield = Imap(Zlist, alpha)
    # sum up the product of the fluoresence from each slab times the amplitude in the slab
    y = np.sum(Ifield*np.expand_dims(Avec,1),0)
    return(y)


def pars_to_layer(pars: Dict[str, Any], dinfo: Dict[str, Any]) -> Any:
    """
    Convert parameter values to layer information based on fit flag.

    Parameters:
    -----------
    pars : Dict[str, Any]
        Dictionary containing parameter values.
    dinfo : Dict[str, Any]
        Dictionary containing fitting information including the fit flag.

    Returns:
    --------
    layers : Any
        Layer information generated by the sample simulation function.
    """
    if dinfo['fitflag'] == 'NN':
        expected_params = {'d_overlay', 'sig_overlay', 'G', 'D', 'sig_W', 'sig_SiC', 'D_Cr', 'sig_Cr', 'sig_Si_Bot'}
        sample_fun = fluor_fit.sample_sim_new
        water_flag = True 
        bilayer_flag = True 
        new_cell_flag = False
    elif (dinfo['fitflag'] == 'OO')  or (dinfo['fitflag'] == 'NO'):
        expected_params = {'G', 'D', 'sig_Mo', 'sig_Si', 'overlay', 'sig_Si_top', 'D_Ti', 'sig_Ti', 'D_SiO2', 'sig_SiO2',
                           'D_SiO2_Bot', 'sig_SiO2_Bot', 'sig_Si_Bot'}
        sample_fun = fluor_fit.sample_sim
        water_flag = True 
        bilayer_flag = True 
        new_cell_flag = None
    else:
        raise ValueError(f"Unknown fitflag: {dinfo['fitflag']}")

    filtered_par = {key: value.value for key, value in pars.items() if key in expected_params}

    layers = sample_fun(**filtered_par, water=water_flag, bilayer=bilayer_flag, new_cell=new_cell_flag)
    return layers

def plot_N_slab_result(result,NUM_SLABS, zmax):
    """
    Plot the fluorophore concentration across three slabs up to a maximum height.

    Parameters:
    result : object containing simulation parameters and results
    zmax : float, the maximum height to consider for plotting
    """
    # Constants
    ANGSTROM = scc.angstrom  # This assumes scc has been properly imported

    # Unpacking parameters
    A = [result.params[f'A{i}'].value for i in range(NUM_SLABS)]
    dA = [result.params[f'A{i}'].stderr for i in range(NUM_SLABS)]
    _, edgelist = get_Zlist(NUM_SLABS, zmax)

    norm = np.sum(A)

    # Check that edgelist is sufficiently long
    if len(edgelist) < NUM_SLABS + 1:
        raise ValueError("edgelist does not contain enough entries.")

    # Plotting
    for i, (tA,tdA) in enumerate(zip(A,dA)):
        edge1 = edgelist[i] / ANGSTROM
        edge2 = edgelist[i + 1] / ANGSTROM
        CEN = (edge1+edge2)/2
        plt.plot([edge1, edge1], [0, 100*tA/norm], '-k')
        plt.plot([edge1, edge2], [100*tA/norm, 100*tA/norm], '-k')
        plt.plot([edge2, edge2], [100*tA/norm, 0], '-k')
        if tdA  is not None:
            plt.errorbar([CEN],[100*tA/norm],[100*tdA/norm],fmt='ks')

    # now plot error bars

    plt.xlabel('height ($\\mathrm{\\AA}$)')
    plt.ylabel('fluorophore concentration (percent)')
    plt.title('Fluorophore Concentration Profile')

def get_bilayer_position(layers: List[Tuple[str, float, float, float]]) -> Tuple[float, float]:
    """
    Calculate the position and thickness of the bilayer in the given list of layers.

    Parameters:
    -----------
    layers : List[Tuple[str, float, float, float]]
        A list of tuples, each containing (material, density, thickness, roughness).

    Returns:
    --------
    bilayer_top : float
        The depth at which the top of the bilayer is found.
    bilayer_thickness : float
        The total thickness of the bilayer.
    """
    depth = 0.0
    found_top = False
    bilayer_thickness = 0.0
    bilayer_top = 0.0

    for material, density, thickness, roughness in layers:
        if not found_top and material == 'CH2':
            bilayer_top = depth
            found_top = True

        depth -= thickness

        if material == 'CH2':
            bilayer_thickness += thickness

    return bilayer_top, bilayer_thickness

def get_standing_wave(
    dinfo: Dict[str, Any], 
    layers: Any, 
    bilayer_top: float, 
    bilayer_thickness: float, 
    result_reflectivity: Any, 
    thoff: float, 
    th_com: float, 
    plot_wave: bool = True
) -> RectBivariateSpline:
    """
    Calculate the standing wave field and optionally plot it.

    Parameters:
    -----------
    dinfo : Dict[str, Any]
        Dictionary containing fitting information and parameters.
    layers : Any
        Layer structure used in the reflection matrix calculation.
    bilayer_top : float
        The top position of the bilayer.
    bilayer_thickness : float
        The thickness of the bilayer.
    result_reflectivity : Any
        Result object containing fitted parameters.
    thoff : float
        The offset angle obtained from the reflectivity fit
    th_com : float
        The reflection center angle.
    plot_wave : bool, optional
        Whether to plot the standing wave field. Default is True.

    Returns:
    --------
    SW : RectBivariateSpline
        Bivariate spline object representing the standing wave field.
    """
    try:
        alpha = np.linspace(0.1, 1, 1000) * scc.degree

        if (dinfo['fitflag'] == 'NN') or (dinfo['fitflag'] == 'NO'):
            alphap = AuI_funs.water_refract(alpha / scc.degree, dinfo['Energy']) * scc.degree
        elif dinfo['fitflag'] == 'OO':
            alphap = alpha
        else:
            print('error: unknown fit flag')

        t, r, kz, X, rr, tp, zm = refl_funs.reflection_matrix(alphap, dinfo['Energy'], layers)
        heights0 = np.linspace(-1000, 500, 1000) * scc.angstrom

        print(f'using thoff = {thoff:f}')
        print(f'using energy = {dinfo["Energy"]:f}')
        print(f'using fitflag {dinfo["fitflag"]:s}')
        result_reflectivity.params.pretty_print()

        If, Ef = refl_funs.standing_wave(heights0, t, r, kz, zm)
        offset = (bilayer_top - bilayer_thickness) * scc.angstrom
        SW = RectBivariateSpline(heights0 - offset, alpha+thoff*scc.degree, If)

        alpha_sim = np.linspace(0.1, 0.8, 1000) * scc.degree
        heights_sim = np.linspace(-500, 500, 1000) * scc.angstrom
        Isim = SW(heights_sim, alpha_sim)

        if plot_wave:
            plt.imshow(
                Isim, aspect='auto', extent=(alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree,
                                             heights_sim[0]/scc.angstrom, heights_sim[-1]/scc.angstrom),
                origin='lower'
            )
            plt.xlabel('MU (deg)')
            plt.ylabel('z (angstrom)')
            plt.title('Standing Wave Intensity')
            plt.plot([alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree], [0, 0], '--r', label='Bilayer bottom')
            plt.plot([alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree], [bilayer_thickness, bilayer_thickness], '-r', label='Bilayer top')

            d_overlay = result_reflectivity.params.get('d_overlay', result_reflectivity.params.get('overlay')).value
            plt.plot([alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree], [-d_overlay, -d_overlay], '-y', label='Multilayer top')

            plt.plot([th_com, th_com], [heights_sim[0]/scc.angstrom, heights_sim[-1]/scc.angstrom], '-m', label='Reflection center')

            plt.legend()

        return SW
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Model for three slabs

def three_slab(theta,A0,A1,A2,bg, Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2],Imap,zmax) + bg

three_slab_model = Model(three_slab, independent_vars = ['theta', 'Imap', 'zmax'])

def fit_three_layer(angles, mca_amplitudes, mca_errors, bilayer_thickness,  SW, nflist, dinfo, plot=True): 
    # Here we fit the measured fluorescence to the calculated fluorescence
    angles = np.array(angles) 
    astart = np.mean(mca_amplitudes)/3.0
    params = three_slab_model.make_params(A0 =astart, A1 = astart, A2 = astart, bg = astart)
    params['A0'].vary=True
    params['A0'].min = 0
    params['A1'].vary=True
    params['A1'].min = 0
    params['A2'].vary=True
    params['A2'].min = 0
    params['bg'].vary = True 
    params['bg'].min = 0
    params['bg'].max = astart*1.5

    zmax = bilayer_thickness*scc.angstrom
    result3 = three_slab_model.fit(mca_amplitudes ,params = params,
                theta = angles, Imap = SW, zmax = zmax,
                weights = 1/mca_errors)
    thsim = np.linspace(angles[0],angles[-1],1000)
    ysim = result3.eval(theta = thsim, Imap = SW, zmax = zmax)
    if plot:
        norm = result3.params['A0']+result3.params['A1']+result3.params['A2']
        bg = result3.params['bg']
        plt.plot(thsim,(ysim-bg)/norm,'-r')
        plt.errorbar(angles,(mca_amplitudes-bg)/norm,mca_errors/norm,fmt='-ks')
        print(result3.fit_report())
        plt.xlabel('angle (deg)')
        plt.ylabel('Relative Fluorescence Intensity (counts)')
        plt.title(f'fluorescence scans: {nflist:s} file:{dinfo["vortex_filename_stub"]:s}')
        plt.xlim(.40,.52)
    return result3, zmax

# Model for five slabs
def five_slab(theta,A0,A1,A2,A3, A4, bg, Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2,A3,A4],Imap,zmax) + bg

five_slab_model = Model(five_slab, independent_vars = ['theta', 'Imap', 'zmax'])

def fit_five_layer(angles, mca_amplitudes, mca_errors, bilayer_thickness,  SW, nflist, dinfo, plot=True): 
    # Here we fit the measured fluorescence to the calculated fluorescence
    astart = np.mean(mca_amplitudes)/5.0
    angles = np.array(angles)
    params = five_slab_model.make_params(A0 =astart, A1 = astart, A2 = astart, A3 = astart, A4 = astart, bg = astart)
    params['A0'].vary=True
    params['A0'].min = 0
    params['A0'].max = 10*astart
    params['A1'].vary=True
    params['A1'].min = 0
    params['A1'].max = 10*astart
    params['A2'].vary=True
    params['A2'].min = 0
    params['A2'].max = 10*astart
    params['A3'].vary=True
    params['A3'].min = 0
    params['A3'].max = 10*astart
    params['A4'].vary=True
    params['A4'].min = 0
    params['A4'].max = 10*astart
    params['bg'].vary = True 
    params['bg'].min = 0
    params['bg'].max = 10*astart

    zmax = bilayer_thickness*scc.angstrom
    result5 = five_slab_model.fit(mca_amplitudes ,params = params,
                theta = angles, Imap = SW, zmax = zmax,
                weights = 1/mca_errors, method='differential_evolution')
    thsim = np.linspace(angles[0],angles[-1],1000)
    ysim = result5.eval(theta = thsim, Imap = SW, zmax = zmax)
    if plot:
        plt.plot(thsim,ysim,'-r')
        plt.errorbar(angles,mca_amplitudes,mca_errors,fmt='-ks')
        print(result5.fit_report())
        plt.xlabel('angle (deg)')
        plt.ylabel('Fluorescence Intensity (counts)')
        plt.title(f'fluorescence scans: {nflist:s} file:{dinfo["vortex_filename_stub"]:s}')
        plt.xlim(.40,.52)
    return result5, zmax

def kapton_correct(th: float, Iin: float, dinfo: Dict[str, Any]) -> float:
    """
    Corrects the input intensity (Iin) for kapton absorption.

    Parameters:
    th (float): The angle in degrees.
    Iin (float): The input intensity to be corrected.
    dinfo (dict): Dictionary containing relevant parameters:
        - 'fitflag' (str): Flag indicating fit status. If 'OO', no correction is applied.
        - 'Energy' (float): Energy value for material_mu calculation.
        - 'sample_L' (float): Length of the sample.
        - 'd_kapton' (float): Thickness of the kapton.

    Returns:
    float: Corrected intensity if 'fitflag' is not 'OO'. Otherwise, returns the input intensity (Iin).
    """
    if dinfo['fitflag'] == 'OO':
        return Iin

    kapton = xdb.find_material('kapton')
    mu = xdb.material_mu(kapton.formula, dinfo['Energy'], kapton.density, kind='total') / scc.centi
    alpha = th * scc.degree

    npt = 3  # Using 3 points for numerical integration
    x = np.linspace(0, dinfo['sample_L'], npt)
    trans = 0

    for tx in x:
        l1 = np.min(np.vstack((dinfo['d_kapton'] / np.sin(th * scc.degree), tx / np.cos(th * scc.degree))), axis=0)
        l2 = np.min(np.vstack((dinfo['d_kapton'] / np.sin(th * scc.degree), (dinfo['sample_L'] - tx) / np.cos(th * scc.degree))), axis=0)
        trans += np.exp(-mu * (l1 + l2))
    trans /= npt
    return Iin / trans

def plot_spec_scan(th, I, dinfo, scan_number):
    plt.plot(th,I, '-ks')
    plt.xlabel('th (deg)')
    plt.ylabel('I (count/monitor)')
    plt.title(f'{dinfo["spec_filename_stub"]:s} scan {scan_number:d}')

def plot_ref_and_fluor(th, mca_amplitudes, mca_errors, I, dinfo,  nflist):
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('$\\theta$ (deg)')
    ax1.set_ylabel('fluorecence counts', color=color)
    ax1.errorbar(th, mca_amplitudes, mca_errors, fmt = '-ks',  color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'black'
    ax2.set_ylabel('Reflectivity (cps)', color=color)
    ax2.plot(th, I, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    tit =  f' {dinfo["vortex_filename_stub"]:s} scan {nflist:s}'
    plt.title(tit)
    fig.tight_layout()  
    plt.show()

def no_offset_fluor_merge(scanlist, dinfo):
    nflist = ", ".join(map(str, scanlist))
    for ii, scan in enumerate(scanlist):
        mca_data, mca_sum, ndset, angles, npt, exposure_time, norm = spec_utils.get_fluor_data(dinfo, scan)
        mca_amplitudes, mca_errors, start_pars = get_fluorescence_data(mca_data/exposure_time, dinfo, norm = None, plot_fit = False)
        if ii==0:
            M_Y = mca_amplitudes
            DM_Y = mca_errors**2
        else:
            M_Y += mca_amplitudes
            DM_Y += mca_errors**2

    DM_Y = np.sqrt(DM_Y)**angles/.47
    M_Y = M_Y*angles/.47    
    return M_Y, DM_Y, nflist

def plot_offset_scans(scanlist,dinfo):
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('$\\theta$ (deg)')
    ax1.set_ylabel('fluorecence counts (arb)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  
    color = 'black'
    ax2.set_ylabel('Reflectivity (arb)', color=color)   
    ax2.tick_params(axis='y', labelcolor=color)
    nflist = ", ".join(map(str, scanlist))

    for align_scan_number in scanlist:
        data,scan_info  = spec_utils.readscan(dinfo['spec_filename'],align_scan_number)
        th, I, exposure_time, norm =  spec_utils.get_DND_refl(data)
        thoff, th_peak, result_reflectivity = AuI_funs.get_offset_fit(th,I,np.sqrt(I),dinfo, 
        align_scan_number,varylist=['bg'], showfit = False)
        Inorm = result_reflectivity.params['I0'].value
        bg = result_reflectivity.params['bg'].value
        fluorescence_scan_number = align_scan_number
        mca_data, mca_sum, ndset, angles, npt, exposure_time, norm = spec_utils.get_fluor_data(dinfo, fluorescence_scan_number) 
        mca_amplitudes, mca_errors, start_pars = AuI_funs.get_fluorescence_data(mca_data/exposure_time, dinfo, norm = None, plot_fit = False)
        ax1.errorbar(th-thoff, mca_amplitudes/Inorm, mca_errors/Inorm, label=f'{align_scan_number:d}')
        ax2.plot(th-thoff, (I-bg)/Inorm)
    plt.title(f'{dinfo["spec_filename_stub"]} scans:{nflist:s}')
    fig.tight_layout()  
    ax1.legend()
    fig.show()