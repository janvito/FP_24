import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat,unumpy
import scipy.constants as c
# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2
# Load data from CSV files
z, counts = np.genfromtxt('../Daten/CSV_Output/zscan2.csv', delimiter=',', skip_header=1, unpack=True)
plt.plot(z,counts)
zdown=z[(z<=0.16)]
zup=z[(z>=0.32)]
cup=counts[(z<=0.16)]
cdown=counts[(z>=0.32)]
cdownmean=np.mean(cdown)
cupmean=np.mean(cup)
cdownstd=np.std(cdown)
cupstd=np.std(cup)
plt.axvline(zdown[-1],color="red")
plt.axvline(zup[0],color="red")
print(f"{cupmean}+-{cupstd}\n{cdownmean}+-{cdownstd}")
print(f"Strahlbreite: {zup[0]-zdown[-1]}")
plt.plot(z[(z<=0.16)],cupmean*np.ones(np.shape(cup)),"r-")
plt.plot(z[(z>=0.32)],cdownmean*np.ones(np.shape(cdown)),"r-")
plt.savefig("../Ressourcen/zscan.pdf")

