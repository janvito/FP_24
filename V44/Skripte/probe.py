import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
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

# Constants
D = 0.02 # Aus dem X-Scan in m
d0 = 0.00016 # Aus dem Z-Scan in m
Z = 14 
rho = 2.336
r_0 = 5.29e-11
Mm = 28 * c.u
N = rho * Z / Mm
lamda = 1.5*10**(-10)
print("Nr0: ",N*r_0)
Nr0=20*10**10
delta_ = N * r_0 * lamda ** 2 / (2 * np.pi) #Formel aus Quellen
print("delta aus Werten mit N selber berechnet: ",delta_)
delta_ = Nr0 * lamda ** 2 / (2 * np.pi) #Formel aus Quellen
print("delta aus Werten aus Skript: ",delta_)
delta = 7.6 * 10 ** (-6) #literaturwert
print("delta aus Anleitungs: ",delta)

Imax = 445506 * 5 # Aus dem Detektorscan

# Functions
def G(alpha):
    return (D * np.sin(alpha * 2 * np.pi / 360) / d0)

def alphat(alpha):
    return np.sqrt(alpha**2-a_c**2)

def fresnel2(thetas):
    retheta=[]
    for theta in thetas:
        if theta < a_c:
            retheta.append(1)
        else:
            #theta-=thetaclean[43]
            retheta.append(((theta - alphat(theta)) / (theta + alphat(theta)))**2)
    return retheta

# Prepare for plotting
plt.xlabel(r"$\theta$ $[\si{\degree}]$")
plt.ylabel(r"Counts")
plt.yscale('log')

# Load and process data
a_c = np.sqrt(2 * delta) * 360 / (2 * np.pi)
print("a_c=",a_c)
theta1, counts1 = np.genfromtxt('../Daten/CSV_Output/MessungProbe.csv', delimiter=',', skip_header=1, unpack=True)
theta2, counts2 = np.genfromtxt('../Daten/CSV_Output/MessungProbeDiffus.csv', delimiter=',', skip_header=1, unpack=True)
theta1, counts1, theta2, counts2 = theta1[theta1 < 1], counts1[theta1 < 1], theta2[theta1 < 1], counts2[theta1 < 1]
theta1, counts1, theta2, counts2 = theta1[1:], counts1[1:], theta2[1:], counts2[1:]
counts1 /= Imax
counts2 /= Imax
thetaclean = theta1
countsclean = counts1 - counts2

# Plot ideal Fresnel reflectivity
fresnelcount = fresnel2(thetaclean)
plt.plot(thetaclean, fresnelcount, "gray", alpha=0.7, label=r'Ideale Fresnelreflektivität für Silizium')

# Plot raw data
plt.plot(theta1, counts1, "b-", label=r'Reflektivitätsscan')
plt.plot(theta2, counts2, "b-", alpha=0.5, label=r'Diffuser Scan')

# Apply corrections
a_g = np.arcsin(d0 / D) * 360 / (2 * np.pi)
print("a_g=",a_g)
a_g_gemessen=0.3820697736481243
countsG = countsclean.copy()

for i in range(np.shape(thetaclean)[0]):
    if thetaclean[i] < a_g:
        countsG[i] = countsG[i]/G(thetaclean[i])

# Find peaks and calculate layer thickness
peaks, props = find_peaks(countsG)
thetapeaks = thetaclean[peaks]
deltatheta = thetapeaks[1:] - thetapeaks[:-1]
T_a = np.mean(deltatheta[1:])
T_s = np.std(deltatheta[1:])
T_u = ufloat(T_a, T_s)
layer_thickness = lamda / (2 * T_u)
print("Schichtdicke= ", layer_thickness)


# Plot corrected data
plt.plot(thetaclean, countsclean, "k-", label=r'Bereinigter Scan')
plt.plot(thetaclean, countsG, "r-", label=r'Korrigierter Scan')
plt.plot(thetaclean[peaks], countsG[peaks], "rx")
plt.axvline(a_c,color='green',label=r'Kritischer Winkel')
# Save the plot
plt.legend(prop={'size': 16})
plt.tight_layout()
plt.savefig("../Ressourcen/probe.pdf")
plt.clf()

# Save cleaned data to CSV
cleandata = np.array([thetaclean, countsG])
cleandata_transposed = cleandata.T
with open('../Daten/CSV/probenscan_clean.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(cleandata_transposed)
