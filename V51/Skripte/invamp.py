import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
from uncertainties import ufloat
# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 22
plt.rcParams['lines.linewidth'] = 2

def fit(x, m, b):
    return np.exp(b + m * np.log(x))

# Update rcParams with custom settings
plt.xlabel(r"$f$ $[\si{\hertz}]$")
plt.ylabel(r"$\frac{U_0}{U_i}$")
plt.yscale("log")
plt.xscale("log")

# Load data
f, U_0, U_i, phi = np.genfromtxt("../Daten/invamp.csv", delimiter=",", unpack=True, skip_header=1)

# Calculate voltage ratio
U = U_0 / U_i

# Fit the curve for the higher frequencies
params, cov = curve_fit(fit, f[9:], U[9:])
upar = [params, np.sqrt(np.diag(cov))]
print("params: ", *upar)

# Calculate mean and standard deviation for the lower frequencies
Umean = [U[:9].mean(), U[:9].std()]
print("Umean: ", Umean)

# Generate fit line
y = fit(f, *params)

# Plot the data and fit lines
plt.plot(f, U, "kx", label="Messdaten")
plt.plot(f[9:], y[9:], "r-", label="Ausgleichsgerade")
plt.plot(f[:9], np.ones(9) * Umean[0], "b-", label="Gemitteltes Spannungsverhältnis")

# Add shaded area for uncertainty of the mean
plt.fill_between(f[:9], (np.ones(9) * (Umean[0] - Umean[1])), (np.ones(9) * (Umean[0] + Umean[1])), color='b', alpha=0.2, label=r"Unsicherheit des Mittelwerts")

plt.legend()
plt.savefig("../Ressourcen/invamp_plot.png")
# Calculate the cutoff frequency
cutoff_gain = Umean[0] / np.sqrt(2)

# Interpolate to find the frequency where the gain is equal to cutoff_gain
from scipy.interpolate import interp1d

interpolator = interp1d(U[9:], f[9:], kind='linear', bounds_error=False, fill_value="extrapolate")
cutoff_frequency = interpolator(cutoff_gain)
cutoff_frequency1 = interpolator(cutoff_gain + Umean[1] / np.sqrt(2))
cutoff_frequency2 = interpolator(cutoff_gain - Umean[1] / np.sqrt(2))
ucutoff = ufloat(cutoff_frequency,cutoff_frequency2-cutoff_frequency)
print("Cutoff Frequency (Grenzfrequenz):", cutoff_frequency)
print(f"Cutoff Frequency (Grenzfrequenz): {ucutoff:.2f}")
Umean = ufloat(Umean[0],Umean[1])
bandwidthp= ucutoff * Umean
print(f"band: {bandwidthp:.2f}")