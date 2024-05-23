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
x, counts = np.genfromtxt('../Daten/CSV_Output/xscan.csv', delimiter=',', skip_header=1, unpack=True)
plt.plot(x,counts)
plt.savefig("../Ressourcen/xscan.pdf")