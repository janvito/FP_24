import numpy as np
import matplotlib.pyplot as plt

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

    return np.abs(x1) ** 2


theta, counts = np.genfromtxt('../Daten/CSV/probenscan_clean.csv', delimiter=',', unpack=True)
theta, counts = theta[25:320], counts[25:320]
lamda = 1.54 * 10**(-10)
initial_guess1 = np.array([7.648577896993004e-06 ,0.0012410968451660746 ,1.8963141350166085e-09 ,3.4233238181111846e-08 ,2.416951357029224e-06])
guess= np.array([8.76e-7, 7.11e-6, 6.43e-10, 8.30e-10, 1.77e-7, 3.555e-08, 8.73e-8])
plt.axvline(np.sqrt(2*7.809387428660141e-06)*360/(2*np.pi),color="red",label=r"Bestimmter kritischer Winkel von Silizium")
plt.plot(theta,(counts),"k-",alpha=0.5,label=r"Gemessene Reflexivität")
plt.plot(theta,parratt(theta,*guess),color="blue",label=r"Parratt-Reflexivität")
plt.tight_layout()
#plt.show()
plt.legend()

plt.savefig("../Ressourcen/parratttipp.png")