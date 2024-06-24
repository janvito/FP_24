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

def linear_fit(x, m, b):
    return np.exp(b + m * np.log(x))

# Update rcParams with custom settings
plt.xlabel(r"$f$ $[\si{\hertz}]$")
plt.ylabel(r"$\frac{U_0}{U_i}$")
plt.yscale("log")
plt.xscale("log")

# Load data
f, U_i, U_0 = np.genfromtxt("../Daten/differentiator.csv", delimiter=",", unpack=True, skip_header=1)

# Calculate voltage ratio
U = U_0 / U_i

# Fit the curve for the data
params, cov = curve_fit(linear_fit, f, U)
errors = np.sqrt(np.diag(cov))
m = ufloat(params[0], errors[0])
b = ufloat(params[1], errors[1])

print(f"Fit parameters: m = {m}, b = {b}")

# Generate fit line
y = linear_fit(f, params[0], params[1])

# Plot the data and fit lines
plt.plot(f, U, "kx", label="Messdaten")
plt.plot(f, y, "r-", label="Ausgleichsgerade")

plt.legend()
plt.savefig("../Ressourcen/differentiator_plot.png")
plt.show()

# Calculate the ideal time constant
R = 100e3  # 10 kOhm
C = 22e-9  # 100 nF
tau = R * C
print(f"Ideal time constant (tau): {tau} s")

print(f"Ideal m: {np.log(tau)}")