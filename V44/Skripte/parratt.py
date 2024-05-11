import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import minimize
import random

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
theta, counts = theta[15:100], counts[15:100]
_theta=np.linspace(theta[0],theta[-1],1000)
counts = np.log(counts)
layer_thickness = 1.7e-9
layer_thickness2 = 6.819180819180819e-08
lamda = 1.54 * 10**(-10)
initial_guess1 = np.array([7.648577896993004e-06 ,0.0012410968451660746 ,1.8963141350166085e-09 ,3.4233238181111846e-08 ,3.643402232484923e-07*1.5*1.3 ,1.0573950235770515e-05*0.9 ,2.416951357029224e-06])
initial_guess1 = np.array([7.9557e-06 ,1.2046e-03 ,1.7548e-09 ,3.3993e-08 ,6.2143e-07 ,9.1987e-06 ,2.4208e-06])
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for i, ax in enumerate(axes.flatten()):
    lowest = 4
    for k in range(200):
        # Gaussian perturbation
        perturbed_guess = np.copy(initial_guess1)
        for j, guess in enumerate(initial_guess1):
            perturbed_guess[j] = np.random.normal(guess, abs(guess) * 0.01)
        try:
            params, _ = curve_fit(parratt, theta, counts, p0=perturbed_guess, maxfev=50000)
        except:
            print("lol")
        errors = counts - parratt(theta, *params)
        valid_indices = np.logical_and(np.isfinite(errors), ~np.isnan(errors))
        squared_errors = errors[valid_indices] ** 2
        mse = np.sum(squared_errors)
        
        if mse < lowest and  mse!=0:
            lowest = mse
            print(f"{i}: ", end="")
            for par in perturbed_guess:
                print(f"{par:.4e}", ",", end="")
            print("\tms: ", mse)
            # Plot the curve on the current subplot
            ax.plot(theta, counts, label="data")
            ax.plot(theta, parratt(theta, *params), label="fit")
            ax.set_title(f"Iteration {i+1}")
            ax.set_xlabel("Theta")
            ax.set_ylabel("Intensity")
            ax.grid(True)
            break  # Exit the while loop when MSE condition is met

plt.tight_layout()
plt.show()
# Add legend outside the loop
plt.legend()

#for res in initial_guess1:
#    print(f"{res:.4e}",",",end="")
#print("")
#plt.plot(_theta,parratt(_theta,*params),label="fit")
#plt.plot(_theta,parratt(_theta,*initial_guess1),label="initial")
#plt.plot(theta,counts,label="data")
#plt.legend()
plt.savefig("../Ressourcen/parratt.png")