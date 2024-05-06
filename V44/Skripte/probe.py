import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from uncertainties import ufloat
from scipy.signal import find_peaks
import scipy.constants as c
# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2
Z = 14
rho=2.336
r_0=5.29*10**-11
Mm=28*c.u
N=rho*Z/(Mm)
lamda=1.5*10**-10
delta=N*r_0*lamda**2/(2*c.pi)
def alphat2(alpha):
    return np.sqrt(alpha**2-2*delta)
def alphat(alpha):
    return np.arccos(1/(1-delta)*np.cos(alpha))
def fresnel2(theta):
    return (theta-alphat(theta))/(theta+alphat(theta))
# Update rcParams with custom settings
plt.xlabel(r"$\theta$ $[\si{\degree}]$")
plt.ylabel(r"Counts")
def cut(arr):
    mask = theta1<0.5
    return arr[mask]
# Load data from CSV files
theta1, counts1 = np.genfromtxt('../Daten/CSV_Output/MessungProbe.csv', delimiter=',', skip_header=1, unpack=True)
theta2, counts2 = np.genfromtxt('../Daten/CSV_Output/MessungProbeDiffus.csv', delimiter=',', skip_header=1, unpack=True)
theta1,counts1,theta2,counts2=cut(theta1),cut(counts1),cut(theta2),cut(counts2)
thetaclean = theta1
countsclean = counts1-counts2
plt.plot(thetaclean[5:],fresnel2(thetaclean[5:])*(counts1[5]/fresnel2(thetaclean[5])),"gray",alpha=0.7,label=r'Ideale Fresnelreflektivität für Silizium')
plt.plot(theta1, counts1, "b-", label=r'Reflektivitätsscan')
plt.legend()
plt.tight_layout()
plt.plot(theta2, counts2, "b-",alpha=0.5, label=r'Diffuser Scan')
plt.legend()
plt.tight_layout()
peaks,props=find_peaks(countsclean)
thetapeaks=thetaclean[peaks]
deltatheta = thetapeaks[1:]-thetapeaks[:-1]
print(thetapeaks)
print(f"{deltatheta[1:].mean():.2f}")
plt.plot(thetaclean, countsclean, "k-", label=r'Bereinigter Scan')
plt.plot(thetaclean[peaks],countsclean[peaks],"rx")
print(delta)
plt.legend()
plt.tight_layout()
plt.savefig("../Ressourcen/probe.pdf")
plt.clf()