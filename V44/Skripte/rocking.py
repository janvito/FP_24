import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from uncertainties import ufloat
from scipy.signal import find_peaks
import scipy.constants as c

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2

# Load data
theta, counts = np.genfromtxt('../Daten/CSV_Output/Rockingscan6_final2.csv', delimiter=',', skip_header=1, unpack=True)

# Plot data
plt.plot(theta, counts, label="rockingscan")

# Identify the peaks
peaks, _ = find_peaks(counts, height=1000)
print(peaks)
peak_positions = counts[peaks]
print(peak_positions)

# Define linear function
def linear_func(x, m, b):
    return m * x + b

# Highlight peaks on the plot
plt.plot(theta[peaks], counts[peaks], "rx")

# Fit the line to the data around the first peak
x_data = theta[peaks[0]:peaks[0]+11]
y_data = counts[peaks[0]:peaks[0]+11]
fit_params, covariance = curve_fit(linear_func, x_data, y_data, p0=[-1, 0])  # Initial guess for parameters: slope = -1, intercept = 0
errors = np.sqrt(np.diag(covariance))  # Extract standard deviations of fit parameters

# Extract fit parameters with uncertainties
slope = ufloat(fit_params[0], errors[0])
intercept = ufloat(fit_params[1], errors[1])

# Calculate the intersection with y=0 with uncertainties
intersection_x = -intercept / slope
print("Intersection with y=0:", intersection_x)

# Generate data for plotting the fitted line
x_lin = np.linspace(min(x_data), max(x_data), 1000)

# Plot the data and the fitted line
plt.plot(x_data, y_data, label="Data around peak")
plt.plot(x_lin, linear_func(x_lin, *fit_params), 'r--', label='Fitted Line')
plt.legend()
plt.xlabel(r'$\theta$ [\si{\degree}]')
plt.ylabel('Counts')

# Save the plot
plt.savefig("../Ressourcen/rocking.pdf")
plt.clf()
