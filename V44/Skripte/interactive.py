import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')
plt.rc('font', family='serif')
plt.rcParams['figure.figsize'] = (10, 12)  # Increased figure height for sliders
plt.rcParams['font.size'] = 20
plt.rcParams['lines.linewidth'] = 2

def parratt(a_i, del2, del3, sig1, sig2,b2,b3, d2):
    a_irad = np.deg2rad(a_i)
    k = 2 * np.pi / lamda
    #b2 = del2 / 40
    #b3 = del3 / 200
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

# Load data
theta, counts = np.genfromtxt('../Daten/CSV/probenscan_clean.csv', delimiter=',', unpack=True)
theta, counts = theta[25:320], counts[25:320]
lamda = 1.54e-10
guess= np.array([8.76e-7, 7.11e-6, 6.43e-10, 8.30e-10, 1e-7, 3.555e-08, 8.73e-8])
for g in guess:
    print(g)
# Create figure with adjusted layout
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15, right=0.95, bottom=0.45, top=0.95)  # More bottom space

# Initial plot
ax.plot(theta, counts, "k-",alpha=0.5, label=r"Gemessene Reflexivität")
line, = ax.plot(theta, parratt(theta, *guess), color="blue", label=r"Parratt-Reflexivität")
ax.axvline(np.sqrt(2*7.809387428660141e-06)*360/(2*np.pi), color="red")
ax.set_xlabel(r"$\theta$ $[\si{\degree}]$")
ax.set_ylabel(r"$X_1=\frac{R_1}{T_1}$")
ax.set_yscale("log")
ax.legend()

# Updated slider parameters with b2 and b3
slider_params = [
    (r'$\delta_2$ scale', 0.5, 2.0, 0.45),
    (r'$\delta_3$ scale', 0.5, 2.0, 0.40),
    (r'$\sigma_1$ scale', 0.5, 2.0, 0.35),
    (r'$\sigma_2$ scale', 0.5, 2.0, 0.30),
    (r'$b_2$ scale', 0.5, 2.0, 0.25),    # New slider
    (r'$b_3$ scale', 0.5, 2.0, 0.20),    # New slider
    (r'$d_2$ scale', 0.5, 2.0, 0.15)     # Adjusted position
]

sliders = []
for label, valmin, valmax, bottom_pos in slider_params:
    ax_slider = plt.axes([0.25, bottom_pos, 0.6, 0.03])
    slider = Slider(ax=ax_slider, label=label, valmin=valmin, valmax=valmax, valinit=1.0)
    sliders.append(slider)

def update(val):
    scaled_params = [guess[i] * sliders[i].val for i in range(7)]  # Now 7 parameters
    line.set_ydata(parratt(theta, *scaled_params))
    fig.canvas.draw_idle()

for slider in sliders:
    slider.on_changed(update)

plt.show()