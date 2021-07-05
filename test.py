import sdrdata as sdr
import matplotlib.pyplot as plt

FILEPATH1 = r'SDR1_ch0.bin'
FSAMPLE1 = 2e6
FILEPATH2 = r'SDR2_ch0.bin'
FSAMPLE2 = 2e6
FFTPTS = 2**15

d1 = sdr.Dataset(FILEPATH1, FSAMPLE1, FFTPTS)
d2 = sdr.Dataset(FILEPATH2, FSAMPLE2, FFTPTS)
xsdfreq, xsd = d1.xspec_with(d2)

# Time domain plot
plt.plot(d1.time, d1.phase, label='SDR1')
plt.plot(d2.time, d2.phase, label='SDR2')
plt.xlabel('Time (s)', size=16, fontname='Arial')
plt.ylabel('Phase (rad)', size=16, fontname='Arial')
plt.legend(fontsize=12)
plt.show()

# Frequency domain plot
plt.semilogx(d1.freq, d1.phase_noise, label='SDR1')
plt.semilogx(d2.freq, d2.phase_noise, label='SDR2')
plt.semilogx(xsdfreq, xsd, label='Cross spectral density')
plt.grid(which='both')
plt.xlabel('Offset frequency (Hz)', size=16, fontname='Arial')
plt.ylabel('Phase noise (dBc/Hz)', size=16, fontname='Arial')
plt.legend(fontsize=12)
plt.show()

print('Number of averages: {}'.format(d1.num_pts//d1.fftpts))