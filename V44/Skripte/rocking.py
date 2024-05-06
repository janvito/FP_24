import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from uncertainties import ufloat
from scipy.signal import find_peaks
import scipy.constants as c

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2

data1 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan1"]
data2 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan2.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan2"]
data3 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan3.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan3"]
data4 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan4.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan4"]
data5 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan5.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan5"]
data6 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan6_final.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan6"]
data62 = [np.genfromtxt('../Daten/CSV_Output/Rockingscan6_final2.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan62"]
data63 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan_2theta03.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan 2theta03"]
data64 = [np.genfromtxt('../Daten/CSV_Output/Rockingscan_2theta05.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan 2theta05"]

for data in [data1,data2,data3,data4,data5,data6,data62]:
    plt.plot(data[0][0],data[0][1],label=data[1])
plt.legend()
plt.savefig("../Ressourcen/rocking.pdf")
plt.clf()
for data in [data63,data64]:
    plt.plot(data[0][0],data[0][1],label=data[1])
    plt.legend()
plt.savefig("../Ressourcen/rocking2.pdf")