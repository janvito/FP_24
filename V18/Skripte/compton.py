import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from scipy.optimize import curve_fit
from scipy import constants as const
from uncertainties import ufloat
# Enable LaTeX rendering in Matplotlib
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)  # Sets the default font size for all plot elements

# Load the CSV file into a DataFrame
csv_file = '../Daten/137Caesium.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Find peaks in the spectrum
peaks, _ = find_peaks(df['Counts'], prominence=70)
df['Energy'] = df['Channel'] * 0.1032 - 0.8336

def Q(E):
    return 0.0901 * 0.9952**E + 0.0074

df['Counts'] = df['Counts'] / Q(df['Energy'])

fep_E=661.687

E_fit=df['Energy'][3000:4200]
C_fit=df['Counts'][3000:4200]
df['Energy']=df['Energy'][60:5000]
df['Counts']=df['Counts'][60:5000]
def difCR(E, a):
    c = const.c
    m = const.m_e
    e = const.e
    m_E = m * c**2 / e
    r = 1000 * fep_E / (m_E)
    return a * (2 - 2 * E / (r * (fep_E - E)) + E**2 / (r**2 * (fep_E - E)**2) + E**2 / (fep_E * (fep_E - E)))

def compP():
    c = const.c
    m = const.m_e
    e = const.e
    m_E = m * c**2 / e
    r = 1000 * fep_E / (m_E)
    return fep_E * 2 * r / (1 + 2 * r)

def backP():
    c = const.c
    m = const.m_e
    e = const.e
    m_E = m * c**2 / e
    r = 1000 * fep_E / (m_E)
    return fep_E / (1 + 2 * r)

par, cov = curve_fit(difCR, E_fit, C_fit,p0=[224.62])
err = np.sqrt(np.diag(cov))
print(par)
comp_fit = ufloat(par, err)

x = np.linspace(df['Energy'][60], compP(), 10**5)
y = difCR(x, comp_fit)
print(f'Differential Cross Section Fit:\n')
print(f'a = {comp_fit.n:.2f} +- {comp_fit.s:.2f}\n')
print(f'Compton Edge: E = {compP():.2f} keV')
print(f'Escape Peak:  E = {backP():.2f} keV')
comp_tot = np.sum((x[1:] - x[:-1]) * y[1:]) 
print(f'Total COMP Content: N = {comp_tot.n:6.0f} +- {comp_tot.s:4.0f}')
plt.figure(figsize=(10, 6))
plt.plot(df['Energy'], df['Counts'], ".", color="black", alpha=0.05, label=r'Messdaten')
plt.plot(E_fit,C_fit,".",color="green",alpha=0.05)
plt.plot(x, difCR(x, comp_fit.n), c='olivedrab', label='Fit')
plt.axvline(x=compP(), color='steelblue', linewidth=2, zorder=10, label="Compton-Peak")
plt.axvline(x=backP(), color='firebrick', linewidth=2, zorder=10, label="Backscattering Peak")
plt.xlabel(r'E (keV)')
plt.ylabel(r'Counts')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
#plt.yscale('log')
output_plot_original = '137Caesium_compton.png'
#plt.savefig(output_plot_original, dpi=300)
