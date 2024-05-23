import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2

plt.xlabel(r"$\theta$ $[\si{\degree}]$")
plt.ylabel(r"$X_1=\frac{R_1}{T_1}$")
#plt.yscale("log")

def parratt(a_i, del2, del3, sig1, sig2, b2, b3, d2):
    a_irad = np.deg2rad(a_i)
    k = 2 * np.pi / lamda

    n2 = 1 - del2 - b2 * 1j
    n3 = 1 - del3 - b3 * 1j

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

# Load data
theta, counts = np.genfromtxt('../Daten/CSV/probenscan_clean.csv', delimiter=',', unpack=True)
theta, counts = theta[15:70], counts[15:70]
counts = np.log(counts)

layer_thickness = 1.7e-9
layer_thickness2 = 6.819180819180819e-08
lamda = 1.54 * 10**(-10)
initial_guess1 = np.array([7.6e-06, 3.8e-06, 1.8963141350166085e-09, 3.4233238181111846e-09, 1.03e-7, 4.81e-9, 6.8e-8])
initial_guess1 = np.array([7.799569703317446e-06 ,3.6e-06 ,2.335367669708172e-09 ,1.285087370068476e-09 ,2.575904416440772e-07 ,4.678954680735597e-09 ,5.027821952764016e-08])
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
print(initial_guess1)

# Define bounds for the parameters (all positive)
lower_bounds = [7.5e-6,3.6e-6,1e-9,1e-9,0.5e-7,1e-9,layer_thickness/10]
upper_bounds = [8.5e-6,5.6e-6,9e-9,9e-9,3e-7,9e-9,layer_thickness*1000]

params, _ = curve_fit(parratt, theta, counts, p0=initial_guess1, bounds=(lower_bounds, upper_bounds), maxfev=50000)

plt.plot(theta,counts,label=r"Messdaten")
plt.plot(theta,parratt(counts,*params),label=r"Parratt-Reflektivität")
plt.show()
for i, ax in enumerate(axes.flatten()):
    lowest = 3
    best_params = None
    for k in range(200):
        # Gaussian perturbation
        perturbed_guess = np.copy(initial_guess1)
        for j, guess in enumerate(initial_guess1):
            perturbed_guess[j] = np.abs(np.random.normal(guess, abs(guess) * 0.001))
        try:
            params, _ = curve_fit(parratt, theta, counts, p0=perturbed_guess, bounds=(lower_bounds, upper_bounds), maxfev=50000)
        except Exception as e:
            print("Error: ", e)
            continue

        errors = counts - parratt(theta, *params)
        valid_indices = np.logical_and(np.isfinite(errors), ~np.isnan(errors))
        squared_errors = errors[valid_indices] ** 2
        mse = np.sum(squared_errors)
        
        if mse < lowest and mse != 0:
            lowest = mse
            best_params = params

    if best_params is not None:
        ax.cla()  # Clear the axes
        ax.plot(theta, counts, label="data")
        ax.plot(theta, parratt(theta, *best_params), label="fit")
        ax.set_title(f"Iteration {i+1}")
        ax.set_xlabel(r"$\theta$ $[\si{\degree}]$")
        ax.set_ylabel(r"$X_1=\frac{R_1}{T_1}$")
        ax.grid(True)
        ax.legend()

        print(f"{i}: ", end="")
        for par in best_params:
            print(f"{par:.15e}", ",", end="")
        print(f"\tms: {lowest}")

plt.show()
#plt.plot(theta,counts,label=r"Messdaten")
#plt.plot(theta,parratt(theta,*initial_guess1),label=r"Parratt-Reflektivität")
#plt.legend()
#plt.tight_layout()
#plt.savefig("../Ressourcen/parratt.png")
