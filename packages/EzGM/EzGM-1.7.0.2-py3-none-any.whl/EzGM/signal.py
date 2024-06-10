"""
Signal processing toolbox
"""

# Import python libraries
import numpy as np
import numpy.matlib
from scipy.signal import butter, windows, find_peaks, filtfilt
from scipy.integrate import cumtrapz, trapz
from scipy.fft import fft, fftfreq, fftshift


def baseline_correction(values, dt, polynomial_type):
    """
    Details
    -------
    This function performs base line correction on the given signal.
    
    Notes
    -----
    Applicable for Constant, Linear, Quadratic and Cubic polynomial functions.
        
    References
    ----------
    Kramer, Steven L. 1996. Geotechnical Earthquake Engineering. Prentice Hall.
        
    Parameters
    ----------
    values : numpy.ndarray
        Input signal values.
    dt : float          
        Sampling interval.
    polynomial_type : str
        Type of baseline correction 'Constant', 'Linear', 'Quadratic', 'Cubic'.
        
    Returns
    -------
    values_corrected : numpy.ndarray
        Corrected signal values
    """

    if polynomial_type == 'Constant':
        n = 0
    elif polynomial_type == 'Linear':
        n = 1
    elif polynomial_type == 'Quadratic':
        n = 2
    elif polynomial_type == 'Cubic':
        n = 3

    t = np.linspace(0, (len(values) - 1) * dt, len(values))  # Time array
    P = np.polyfit(t, values, n)  # Best fit line of values
    po_va = np.polyval(P, t)  # Matrix of best fit line
    values_corrected = values - po_va  # Baseline corrected values

    return values_corrected


def butterworth_filter(values, dt, cut_off=(0.1, 25), filter_order=4, filter_type='bandpass', alpha_window=0.0):
    """
    Details
    -------
    This function performs acausal or two-pass (forward and reverse) infinite impulse response (IIR) filtering.
    The acausal filter is preferable to a causal filter (one pass) as it does not cause phase shift, in other words it is a zero-phase filter.
    It uses butterworth digital and analog filter design.
    
    References
    ----------
    Boore, D. M., and S. Akkar (2003). Effect of causal and acausal filters on
    elastic and inelastic response spectra, Earthquake Eng. Struct. Dyn. 32, 1729–1748.
    Boore, D. M. (2005). On Pads and Filters: Processing Strong-Motion Data. 
    Bulletin of the Seismological Society of America, 95(2), 745–750. 
    doi: 10.1785/0120040160

    Parameters
    ----------
    values : numpy.ndarray
        Input signal.
    dt : float
        Sampling interval.
    cut_off : float, tuple, list, numpy.ndarray, optional (The default is (0.1, 25)
        Cut off frequencies for the filter (Hz).
        For lowpass and highpass filters this parameters is a float e.g. 25 or 0.1
        For bandpass or bandstop filters this parameter is a tuple or list e.g. (0.1, 25)
    filter_type : str, optional (The default is 'lowpass')
        The type of filter {'lowpass', 'highpass', 'bandpass', 'bandstop'}.
    filter_order : int, optional (The default is 4)
        Order of the Butterworth filter.
    alpha_window : float, optional (The default is 0.0)
        Shape parameter of the Tukey window

    Returns
    -------
    values_filtered : numpy.ndarray
        Filtered signal values.
    """

    if isinstance(cut_off, list) or isinstance(cut_off, tuple):
        cut_off = np.array(cut_off)

    sampling_rate = 1.0 / dt  # Sampling rate
    nyq_freq = sampling_rate * 0.5  # Nyquist frequency
    wn = cut_off / nyq_freq  # The critical frequency or frequencies. For lowpass and highpass filters,
    pad_length = round(len(values) /2)  # Half of signal length
    w = windows.tukey(len(values), alpha_window)  # This is the window
    values = w * values  # Apply the tapered cosine window
    values = np.append(np.append(np.zeros(pad_length), values), np.zeros(pad_length))  # Add zero pads to start and end
    # Wn is a scalar; for bandpass and bandstop filters, Wn is a length-2 sequence.
    b, a = butter(filter_order, wn, filter_type)  # Numerator (b) and denominator (a) polynomials of the IIR filter.
    values = filtfilt(b, a, values)  # Filtering data with an IIR or FIR filter.
    values_filtered = values[pad_length: -pad_length]  # removing extra zeros

    return values_filtered


