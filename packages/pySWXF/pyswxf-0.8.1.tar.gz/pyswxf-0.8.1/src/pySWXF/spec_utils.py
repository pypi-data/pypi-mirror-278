import pandas as pd
import re
import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import scipy.constants as scc
from lmfit.models import LinearModel, GaussianModel
import xraydb as xdb
from numpy import zeros
from lmfit import Model
import os
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch
import logging
logger = logging.getLogger(__name__)

def readscan(specfile,scanno):
    '''
    readscan(specfile,scanno)
    Input: 
    specfile string
    scanno integer

    Returns: 
     data: Array of column information in scans
     scan_info: Dictionary of columns, title, mvals
     columns are the column names
     title is the scan title
     mvals are the values of all the moters

    '''
    with open(specfile,'r') as fp:
            mpairs = []
            break_out = False
            for i, line in enumerate(fp):
                if break_out:
                    break
                if '#O' in line:
                    tmnames = line[4:-1].split('  ')
                    for ttmnames in tmnames:
                        if len(ttmnames) > 0:
                            mpairs.append([ttmnames,0.0])
                if '#S {0:d}'.format(scanno) in line:
                    title = line
                    nlines = int(line.split()[-2])+1
                    nother = 0
                    mindex = 0
                    nrows = 0 
                    filestart = i+1
                    start = False
                    for line  in fp:
                        if break_out:
                            break
                        if not start:
                            if '#L' in line:
                                cnames = re.split('\s{2,}',line[3:-1])   
                                nother += 1
                            elif '#P' in line:
                                tmvals = line[4:-1].split(' ')
                                for ttmval in tmvals:
                                    if len(ttmval) > 0:
                                        mpairs[mindex][1] += float(ttmval)
                                        mindex += 1
                                nother +=1
                            elif ('#' in line):
                                nother += 1
                            elif (not '#' in line):
                                nrows += 1
                                start = True
                        else:
                            if ('#C' in line):
                                break_out = True
                                break
                            elif (nrows == nlines):
                                break_out = True
                                break
                            else:
                                nrows += 1
    # clean up mvals
    mvals = {}
    for tpair in mpairs:
        mvals[tpair[0]] = tpair[1]
    scan_info = {'columns':cnames[1:],'title':title,'mvals':mvals}
    if nrows == 0:
        logger.info('scan aborted')
        return([],scan_info)
    else:
        data = pd.read_csv(specfile,skiprows=filestart+nother,
                       nrows=nrows,delim_whitespace=True,header=None)                                
        data.columns=cnames        
        return(data,scan_info)
    
def readmcascan(specfile,scanno):
    with open(specfile,'r') as fp:
        # read down to start of scan
        start = False
        mca = False
        mca_i = 0
        nmca = 0
        mca_data = []
        M_mca_data = []
        start_chan = 0
        end_chan = 0
        data = []
        for i, line in enumerate(fp):
            if not start and '#S {0:d} '.format(scanno) in line:
                logger.info(f'found scan {scanno:d} at line {i:d}')
                start = True
                continue
            if start and '#@CHANN ' in line:
                channels = re.split('\s{1,}',line[8:-1])
                start_chan = int(channels[1])
                end_chan = int(channels[2])
                logger.info(f'start chan {start_chan:d} end_chan {end_chan:d}')
                continue
            if start and '#@MCA ' in line:
                data_per_line = int(line[-4:-2])
                continue
            if start and '@A' in line:
                mca = True
                nmca = (end_chan-start_chan)+1
                mca_data = np.zeros(nmca)
                mca_i = 0
            if start and mca:
                if mca_i == 0:
                    ifst = 3
                else:
                    ifst = 1
                if ord(line[-1]) == 10:
                    line = line[:-1]
                if ord(line[-1]) == 92:
                    line = line[:-1]
                tdata = list(map(int,line[ifst:].split())) 
                n1 = mca_i+data_per_line
                n2 = nmca 
                mca_data[mca_i:min(n1,n2)] = tdata
                mca_i += np.size(tdata)
                if mca_i == nmca:
                    M_mca_data.append(mca_data)
                    mca = False
                continue
            if start and not mca and not '#' in line:
                tdata = list(map(float,line[0:-1].split()))
                data.append(tdata)
            if start  and '#S' in line:
                start = False
    data['end channel'] = end_chan
    data['start_chan'] = start_chan
    return(M_mca_data,data) 

