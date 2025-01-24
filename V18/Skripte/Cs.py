import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from scipy.optimize import curve_fit

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)  # Sets the default font size for all plot elements

# Load the CSV file into a DataFrame
csv_file = '../Daten/137Caesium.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Find peaks in the spectrum
peaks, _ = find_peaks(df['Counts'], prominence=70)
df['Channel'] = df['Channel'] * 0.1032 - 0.8336

def Q(E):
    return 0.0901 * 0.9952**E + 0.0074

df['Counts'] = df['Counts'] / Q(df['Channel'])

# Plot 1: Original Spectrum with Peak Marked
plt.figure(figsize=(8, 6))
plt.plot(df['Channel'], df['Counts'], ".", color="black", alpha=0.05, label=r'Messdaten')
plt.plot(df['Channel'][peaks], df['Counts'][peaks], "rx", label=r'FEP')
plt.xlabel(r'E (keV)')
plt.ylabel(r'Counts')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.yscale('log')

# Save and show the original spectrum plot
output_plot_original = '137Caesium_original.png'
plt.savefig(output_plot_original, dpi=300)
plt.show()

# Extract the peak region (100 points around the detected peak)
peak_index = peaks[0]  # Assuming only one peak
start_index = max(peak_index - 50, 0)
end_index = min(peak_index + 50, len(df) - 1)

# Subset the data around the peak
df_peak = df.iloc[start_index:end_index]

# Define the Gaussian function
def gaussian(E, N, mu, sigma, b):
    return N / (np.sqrt(2 * np.pi * sigma**2)) * np.exp(-0.5 * ((E - mu) / sigma) ** 2) + b

# Perform the curve fitting
initial_guess = [df_peak['Counts'].max(), df_peak['Channel'].mean(), 1, df_peak['Counts'].min()]
params, covariance = curve_fit(gaussian, df_peak['Channel'], df_peak['Counts'], p0=initial_guess)

# Extract fitted parameters
N_fit, mu_fit, sigma_fit, b_fit = params

# Generate the fitted curve
x_fit = np.linspace(df_peak['Channel'].min(), df_peak['Channel'].max(), 500)
y_fit = gaussian(x_fit, N_fit, mu_fit, sigma_fit, b_fit)

# Plot 2: Gaussian Fit Only
plt.figure(figsize=(8, 6))
plt.plot(df_peak['Channel'], df_peak['Counts'], "k.", alpha=0.7, label=r'Messdaten')
plt.plot(x_fit, y_fit, "b-", label=r'Gaussian Fit')
plt.xlabel(r'E (keV)')
plt.ylabel(r'Counts')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.yscale('linear')

# Print results
print(f"Fitted Parameters: N = {N_fit:.3f}, mu = {mu_fit:.3f}, sigma = {sigma_fit:.3f}, b = {b_fit:.3f}")
print(f"Original spectrum saved to: {output_plot_original}")
# Calculate FWHM and TWHM
FWHM = 2 * np.sqrt(2 * np.log(2)) * sigma_fit
TWHM = 2 * np.sqrt(2 * np.log(10)) * sigma_fit

# Ratio of FWHM to TWHM
ratio = FWHM / TWHM

# Print the results
print(f"FWHM: {FWHM:.3f} keV")
print(f"TWHM: {TWHM:.3f} keV")
print(f"Verhältnis (FWHM/TWHM): {ratio:.3f}")
# Calculate the heights for FWHM and TWHM
half_max = N_fit / (np.sqrt(2 * np.pi * sigma_fit**2)) / 2
tenth_max = N_fit / (np.sqrt(2 * np.pi * sigma_fit**2)) / 10

# Calculate the bounds for FWHM and TWHM
FWHM_left = mu_fit - FWHM / 2
FWHM_right = mu_fit + FWHM / 2

TWHM_left = mu_fit - TWHM / 2
TWHM_right = mu_fit + TWHM / 2

# Add FWHM and TWHM to the plot
plt.axhline(y=half_max, color='green', linestyle='--', label=r'FWHM Höhe')
plt.axhline(y=tenth_max, color='orange', linestyle='--', label=r'TWHM Höhe')
plt.plot([FWHM_left, FWHM_right], [half_max, half_max], 'g-', label=r'FWHM Breite')
plt.plot([TWHM_left, TWHM_right], [tenth_max, tenth_max], 'orange', label=r'TWHM Breite')

# Update the legend
plt.legend()

# Save and show the Gaussian fit plot
output_plot_fit = '137Caesium_gaussian_fit_only.png'
plt.savefig(output_plot_fit, dpi=300)
plt.show()

# Maximalwert der Fit-Funktion
max_value = N_fit / (np.sqrt(2 * np.pi * sigma_fit**2))
half_max = max_value / 2
tenth_max = max_value / 10

# Find the closest index to half_max
half_max_index = (df_peak['Counts'] - half_max).abs().idxmin()

# Find the closest index to tenth_max
tenth_max_index = (df_peak['Counts'] - tenth_max).abs().idxmin()

# Get the channel values for FWHM and TWHM
FWHM_channel_left = df_peak.loc[:half_max_index, 'Channel'].min()
FWHM_channel_right = df_peak.loc[half_max_index:, 'Channel'].max()
FWHM_actual = FWHM_channel_right - FWHM_channel_left

TWHM_channel_left = df_peak.loc[:tenth_max_index, 'Channel'].min()
TWHM_channel_right = df_peak.loc[tenth_max_index:, 'Channel'].max()
TWHM_actual = TWHM_channel_right - TWHM_channel_left

# Results
print(f"FWHM (tatsächlich): {FWHM_actual:.3f} keV")
print(f"TWHM (tatsächlich): {TWHM_actual:.3f} keV")
if FWHM_actual and TWHM_actual:
    print(f"Verhältnis (FWHM/TWHM): {FWHM_actual / TWHM_actual:.3f}")
