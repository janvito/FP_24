import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2
plt.xlabel(r"$\theta$ $[\si{\degree}]$")
plt.ylabel(r"Counts")

def parratt(a_i, del2, del3, sig1, sig2, b2, b3, d2):
    a_irad = np.deg2rad(a_i)
    k = 2 * np.pi / lamda

    n2 = 1 - del2 + b2 * 1j
    n3 = 1 - del3 + b3 * 1j

    kz1 = k * np.sqrt(1 - np.cos(a_irad) ** 2)
    kz2 = k * np.sqrt(n2 ** 2 - np.cos(a_irad) ** 2)
    kz3 = k * np.sqrt(n3 ** 2 - np.cos(a_irad) ** 2)

    rauigkeit1 = np.exp(-2 * kz1 * kz2 * sig1 ** 2)
    rauigkeit2 = np.exp(-2 * kz2 * kz3 * sig2 ** 2)

    r12 = (kz1 - kz2) / (kz1 + kz2) * rauigkeit1
    r23 = (kz2 - kz3) / (kz2 + kz3) * rauigkeit2

    x2 = np.exp(-2j * kz2 * d2) * r23
    x1 = (r12 + x2) / (1 + r12 * x2)

    return np.log(np.abs(x1) ** 2)

def custom_loss_function(params, x, y):
    model_values = parratt(x, *params)
    absolute_distances = np.abs(y - model_values)
    return np.sum(absolute_distances)  # Sum of absolute distances as loss

# Load data
theta, counts = np.genfromtxt('../Daten/CSV/probenscan_clean.csv', delimiter=',', unpack=True)
theta, counts = theta[15:], counts[15:]
counts = np.log(counts)
layer_thickness = 1.7e-9
layer_thickness2 = 6.819180819180819e-08
lamda = 1.5 * 10**(-10)
initial_guess1 = np.array([6.69143022e-06, 6.63675964e-06, 8.60667821e-10, 5.58822780e-10, -2.25500661e-07, -1.20162786e-06, 7.70159198e-08])#von komplizierteren Fit methode mit manuell angepassten parametern

# Minimize the custom loss function
result = minimize(custom_loss_function, initial_guess1, args=(theta, counts), method='Nelder-Mead')

# Plotting
plt.plot(theta, counts, label='Data')
#plt.plot(theta, parratt(theta, *result.x), label='Nelder-Mead Fit')
plt.plot(theta,parratt(theta,*initial_guess1),label="Initial Guess")
plt.legend()
plt.savefig("../Ressourcen/parratt.pdf")
plt.show()

result=[ 6.14347584e-06, 5.39605945e-06, 7.78018779e-10, 8.74693431e-10, -7.42206653e-08, -1.02411491e-06, 7.73171086e-08 ]
initial_guess = [6.69143022e-06, 6.63675964e-06, 8.60667821e-10, 5.58822780e-10, -2.25500661e-07, -1.20162786e-06, 7.70159198e-08]