def readscan_2_original(specfile,scanno):
    with open(specfile,'r') as fp:
        # read down to start of scan
        start = False
        mca = False
        mca_i = 0
        nmca = 0
        mca_data = []
        M_mca_data = []
        start_chan = 0
        end_chan = 0
        data = []
        for i, line in enumerate(fp):
            if not start and '#S {0:d} '.format(scanno) in line:
                logger.info(f'found scan {scanno:d} at line {i:d}')
                start = True
                title = line
                continue
            if start and '#L' in line:
                cnames = re.split('\s{2,}',line[3:-1]) 
                continue
            if start and '#@CHANN ' in line:
                channels = re.split('\s{1,}',line[8:-1])
                start_chan = int(channels[1])
                end_chan = int(channels[2])
                continue
            if start and '@A' in line:
                mca = True
                nmca = (end_chan-start_chan+1)
                mca_data = np.zeros(nmca)
                mca_i = 0
            if start and mca:
                if mca_i == 0:
                    ifst = 3
                else:
                    ifst = 1
                if ord(line[-1]) == 10:
                    line = line[:-1]
                if ord(line[-1]) == 92:
                    line = line[:-1]
                tdata = list(map(int,line[ifst:].split()))   
                mca_data[mca_i:min(mca_i+16,nmca)] = tdata
                mca_i += np.size(tdata)
                if mca_i == nmca:
                    M_mca_data.append(mca_data)
                    mca = False
                continue
            if start and not mca and not '#' in line:
                tdata = list(map(float,line[0:-1].split()))
                if len(tdata) == len(cnames):
                    data.append(tdata)
            if start  and '#S' in line:
                start = False
        pdata = pd.DataFrame(data)
        pdata.columns = cnames
        scan_info = {'columns':cnames[1:],'title':title}
    return(pdata,scan_info,M_mca_data,start_chan,end_chan)

def readscan_2(specfile, scanno):
    """
    Reads a scan from a spec file.

    Parameters:
    - specfile (str): The path to the spec file.
    - scanno (int): The scan number to read.

    Returns:
    - pdata (pd.DataFrame): Data from the scan as a pandas DataFrame.
    - scan_info (dict): Information about the scan, including column names and title.
    - M_mca_data (list): List of MCA data arrays.
    - start_chan (int): Starting channel.
    - end_chan (int): Ending channel.
    """
    try:
        with open(specfile, 'r') as fp:
            # Initialize variables
            start = False
            mca = False
            mca_i = 0
            nmca = 0
            mca_data = []
            M_mca_data = []
            start_chan = 0
            end_chan = 0
            data = []
            
            for i, line in enumerate(fp):
                line = line.rstrip()
                
                if not start and f'#S {scanno} ' in line:
                    logger.info(f'Found scan {scanno} at line {i}')
                    start = True
                    title = line
                    continue
                
                if start and line.startswith('#L'):
                    cnames = re.split(r'\s{2,}', line[3:])
                    continue
                
                if start and line.startswith('#@CHANN '):
                    channels = re.split(r'\s+', line[8:])
                    start_chan = int(channels[1])
                    end_chan = int(channels[2])
                    continue
                
                if start and line.startswith('@A'):
                    mca = True
                    nmca = end_chan - start_chan + 1
                    mca_data = np.zeros(nmca)
                    mca_i = 0
                
                if start and mca:
                    if mca_i == 0:
                        ifst = 3
                    else:
                        ifst = 1
                    
                    if line.endswith('\\'):
                        line = line[:-1]
                    
                    tdata = list(map(int, line[ifst:].split()))
                    mca_data[mca_i:mca_i + len(tdata)] = tdata
                    mca_i += len(tdata)
                    
                    if mca_i == nmca:
                        M_mca_data.append(mca_data.copy())
                        mca = False
                    continue
                
                if start and not mca and not line.startswith('#'):
                    tdata = list(map(float, line.split()))
                    if len(tdata) == len(cnames):
                        data.append(tdata)
                
                if start and line.startswith('#S') and f'#S {scanno} ' not in line:
                    start = False
            
            pdata = pd.DataFrame(data, columns=cnames)
            scan_info = {'columns': cnames[1:], 'title': title}
        
        return pdata, scan_info, M_mca_data, start_chan, end_chan
    
    except FileNotFoundError:
        logger.error(f"Error: The file '{specfile}' was not found.")
        return None, None, None, None, None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None, None, None, None, None

