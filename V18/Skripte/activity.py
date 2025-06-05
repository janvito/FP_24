from uncertainties import ufloat
import numpy as np
A_0=ufloat(4130,60)
print(A_0*np.exp(-np.log(2)/4934*8941))