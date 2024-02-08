# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:56:43 2024

@author: asklodow
"""

#%% Importing libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, tukey

#%% Defining parameters

fs = 1+0 * 10**6  # sampling frequency, Hz
alpha = 0.5  # Tukey window parameter (0 for rectangular window, 1 for Hann window)

tappering_probe_signal = "yes" # "yes" or "no"

dur_pump = 11 * 10**-3  # seconds
f0_pump = 10 * 10**3  # start frequency, Hz
f1_pump = 50 * 10**3  # end frequency, Hz
t_pump = np.linspace(0, dur_pump, int(dur_pump * fs))

dur_probe = 0.2 * 10**-3  # seconds
f0_probe = 200 * 10**3  # start frequency, Hz
f1_probe = 800 * 10**3  # end frequency, Hz
t_probe = np.linspace(0, dur_probe, int(dur_probe * fs))
 
#%% Generate chirp signal

signal_pump = chirp(t_pump, f0_pump, dur_pump, f1_pump, method='linear')
signal_probe = chirp(t_probe, f0_probe, dur_probe, f1_probe, method='linear')

#%% taper for probe signal

# Calculate length of tapering region (1/4 of signal length)
taper_length = len(signal_probe) // 4
# Generate Tukey window
taper_window = tukey(len(signal_probe), alpha=alpha)

# # Generate tapering window
# taper_window = np.ones_like(signal_probe)
# taper_window[:taper_length] = np.linspace(0, 1, taper_length)  # Tapering at the beginning
# taper_window[-taper_length:] = np.linspace(1, 0, taper_length)  # Tapering at the end

# Apply tapering window to the signal
if tappering_probe_signal == "yes":
    signal_probe = signal_probe * taper_window


#%% Plot chirp signal 
fig, axs = plt.subplots(2,1, figsize = (10, 5))

#pump
ax = axs[0]
ax.plot(t_pump, signal_pump)
ax.set_title('Linear Chirp Signal - Pump')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.grid(True)


#probe
ax = axs[1]
ax.plot(t_probe, signal_probe, color = 'orange')
ax.set_title('Linear Chirp Signal - Probe')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.grid(True)

fig.tight_layout()