def getscan_mca(filename,scan_no):
    data, scan_info,M_mca_data,start_ch,end_ch = readscan_2(filename,scan_no)
    x = data['Two Theta']
    y = data['Detector']
    mon = data['Seconds']
    dy = np.sqrt(y)
    y /= mon
    dy /= mon
    y_mca = y*0
    for i,mca_data in enumerate(M_mca_data):
        y_mca[i] = np.sum(mca_data)
    dy_mca = np.sqrt(y_mca)
    y_mca/=mon
    dy_mca /= mon
    return x,y,dy,y_mca,dy_mca

def merge_scans(specfile,scanset,norm='mca',mca=False):
    x = np.array([])
    y = np.array([])
    dy = np.array([])
    for scanno, bg, att in scanset:
        if bg:
            if mca:
                tx,ty,tdy = getscan_bg_mca(specfile,scanno,norm)
            else:
                tx,ty,tdy = getscan_bg(specfile,scanno,norm)
            ty *= att
            tdy *= att
        else:
            if mca:
                tx,ty,tdy,y_mca,dy_mca = getscan_mca(specfile,scanno)
            else:
                tx,ty,tdy = getscan(specfile,scanno, norm)
            ty *= att
            tdy *= att
        x = np.append(x,tx)
        y = np.append(y,ty)
        dy = np.append(dy,tdy)
    ind = np.argsort(x)
    x = x[ind]
    y = y[ind]
    dy = dy[ind]
    return x,y,dy

def getscan_bg_mca(filename,scan_no,norm):
    x,y,dy,x_mca,y_mca = getscan_mca(filename,scan_no)
    x,yb1,dyb1,x_mca,y_mca = getscan_mca(filename,scan_no+1)
    x,yb2,dyb2,x_mca,y_mca = getscan_mca(filename,scan_no+2)
    ys = y-(yb1+yb2)/2
    dys = np.sqrt(dy**2 + dyb1**2 + dyb2**2)
    return x,ys,dys


def merge_duplicates(x,y,dy):
    # sort and reorder x
    w = np.argsort(x)
    x=x[w]
    y=y[w]
    dy=dy[w]
    # now look for duplicates
    wdup = x[0:-1]-x[1:]==0
    while np.sum(wdup)>0:
        ofst = 0
        for j in np.argwhere(wdup):
            i = int(j-ofst)
            y[i],dy[i] = cbwe_s(y[i],dy[i],y[i+1],dy[i+1])
            y = np.append(y[0:i+1],y[i+2:])
            x = np.append(x[0:i+1],x[i+2:])
            dy = np.append(dy[0:i+1],dy[i+2:])
            ofst += 1
        wdup = x[0:-1]-x[1:]==0
    return(x,y,dy)
        
