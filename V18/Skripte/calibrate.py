import numpy as np
import matplotlib.pyplot as plt
emission_energies = [121.7824, 244.6989, 344.2811, 411.126, 443.965, 778.903, 867.390, 964.055, 1085.842, 1089.767, 1112.087, 1212.970, 1299.152, 1408.022]

# Given energies and channels
Es = [121.7824, 244.6989, 344.2811, 411.126, 443.965]  # Energies in keV
Cs = [1186, 2378, 3344, 3992, 4312]  # Channels
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
# Linear fit
coefficients = np.polyfit(Cs, Es, 1)  # Perform linear fit (y = mx + b)
linear_fit = np.poly1d(coefficients)

# Generate linear fit line
channel_range = np.linspace(min(Cs), max(Cs), 500)  # Smooth range of channel values
fitted_energies = linear_fit(channel_range)

# Plot the data and linear fit
plt.figure(figsize=(10, 6))
plt.plot(Cs, Es, "x", color="black", label=r'\textbf{Data Points}')  # Data points
plt.plot(channel_range, fitted_energies, "-", color="red", label=rf'\textbf{{Linear Fit: $E = {coefficients[0]:.2f} \cdot C + {coefficients[1]:.2f}$}}')

# Labeling the plot
plt.xlabel(r'Channel', fontsize=12)
plt.ylabel(r'{E (keV)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()

# Save and show the plot
output_plot = 'Energy_vs_Channel.png'
plt.savefig(output_plot, dpi=300)
plt.show()

print(f"Plot saved to: {output_plot}")
print(f"Slope (m): {coefficients[0]:.4f}, Intercept (b): {coefficients[1]:.4f}")