def sdof_ltha(ag, dt, periods, xi, m=1):
    """
    Details
    -------
    This function carries out linear time history analysis for SDOF system
    It currently uses Newmark Beta Method.
    
    References
    ---------- 
    Chopra, A.K. 2012. Dynamics of Structures: Theory and 
    Applications to Earthquake Engineering, Prentice Hall.
    N. M. Newmark, “A Method of Computation for Structural Dynamics,”
    ASCE Journal of the Engineering Mechanics Division, Vol. 85, 1959, pp. 67-94.
    
    Notes
    -----
    * Linear Acceleration Method: Gamma = 1/2, Beta = 1/6
    * Average Acceleration Method: Gamma = 1/2, Beta = 1/4
    * Average acceleration method is unconditionally stable,
      whereas linear acceleration method is stable only if dt/Tn <= 0.55
      Linear acceleration method is preferable due to its accuracy.
    
    Parameters
    ----------
    ag : numpy.ndarray    
        Acceleration values.
    dt : float
        Time step [sec]
    periods :  float, numpy.ndarray.
        Considered period array e.g. 0 sec, 0.1 sec ... 4 sec.
    xi : float
        Damping ratio, e.g. 0.05 for 5%.
    m :  float
        Mass of SDOF system.
        
    Returns
    -------
    u : numpy.ndarray       
        Relative displacement response history.
    v : numpy.ndarray   
        Relative velocity response history.
    ac : numpy.ndarray 
        Relative acceleration response history.
    ac_tot : numpy.ndarray 
        Total acceleration response history.
    """

    if isinstance(periods, (int, float)):
        periods = np.array([periods])
    if isinstance(periods, list):
        periods = np.array(periods)
    elif isinstance(periods, numpy.ndarray):
        periods = periods

    # Get the length of acceleration history array
    n1 = max(ag.shape)
    # Get the length of period array
    n2 = max(periods.shape)
    periods = periods.reshape((1, n2))

    # Assign the external force
    p = -m * ag

    # Calculate system properties which depend on period
    fn = 1 / periods  # frequency
    wn = 2 * np.pi * fn  # circular natural frequency
    k = m * wn ** 2  # actual stiffness
    c = 2 * m * wn * xi  # actual damping coefficient

    # Newmark Beta Method coefficients
    Gamma = np.ones((1, n2)) * (1 / 2)
    # Use linear acceleration method for dt/T<=0.55
    Beta = np.ones((1, n2)) * 1 / 6
    # Use average acceleration method for dt/T>0.55
    Beta[np.where(dt / periods > 0.55)] = 1 / 4

    # Compute the constants used in Newmark's integration
    a1 = Gamma / (Beta * dt)
    a2 = 1 / (Beta * dt ** 2)
    a3 = 1 / (Beta * dt)
    a4 = Gamma / Beta
    a5 = 1 / (2 * Beta)
    a6 = (Gamma / (2 * Beta) - 1) * dt
    kf = k + a1 * c + a2 * m
    a = a3 * m + a4 * c
    b = a5 * m + a6 * c

    # Initialize the history arrays
    u = np.zeros((n1, n2))  # relative displacement history
    v = np.zeros((n1, n2))  # relative velocity history
    ac = np.zeros((n1, n2))  # relative acceleration history
    ac_tot = np.zeros((n1, n2))  # total acceleration history

    # Set the Initial Conditions
    u[0] = 0
    v[0] = 0
    ac[0] = (p[0] - c * v[0] - k * u[0]) / m
    ac_tot[0] = ac[0] + ag[0]

    for i in range(n1 - 1):
        dpf = (p[i + 1] - p[i]) + a * v[i] + b * ac[i]
        du = dpf / kf
        dv = a1 * du - a4 * v[i] - a6 * ac[i]
        da = a2 * du - a3 * v[i] - a5 * ac[i]

        # Update history variables
        u[i + 1] = u[i] + du
        v[i + 1] = v[i] + dv
        ac[i + 1] = ac[i] + da
        ac_tot[i + 1] = ac[i + 1] + ag[i + 1]

    return u, v, ac, ac_tot


