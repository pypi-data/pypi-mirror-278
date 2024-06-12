from typing import Callable
from itertools import product
from scipy.integrate import solve_ivp
from scipy.special import comb
import numpy as np

def solve_subset_sum_problem(p: int) -> list[tuple]:
	"""
	Return a list of all tuple 'a=(a_1,a_2,...)' that solve the subset sum problem

		(*) a_1 + a_2 + ... = p

	for a given positive integer 'p' where 'a_i in {1,...,p}'.

	Implementation via dynamical programming.

	Example:
		For 'p=3' returns '[(1, 1, 1), (1, 2), (3,)]' or for 'p=4' returns
		'[(1, 1, 1, 1), (1, 1, 2), (1, 3), (2, 2), (4,)]'.
	"""

	def Integers(a: int, b: int, d: int=1) -> range:
		"""Returns generator that yields all integers {a,a+d,a+2*d,...b} (including b)."""
		return range(a, b+1, d)
	
	def write_into_new_column(x: int, k: int) -> bool:
		"""Indicate that we have to write into a new column."""
		return len(table[x]) == k
	
	def union(T: list, t: list, i: int) -> list:
		"""
		For each 'E' in 'T' do 'e=sort(union(E,{i}))'.
		If 'e' not in 't' append it to the output 'TT'.
		"""
		TT = []
		for tt in (sorted(_ + [i]) for _ in table[x_new][k_new]):
			if tt not in t:
				TT.append(tt)

		return TT

	# Fill table with default cases (0-th and 1-st column).
	# We keep the 0-th column (ie the "None") in order to not have to worry
	# about index shifts x,k -> x-1,k-1 during accessing of data.
	table = [[None, [[1]*i]] if i > 0 else [] for i in Integers(0,p)]
	
	# Now fill remainder of table.
	for x in Integers(2,p):
		for k in Integers(2,x):
			t = []
			for i in Integers(1,k):

				x_new, k_new = (x-i,k-i)

				if write_into_new_column(x,k_new) or x_new == 0 or k_new == 0:
					t.append([i])
					continue

				t += union(table[x_new][k_new], t, i)
			
			table[x].append(t)
	
	return [tuple(t) for t in table[p][p]]

def trigonometric_product_to_Fourier_series(indices: tuple) -> tuple[tuple,tuple]:
	"""
	Returns the tuple '(L,B)' that identifies a Fourier series with coefficients
	'b_l in B subset reals' for each 'l in L subset integers' such that

		prod_{i in indices} phi_i(x) = sum_{l in L} b_l*phi_l(x)
	
	where 'phi_l' are the trigonometric basis functions

		phi_l(x) = 1,        l = 0 ,
		         = cos(k*x), l = 2k-1 ,
				 = sin(k*x), l = 2k .

	For this, the indices 'i in indices' are split by cosine and sine indices
	such that

		prod_{i in indices} phi_i(x)
		= prod_{j in cos_indices} cos(j*x) * prod_{j in sin_indices} sin(j*x) .

	The Fourier series '(L,B)' is obtained indirectly. First, an intermediate 
	Fourier series '(L_inter,B_inter)' is generated where elements of 'L_inter'
	may occur multiple times with individual weights in 'B_inter'. These are
	summed up to then obtain '(L,B)'.
	"""

	# Get all 'i in indices' with 'i=2j-1' where 'j -> cos(j*x).
	cos_indices = tuple((j+1)//2 for j in indices if j % 2)

	# Get all 'i in indices' with 'i=2j>0' where 'j -> sin(j*x).
	sin_indices = tuple(j//2 for j in indices if j > 0 and not (j % 2))

	# Compute constant fraction.
	constant = (-1)**int(len(sin_indices)/2) / (2**(len(cos_indices) + len(sin_indices) + 1))

	# Generate all combinations '(s,t) in {-1,1}^len(cos_indices) x {-1,1}^len(sin_indices)'.
	S = product(product((-1,1), repeat=len(cos_indices)), product((-1,1), repeat=len(sin_indices)))
	
	# Generate intermediate Fourier series '(L_temp,B_temp)'.
	L_temp, B_temp = [], []
	for s_cos, s_sin in S:

		# Determine sign of coefficient by counting how many "-1" in s_sin and multiply by fraction.
		if sum(1 for s in s_sin if s < 0) % 2:
			constant_temp = -constant
		else:
			constant_temp = constant

		# Compute new harmonic index.
		a_cos = sum(a*b for a,b in zip(cos_indices, s_cos))
		a_sin = sum(a*b for a,b in zip(sin_indices, s_sin))
		k = (a_cos - a_sin, a_cos + a_sin)

		if len(sin_indices) % 2: # Sine terms only
			L_temp += [2*abs(k[0]), 2*abs(k[1])]
			B_temp += [-constant_temp*np.sign(k[0]), constant_temp*np.sign(k[1])]

		else: # Cosine terms only
			L_temp += [2*abs(i)-1 if i != 0 else 0 for i in k]
			B_temp += [constant_temp]*2

	# Add up multiplicities of '(L_temp,B_temp)' to obtain Fourier series '(L,B)'.
	L, B = [], []
	l_last = -1
	for l_current, b_inter in sorted(zip(L_temp, B_temp)):
		if l_current == l_last:
			B[-1] += b_inter
		else:
			L.append(l_current)
			B.append(b_inter)
		l_last = l_current

	# Remove all pairs '(l,b)' with 'b=0' from Fourier series '(L,B)'.
	# Note that since b in B is +/- 2**(negative number) it is save to test against exact zero.
	mask = tuple(i for i in range(len(B)) if B[i] != 0)
	L = tuple(L[i] for i in mask)
	B = tuple(B[i] for i in mask)

	return L, B

def multinomial_coefficient(n: int, K: list) -> int:
	'''
	Returns the multinomial coefficient "n choose K" where K is a list of integers
	and "k_0 + k_1 + ... + k_m = n for k_i in K".
	'''

	c = 1
	s = 0
	for k in K:
		s += k
		c *= comb(s, k, exact=True)
	return c