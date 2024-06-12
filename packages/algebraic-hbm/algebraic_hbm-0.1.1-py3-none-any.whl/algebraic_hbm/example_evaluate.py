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

# Compile multivariate polynomials into excecutable functions 'F' and
# 'DF=(dF/dc,dF/da)' where 'c' is the HBM coefficient vector and 'a'
# the excitation frequency of 'ode.excitation'.
F, DF = HBM.compile()

# Examplary use case:
# Evaluation of 'F' and 'DF' at a given pair '(c,a)'.
c, a = ones(HBM.subspace_dim), 0.
print(F(c,a)) # Evaluate 'F'
print(DF[0](c,a)) # Evaluate 'dFdc'
print(DF[1](c,a)) # Evaluate 'dF/da'