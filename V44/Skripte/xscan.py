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
plt.xlabel(r"$x$ $[\si{\milli\meter}]$")
plt.ylabel(r"Counts")

# Load data from CSV files
x, counts = np.genfromtxt('../Daten/CSV_Output/xscan.csv', delimiter=',', skip_header=1, unpack=True)
plt.plot(x, counts, label=r"Messdaten")
plt.axvline(-10.5, color="red", label=r"Gewählte Grenzen der Probe")
plt.axvline(9.5, color="red")
plt.legend(loc="upper center")

# Define custom tick formatter function
def comma_formatter(x, pos):
    """
    Format ticks with commas instead of points.
    """
    return "{:,.0f}".format(x)

# Apply the custom tick formatter to the x-axis
plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))

plt.tight_layout()
plt.savefig("../Ressourcen/xscan.pdf")