def getscan(filename,scan_no,norm):
    data, scan_info = readscan(filename,scan_no)
    x = data['Two Theta']
    y = data['Detector']
    if norm == 'mca':
        mon = data['mca']
        if np.mean(mon)<1000:
            mon = mon*0+np.mean(mon)
        mon = mon*np.mean(data['Seconds']/data['mca'])
    else:
        mon = data['Seconds']
    dy = np.sqrt(y)
    y /= mon
    dy /= mon
    return x,y,dy

def getscan_bg(filename,scan_no,norm):
    x,y,dy = getscan(filename,scan_no,norm)
    x,yb1,dyb1 = getscan(filename,scan_no+1,norm)
    x,yb2,dyb2 = getscan(filename,scan_no+2,norm)
    ys = y-(yb1+yb2)/2
    dys = np.sqrt(dy**2 + dyb1**2 + dyb2**2)
    return x,ys,dys


def list_scans(filename,start_no=0, end_no=np.Inf):
    try:
        with open(filename,'r') as fd:
            for line in fd:
                lar = line.split()
                if len(lar) > 0:
                    if lar[0] == '#S':
                        scan_no = int(lar[1])
                        if scan_no > start_no and scan_no < end_no:
                            print(f'{line.strip():s}')
    except FileNotFoundError:
        logger.error(f"Error: The file '{filename}' was not found.")
    except IOError:
        logger.error(f"Error: An error occurred while reading the file '{filename}'.")


def get_reflectivity_CLS(fname, datadir, scan):
    specfile = datadir + fname
    if os.path.isfile(specfile):
        data,scan_info  = readscan(specfile,scan)
        y0 = data['L_ROI1']
        bg = (data['L_ROI2']+data['L_ROI3'])/2 
        y = y0-bg
        dy = np.sqrt(y0 + bg)
        x = data['MU']
    else:
        logger.error(f'File {specfile} does not exist')
    return(x, y,dy)

def get_refl_sequence_CLS(fname, datadir, firstscan):
    norm = 2.02e-3
    x1, y1, dy1 = get_reflectivity_CLS(fname,datadir, firstscan)
    y1 /= norm 
    dy1 /= norm
    x2, y2, dy2 = get_reflectivity_CLS(fname,datadir, firstscan +1)
    y = np.concatenate((y1,y2))
    dy = np.concatenate((dy1,dy2))
    x = np.concatenate((x1,x2))
    x, y, dy = merge_duplicates(x,y,dy)
    return x, y, dy

def plot_refl_sequence_CLS(fname, datadir, firstscan, k, plotdip = True):
    x, y, dy = get_refl_sequence_CLS(fname, datadir, firstscan)
    if k:
        q = 2*k*np.sin(x*scc.degree)
        plt.errorbar(q,y,dy,fmt='k.')
        plt.xlabel('q (inv ang)')
        if plotdip:
            arrow = FancyArrowPatch((.07, 1e7), (.07,1e5),
            arrowstyle='-|>',  # Line and arrow head
            mutation_scale=20,  # Size of the arrow head
            color='black', linewidth=1)
            ax = plt.gca()
            ax.add_patch(arrow)
            plt.text(.07,1e7,'expected dip')
    else:
        plt.errorbar(x,y,dy,fmt='k.')
        plt.xlabel('mu (deg)')
    plt.ylabel('Lambda counts')
    plt.yscale('log')
    plt.title(f'{fname:s} scans {firstscan:d} - {firstscan+1:d}')

def half(q,I,dI):
    '''
    and merges all pairs of adjacent points in q, 
    so that there are half as many q points with 
    correspondingly smaller error bars.  
    '''
    nlen = int(2*np.floor(len(q)/2))
    q = q[0:nlen]
    I = I[0:nlen]
    dI = dI[0:nlen]
    eve = np.arange(0,nlen-1,2).astype(int)
    odd = np.arange(1,nlen,2).astype(int)
    qout = (q[eve]+q[odd])/2
    Iout,dIout = cbwe(I[eve],dI[eve],I[odd],dI[odd])
    return  qout,Iout,dIout 

