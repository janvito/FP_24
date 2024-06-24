import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
from uncertainties import ufloat
from scipy.signal import find_peaks

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 22
plt.rcParams['lines.linewidth'] = 2

# Update rcParams with custom settings
plt.xlabel(r"$f$ $[\si{\hertz}]$")
plt.ylabel(r"$\frac{U_0}{U_i}$")

def fit(x,A,w,phi):
    return A*np.sin(w*x+phi)
# Load data
for scope in ["0","1","3","6","7"]:
    t, U_0,U_i = np.genfromtxt(f"../Daten/clean/scope_{scope}.csv", delimiter=",", unpack=True, skip_header=1)
    plt.plot(t, U_i, color = "orange", label="Eingang")
    plt.plot(t, U_0, "g-", label="Ausgang")
    if scope == "3":
        par,_=curve_fit(fit,t,U_i,p0=[2,1000,0])
        print(f"Amp: {par[0]} \nfreq: {par[1]/(2*np.pi)}")
        plt.plot(t,fit(t,*par),"k-", label = "Sinus-Fit")
        peaks = find_peaks(U_0,prominence=10)
        print(f"peak freq: {1/(t[peaks[0][1]]-t[peaks[0][0]])}")
        print(f"peak Amp: {U_0[peaks[0][1]]}")
        plt.plot(t[peaks[0][0]],U_0[peaks[0][0]], "ro", label="Peaks")
        plt.plot(t[peaks[0][1]],U_0[peaks[0][1]], "ro")

    plt.legend()
    plt.savefig(f"../Ressourcen/signal_{scope}.png")
    plt.clf()

for scop in ["10","11","12","13"]:
    t, U = np.genfromtxt(f"../Daten/clean/scope_{scop}.csv", delimiter=",", unpack=True, skip_header=1)
    plt.plot(t, U, "r-", label="Eingang")
    plt.legend()
    plt.savefig(f"../Ressourcen/signal_{scop}.png")
    plt.clf()