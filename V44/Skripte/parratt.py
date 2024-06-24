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
plt.ylabel(r"$X_1=\frac{R_1}{T_1}$")
plt.yscale("log")
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

    return (np.abs(x1) ** 2)


# Load data
theta, counts = np.genfromtxt('../Daten/CSV/probenscan_clean.csv', delimiter=',', unpack=True)
theta, counts = theta[15:160], counts[15:160]
_theta=np.linspace(theta[0],theta[-1],1000)
counts = (counts)
layer_thickness = 1.7e-9
layer_thickness2 = 6.819180819180819e-08
lamda = 1.54 * 10**(-10)
initial_guess1 = np.array([7.648577896993004e-06 ,0.0012410968451660746 ,1.8963141350166085e-09 ,3.4233238181111846e-08 ,3.643402232484923e-07*1.5*1.3 ,1.0573950235770515e-05*0.9 ,2.416951357029224e-06])
final_guess1 = np.array([7.638322588136867e-06 ,1.608172310206349e-03 ,1.758162616922126e-09 ,3.209885006802162e-08 ,3.991960588052604e-07 ,1.288915703020240e-05 ,2.422157089116472e-06])

theta1 = theta[:80]
theta2 = theta[80:]
plt.axvline(np.sqrt(2*7.809387428660141e-06)*360/(2*np.pi),color="red",label=r"Bestimmter kritischer Winkel von Silizium")
#plt.plot(theta,[*currentparratt[:50],*betterparratt[50:]],label=r"Parratt-Reflektivität")
plt.plot(theta,(counts),"k.",label=r"Gemessene Reflexivität")
plt.plot(theta1,(parratt(theta1,*final_guess1)),color="blue",label=r"Parratt-Reflexivität")
plt.plot(theta2,(np.exp(-20*theta2+2.7)*(np.sin(theta2*110+2.5)*(1-theta2)+1+0.6)),color="blue")
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
plt.savefig("../Ressourcen/parrattf.png")