def cbwe(y1,dy1,y2,dy2):
    if (dy1 == 0 ) and (dy2 == 0):
        return (y1+y2)/2, 0
    elif (dy1 == 0):
        return y2, dy2
    elif (dy2 == 0):
        return y1, dy1
    else:
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

MCA_DATASIZE = 2048

def get_mca_data_CLS_Nov(mca_filename,scan_number,exposure,quiet=False):
    ''' 
	  Routine to met mca data from November 2023 CLS data
	  February 2024 data changed format so this no longer works
	  quite suppresses printout of dead time percentage
    returns mca data as a two dimensional array of scan point and mca data
    also returns number of points in the dataset (ndset)
    '''
    df = pd.read_csv(f'{mca_filename}_{scan_number}.txt',sep=' ',header=None)
    xy = df.to_numpy() 
    y= np.array(xy[:,1])
    ndset = int(np.size(y)/MCA_DATASIZE)
    mca = np.reshape(y,(ndset,MCA_DATASIZE))
    # correct data for deadtime
    for i in range(ndset):
        mca[i,:] = dtcorrect(mca[i,:],exposure,quiet)
    return(mca,ndset)

def get_DND_refl(data):
    I = data['ic_refl'].to_numpy()
    th = data['Kphi'].to_numpy()
    norm = data['IC5IDB']
    exposure_time = np.mean(data['Seconds'])
    return th, I, exposure_time, norm

def get_CLS_refl(data):
    I = data['L_ROI1'].to_numpy()
    th = data['MU'].to_numpy()
    norm = data['IC2']
    exposure_time = np.mean(data['Seconds'])
    return th, I, exposure_time, norm

def get_fluor_data(dinfo,  scan_number, quiet=True):
    data,scan_info  = readscan(dinfo['spec_filename'],scan_number)
    if dinfo['run_date'] == 'Feb24':
        mca,Energy = get_mca_data_CLS('',dinfo['mca_filename'],scan_number,quiet=quiet)
        angles, I, exposure_time, norm = get_CLS_refl(data)
    elif dinfo['run_date'] == 'Nov23':
        mca,ndset = get_mca_data_CLS_Nov(dinfo['mca_filename'],scan_number,exposure_time,quiet=quiet)
        angles, I, exposure_time, norm = get_CLS_refl(data)
    elif dinfo['run_date'] == 'Mar23':
        mca = get_mca_data_DND(dinfo['mca_filename'],scan_number)
        angles, I, exposure_time, norm = get_DND_refl(data)
    else:
        logger.error(f'Not configured for run_date {dinfo["run_date"]}')
        sys.exit() 
  
    mca_sum = np.sum(mca,0) # sum over each point in the scan
    ndset = np.shape(mca)[0]
    npt = np.shape(mca)[1]
    return mca,mca_sum,ndset,angles,npt,exposure_time,norm

def fit_fluor_data(mca, ndset, npt, exposure_time, norm, peak_model, pars, E, data_range):
    ''' Fit each mca set to a model for peak and return array of amplitudes'''
    amplitude_array = np.zeros(npt)
    amplitude_uncertainty = np.zeros(npt)

    mean_norm = np.mean(norm) / norm  # Compute once and use for all iterations
    X = E[data_range]
    summed_data =  np.sum(mca,0)[data_range]
    global_result =  peak_model.fit(summed_data, x=X, params=pars)
    global_result.plot_fit()
    #print(global_result.fit_report())

    for mca_scan_number in range(ndset):
        single_data_set = mca[mca_scan_number, :][data_range]
        
        this_result = peak_model.fit(single_data_set, x=X, params=pars)

        amplitude_value = this_result.params['amplitude'].value / exposure_time
        amplitude_error = this_result.params['amplitude'].stderr if isinstance(this_result.params['amplitude'].stderr, float) else 0
        amplitude_error /= exposure_time

        amplitude_array[mca_scan_number] = amplitude_value * mean_norm[mca_scan_number]
        amplitude_uncertainty[mca_scan_number] = amplitude_error * mean_norm[mca_scan_number]

    return amplitude_array, amplitude_uncertainty


