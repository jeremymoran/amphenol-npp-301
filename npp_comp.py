# NPP Compensation Resistor Determination
# Version 2.1
# Release Notes:
#
# V1.0
# - Basic funtionality to determine compensation resistance.
# - Bridge input voltage is hard-coded in script
#
# V2.0
# - Modified so resistor values are read in from a TAB delimited file, more
# suitable for large batches of gauges.
#
# V2.1
# Compensation branch included in output
#
# V2.2
# Improved funcitionality with varying length input files. Fixed errors.
# Preamble
#
# V2.3
# Converted to Python3

import numpy as np

# Load Assets
resval = np.array([0, 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 31, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91, 100, 110, 120, 130, 150, 160, 180, 200])
resval = resval.flatten()
Rdata = np.genfromtxt('weston-k-ramjet-10-24.txt', skip_header=1)
Rheader = np.genfromtxt('weston-k-ramjet-10-24.txt', dtype=str, max_rows=1)



Vin = 5

# Initialize output array
RcompVal = np.zeros((Rdata.shape[1], 2))


# Since numpy is a pain and needs to know if its 1D or 2D, we need to do this
if len(Rdata .shape) == 1:
    nAmphenols = 1
else:
    nAmphenols = Rdata .shape[1]
print("Number of Amphenols: %i" % nAmphenols)

# Determine Current Bridge Values
for j in range(nAmphenols):
    if nAmphenols == 1:
        hexVal = Rheader
        rp8_2 = Rdata[0]
        rp8_6 = Rdata[1]
        rp2_4 = Rdata[2]
        rp6_5 = Rdata[3]
    else:
        hexVal = Rheader[j]
        rp8_2 = Rdata[0, j]
        rp8_6 = Rdata[1, j]
        rp2_4 = Rdata[2, j]
        rp6_5 = Rdata[3, j]

    # Calculate output voltages for a range of compensation resistor values
    
    Vb_824 = np.zeros(len(resval))
    Vb_865 = np.zeros(len(resval))
    for i in range(len(resval)):
        Vb_824[i] = Vin * ((rp2_4 + resval[i]) / (rp8_2 + (rp2_4 + resval[i])) - rp6_5 / (rp8_6 + rp6_5))
        Vb_865[i] = Vin * ((rp6_5 + resval[i]) / (rp8_6 + (rp6_5 + resval[i])) - rp2_4 / (rp8_2 + rp2_4))

    # Find value and index of minimum bridge voltage
    Vb_824_min = np.min(np.abs(Vb_824))
    idx1 = np.where(np.abs(Vb_824) == Vb_824_min)[0]
    Vb_865_min = np.min(np.abs(Vb_865))
    idx2 = np.where(np.abs(Vb_865) == Vb_865_min)[0]

    if Vb_824_min < Vb_865_min:
        Leg = 824
        RcompVal[j, 0] = resval[idx1[0]]
        idx = idx1[0]
        Vb_min = Vb_824_min
    else:
        Leg = 865
        RcompVal[j, 1] = resval[idx2[0]]
        idx = idx2[0]
        Vb_min = Vb_865_min

    # Present output to user
    print('\n------')
    print('AMPHENOL %s' % hexVal)
    print('------')
    print('Input Voltage: %.2f V' % Vin)
    print('Suggested Compensation Resistance: %i Ohms' % resval[idx])
    print('Compensation on Leg: %i' % Leg)
    print('Vb: %.2f mV' % (Vb_min*1e3))
