import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import numpy as np

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)  # Sets the default font size for all plot elements

# Load the CSV file into a DataFrame
csv_file = '../Daten/152Europium.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)
df['Channel'] = df['Channel'] * 0.1032 - 0.8336

# Define Q(E) function
def Q(E):
    return 0.0901 * 0.9952**E + 0.0074

df['Counts'] = df['Counts'] / Q(df['Channel'])

# Known emission energies of 152Europium (in keV)
emission_energies = [121.7824, 244.6989, 344.2811, 411.126, 443.965, 778.903]
intensities = [0.2837, 0.0753, 0.2657, 0.02238, 0.03125, 0.1297]  # Based on table

# Find peaks in the spectrum closest to the known emission energies
closest_peaks = []
for energy in emission_energies:
    idx = (df['Channel'] - energy).abs().idxmin()
    closest_peaks.append(idx)

# Define Gaussian function
def gaussian(x, A, mu, sigma, b):
    return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2) + b

# Create a figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1]})
plt.subplots_adjust(hspace=0.3)

# Top subplot: spectral data with Gaussian fits
axs[0].plot(df['Channel'], df['Counts'], ".", color="black", alpha=0.1, label=r'Messdaten')

gaussian_fits = []
for idx, energy in zip(closest_peaks, emission_energies):
    # Extract data around the peak
    x_data = df['Channel'][idx - 50:idx + 50]
    y_data = df['Counts'][idx - 50:idx + 50]

    # Perform Gaussian fit
    try:
        popt, _ = curve_fit(gaussian, x_data, y_data, p0=[max(y_data), energy, 1, 10])
        A, mu, sigma, b = popt
        gaussian_fits.append((mu, A, sigma, b))

        # Generate Gaussian curve
        x_fit = np.linspace(x_data.min(), x_data.max(), 500)
        y_fit = gaussian(x_fit, *popt)

        # Plot Gaussian
        axs[0].plot(x_fit, y_fit, "r-")

    except RuntimeError:
        print(f"Gaussian fit failed for peak at {energy} keV.")

axs[0].set_title(r'$^{152}$Europium Spektrum mit Gauß-Fits')
axs[0].set_xlabel(r'E (keV)')
axs[0].set_ylabel(r'Counts')
axs[0].set_yscale('log')
axs[0].grid(True, linestyle='--', alpha=0.7)
axs[0].legend(loc='upper right', fontsize=10)

# Bottom subplot: known emission energies
axs[1].stem(emission_energies, intensities, basefmt=" ", linefmt='k-', markerfmt='')
axs[1].set_title(r'$^{152}$Europium Emissions-Energien')
axs[1].set_xlabel(r'E (keV)')
axs[1].set_ylabel(r'I')
axs[1].grid(True, linestyle='--', alpha=0.7)
axs[1].set_xlim(axs[0].get_xlim())  # Set x-limits of the bottom subplot to match the top subplot
axs[1].set_yscale('log')
# Save the combined plot
output_plot = "152Europium_with_Gaussians_and_Energies.png"
plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.show()

print(f"Plot saved to: {output_plot}")
