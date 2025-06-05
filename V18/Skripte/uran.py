import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)  # Default font size for all plot elements

# ------------------------------------------------------------------------------
# 1. Load the Uranium spectrum data
# ------------------------------------------------------------------------------
csv_file = '../Daten/Uran.csv'  # Adjust the path to your CSV file if necessary
df = pd.read_csv(csv_file)
df['Energy'] = df['Channel'] * 0.1032 - 0.8336  # Calibration: Channel -> Energy (keV)

def Q(E):
    return 0.0901 * 0.9952**E + 0.0074

df['Counts'] = df['Counts'] / Q(df['Energy'])

# ------------------------------------------------------------------------------
# 2. Find peaks in the spectrum
# ------------------------------------------------------------------------------
peaks, _ = find_peaks(df['Counts'][:-200], prominence=5000)
print("Detected peak energies (keV):")
for val in df['Energy'][peaks].values:
    print(f"{val:.3f}", end=", ")
print("")

# ------------------------------------------------------------------------------
# 3. Load emission data from provided files using ndmin=2 to ensure 2D arrays
# ------------------------------------------------------------------------------
ra_data = np.loadtxt('../Daten/ra-lit.txt', comments='#', ndmin=2)
pb_data = np.loadtxt('../Daten/pb-lit.txt', comments='#', ndmin=2)
k_data  = np.loadtxt('../Daten/k-lit.txt', comments='#', ndmin=2)
bi_data = np.loadtxt('../Daten/bi-lit.txt', comments='#', ndmin=2)

# Unpack the data (each file contains two columns: Energy, Probability)
ra_energies, ra_probs = ra_data[:, 0], ra_data[:, 1]
pb_energies, pb_probs = pb_data[:, 0], pb_data[:, 1]
k_energies,  k_probs  = k_data[:, 0],  k_data[:, 1]
bi_energies, bi_probs = bi_data[:, 0], bi_data[:, 1]

# ------------------------------------------------------------------------------
# 4. Create a figure with two subplots
# ------------------------------------------------------------------------------
fig, axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
plt.subplots_adjust(hspace=0.3)  # Adjust space between plots

# ------------------------------------------------------------------------------
# 5. Top Subplot: Uranium Spectrum
# ------------------------------------------------------------------------------
axs[0].plot(df['Energy'], df['Counts'], "k.", alpha=0.05, label='Data')
axs[0].plot(df['Energy'][peaks], df['Counts'][peaks], "rx", label='Peaks')
axs[0].set_xlabel(r'Energy (keV)')
axs[0].set_ylabel(r'Counts')
axs[0].set_yscale("log")
axs[0].grid(True, linestyle='--', alpha=0.7)
axs[0].legend(loc="upper right")

# ------------------------------------------------------------------------------
# 6. Bottom Subplot: Emission Energies & Intensities
# ------------------------------------------------------------------------------
axs[1].stem(ra_energies, ra_probs, linefmt='r-', basefmt=' ',
            label=r'$^{226}\mathrm{Ra}$')
axs[1].stem(pb_energies, pb_probs, linefmt='g-', basefmt=' ',
            label=r'$^{214}\mathrm{Pb}$')
axs[1].stem(bi_energies, bi_probs, linefmt='b-', basefmt=' ',
            label=r'$^{214}\mathrm{Bi}$')
axs[1].stem(k_energies,  k_probs,  linefmt='m-', basefmt=' ',
            label=r'$^{40}\mathrm{K}$')
axs[1].set_xlim(left=-45, right=df['Energy'].max()+40)
axs[1].set_xlabel('Energy (keV)')
axs[1].set_ylabel('I')

axs[1].grid(True, linestyle='--', alpha=0.7)
axs[1].legend(loc="upper center", bbox_to_anchor=(0.55, 1.0))

plt.tight_layout()
output_plot = "Uran_with_emission_energies.png"
plt.savefig(output_plot, dpi=300)

print(f"Plot saved to: {output_plot}")