def get_parameters(ag, dt, periods, xi):
    """
    Details
    -------
    This function computes various ground motion parameters or intensity measures for a given record.
        
    References
    ---------- 
    Kramer, Steven L. 1996. Geotechnical Earthquake Engineering, Prentice Hall
    Chopra, A.K. 2012. Dynamics of Structures: Theory and 
    Applications to Earthquake Engineering, Prentice Hall.
        
    Parameters
    ----------
    ag : numpy.ndarray    
        Acceleration values [m/s2].
    dt : float
        Time step [sec]
    periods :  float, numpy.ndarray.
        Considered period array e.g. 0 sec, 0.1 sec ... 4 sec.
    xi : float
        Damping ratio, e.g. 0.05 for 5%.
        
    Returns
    -------
    param : dictionary
        Contains the following intensity measures (keys as strings):
        PSa : numpy.ndarray
            Elastic pseudo-acceleration response spectrum [m/s2].
        PSv : numpy.ndarray
            Elastic pseudo-velocity response spectrum [m/s].
        Sd : numpy.ndarray
            Elastic relative displacement response spectrum [m].
        Sv : numpy.ndarray
            Elastic relative velocity response spectrum [m/s].
        Sa_r : numpy.ndarray
            Elastic relative acceleration response spectrum [m/s2].
        Sa_a : numpy.ndarray
            Elastic absolute acceleration response spectrum [m/s2].
        Ei_r : numpy.ndarray
            Relative input energy spectrum for elastic system [N.m].
        Ei_a : numpy.ndarray
            Absolute input energy spectrum for elastic system [N.m].
        Periods : numpy.ndarray 
            Periods where spectral values are calculated [sec].
        FAS : numpy.ndarray 
            Fourier amplitude spectra.
        PAS : numpy.ndarray 
            Power amplitude spectra.
        PGA : float
            Peak ground acceleration [m/s2].
        PGV : float
            Peak ground velocity [m/s].
        PGD : float
            Peak ground displacement [m].
        Aint : numpy.ndarray 
            Arias intensity ratio vector with time [m/s].
        Arias : float 
            Maximum value of arias intensity ratio [m/s].
        HI : float
            Housner intensity ratio [m].
            Requires T to be defined between (0.1-2.5 sec), otherwise not applicable, and equal to -1.
        CAV : float
            Cumulative absolute velocity [m/s]        
        t_5_75 : list
            Significant duration time vector between 5% and 75% of energy release (from Aint).
        D_5_75 : float
            Significant duration between 5% and 75% of energy release (from Aint).
        t_5_95 : list    
            Significant duration time vector between 5% and 95% of energy release (from Aint).
        D_5_95 : float
            Significant duration between 5% and 95% of energy release (from Aint).
        t_bracketed : list 
            Bracketed duration time vector (acc>0.05g).
            Not applicable, in case of low intensity records, thus, equal to -1.
        D_bracketed : float
            Bracketed duration (acc>0.05g)
        t_uniform: list 
            Uniform duration time vector (acc>0.05g)
            Not applicable, in case of low intensity records, thus, equal to -1.
        D_uniform : float 
            Uniform duration (acc>0.05g)
        Tm : float
            Mean period.
        Tp : float             
            Predominant Period.
        aRMS : float 
            Root mean square root of acceleration [m/s2].
        vRMS : float
            Root mean square root of velocity [m/s].
        dRMS : float  
            Root mean square root of displacement [m].
        Ic : float
            Characteristic intensity.
            End time might which is used herein, is not always a good choice.
        ASI : float   
            Acceleration spectrum intensity [m/s].
            Requires T to be defined between (0.1-0.5 sec), otherwise not applicable, and equal to -1.
        MASI : float 
            Modified acceleration spectrum intensity [m].
            Requires T to be defined between (0.1-2.5 sec), otherwise not applicable, and equal to -1.
        VSI : float
            Velocity spectrum intensity [m].
            Requires T to be defined between (0.1-2.5 sec), otherwise not applicable, and equal to -1.
    """
    # TODO: there are bunch of other IMs which can be computed. Add them here.
    
    # CONSTANTS
    G = 9.81 # Gravitational acceleration (m/s2)
    M = 1 # Unit mass (kg)

    # INITIALIZATION
    if isinstance(periods, (int, float)):
        periods = np.array([periods])
    if isinstance(periods, list):
        periods = np.array(periods)
    elif isinstance(periods, numpy.ndarray):
        periods = periods
    periods = periods[periods != 0]  # do not use T = zero for response spectrum calculations
    param = {'Periods': periods}

    # GET SPECTRAL VALUES
    # Get the length of acceleration history array
    n1 = max(ag.shape)
    # Get the length of period array
    n2 = max(periods.shape)
    # Create the time array
    t = dt * np.arange(0, n1, 1)
    # Get ground velocity and displacement through integration
    vg = cumtrapz(ag, t, initial=0)
    dg = cumtrapz(vg, t, initial=0)
    # Carry out linear time history analyses for SDOF system
    u, v, ac, ac_tot = sdof_ltha(ag, dt, periods, xi, M)
    # Calculate the spectral values
    param['Sd'] = np.max(np.abs(u), axis=0)
    param['Sv'] = np.max(np.abs(v), axis=0)
    param['Sa_r'] = np.max(np.abs(ac), axis=0)
    param['Sa_a'] = np.max(np.abs(ac_tot), axis=0)
    param['PSv'] = (2 * np.pi / periods) * param['Sd']
    param['PSa'] = ((2 * np.pi / periods) ** 2) * param['Sd']
    ei_r = cumtrapz(-numpy.matlib.repmat(ag, n2, 1).T, u, axis=0, initial=0) * M
    ei_a = cumtrapz(-numpy.matlib.repmat(dg, n2, 1).T, ac_tot, axis=0, initial=0) * M
    param['Ei_r'] = ei_r[-1]
    param['Ei_a'] = ei_a[-1]

    # GET PEAK GROUND ACCELERATION, VELOCITY AND DISPLACEMENT
    param['PGA'] = np.max(np.abs(ag))
    param['PGV'] = np.max(np.abs(vg))
    param['PGD'] = np.max(np.abs(dg))

    # GET ARIAS INTENSITY
    Aint = np.cumsum(ag ** 2) * np.pi * dt / (2 * G)
    param['Arias'] = Aint[-1]
    temp = np.zeros((len(Aint), 2))
    temp[:, 0] = t
    temp[:, 1] = Aint
    param['Aint'] = temp

    # GET HOUSNER INTENSITY
    try:
        index1 = np.where(periods == 0.1)[0][0]
        index2 = np.where(periods == 2.5)[0][0]
        param['HI'] = np.trapz(param['PSv'][index1:index2], periods[index1:index2])
    except:
        param['HI'] = -1

    # SIGNIFICANT DURATION (5%-75% Ia)
    mask = (Aint >= 0.05 * Aint[-1]) * (Aint <= 0.75 * Aint[-1])
    timed = t[mask]
    t1 = round(timed[0], 3)
    t2 = round(timed[-1], 3)
    param['t_5_75'] = [t1, t2]
    param['D_5_75'] = round(t2 - t1, 3)

    # SIGNIFICANT DURATION (5%-95% Ia)
    mask = (Aint >= 0.05 * Aint[-1]) * (Aint <= 0.95 * Aint[-1])
    timed = t[mask]
    t1 = round(timed[0], 3)
    t2 = round(timed[-1], 3)
    param['t_5_95'] = [t1, t2]
    param['D_5_95'] = round(t2 - t1, 3)

    # BRACKETED DURATION (0.05g)
    try:
        mask = np.abs(ag) >= 0.05 * G
        # mask = np.abs(Ag) >= 0.05 * np.max(np.abs(Ag))
        indices = np.where(mask)[0]
        t1 = round(t[indices[0]], 3)
        t2 = round(t[indices[-1]], 3)
        param['t_bracketed'] = [t1, t2]
        param['D_bracketed'] = round(t2 - t1, 3)
    except:  # in case of ground motions with low intensities
        param['t_bracketed'] = -1
        param['D_bracketed'] = 0

    # UNIFORM DURATION (0.05g)
    try:
        mask = np.abs(ag) >= 0.05 * G
        # mask = np.abs(Ag) >= 0.05 * np.max(np.abs(Ag))
        indices = np.where(mask)[0]
        t_treshold = t[indices]
        param['t_uniform'] = [t_treshold]
        temp = np.round(np.diff(t_treshold), 8)
        param['D_uniform'] = round(np.sum(temp[temp == dt]), 3)
    except:  # in case of ground motions with low intensities
        param['t_uniform'] = -1
        param['D_uniform'] = 0

    # CUMULATVE ABSOLUTE VELOCITY
    param['CAV'] = np.trapz(np.abs(ag), t)

    # CHARACTERISTIC INTENSITY, ROOT MEAN SQUARE OF ACC, VEL, DISP
    Td = t[-1]  # note this might not be the best indicative, different Td might be chosen
    param['aRMS'] = np.sqrt(np.trapz(ag ** 2, t) / Td)
    param['vRMS'] = np.sqrt(np.trapz(vg ** 2, t) / Td)
    param['dRMS'] = np.sqrt(np.trapz(dg ** 2, t) / Td)
    param['Ic'] = param['aRMS'] ** 1.5 * np.sqrt(Td)

    # ACCELERATION AND VELOCITY SPECTRUM INTENSITY
    try:
        index3 = np.where(periods == 0.5)[0][0]
        param['ASI'] = np.trapz(param['PSa'][index1:index3], periods[index1:index3])
    except:
        param['ASI'] = -1
    try:
        param['MASI'] = np.trapz(param['PSa'][index1:index2], periods[index1:index2])
        param['VSI'] = np.trapz(param['PSv'][index1:index2], periods[index1:index2])
    except:
        param['MASI'] = -1
        param['VSI'] = -1

    # GET FOURIER AMPLITUDE AND POWER AMPLITUDE SPECTRUM
    # Number of sample points, add zeropads
    freq_len = 2 ** int(np.ceil(np.log2(len(ag))))
    famp = fft(ag, freq_len)
    famp = np.abs(fftshift(famp)) * dt
    freq = fftfreq(freq_len, dt)
    freq = fftshift(freq)
    famp = famp[freq > 0]
    freq = freq[freq > 0]
    pamp = famp ** 2 / (np.pi * t[-1] * param['aRMS'] ** 2)
    fas = np.zeros((len(famp), 2))
    fas[:, 0] = freq
    fas[:, 1] = famp
    pas = np.zeros((len(famp), 2))
    pas[:, 0] = freq
    pas[:, 1] = pamp
    param['FAS'] = fas
    param['PAS'] = pas

    # MEAN PERIOD
    mask = (freq > 0.25) * (freq < 20)
    indices = np.where(mask)[0]
    fi = freq[indices]
    Ci = famp[indices]
    param['Tm'] = np.sum(Ci ** 2 / fi) / np.sum(Ci ** 2)

    # PREDOMINANT PERIOD
    mask = param['PSa'] == max(param['PSa'])
    indices = np.where(mask)[0]
    param['Tp'] = periods[indices]

    return param