def get_mca_data_DND(specfile,scanno):
    with open(specfile,'r') as fp:
        # read down to start of scan
        start = False
        mca = False
        mca_i = 0
        nmca = 0
        mca_data = []
        M_mca_data = []
        start_chan = 0
        end_chan = 2047
        channels = 2048
        data = []
        for i, line in enumerate(fp):
            if not start and '#S {0:d} '.format(scanno) in line:
                logger.info(f'found scan {scanno:d} at line {i:d}')
                start = True
                title = line
                continue
            if start and '#L' in line:
                cnames = re.split('\s{2,}',line[3:-1]) 
                continue
            if start and '@0' in line:
                mca = True
                nmca = (end_chan-start_chan+1)
                mca_data = np.zeros(nmca)
                mca_i = 0          
            if start and mca:
                line0=line
                if mca_i == 0:
                    ifst = 1
                else:
                    ifst = 1
                if ord(line[-2]) == 92:
                    line = line[:-2]
                tdata = list(map(int,line[ifst:].split())) 
                mca_data[mca_i:min(mca_i+32,nmca)] = tdata
                mca_i += np.size(tdata)
                if mca_i == nmca:
                    M_mca_data.append(mca_data)
                    mca = False
                continue
            if start  and '#S' in line:
                start = False
    return(np.array(M_mca_data))

def dtcorrect(y,exposure,quiet):
    ''' Correct Dead Time for CLS MCA'''
    N = np.sum(y)/exposure
    tau = 4.1e-6
    N0 = fsolve(lambda N0: N - N0*np.exp(-N0*tau),N)[0] 
    if not quiet:
        logger.info('percent dead time: {0:2.0f}'.format((1-N/N0)*100))
    return y*N0/N

def get_mca_data_CLS(dir,fname,scan_nu,quiet=True):
    # exposure is the exposure time of the mca
    # If not quiet, then dtcorrect prints the dead time
    with open(dir+fname,'r') as fd:
        mca_size = 2048
        for line1 in fd:
            if line1.startswith(f"#S {scan_nu:d}"):
                logger.info(f'found scan {scan_nu:d}')
                line2 = fd.readline()
                line3 = fd.readline()
                line4 = fd.readline()
                line5 = fd.readline()
                line6 = fd.readline()
                npt = int(line1.split()[-2])+1
                mca_size = int(line3.split()[1])
                exposure = float(line4.split()[1])
                pnum = int(line5.split()[1])
                mca = zeros([npt,mca_size])
                Energy = zeros(mca_size)
                for i in range(mca_size):
                    nline = fd.readline()
                    Energy[i] =float(nline.split()[1])
                    mca[0,i] = int(nline.split()[2])
                for j in range(npt-1):
                    for k in range(8):
                        fd.readline()
                    for l in range(mca_size):
                        mca[j+1,l] = int(fd.readline().split()[2])
                break
    for i in range(npt):
                mca[i,:] = dtcorrect(mca[i,:],exposure,quiet)
    return mca,Energy

def plot_mca_sum(datadir,fname,snum,xmin=1400,xmax=14800,scale='log'):
    mca, Energy = get_mca_data_CLS(datadir,fname,snum,True)
    mca_sum = np.sum(mca,0)
    rr = (Energy>xmin)*(Energy<xmax)
    plt.plot(Energy[rr],mca_sum[rr],'-k')
    plt.xlabel('Energy (keV)')
    plt.ylabel('counts')
    plt.yscale(scale)
    plt.title(f'{fname:s} scan {snum:d}')

