import random
import vote_gen
import functools
import math

def ShamirSecretSharing(n, t, s, q):
	# all parameteres are int
	# return value is array of ints
	s_a = [0]*n
	x, s_a = zip(*split_secret(s, t, n, q))
	return s_a


# Partial decrytption
# Output: List of Omegas
def PartialDecryption(X, a, Lambda, t, p):
	Omega = []
	for i in range(t):
		Omega.append((a[i] + 1, (pow(X, Lambda[i], p))))
	return Omega


# Decryption Function
def FullDecryption(X, Y, a, Omega, G, t, p, q, k, ell):
	result = 1
	x_s, y_s = zip(*Omega)

	for i in range(t):
		noms = 1
		dens = 1
		for j in range(t):
			if x_s[i] != x_s[j]:
				noms *= x_s[j]
				dens *= (x_s[j] - x_s[i])

		############# V1 ##############
		div = noms * (pow(dens, q-2, q) % q)
		div %= q
		# print("Float Div: ", div)
		div = int(div)
		# print("Int Div: ", div)

		# print("Div: ", div)
		if div < 0:
			div = abs(div)
			temp = pow(y_s[i], p-2, p)
			result *= pow(temp, div, p)

		else:
			result *= pow(y_s[i], div, p)
		###############################
	result = _divmod(Y, result, p)
	result %= p
	votes = vote_gen.vote_cnt(G, p, k, ell, result)
	return votes


def CheckQuorum(a, h_a_lambda, p, q):
	return


def ZK_commonexp(Lambda_i, h_a_lambda_i, Omega_i, p, q):
	return


# HELPERS

def _eval_at(poly, x, prime):
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


def split_secret(secret, threshold, nmany, prime):
    poly = [secret]
    poly1 = [random.randint(0, prime) for i in range(threshold - 1)]
    poly.extend(poly1)
    # print("Poly: ", poly)
    points = [(i, _eval_at(poly, i, prime)) for i in range(1, nmany + 1)]
    # print("Points: ", points)
    return points


# division in integers modulus p means finding the inverse of the denominator
# modulo p and then multiplying the numerator by this inverse
# (Note: inverse of A is B such that A*B % p == 1)
# this can be computed via extended euclidean algorithm
# http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
def _extended_gcd(a, b):
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b,  a%b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    '''
    compute num / den modulo prime p
    To explain what this means, the return
    value will be such that the following is true:
    den * _divmod(num, den, p) % p == num
    '''
    inv, _ = _extended_gcd(den, p)
    return num * inv
