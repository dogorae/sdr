import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.fft import fft

class Dataset:
    """
    A collection of things you can derive from phase data
    ----------
    Attributes
    ----------
    filepath    : path to the .bin file containing phase data
    fs          : sampling rate
    phase       : unwrapped, linear-removed phase data in radians
    num_pts     : number of total data points
    fftpts      : number of points in each segment used for fft & averaging
    time        : time array
    freq        : fft frequency
    phase_noise : phase noise psd in dBc/Hz

    """
    def __init__(self, filepath, fs, fftpts=256):
        self.filepath = filepath
        self.fs = fs
        
        # Time domain
        self.phase = self.__detrend(self.__unwrap(np.angle(self.__load(filepath))))
        self.num_pts = len(self.phase)
        if fftpts <= self.num_pts:
            self.fftpts = fftpts
        else:
            self.fftpts = self.num_pts
        self.time = np.array(range(self.num_pts),dtype=np.float64)/self.fs
        # Takuma says float64 is important

        # Frequency domain
        self.compute_phase_noise()  # Initializes self.freq and self.phase_noise
        
    def __load(self, filepath):
        return np.fromfile(filepath, dtype=np.complex64)
        
    def __unwrap(self, wrapped_phase):
        d = np.diff(wrapped_phase)
        wraps    = 1*(d >= 1.5*np.pi) - 1*(d <= -1.5*np.pi)
        cumwraps = np.cumsum(wraps)
        unwrapped_phase = wrapped_phase - 2*np.pi*np.insert(cumwraps,0,0)
        return unwrapped_phase

    def __detrend(self, unwrapped_phase):
        return signal.detrend(unwrapped_phase, type='linear')

    def compute_phase_noise(self):
        """Updates 'freq' and 'phase_noise' attributes
        
        Args:
            fftpts: number of points to use for the Welch method (scipy.signal.welch)
        
        Returns:
            None. Only used for the side effect of updating 'freq' and 'phase_noise'

        """
        freq, psd = signal.welch(self.phase, self.fs,
                                 nperseg=self.fftpts,
                                 window='hann',
                                 detrend='linear') # Takuma detrends his data too
        phase_noise = 10*np.log10(psd) - 3 # in dBc/Hz
        
        self.freq = freq
        self.phase_noise = phase_noise

    def xspec_with(self, other):
        """Computes the cross spectral density with another dataset
        
        Args:
            dataset : another Dataset instance to compute xsd with

        Returns:
            xsdfreq : fft frequency
            xsd     : cross spectral density in dBc/Hz
        testtesttest

        """
        xsdfreq, xsd = signal.csd(self.phase, other.phase, fs=self.fs,
                         nperseg=self.fftpts,
                         window='hann',
                         detrend='linear')
        xsd = 10*np.log10(xsd) - 3 # in dBc/Hz

        return (xsdfreq, xsd)