def get_sa_rotdxx(ag1, ag2, dt, periods, xi, xx):
    """
    Details
    -------
    This function computes RotDxx spectrum. It currently uses Newmark Beta Method.
    
    References
    ---------- 
    Boore, D. M. (2006). Orientation-Independent Measures of Ground Motion. 
    Bulletin of the Seismological Society of America, 96(4A), 1502–1511.
    Boore, D. M. (2010). Orientation-Independent, Nongeometric-Mean Measures 
    of Seismic Intensity from Two Horizontal Components of Motion. 
    Bulletin of the Seismological Society of America, 100(4), 1830–1835.
        
    Parameters
    ----------
    ag1: numpy.ndarray    
         Acceleration values of 1st horizontal ground motion component.
    ag2: numpy.ndarray    
         Acceleration values of 2nd horizontal ground motion component.
    dt:  float
         Time step [sec].
    periods:   float, numpy.ndarray
         Considered period array e.g. 0 sec, 0.1 sec ... 4 sec.
    xi:  float
         Damping ratio, e.g. 0.05 for 5%.
    xx:  int, list
         Percentile to calculate, e.g. 50 for RotD50.
        
    Returns
    -------
    Sa_RotDxx: numpy.ndarray 
        RotDxx Spectra.
    """

    # CONSTANTS
    M = 1 # Unit mass (kg)

    # INITIALIZATION
    if isinstance(periods, (int, float)):
        periods = np.array([periods])
    if isinstance(periods, list):
        periods = np.array(periods)
    elif isinstance(periods, numpy.ndarray):
        periods = periods
    periods = periods[periods != 0]  # do not use T = zero for response spectrum calculations

    # Verify if the length of arrays are the same
    if len(ag1) == len(ag2):
        pass
    elif len(ag1) > len(ag2):
        ag2 = np.append(ag2, np.zeros(len(ag1) - len(ag2)))
    elif len(ag2) > len(ag1):
        ag1 = np.append(ag1, np.zeros(len(ag2) - len(ag1)))

    # Get the length of period array 
    n2 = max(periods.shape)

    # Carry out linear time history analyses for SDOF system
    u1, _, _, _ = sdof_ltha(ag1, dt, periods, xi, M)
    u2, _, _, _ = sdof_ltha(ag2, dt, periods, xi, M)

    # RotD definition is taken from Boore 2010.
    rot_disp = np.zeros((180, n2))
    for theta in range(0, 180, 1):
        rot_disp[theta] = np.max(np.abs(u1 * np.cos(np.deg2rad(theta)) + u2 * np.sin(np.deg2rad(theta))), axis=0)

    # Pseudo-acceleration
    rot_acc = rot_disp * (2 * np.pi / periods) ** 2
    if isinstance(xx, list):
        Sa_RotDxx = [np.percentile(rot_acc, value, axis=0) for value in xx]
    else:
        Sa_RotDxx = np.percentile(rot_acc, xx, axis=0)

    return periods, Sa_RotDxx

