from ode import ODE_2nd_Order_Poly_Coeffs as ODE
from algebraic_hbm import Algebraic_HBM
from numpy import ones

# Define classical softening Duffing oscillator as 2nd order ODE with polynomial coefficients.
ode = ODE(mass=1, damping=.4, stiffness=1, excitation=(0,.3), monomials={3: -.4})

# HBM ansatz order.
n = 1

# Initialize HBM
HBM = Algebraic_HBM(ODE=ode, order=n)

# Generate multivariate polynomials.
HBM.generate_multivariate_polynomials()

# Get monomial coefficient matrix for Macauly matrix framework 
# evaluated at a given excitation frequency 'a'
a = 1.
A = HBM.get_monomial_coefficient_matrix(a)
print(A)