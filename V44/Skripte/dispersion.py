import numpy as np
def delta(rhor0,lamda):
    return rhor0*lamda**2*1/(2*np.pi)
def beta(gamma,lamda):
    return gamma/(4*np.pi)*lamda

deltat1 = 7.6e-6
deltat2 = 3.5e-6
gammat1 = 86*100
gammat2 = 4*100
rhor0t1 = 20*10**10 *10000
rhor0t2 = 9.5*10**10 *10000

lamda = 0.1514e-9
print((deltat1-delta(rhor0t1,lamda))/deltat1)
print((deltat2-delta(rhor0t2,lamda))/deltat2)
print(beta(gammat1,lamda))
print(beta(gammat2,lamda))