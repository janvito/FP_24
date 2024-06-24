import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from uncertainties import ufloat, unumpy
import scipy.constants as c

# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2

# Function to format ticks with commas
def comma_formatter(x, pos):
    return "{:,.0f}".format(x).replace(",", ".")

plt.xlabel(r"$z$ $[\si{\milli\meter}]$")
plt.ylabel(r"Counts")

# Load data from CSV files
z, counts = np.genfromtxt('../Daten/CSV_Output/zscan2.csv', delimiter=',', skip_header=1, unpack=True)
plt.plot(z, counts, label=r"Messdaten")
zdown = z[(z <= 0.16)]
zup = z[(z >= 0.32)]
cup = counts[(z <= 0.16)]
cdown = counts[(z >= 0.32)]
cdownmean = np.mean(cdown)
cupmean = np.mean(cup)
cdownstd = np.std(cdown)
cupstd = np.std(cup)
plt.axvline(zdown[-1], color="red", label=r"gewählte Grenzen des Strahls")
plt.axvline(zup[0], color="red")
print(f"{cupmean}+-{cupstd}\n{cdownmean}+-{cdownstd}")
strahlbreite = zup[0] - zdown[-1]

# Calculate uncertainties
zup_err = np.std(zup)
zdown_err = np.std(zdown)

strahlbreite_err = np.sqrt(zup_err**2 + zdown_err**2)

# Create uncertainty object for strahlbreite
strahlbreite_with_uncertainty = ufloat(strahlbreite, strahlbreite_err)

print(f"Strahlbreite: {strahlbreite_with_uncertainty}")
#plt.plot(z[(z<=0.16)],cupmean*np.ones(np.shape(cup)),"r-")
#plt.plot(z[(z>=0.32)],cdownmean*np.ones(np.shape(cdown)),"r-")
plt.legend()

# Set the tick formatter for y-axis
plt.gca().yaxis.set_major_formatter(FuncFormatter(comma_formatter))

plt.tight_layout()
plt.savefig("../Ressourcen/zscan.pdf")