def get_fiv3(ag, dt, periods, alpha = 0.7, beta = 0.85):
    """
    Details
    -------
    This function computes the filtered incremental velocity for a ground motion

    References
    ----------
    Dávalos H, Miranda E. Filtered incremental velocity: A novel approach in intensity measures for seismic collapse estimation. 
    Earthquake Engineering & Structural Dynamics 2019; 48(12): 1384-1405. DOI: 10.1002/eqe.3205.

    Parameters
    ----------
    ag: numpy.ndarray    
        Acceleration values.
    dt: float
        Time step [sec]
    periods:  float, numpy.ndarray.
        Considered period array e.g. 0 sec, 0.1 sec ... 4 sec.
    alpha : float
        Period factor, by default 0.7
    beta : float
        Cut-off frequency factor, by default 0.85

    Returns
    ----------
    fiv3: numpy.ndarray 
        filtered incremental velocity, FIV3 as per Eq. (3) of Davalos and Miranda (2019)
    """
    
    if isinstance(periods, (int, float)):
        periods = np.array([periods])
    if isinstance(periods, list):
        periods = np.array(periods)
    elif isinstance(periods, numpy.ndarray):
        periods = periods

    periods = periods[periods != 0]  # do not use T = zero for response spectrum calculations

    # Time series of the signal
    t = dt * np.arange(0, len(ag), 1)

    # FIV3 array
    fiv3 = []

    # apply a 2nd order Butterworth low pass filter to the ground motion
    for tn in periods:
        wn = beta / tn / (0.5 / dt)
        b, a = butter(2, wn, 'lowpass')
        ugf = filtfilt(b, a, ag)

        # filtered incremental velocity (FIV)
        ugf_pc = np.zeros((np.sum(t < t[-1] - alpha * tn), int(np.floor(alpha * tn / dt))))
        for i in range(int(np.floor(alpha * tn / dt))):
            ugf_pc[:, i] = ugf[np.where(t < t[-1] - alpha * tn)[0] + i]
        fiv = dt * trapz(ugf_pc, axis=1)

        # Find the peaks and troughs of the FIV array
        pks_ind, _ = find_peaks(fiv)
        trs_ind, _ = find_peaks(-fiv)

        # Sort the values
        pks_srt = np.sort(fiv[pks_ind])
        trs_srt = np.sort(fiv[trs_ind])

        # Get the peaks
        pks = pks_srt[-3:]
        trs = trs_srt[0:3]

        # Compute the FIV3
        fiv3_tmp = np.max([np.sum(pks), np.sum(trs)])

        # Append the computed FIV3
        fiv3.append(fiv3_tmp)
    
    # Convert list to an array
    fiv3 = np.array(fiv3)

    return fiv3