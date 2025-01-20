import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Load the CSV file into a DataFrame
csv_file = '../Daten/152Europium.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Find peaks in the spectrum
peaks, _ = find_peaks(df['Counts'], prominence=22)

# Known emission energies of 152Europium (in keV)
emission_energies = [121.7824, 244.6989, 344.2811, 411.126, 443.965, 778.903, 867.390, 964.055, 1085.842, 1089.767, 1112.087, 1212.970, 1299.152, 1408.022]
intensities = [0.2837, 0.0753, 0.2657, 0.02238, 0.03125, 0.1297, 0.04214, 0.1463, 0.1013, 0.01731, 0.1354, 0.01412, 0.01626, 0.2085]  # Based on table

# Create a figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
plt.subplots_adjust(hspace=0.3)  # Adjust space between plots

# Plot the spectral data (Top subplot)
axs[0].plot(df['Channel'], df['Counts'], "-", color="black", alpha=0.5, label=r'\textbf{Spectral Data}')
axs[0].plot(df['Channel'][peaks], df['Counts'][peaks], "rx", label=r'\textbf{Peaks}')
axs[0].set_title(r'$^{152}$Europium Spektrum', fontsize=14)
axs[0].set_xlabel(r'\textbf{Channel}', fontsize=12)
axs[0].set_ylabel(r'\textbf{Counts}', fontsize=12)
axs[0].grid(True, linestyle='--', alpha=0.7)
axs[0].legend(fontsize=12)
axs[0].set_yscale('log')

# Plot the emission energies (Bottom subplot)
axs[1].stem(emission_energies, intensities, basefmt=" ", linefmt='k-', markerfmt='', label=r'\textbf{Emission Energies}')
axs[1].set_title(r'$^{152}$Europium Emissions-Energien', fontsize=14)
axs[1].set_xlabel(r'\textbf{E (keV)}', fontsize=12)
axs[1].set_ylabel(r'\textbf{I}', fontsize=12)
axs[1].grid(True, linestyle='--', alpha=0.7)
axs[1].legend(fontsize=12)

# Save and show the combined plot
output_plot = '152Europium_with_emission.png'  # Replace with the desired path for saving the plot
plt.savefig(output_plot, dpi=300)  # Save the plot as a PNG file with high resolution
plt.show()  # Display the plot
print(f"Channel Peaks: {df['Channel'].values[peaks]}")
print(f"Plot saved to: {output_plot}")



