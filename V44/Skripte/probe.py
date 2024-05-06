import numpy as np
import csv
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from uncertainties import ufloat,unumpy
from scipy.signal import find_peaks
import scipy.constants as c
# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2
D=0.02
d0=0.00016
def G(alpha):
    if alpha == 0:
        return 1
    return np.max([1.0,1/(D*np.sin(alpha*2*c.pi/360)/d0)])
Z = 14
rho=2.336
r_0=5.29*10**-11
Mm=28*c.u
N=rho*Z/(Mm)
lamda=1.5*10**-10
delta=N*r_0*lamda**2/(2*c.pi)
delta=7.6*10**(-6)
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
a_gla= np.sqrt(2*delta)*360/(2*c.pi)
# Load data from CSV files
theta1, counts1 = np.genfromtxt('../Daten/CSV_Output/MessungProbe.csv', delimiter=',', skip_header=1, unpack=True)
theta2, counts2 = np.genfromtxt('../Daten/CSV_Output/MessungProbeDiffus.csv', delimiter=',', skip_header=1, unpack=True)
theta1,counts1,theta2,counts2=cut(theta1),cut(counts1),cut(theta2),cut(counts2)
thetaclean = theta1
countsclean = counts1-counts2
print("a_gla:",a_gla)
plt.plot(thetaclean,np.concatenate([np.sqrt(2*delta)*360/(2*c.pi)*np.ones(5)*(counts1[1]/fresnel2(thetaclean[1])),fresnel2(thetaclean[5:])*(counts1[5]/fresnel2(thetaclean[5]))]),"gray",alpha=0.7,label=r'Ideale Fresnelreflektivität für Silizium')
plt.plot(theta1, counts1, "b-", label=r'Reflektivitätsscan')
plt.legend()
plt.tight_layout()
plt.plot(theta2, counts2, "b-",alpha=0.5, label=r'Diffuser Scan')
plt.legend()
plt.tight_layout()
plt.yscale('log')
a_g=np.arcsin(d0/D)*360/(2*c.pi)
countsG=np.array(countsclean[:])
for i in range(np.shape(thetaclean)[0]):
    if thetaclean[i]<a_g:
        countsG[i]=countsG[i]*G(thetaclean[i])
peaks,props=find_peaks(countsG)
thetapeaks=thetaclean[peaks]
deltatheta = thetapeaks[1:]-thetapeaks[:-1]
T_a= np.mean(deltatheta[1:])
T_s= np.std(deltatheta[1:])
T_u=ufloat(T_a,T_s)
dicke=lamda/(2*T_u)
print("a_g: ",np.arcsin(d0/D)*360/(2*c.pi))
print(f"DeltaThetaarr = {deltatheta[1:]}")
print(f"DeltaTheta = {deltatheta[1:].mean():.2f}+-{T_s:.2f}")
G0=G(thetaclean[0])
print("G0:",G0)
G1=G(thetaclean[1])
print("G1:",G1)
print("glanzwinkel:",np.sqrt(2*delta)*360/(2*c.pi))
print("Schichtdicke= ",dicke)

plt.plot(thetaclean, countsclean, "k-", label=r'Bereinigter Scan')
plt.plot(thetaclean, countsG, "r-", label=r'Korrigierter Scan')
plt.plot(thetaclean[peaks],countsG[peaks],"rx")
print(delta)
plt.legend()
plt.tight_layout()
plt.savefig("../Ressourcen/probe.pdf")
plt.clf()

# Assuming cleandata is a NumPy array
cleandata = np.array([thetaclean, countsG])

# Transpose the array
cleandata_transposed = cleandata.T

# Open the file in the write mode
with open('../Daten/CSV/probenscan_clean.csv', 'w', newline='') as f:
    # Write a row to the CSV file
    writer = csv.writer(f)
    for row in cleandata_transposed:
        writer.writerow(row)