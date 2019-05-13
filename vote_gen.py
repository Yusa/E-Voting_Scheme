import random
from decimal import Decimal


def vote_cast(p, q, g, Gj, h):
	ri = random.randint(1, q-1)
	xi = pow(g, ri, p)
	yi = pow(h, ri, p) * Gj
	return xi, yi


def combine(x, y, ell, p):
	bigX = 1
	bigY = 1
	for i in range(ell):
		bigX *= x[i]
		bigX %= p
		bigY *= y[i]
		bigY %= p

	return bigX, bigY


def decrypt(X, Y, p, q, s):
	powRes = pow(X, p-2, p)

	powRes = pow(powRes, s, p)
	yxs = Y * powRes % p
	return yxs


def vote_cnt(G, p, k, ell, result, votesR):
	voteList = list(f(k,ell))
	resVotes = None
	for votes in voteList:
		resTry = 1
		for j in range(k):
			resTry *= pow(G[j], votes[j], p)
			resTry %= p
		
		if resTry == result:
			resVotes = votes
			print("Suc Exhaust: ", resTry)
			print("Suc Origres: ", result)
			break

		if votes == votesR:
			print("Exhaust: ", resTry)
			print("Origres: ", result)
			break

	return resVotes

######### HELPERS ##########

def f(length,total_sum):
    if length == 1:
        yield [total_sum,]
    else:
        for value in range(total_sum + 1):
            for permutation in f(length - 1,total_sum - value):
                yield [value,] + permutation
