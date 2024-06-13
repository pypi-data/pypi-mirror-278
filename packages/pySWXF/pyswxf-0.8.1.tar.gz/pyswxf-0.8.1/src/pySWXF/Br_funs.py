def fluor_multifit_Br(N_align, N_fluor, dinfo):
    """
    Perform multifit for fluorescence data.

    Parameters:
    - N_align: List of alignment scan numbers.
    - N_fluor: List of fluorescence scan numbers.
    - dinfo: Dictionary containing relevant data information.

    Returns:
    - angles: Array of angles.
    - mca_amplitudes: Array of MCA amplitudes.
    - mca_errors: Array of MCA errors.
    - nflist: Comma-separated string of N_fluor values.
    """
    nflist = ", ".join(map(str, N_fluor))
    
    # Loop through all the data, offset and sum
    for i, (align_scan_number, fluorescence_scan_number) in enumerate(zip(N_align, N_fluor)):
        print(f'Working on dataset {i+1} align scan {align_scan_number} fluor scan {fluorescence_scan_number}')
        
        # Get reflectivity data
        data, _ = spec_utils.readscan(dinfo["align_filename"], align_scan_number)
        th = np.array(data['MU'])
        I = np.array(data['L_ROI1'])
        dI = np.sqrt(I)
        
        rr = (th>.4)*(th<.6)
        theta_offset, _ = AuI_funs.get_offset_fit(th[rr], I[rr], dI[rr], dinfo["Energy_Nov"], dinfo["fitflag"], showfit=False, verbose=True)
        
        # Get fluorescence data
        mca, _, _, angles, _, _, norm = spec_utils.get_fluor_data(dinfo["spec_filename"], dinfo["mca_filename"], fluorescence_scan_number)
        
        nscanpoints = mca.shape[0]
        mca_amplitudes = np.empty(nscanpoints)
        mca_errors = np.empty(nscanpoints)
        
        for ii in range(nscanpoints):
            A, dA = AuI_funs.get_gold_amplitude(dinfo["E"], mca[ii, :])
            mca_amplitudes[ii] = A
            mca_errors[ii] = dA
        
        norm_factor = norm / np.average(norm)
        mca_amplitudes *= norm_factor
        mca_errors *= norm_factor
        
        if i == 0:
            thoff = theta_offset
            mca_amplitudes_0 = mca_amplitudes
            mca_errors_0 = mca_errors
            angles_0 = angles
        else:
            adjusted_angles = angles + theta_offset - thoff
            interpolated_amplitudes = np.interp(angles, adjusted_angles, mca_amplitudes)
            interpolated_errors = np.interp(angles, adjusted_angles, mca_errors)
            mca_amplitudes_0, mca_errors_0 = spec_utils.cbwe_s(mca_amplitudes_0, mca_errors_0, interpolated_amplitudes, interpolated_errors)
    
    return angles_0, mca_amplitudes_0, mca_errors_0, nflist