def peak_label(Energy,Info,height=.8,linespec='-r'):
    ax = plt.gca()
    y_min, y_max = ax.get_ylim()
    
    # Determine if the y-axis is log scale
    is_log = ax.get_yscale() == 'log'
    
    if is_log:
        # Calculate the y-values for 20% and 80% of the y-axis range in log scale
        y_start = np.power(10, np.log10(y_min) + (1-height) * (np.log10(y_max) - np.log10(y_min)))
        y_end = np.power(10, np.log10(y_min) + height * (np.log10(y_max) - np.log10(y_min)))
    else:
        # Calculate the y-values for 20% and 80% of the y-axis range in linear scale
        y_start = y_min + (1-height) * (y_max - y_min)
        y_end = y_min + height * (y_max - y_min)
    
    # Draw the vertical line using ax.plot
    ax.plot([Energy, Energy], [y_start, y_end], fmt )
    ax.text(Energy,y_end,Info)

def peak_label(Energy,Info,height=.8,linespec='-r'):
    ax = plt.gca()
    y_min, y_max = ax.get_ylim()
    
    # Determine if the y-axis is log scale
    is_log = ax.get_yscale() == 'log'
    
    if is_log:
        # Calculate the y-values for 20% and 80% of the y-axis range in log scale
        y_start = np.power(10, np.log10(y_min) + .1 * (np.log10(y_max) - np.log10(y_min)))
        y_end = np.power(10, np.log10(y_min) + height * (np.log10(y_max) - np.log10(y_min)))
    else:
        # Calculate the y-values for 20% and 80% of the y-axis range in linear scale
        y_start = y_min + .1 * (y_max - y_min)
        y_end = y_min + height * (y_max - y_min)
    
    # Draw the vertical line using ax.plot
    ax.plot([Energy, Energy], [y_start, y_end], linespec )
    ax.text(Energy,y_end,Info)

def K_label(elem,height=.8):
    ax = plt.gca()
    x_min, x_max = ax.get_xlim()
    lines = xdb.xray_lines(elem,'K')
    lines = ['Ka1','Kb1']
    nlab = 0
    for line in lines:
        try:
            lE = xdb.xray_lines(elem,'K')[line][0]
            N2 = xdb.xray_lines(elem,'K')[line][1]
            if (lE > x_min) and (lE < x_max):
                logger.info(f'{elem:s} K {line:s} E = {lE:5.2f}')
                if nlab == 0:
                    peak_label(lE,elem,linespec='-r',height=height)
                    nlab += 1
                else:
                    peak_label(lE,'',linespec='--r',height=height)
        except:
            continue

def L_label(elem,height=.8):
    ax = plt.gca()
    x_min, x_max = ax.get_xlim()
    edges = ['L1','L2','L3']
    for edge in edges:
        N1 = xdb.xray_edge(elem,edge)[1]
        N1 *= xdb.xray_edge(elem,edge)[2]-1
        lines = xdb.xray_lines('Au',edge)

        for line in lines:
            try:
                lE = xdb.xray_lines(elem,edge)[line][0]
                N2 = xdb.xray_lines(elem,edge)[line][1]
                if (N2*N1 > .02) and (lE > x_min) and (lE < x_max):
                    logger.info(f'{elem:s} L {edge:s} {line:s} E = {lE:5.2f}')
                    peak_label(lE,elem,linespec='-y', height=height)
            except:
                continue

def plot_br_fluor():
    DeltaE = (Energy[-1]-Energy[0])/2048
    dms = np.shape(mcas)
    y = np.zeros(dms[0])
    dy = np.zeros(dms[0])
    par = Br_peak_mod.make_params()
    par['A_Au'].value=1e5
    par['A_Br'].value=1e5
    par['sig'].value=111
    par['sig'].vary = 0
    par['intercept'].value=0
    par['slope'].value=0
    result = Br_peak_mod.fit(np.sum(mcas,0)[rr],x=Energy[rr],params=par)
    #nresult.plot_fit()
    par = result.params;
    par['A_Au'].value /= dms[0]
    par['A_Br'].value /= dms[0]
    for i,mca in enumerate(mcas):
        result = Br_peak_mod.fit(mca[rr],x=Energy[rr],params=par)
        y[i] = result.params['A_Br'].value/DeltaE
        dy[i] = result.params['A_Br'].stderr/DeltaE
    return y, dy

