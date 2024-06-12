from __future__ import annotations # required for type hinting
from dataclasses import dataclass
from itertools import combinations, permutations
import numpy as np
import numba

from ode import ODE_2nd_Order_Poly_Coeffs
from fourier_series import Fourier_Series
from utils import solve_subset_sum_problem, multinomial_coefficient, trigonometric_product_to_Fourier_series


#Todo: Add doc-string.
@dataclass
class Algebraic_HBM():

	# User-input
	ODE:   ODE_2nd_Order_Poly_Coeffs = None
	order:                       int = None
	subspace_dim:                int = None
	project_onto_subspace:      bool = True
	include_constant_harmonic:  bool = True
	use_jit:                    bool = True

	_mass:      float = None
	_damping:   float = None
	_stiffness: float = None
	_excitation: Fourier_Series = None
	_ODE_polynomial_coefficients: tuple = None

	_monomials_linear_part:    list = None
	_monomials_nonlinear_part: list = None

	#Todo: Add doc-string.
	def __post_init__(self):

		self._mass = self.ODE.mass if self.ODE.mass is not None else 0.
		self._damping = self.ODE.damping if self.ODE.damping is not None else 0.
		self._stiffness = self.ODE.stiffness if self.ODE.stiffness is not None else 0.
		self._ODE_polynomial_coefficients = self.ODE.monomials if self.ODE.monomials is not None else {}

		if not self.include_constant_harmonic:
			exclude_constant_harmonic = ", excluding constant harmonic"
			self.subspace_dim = 2*self.order + 1
		else:
			exclude_constant_harmonic = ""
			self.subspace_dim = 2*self.order + 1
		print(f"Initialized HBM of order n={self.order}" + exclude_constant_harmonic)

	def generate_multivariate_polynomials(self, project_onto_subspace: bool=None):
		"""
		Generate multivariate polynomials of linear and nonlinear part of HBM residual.
		Also optionally removes constant harmonic from system.
		"""
		
		# Generate multivariate polynomials of linear part of HBM residual.
		self.generate_linear_part()

		# Generate multivariate polynomials of nonlinear part of HBM residual.
		self.generate_nonlinear_part()

		# Remove constant harmonic from system.
		self.remove_constant_harmonic()

	#Todo: Add doc-string.
	def generate_linear_part(self):

		print(f"Generating linear part of algebraic Fourier coefficients of HBM residual")

		n = self.order
		m = 2*n
		
		# Build data structure of all monomials represented by tuples '(i, b, J)' where 'i' indexes
		# the monomial 'b*y^J' with 'y=(c_0,c_1,...,c_m,f)' being the extended variable list 
		# where 'c' is the HBM coefficient vector and 'f' the excitation frequency. 
		self._monomials_linear_part = []
		self._monomials_linear_part.append((0, self._stiffness, (1,) + (0,)*(m+1)))
		excitation_coefficients = tuple(self.ODE.excitation.coefficients) + (0,)*(m+2-len(self.ODE.excitation.coefficients))
		for i in range(1,m+1):

			if i % 2: # odd index = cosine
				j = np.floor((i+1)/2)
				self._monomials_linear_part.append((i, self._stiffness,  tuple(1 if l == i else 0 for l in range(m+1)) + (0,)))
				self._monomials_linear_part.append((i, -self._mass*j**2, tuple(1 if l == i else 0 for l in range(m+1)) + (2,)))
				self._monomials_linear_part.append((i, self._damping*j,  tuple(1 if l == i+1 else 0 for l in range(m+1)) + (1,)))
			else: # even index = sine
				j = i/2
				self._monomials_linear_part.append((i, self._stiffness,  tuple(1 if l == i else 0 for l in range(m+1)) + (0,)))
				self._monomials_linear_part.append((i, -self._mass*j**2, tuple(1 if l == i else 0 for l in range(m+1)) + (2,)))
				self._monomials_linear_part.append((i, -self._damping*j, tuple(1 if l == i-1 else 0 for l in range(m+1)) + (1,))) #Todo: make sure if the 'l==i' comparison is correct

			# Now add the constant part from the excitation.
			if excitation_coefficients[i] != 0:
				self._monomials_linear_part.append((i, excitation_coefficients[i], (0,)*(m+2)))

	#Todo: Add doc-string.
	def generate_nonlinear_part(self):
		
		print(f"Generating nonlinear part of algebraic Fourier coefficients of HBM residual")

		m = 2*self.order

		# Generate nonlinear part of the truncated residual for each monomial seperately.
		self._nonlinear_part = []
		self._monomials_nonlinear_part = []
		for p in self._ODE_polynomial_coefficients:
			
			alpha_p = self._ODE_polynomial_coefficients[p]
			
			# Solve the subset sum problem, i.e. find all positive integer tuple 
			# 'K=(k_1,...,K_r)' with 'r<=p' such that 'k_1 + ... k_r = p'. 
			K_p = solve_subset_sum_problem(p)

			# Build data structure of all monomials represented by tuples '(l, b, J)'
			# where 'l' indexes the monomial 'b*c^J'.
			# Note: In contrast to the monomials of the linear part we do not have to include
			# the excitation frequency as an additional variable. Hence 'J' here is of length
			# 'm+1' where 'J' of the linear part is of length 'm+2'.
			monomials = []
			for K in K_p:
				
				# Get multinomial coefficient.
				mc = multinomial_coefficient(p,K)
				
				# Check if all elements of the tuple 'K' are the same.
				# If so, then no powers 'k_i in K' of the HBM coeffcients 'c_i' greater than 1 occur,
				# i.e. 'c^K = c_1^{k_1}*...*c_N^{k_N} = c_1*...*c_N'.
				all_tuple_elements_the_same = all(False if k != K[0] else True for k in K)

				# Build set of all tuples 't in {0,1,...,m}^len(K)' ...
				if all_tuple_elements_the_same:
					# ... in sorted order w/o repeated elements.
					J_m = set(combinations(range(0,m+1), r=len(K)))
				else:
					# ... of all possible orderings w/o repeated elements.
					J_m = set(permutations(range(0,m+1), r=len(K)))
				
				for I in J_m:

					# For a given 'K = (k_1,...,k_p)' build the tuple that is the multidegree
					# 'J = (j_1,...,j_1, ..., j_p,...,j_p)' where 'j_i' occurs 'k_i' times in 'J'
					# such that 'b*c^J' is a monomial.
					J = tuple(t for j, k in zip(I,K) for t in (j,)*k)
					
					#Todo: Update 'trigonometric_product_to_Fourier_series' to take 'J_new' instead of 'J' as its input?!
					J_new = [0]*(m+1)
					for i, degree in zip(I,K):
						J_new[i] = degree
					J_new = tuple(J_new)

					# Expand the trigonometric product 'prod_{j in J} (cos(i*t) if j=2i-1 or sin(i*t) if j=2i)'
					# defined by 'J = (j_1,...,j_1, ..., j_p,...,j_p)' into its Fourier series.
					L, B = trigonometric_product_to_Fourier_series(J)

					# Scale each 'b in B' by the current multinomial coefficient and 
					# the coefficient of the current ODE monomial.
					B = tuple(alpha_p*mc*b for b in B)

					# Now append each '(l,b) in L x B' to our data structure.
					for l, b in zip(L, B):
						self._monomials_nonlinear_part.append((l, b, J_new))

		# Perform subspace projection.
		if self.project_onto_subspace:
			print(f"Projecting nonlinear part of HBM residual on subspace of dimension {self.subspace_dim}")
			self._monomials_nonlinear_part = [(l, monomial_coefficient, multidegree) for l, monomial_coefficient, multidegree in self._monomials_nonlinear_part if l <= 2*self.order]
						
	def remove_constant_harmonic(self):
		"""
		For certain ODEs with certain periodic forcing the harmonic with index 0 will be constantly zero
		so we might just not include variable associated with the constant harmonic in the first place.
		"""
		if not self.include_constant_harmonic:
			self._monomials_linear_part = [(l-1, monomial_coefficient, multidegree[1:]) for l, monomial_coefficient, multidegree in self._monomials_linear_part if l > 0 and multidegree[0] == 0]
			self._monomials_nonlinear_part = [(l-1, monomial_coefficient, multidegree[1:]) for l, monomial_coefficient, multidegree in self._monomials_nonlinear_part if l > 0 and multidegree[0] == 0]
	
	#Todo: Add doc-string.
	@staticmethod
	def generate_product_indices_and_multinomial_coefficients(m: int, p: int, K_p: list) -> list:
		
		index_tuples, multinom = [], []
		for K in K_p:

			# Get all integer tuples of length 'len(K)' that are combinations/permutations of
			# the integers 'i=0,1,...,m'. If all elements of 'K' are the same use combinations 
			# else permutations.
			if all(False if k != K[0] else True for k in K):
				J = tuple(combinations(range(0,m+1), r=len(K)))
			else:
				J = tuple(permutations(range(0,m+1), r=len(K)))

			for I in J:
				# Add tuples (as generators) '(i_1,...,i_1,...,i_N,...,i_N)' to list of index
				# tuples where for each 'j=1,...,N' the index 'i_j' occurs 'k_j' times.
				index_tuples.append(tuple(t for j, k in zip(I,K) for t in (j,)*k))

			multinom += (multinomial_coefficient(p,K),)*len(tuple(J))

		return index_tuples, multinom
	
	#Todo: Add non-jitted branch
	def compile(self):
		"""
		Compiles vector-function 'F' and Jacobian matrix-function 'DF_c', 'DF_a'.
		"""

		print(f"Compiling executable system 'F' and its Jacobian 'DF'")

		if self.include_constant_harmonic:
			m = 2*self.order + 1
		else:
			m = 2*self.order		
		
		if self.use_jit:
			# Compile system 'F' and its Jacobian 'DF' while using numba.jit decorator

			"""	Define functions associated with LINEAR part. """

			# Prepare data for numbas jit.
			monomials_linear_part = np.array( tuple((l,) + (b,) + multidegree for l, b, multidegree in self._monomials_linear_part) , dtype=float)

			@numba.jit(nopython=True)
			def F_linear(c: np.ndarray, a: float) -> np.ndarray:
				"""Linear part 'F_linear' of system 'F = F_linear + F_nonlinear'."""

				F = np.zeros(c.shape, dtype=c.dtype)
				
				for monomial in monomials_linear_part:

					l, b, multidegree = int(monomial[0]), monomial[1], [int(l) for l in monomial[2:]]
					prod = b
					for j in range(len(multidegree)):
						
						if multidegree[j] == 0:
							continue
						
						if j < len(multidegree) - 1:
							coeff = c[j]
						else:
							coeff = a
						prod *= coeff**multidegree[j]
				
					F[l] += prod

				return F

			@numba.jit(nopython=True)
			def dF_linear_dc(c: np.ndarray, a: float) -> np.ndarray:
				"""Derivative of linear part 'F_linear' wrt HBM coefficient vector 'c'."""
				
				N = c.shape[0]
				DF = np.zeros((N,N), dtype=c.dtype)

				# Iterate over each partial derivative 'i'.
				for i in range(N):

					# Iterate over each monomial.
					for monomial in monomials_linear_part:

						l, b, multidegree = int(monomial[0]), monomial[1], [int(l) for l in monomial[2:]]							
						
						if multidegree[i] == 0:
							# The derivative of a constant monomial is zero.
							continue

						prod = b

						# Iterate over each variable 'c[0], c[1], ..., c[2n], a'.
						for j in range(len(multidegree)):

							if multidegree[j] == 0:
								continue

							if j < len(multidegree) - 1:
								coeff = c[j]
							else:
								coeff = a
							
							# Consider 'c[j]' as constant if 'j != i'.
							if j != i:
								prod *= coeff**multidegree[j]
							else:
								prod *= multidegree[j]*coeff**(multidegree[j] - 1)
					
						DF[l,i] += prod

				return DF

			@numba.jit(nopython=True)
			def dF_linear_da(c: np.ndarray, a: float) -> np.ndarray:
				"""Derivative of linear part 'F_linear' wrt frequency 'a'."""
				
				N = c.shape[0]
				DF = np.zeros((N,1), dtype=c.dtype)

				# Iterate over each monomial.
				for monomial in monomials_linear_part:

					l, b, multidegree = int(monomial[0]), monomial[1], [int(l) for l in monomial[2:]]							
					
					if multidegree[-1] == 0:
						# The derivative of a constant monomial is zero.
						continue

					prod = b*multidegree[-1]*a**(multidegree[-1] - 1)

					# Iterate over each variable 'c[0], c[1], ..., c[2n], a'.
					for j in range(N):

						if multidegree[j] == 0:
							continue
						
						prod *= c[j]**multidegree[j]
				
					DF[l] += prod

				return DF
			
			"""	Define functions associated with NONLINEAR part. """

			# Prepare data for numba.jit.
			monomials_nonlinear_part = np.array( tuple((l,) + (b,) + multidegree for l, b, multidegree in self._monomials_nonlinear_part) , dtype=float)

			@numba.jit(nopython=True)
			def F_nonlinear(c: np.ndarray) -> np.ndarray:
				"""Nonlinear part 'F_nonlinear' of system 'F = F_linear + F_nonlinear'."""
				
				F = np.zeros(c.shape, dtype=c.dtype)
				
				for monomial in monomials_nonlinear_part:

					l, b, multidegree = int(monomial[0]), monomial[1], [int(l) for l in monomial[2:]]
					prod = b
					for j in range(len(multidegree)):
						
						if multidegree[j] == 0:
							continue

						prod *= c[j]**multidegree[j]
				
					F[l] += prod

				return F

			@numba.jit(nopython=True)
			def dF_nonlinear_dc(c: np.ndarray) -> np.ndarray:
				"""Derivative of nonlinear part 'F_nonlinear' wrt HBM coefficient vector 'c'."""

				N = c.shape[0]
				DF = np.zeros((N,N), dtype=c.dtype)

				# Iterate over each partial derivative 'i'.
				for i in range(N):

					# Iterate over each monomial.
					for monomial in monomials_nonlinear_part:

						l, b, multidegree = int(monomial[0]), monomial[1], [int(l) for l in monomial[2:]]							
						
						if multidegree[i] == 0:
							# The derivative of a constant monomial is zero.
							continue

						prod = b

						# Iterate over each variable 'c[j]'.
						for j in range(N):

							if multidegree[j] == 0:
								continue
							
							# Consider 'c[j]' as constant if 'j != i'.
							if j != i:
								prod *= c[j]**multidegree[j]
							else:
								prod *= multidegree[j]*c[j]**(multidegree[j] - 1)
					
						DF[l,i] += prod

				return DF

		else:
			# Compile system 'F' and its Jacobian 'DF' without using numba.jit decorator
			raise NotImplementedError()

		def F(c: np.ndarray, a: float) -> np.ndarray:
			"""Returns system 'F = F_linear + F_nonlinear'."""
			return F_linear(c,a) + F_nonlinear(c)

		def DF_c(c: np.ndarray, a: float) -> np.ndarray:
			"""Jacobian of system 'F' wrt HBM coefficient vector 'c', i.e. 'DF_c = dF_linear_dc + dF_nonlinear_dc'."""
			return dF_linear_dc(c,a) + dF_nonlinear_dc(c)

		return F, (DF_c, dF_linear_da)
	
	def get_monomial_coefficient_matrix(self, a: float) -> np.ndarray:
		"""
		Returns the coefficient matrix of the algebraic representation for a given
		excitation frequency 'a' where each row represents a single monomial of the
		set of multivariate polynomials	that define the algebraic HBM.

		The structure of the matrix 'A' is as follow:

		  A = [row [l, b, multidegree]_i]_{i=1}^N

		where A has 'N' rows, 'l' is the index of the multivariate polynomial to which 
		the monomial defined by 'b*x^multidegree' is assigned to. The matrix is build
		diffrently from the monomials that represent the linear and the nonlinear part.
		For building the linear part coefficient matrix the last element of the tuple
		'multidegree' represents 'd=multidegree[-1]' in the monomial

		  b*a**d*c**multidegree[:-1]

		where 'multidegree[:-1]' has only one non-zero element (its the linear part 
		after all).

		For example, the system 

		  f0(c) = c_0 - c_1*c_2
		  f1(c) = 4c_0 + c_1**2 - c_2**3 + 5
		  f2(c) = 2c_0*c_1*c2

		is represented by the coefficient matrix

		  A = [
		        [0,  1, 1, 0, 0],
				[0, -1, 0, 1, 1],
				[1,  5, 0, 0, 0],
				[1,  4, 1, 0, 0],
				[1,  1, 0, 2, 0],
				[1, -1, 0, 0, 3],
				[2,  2, 1, 1, 1]
		      ] .

		"""
		
		A = []

		# Linear part first.
		for l, b, multidegree in self._monomials_linear_part:
			A.append([l,b*a**multidegree[-1]] + list(multidegree[:-1]))

		# Now nonlinear part.
		for l, b, multidegree in self._monomials_nonlinear_part:
			A.append([l,b] + list(multidegree))

		return np.array(sorted(A))