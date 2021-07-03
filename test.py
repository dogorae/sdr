import sdrdata
import matplotlib.pyplot as plt

FILEPATH1 = 'SDR1_ch0.bin'
FSAMPLE1 = 100
FILEPATH2 = 'SDR2_ch0.bin'
FSAMPLE2 = 100
FFTPTS = 1*32*128

d1 = sdrdata.Dataset(FILEPATH1, FSAMPLE1, FFTPTS)
d2 = sdrdata.Dataset(FILEPATH2, FSAMPLE2, FFTPTS) 
xsdfreq, xsd = d1.xspec_with(d2)

plt.semilogx(d1.freq, d1.phase_noise, label='SDR1')
plt.semilogx(d2.freq, d2.phase_noise, label='SDR2')
plt.semilogx(xsdfreq, xsd, label='Cross spectral density')
plt.grid(which='both')
plt.xlabel('Offset frequency (Hz)', size=16, fontname='Arial')
plt.ylabel('Phase noise (dBc/Hz)', size=16, fontname='Arial')
plt.legend(fontsize=14)
plt.show()
