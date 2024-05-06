import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from uncertainties import ufloat

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2

# Update rcParams with custom settings
plt.xlabel(r"$\theta$ $[\si{\degree}]$")
plt.ylabel(r"Counts")

# Load data from CSV files
theta1, counts1 = np.genfromtxt('../Daten/CSV_Output/Detektorscan.csv', delimiter=',', skip_header=1, unpack=True)
theta2, counts2 = np.genfromtxt('../Daten/CSV_Output/Detektorscan2.csv', delimiter=',', skip_header=1, unpack=True)

# Define theta ranges for plotting
_theta1 = np.linspace(theta1[0], theta1[-1], 1000)
_theta2 = np.linspace(theta2[0], theta2[-1], 1000)

# Define Gaussian function
def gauss(x, mean, stddev, amplitude):
    return amplitude * np.exp(-((x - mean) / stddev) ** 2 / 2)

# Perform curve fitting for both detectors
params1, pcov1 = curve_fit(gauss, theta1, counts1, p0=[-1, 1, 50000])
params2, pcov2 = curve_fit(gauss, theta2, counts2, p0=[-1, 1, 50000])

# Calculate parameter errors
errors1 = np.sqrt(np.diag(pcov1))
errors2 = np.sqrt(np.diag(pcov2))

# Create ufloat objects for parameters with errors
uparams1 = [ufloat(param, error) for param, error in zip(params1, errors1)]
uparams2 = [ufloat(param, error) for param, error in zip(params2, errors2)]

# Print fitted parameters for both detectors
print("Fitted parameters for detector 1:")
for uparam in uparams1:
    print(f"{uparam:.3e}")

print("\nFitted parameters for detector 2:")
for uparam in uparams2:
    print(f"{uparam:.3e}")

# Plot the data and fitted Gaussian functions for both detectors
plt.plot(theta1, counts1, "k.", label=r'Data')
plt.plot(_theta1, gauss(_theta1, *params1),"r-", label=r"Fitted Gaussian")
plt.legend()
plt.tight_layout()
plt.savefig("../Ressourcen/detektor1.pdf")
plt.clf()

plt.xlabel(r"$\theta$ $[\si{\degree}]$")
plt.ylabel(r"Counts")

plt.plot(theta2, counts2, "k.", label=r'Data')
plt.plot(_theta2, gauss(_theta2, *params2),"r-", label=r"Fitted Gaussian")
plt.legend()
plt.tight_layout()
plt.savefig("../Ressourcen/detektor2.pdf")
plt.clf()
