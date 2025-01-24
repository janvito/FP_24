import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)  # Sets the default font size for all plot elements

# Load the CSV file into a DataFrame
csv_file = '../Daten/152Europium.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)
df['Channel']=df['Channel']*0.1032-0.8336
peaks = [121.7824, 244.6989, 344.2811, 411.126, 443.965, 778.903, 867.390, 964.055, 1085.842, 1089.767, 1112.087, 1212.970, 1299.152, 1408.022]
peak=121.5616
index = (df['Channel'] - peak).abs().idxmin()
import numpy as np

# Define Gaussian function
def gaussian(x, A, mu, sigma,b):
    return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)+b

# Extract the range of data around the peak
x_data = df['Channel'][index-50:index+50]
y_data = df['Counts'][index-50:index+50]

# Perform Gaussian fit
popt, pcov = curve_fit(gaussian, x_data, y_data, p0=[max(y_data), peak, 1,10])  # Initial guesses

# Extract fit parameters
A, mu, sigma, b = popt
print(f"Fit parameters: A = {A:.2f}, mu = {mu:.2f}, sigma = {sigma:.2f}")

# Generate Gaussian curve for plotting
x_fit = np.linspace(x_data.min(), x_data.max(), 500)
y_fit = gaussian(x_fit, *popt)

# Plot the data and the fit
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, "k.", alpha=0.5, label='Data')
plt.plot(x_fit, y_fit, "r-", label='Gaussian Fit')
plt.title(r'Gaussian Fit Around Peak')
plt.xlabel(r'Channel')
plt.ylabel(r'Counts')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
output_plot = "fep.png"
plt.savefig(output_plot, dpi=300)
plt.show()

print(f"Plot saved to: {output_plot}")

plt.clf()

# Peak positions and other constants
peaks = [122.3952, 245.4096, 345.1008, 411.9744, 444.9984, 779.3664]
W = np.array([0.2837, 0.0753, 0.2657, 0.02238, 0.03125, 0.1297])  # Based on table
Activity = 1233

# Calculate Gaussian areas
areas = []
for peak in peaks:
    index = (df['Channel'] - peak).abs().idxmin()
    x_data = df['Channel'][index - 50:index + 50]
    y_data = df['Counts'][index - 50:index + 50]

    popt, _ = curve_fit(gaussian, x_data, y_data, p0=[max(y_data), peak, 1, 10])
    A, mu, sigma, b = popt
    area = A * sigma * np.sqrt(2 * np.pi)
    areas.append(area)

# Create DataFrame for areas and calculate Q
areas_df = pd.DataFrame({'Energy (keV)': peaks, 'Area': areas})
areas_df['Q'] = areas_df['Area'] / (Activity * W * 2700) * (1 / 0.01665)




# Save or display the DataFrame
output_csv = "areas_and_Q.csv"
areas_df.to_csv(output_csv, index=False)
print(f"Results saved to: {output_csv}")
print(areas_df)

# Define the Q function for fitting
def Q(x, a, b, c):
    return a * b**x + c

# Fit the Q function to the data
Qparams, _ = curve_fit(Q, areas_df['Energy (keV)'], areas_df['Q'], p0=[0.2, 0.99, 0.01])
print(f"Q Fit Parameters: a = {Qparams[0]:.4f}, b = {Qparams[1]:.4f}, c = {Qparams[2]:.4f}")

# Generate a smooth curve for Q fit using linspace
x_fit = np.linspace(areas_df['Energy (keV)'].min(), areas_df['Energy (keV)'].max(), 500)
y_fit = Q(x_fit, *Qparams)

# Plot Q vs Energy with the fit curve
plt.figure(figsize=(8, 6))
plt.plot(areas_df['Energy (keV)'], areas_df['Q'], 'k.', label=r'Berechnete Vollenergienachweis-Wahrscheinlichkeit')
plt.plot(x_fit, y_fit, 'r-', label=r'Bestimmte Ausgleichsfunktion')
plt.xlabel(r'Energy (keV)')
plt.ylabel(r'$Q$')
plt.title(r'Q Function vs Energy')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Save the plot
output_plot = "Qfunc.png"
plt.savefig(output_plot, dpi=300)
plt.show()

print(f"Plot saved to: {output_plot}")
