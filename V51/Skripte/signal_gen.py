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
    plt.plot(t, U, "r-", label="Signal")
    plt.legend()
    plt.savefig(f"../Ressourcen/signal_{scop}.png")
    plt.clf()

t, U = t[990:1899], U[990:1900]
U = (U[1:]+U[:-1])/2
peaks, _ = find_peaks(U,prominence=0.11)
tp=t[peaks]
Up=U[peaks]
tp = np.delete(tp, 7)
Up = np.delete(Up, 7)
tp = tp[:-3]
Up = Up[:-3]
tp = np.insert(tp, 0, t[2])
Up = np.insert(Up, 0, U[2])
def expfit(t,A,tau,b):
    return A*np.exp(-t/tau)+b
par,cov = curve_fit(expfit,tp,Up,p0=[1.5,170e-6,0.4])
plt.plot(t, U, "r-", label="Signal")
plt.plot(t, expfit(t,*par), label="Fit")
plt.plot(tp, Up, "kx", label="Maxima")
A = ufloat(par[0], np.sqrt(cov[0, 0]))
tau = ufloat(par[1], np.sqrt(cov[1, 1]))
b = ufloat(par[2], np.sqrt(cov[2, 2]))

# Print the parameters with uncertainties
print(f"A = {A}")
print(f"tau = {tau}")
print(f"b = {b}")
plt.legend()
plt.savefig("../Ressourcen/genvar_plot.png")
plt.clf()