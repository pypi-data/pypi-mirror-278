# Model for gold fluorescence
from lmfit import Model, models
from matplotlib import pyplot as plt
import numpy as np
import scipy.constants as scc
import importlib.resources
from lmfit import Parameters
import xraydb as xdb
from pySWX.fluor_fit import multilayer_ref_new_model

g1 = models.GaussianModel(prefix='g1')
g2 = models.GaussianModel(prefix='g2')
q1 = models.QuadraticModel() 
peak_model = g1+g2+q1

# code to fit reflectivity and find offset

MULTILAYER_FIT = 'NM_clean_NIU_NOKW_Mar26_24_fit4.json'
def NN_offset_fit(th,I,dI,Beam_Energy, showfit = True):
    with importlib.resources.open_text('pySWXF.data', MULTILAYER_FIT) as f:
    params = Parameters.load(f)

    for key in params.keys():
        params[key].vary = False
    params['I0'].vary = True
    params['I0'].max = 1e9
    params['I0'].min = 100
    params['thoff'].vary = True
    params['thoff'].min =-.1
    params['thoff'].max = .1
    params['res'].value = .001

    alphac_water = np.sqrt(2*xdb.xray_delta_beta('H2O',1.00,Beam_Energy)[0])
    thc_water = alphac_water/scc.degree
    th_refrac = np.sqrt(th**2  - thc_water**2)

    result = multilayer_ref_new_model.fit(
        I,theta = th_refrac, params = params, Energy = Beam_Energy,
        water = True, bilayer = True, new_cell = False, weights = 1/dI)
    
    thoff = result.params['thoff'].value
    
    if showfit:    
        ysim=result.eval(theta = th_refrac, 
            Energy = Energy_Nov, water = True, bilayer = True, new_cell = False)
        result = fluor_fit.multilayer_ref_new_model.fit(
        I,theta = th_refrac, params = params, Energy = Energy_Nov,water = True, bilayer = True, new_cell = False, weights = I*0+1)
        ysim=result.eval(theta = th_refrac, Energy = Energy_Nov, water = True, bilayer = True, new_cell = False)
        plt.plot(th,I,label='data')
        plt.plot(th,ysim,'-k',label='fit')
        plt.locator_params(axis='x', nbins=20)
        plt.grid()
        plt.xlabel('th (deg)')
        plt.ylabel('Reflected Intensity')
    
        plt.legend()
        print(f'angular offset = {thoff:7.3f}')
    return(thoff)
    


def get_gold_amplitude(E,mca_data):   
    pars = peak_model.make_params()
    pars['g1center'].value = 13400
    pars['g1center'].vary = 0
    pars['g2center'].value = 13771
    pars['g2center'].vary = 0
    pars['g1sigma'].value = 114.8
    pars['g1sigma'].vary = 0
    pars['g2sigma'].value = 114.9
    pars['g2sigma'].vary = 0
    pars['g1amplitude'].value = 1e5
    pars['g2amplitude'].value = 2e4
    pars['a'].value = 0
    pars['b'].value = -7.5
    pars['c'].value = 50000
    Erange = (E>13000)*(E<14100)
    result = peak_model.fit(mca_data[Erange],params=pars,x=E[Erange])
    fitpars = result.params
    MCA_SLOPE = E[1]-E[0]
    peak_counts = (fitpars['g1amplitude'].value+fitpars['g1amplitude'].value)/MCA_SLOPE
    peak_errs = np.sqrt((fitpars['g1amplitude'].stderr**2+fitpars['g1amplitude'].stderr**2))/MCA_SLOPE
    return(peak_counts,peak_errs)

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
    _, edgelist = get_Zlist(NUM_SLABS, zmax)

    # Check that edgelist is sufficiently long
    if len(edgelist) < NUM_SLABS + 1:
        raise ValueError("edgelist does not contain enough entries.")

    # Plotting
    for i, tA in enumerate(A):
        edge1 = edgelist[i] / ANGSTROM
        edge2 = edgelist[i + 1] / ANGSTROM
        plt.plot([edge1, edge1], [0, tA], '-k')
        plt.plot([edge1, edge2], [tA, tA], '-k')
        plt.plot([edge2, edge2], [tA, 0], '-k')

    plt.xlabel('height ($\\mathrm{\\AA}$)')
    plt.ylabel('fluorophore concentration')
    plt.title('Fluorophore Concentration Profile')

# Model for three slabs

def three_slab(theta,A0,A1,A2,Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2],Imap,zmax)

three_slab_model = Model(three_slab, independent_vars = ['theta', 'Imap', 'zmax'])

# Model for five slabs
def five_slab(theta,A0,A1,A2,A3, A4, Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2,A3, A4],Imap,zmax)

five_slab_model = Model(five_slab, independent_vars = ['theta', 'Imap', 'zmax'])