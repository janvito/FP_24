import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
from scipy.signal import find_peaks
import scipy.constants as c
from uncertainties import unumpy as unp
# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2

colors = ['gray', 'gold','darkorange', 'lightcoral', 'saddlebrown',  'lightpink', 'pink']

# Constants
D = 0.02 # Aus dem X-Scan in m
Du= ufloat(D,0.001)
d0 = 0.00016 # Aus dem Z-Scan in m
d0u= ufloat(d0,0.00002)
Z = 14 
rho = 2.336
r_0 = 5.29e-11
Mm = 28 * c.u
N = rho * Z / Mm
lamda = 1.5*10**(-10)
print("Nr0: ", N*r_0)
Nr0 = 20*10**10
delta_ = N * r_0 * lamda ** 2 / (2 * np.pi) # Formel aus Quellen
print("delta aus Werten mit N selber berechnet: ", delta_)
delta_ = Nr0 * lamda ** 2 / (2 * np.pi) # Formel aus Quellen
print("delta aus Werten aus Skript: ", delta_)
delta = 7.6 * 10 ** (-6) # Literaturwert
print("delta aus Anleitungs: ", delta)
delta_polysterol = 3.5*10**(-6)
Imax = 445506 * 5 # Aus dem Detektorscan

# Functions
def G(alpha):
    return (D * np.sin(alpha * 2 * np.pi / 360) / d0)

def alphat(alpha):
    return np.sqrt(alpha**2 - a_c_silicium**2)

def fresnel2(thetas):
    retheta = []
    for theta in thetas:
        if theta < a_c_silicium:
            retheta.append(1)
        else:
            retheta.append(((theta - alphat(theta)) / (theta + alphat(theta)))**2)
    return retheta

# Prepare for plotting
plt.xlabel(r"$\theta$ $[\si{\degree}]$")
plt.ylabel(r"$X_1=\frac{R_1}{T_1}$")
plt.yscale('log')

# Load and process data
a_c_silicium = np.sqrt(2 * delta) * 360 / (2 * np.pi)
a_c_polysterol = np.sqrt(2 * delta_polysterol) * 360 / (2 * np.pi)
print("a_c,Si=", a_c_silicium)
print("a_c,Po=", a_c_polysterol)

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
plt.plot(thetaclean, fresnelcount, color=colors[0], alpha=0.7, label=r'Ideale Fresnelreflektivität für Silizium')

# Plot raw data
plt.plot(theta1, counts1, color=colors[1], label=r'Reflektivitätsscan')
plt.plot(theta2, counts2, color=colors[2], label=r'Diffuser Scan')

# Apply corrections
a_g = np.arcsin(d0 / D) * 360 / (2 * np.pi)
a_gu = unp.arcsin(d0u / Du) * 360 / (2 * np.pi)
print("a_g=", f"{a_gu:.3f}")
a_g_gemessen = 0.3820697736481243
countsG = countsclean.copy()

for i in range(np.shape(thetaclean)[0]):
    if thetaclean[i] < a_g:
        countsG[i] = countsG[i] / G(thetaclean[i])

# Find peaks and calculate layer thickness
peaks, props = find_peaks(countsG)
thetapeaks = thetaclean[peaks]
deltatheta = thetapeaks[1:] - thetapeaks[:-1]

# Calculate Δq_z
delta_theta_radians = np.radians(deltatheta)
lambda_xray = 1.51 * 10**-10  # X-ray wavelength in meters
delta_qz = (4 * np.pi * np.sin(delta_theta_radians)) / lambda_xray

# Average Δq_z and its uncertainty
delta_qz_avg = np.mean(delta_qz)
delta_qz_std = np.std(delta_qz)
delta_qz_u = ufloat(delta_qz_avg, delta_qz_std)

# Calculate layer thickness using the updated formula
layer_thickness = 2 * np.pi / delta_qz_u
print("Layer thickness =", layer_thickness)

# Plot corrected data
plt.plot(thetaclean, countsclean, color=colors[3], label=r'Bereinigter Scan')
plt.plot(thetaclean, countsG, colors[4], label=r'Korrigierter Scan')
plt.plot(thetaclean[peaks], countsG[peaks], "rx")
plt.axvline(a_c_silicium, color=colors[5], label=r'Kritischer Winkel Silizium')
plt.axvline(a_c_polysterol, color=colors[6], alpha=0.5, label=r'Kritischer Winkel Polysterol')

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