def get_br_amps(Energy,mcas,rr,plot=False):
    DeltaE = (Energy[-1]-Energy[0])/2048
    dms = np.shape(mcas)
    y = np.zeros(dms[0])
    dy = np.zeros(dms[0])
    par = Br_peak_mod.make_params()
    par['A_Au'].value=1e5
    par['A_Br'].value=1e5
    par['sig'].value=111
    par['sig'].vary = 0
    par['intercept'].value=0
    par['slope'].value=0
    result = Br_peak_mod.fit(np.sum(mcas,0)[rr],x=Energy[rr],params=par)
    par = result.params;
    par['A_Au'].value /= dms[0]
    par['A_Br'].value /= dms[0]
    for i,mca in enumerate(mcas):
        result = Br_peak_mod.fit(mca[rr],x=Energy[rr],params=par)
        y[i] = result.params['A_Br'].value/DeltaE
        dy[i] = result.params['A_Br'].stderr/DeltaE
    return y, dy

def plot_br_fluor(datadir,fspec,scans):
    fvort =fspec+"_Vortex.mca"
    data,scan_info  = readscan(datadir+fspec,scans[0])
    mu = data['MU'].to_numpy()
    for i, snum in enumerate(scans):
        if i==0:
            mcas,Energy = get_mca_data_CLS(datadir,fvort,snum,True)
        else:
            tmcas,Energy = get_mca_data_CLS(datadir,fvort,snum,True)
            mcas += tmcas
    rr = (Energy>11000)*(Energy<12500)
    y,dy = get_br_amps(Energy,mcas,rr)
    plt.errorbar(mu,y,dy,fmt='ks')
    plt.xlabel('mu (deg)')
    plt.ylabel('Br fluorescence (fit) ')
    scanlist = ''
    for snum in scans:
        scanlist += f'{snum:d} '
    plt.title(f'{fspec:s} scans {scanlist:s}')
    
def get_edge_absorb(element,edge):
    Ee = xdb.xray_edge(element, edge, energy_only=True)
    delE = 50
    xlow = xdb.incoherent_cross_section_elam(element, Ee-delE)
    xhigh = xdb.incoherent_cross_section_elam(element, Ee+delE)
    del_x = xhigh-xlow 
    return del_x

def Au_L_peak(A,sig0,energy):
    E0 = 14500
    element = 'Au'
    edges = ['L1','L2','L3']
    y = energy*0
    norm = 0
    for edge in edges:
        # First get edge amplitude
        lines = xdb.xray_lines(element,edge)
        N1 = get_edge_absorb(element,edge)
        for line in lines:
                lE = xdb.xray_lines(element,edge)[line][0]
                N2 = xdb.xray_lines(element,edge)[line][1]
                N3 = xdb.fluor_yield(element, edge, line, E0)[0]
                sig = sig0*energy/Br_ka 
                arg = (energy-lE)**2/2/sig**2
                amp = 1/np.sqrt(2*np.pi*sig**2)
                y += N1*N2*N3*amp*np.exp(-arg)
                norm += N1*N2*N3
    y /= norm
    y *= A
    return y
Br_ka = xdb.xray_lines('Br','K')['Ka1'][0]

def Br_K_peak(A,sig,energy):

    arg = (energy-Br_ka)**2/2/sig**2
    amp = A/np.sqrt(2*np.pi*sig**2)
    y = amp*np.exp(-arg)
    return y

def Br_peak_sim(x,A_Br,A_Au,sig):
     y = Br_K_peak(A_Br,sig,x)
     y += Au_L_peak(A_Au,sig,x)
     return y

Br_background = LinearModel()
Br_peak_mod = Model(Br_peak_sim)+Br_background

