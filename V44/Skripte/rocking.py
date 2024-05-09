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

#data1 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan1"]
#data2 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan2.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan2"]
#data3 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan3.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan3"]
#data4 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan4.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan4"]
#data5 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan5.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan5"]
#data6 =  [np.genfromtxt('../Daten/CSV_Output/Rockingscan6_final.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan6"]
theta,counts = np.genfromtxt('../Daten/CSV_Output/Rockingscan6_final2.csv', delimiter=',', skip_header=1, unpack=True)
#data63 = [np.genfromtxt('../Daten/CSV_Output/Rockingscan_2theta03.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan 2theta03"]
#data64 = [np.genfromtxt('../Daten/CSV_Output/Rockingscan_2theta05.csv', delimiter=',', skip_header=1, unpack=True),"Rockingscan 2theta05"]


plt.plot(theta,counts,label="rockingscan")
# Identify the peaks
peaks, _ = find_peaks(counts, height=1000)  # Assuming data62 is the data you want to fit
print(peaks)
# Extract the peak position
peak_position = counts[peaks]
print(peak_position)
# Define a function for the line
def linear_func(x, m, b):
    return m * x + b
plt.plot(theta[peaks],counts[peaks],"rx")
# Fit the line to your data
x_lin = np.linspace(theta[peaks],0.5,1000)
x_data = theta
y_data = counts
fit_params, _ = curve_fit(linear_func, theta[peaks[0]:peaks[0]+10], counts[peaks[0]:peaks[0]+10], p0=[-1, 0])  # Initial guess for parameters: slope = -1, intercept = 0

# Plot the data and the fitted line
plt.plot(x_data, y_data)
plt.plot(x_lin, linear_func(x_lin, *fit_params), 'r--', label='Fitted Line')
plt.legend()
# Calculate the intersection with y=0
intersection_x = -fit_params[1] / fit_params[0]
print("Intersection with y=0:", intersection_x)

# Save the plot
plt.legend()
plt.savefig("../Ressourcen/rocking.pdf")
plt.clf()
#for data in [data63,data64]:
#    plt.plot(data[0][0],data[0][1],label=data[1])
#    plt.legend()
#plt.savefig("../Ressourcen/rocking2.pdf")