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
plt.figure(figsize=(10, 6))
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
plt.clf()
# Extract the peak region (100 points around the detected peak)
peak_index = peaks[0]  # Assuming only one peak
start_index = max(peak_index - 120, 0)
end_index = min(peak_index + 120, len(df) - 1)

# Subset the data around the peak
df_peak = df.iloc[start_index:end_index]
df_peak = df_peak.reset_index(drop=True)

# Define the Gaussian function
def gaussian(E, N, mu, sigma, b):
    return N / (np.sqrt(2 * np.pi * sigma**2)) * np.exp(-0.5 * ((E - mu) / sigma) ** 2) + b

# Perform the curve fitting
initial_guess = [df_peak['Counts'].max(), df_peak['Channel'].mean(), 1, df_peak['Counts'].min()]
params, covariance = curve_fit(gaussian, df_peak['Channel'], df_peak['Counts'], p0=initial_guess)

# Extract fitted parameters
N_fit, mu_fit, sigma_fit, b_fit = params
uncertainties = np.sqrt(np.diag(covariance))
# Generate the fitted curve
x_fit = np.linspace(df_peak['Channel'].min(), df_peak['Channel'].max(), 500)
y_fit = gaussian(x_fit, N_fit, mu_fit, sigma_fit, b_fit)

for v,u in zip(params,uncertainties):
    print(f"{v:.3f}, {u:.3f}")
# Plot 2: Gaussian Fit Only
plt.figure(figsize=(8, 6))
plt.plot(df_peak['Channel'], df_peak['Counts'], "k.", alpha=0.5, label=r'Messdaten')
plt.plot(x_fit, y_fit, "r-", label=r'Gaussian Fit')
plt.xlabel(r'E (keV)')
plt.ylabel(r'Counts')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.yscale('linear')

# Print results
print(f"Fitted Parameters: N = {N_fit:.3f}, mu = {mu_fit:.3f}, sigma = {sigma_fit:.3f}, b = {b_fit:.3f}")
print(f"Original spectrum saved to: {output_plot_original}")
# Calculate FWHM and TWHM
FWHM = 2 * np.sqrt(2 * np.log(2))
TWHM = 2 * np.sqrt(2 * np.log(10))
print(f"Theoretical ratio: {TWHM/FWHM}")

# Calculate the peak height (subtracting the background)
peak_height = gaussian(mu_fit, N_fit, mu_fit, sigma_fit, b_fit) - b_fit

# Calculate half-maximum and tenth-maximum heights
half_max = peak_height / 2 + b_fit
tenth_max = peak_height / 10 + b_fit

# Find nearest indices for FWHM
half_max_left_idx = np.argmin(np.abs(y_fit[:len(y_fit)//2] - half_max))  # Left side
half_max_right_idx = np.argmin(np.abs(y_fit[len(y_fit)//2:] - half_max)) + len(y_fit)//2  # Right side

# Find nearest indices for TWHM
tenth_max_left_idx = np.argmin(np.abs(y_fit[:len(y_fit)//2] - tenth_max))  # Left side
tenth_max_right_idx = np.argmin(np.abs(y_fit[len(y_fit)//2:] - tenth_max)) + len(y_fit)//2  # Right side

plt.hlines(half_max, xmin=x_fit[half_max_left_idx], xmax=x_fit[half_max_right_idx], colors='blue', linestyles='--', label=r'FWHM')
plt.hlines(tenth_max, xmin=x_fit[tenth_max_left_idx], xmax=x_fit[tenth_max_right_idx], colors='green', linestyles='--', label=r'FWTM')

actual_half_max_left_idx = np.argmin(np.abs(df_peak['Counts'][:len(df_peak['Counts'])//2] - half_max))  # Left side
actual_half_max_right_idx = np.argmin(np.abs(df_peak['Counts'][len(df_peak['Counts'])//2:] - half_max)) + len(df_peak['Counts'])//2  # Right side
# Find nearest indices for TWHM
actual_tenth_max_left_idx = np.argmin(np.abs(df_peak['Counts'][:len(df_peak['Counts'])//2] - tenth_max))  # Left side
actual_tenth_max_right_idx = np.argmin(np.abs(df_peak['Counts'][len(df_peak['Counts'])//2:] - tenth_max)) + len(df_peak['Counts'])//2  # Right side

plt.plot(df_peak['Channel'][actual_half_max_left_idx], df_peak['Counts'][actual_half_max_left_idx], "b.", alpha=0.5)
plt.plot(df_peak['Channel'][actual_half_max_right_idx], df_peak['Counts'][actual_half_max_right_idx], "b.", alpha=0.5)
plt.plot(df_peak['Channel'][actual_tenth_max_left_idx],  df_peak['Counts'][actual_tenth_max_left_idx], "g.", alpha=0.5)
plt.plot(df_peak['Channel'][actual_tenth_max_right_idx], df_peak['Counts'][actual_tenth_max_right_idx], "g.", alpha=0.5)

actual_FWHM=df_peak['Channel'][actual_half_max_right_idx]-df_peak['Channel'][actual_half_max_left_idx]
actual_FWTM=df_peak['Channel'][actual_tenth_max_right_idx]-df_peak['Channel'][actual_tenth_max_left_idx]

print(f"actual FWHM: {df_peak['Channel'][actual_half_max_right_idx]-df_peak['Channel'][actual_half_max_left_idx]}")
print(f"actual FWTM: {df_peak['Channel'][actual_tenth_max_right_idx]-df_peak['Channel'][actual_tenth_max_left_idx]}")
print(f"actual ratio: {actual_FWTM/actual_FWHM}")
plt.legend()
plt.savefig("137Caesium_with_Gaussian.png", dpi=300)

# Calculate background subtracted counts in the peak region
counts_subtracted = df_peak['Counts'] - b_fit
