import random
import setup

def voter_I(p, q, g, G, vote, j, h):
	j = j - 1

	r = random.randint(1, q-1)
	x = pow(g, r, p)
	y = pow(h, r, p) * vote % p

	w = random.randint(2, q-1)


	cList = [0] * len(G)
	zList = [0] * len(G)
	aList = [0] * len(G)
	bList = [0] * len(G)

	aList[j] = pow(g, w, p)
	bList[j] = pow(h, w, p)

	for i in range(len(G)):
		if i != j:
			cList[i] = random.randint(2, q-1)
			zList[i] = random.randint(2, q-1)

			# print(h)
			# print(zList[i])
			# print(y)
			# print(cList[i])

			aList[i] = pow(g, zList[i], p) * pow(x, cList[i], p)
			aList[i] %= p
			bList[i] = pow(h, zList[i], p) * pow(y, cList[i], p) * pow(pow(G[i], p-2, p), cList[i], p)
			bList[i] %= p

	# print(aList)
	# print(bList)
	# print(cList)
	# print(zList)
	return x, y, aList, bList, cList, zList, r, w


def voter_III(p, q, g, j, C, cList, zList, r, w):
	j = j - 1
	cList[j] = C - sum(cList)

	# ricj = sum([r * x for x in cList])
	# print(cList)
	# print(ricj)

	zList[j] = w - (r * cList[j]) 

	return cList, zList


def handleNegative(elem1, possibleNeg, prime):
	if possibleNeg < 0:
		possibleNeg = abs(possibleNeg)
		elem1 = pow(elem1, prime-2, prime)
	return elem1, possibleNeg

def HV_IV(p, q, g, h, G, C, x, y, aList, bList, cList, zList):
	firstCond, secondCond, thirdCond = True, True, True
	if C != sum(cList):
		firstCond = False

	for i in range(len(G)):
		gTemp, zVal = handleNegative(g, zList[i], p)
		xTemp, cVal = handleNegative(x, cList[i], p)
		ai = pow(gTemp, zVal, p) * pow(xTemp, cVal, p)
		ai %= p
		if ai != aList[i]:
			secondCond = False


	for i in range(len(G)):
		hTemp, zVal = handleNegative(h, zList[i], p)
		yTemp, cVal = handleNegative(y, cList[i], p)
		GTemp, _ = handleNegative(G[i], -1, p)
		GTemp, cVal2 = handleNegative(GTemp, cList[i], p)
		# print("--------------\n\n\n------------")
		# print(hTemp) 
		# print(zVal)
		# print(yTemp) 
		# print(cVal)

		bi = pow(hTemp, zVal, p) * pow(yTemp, cVal, p) * pow(GTemp, cVal2, p)
		bi %= p
		# print(bi)
		# print(bList[i])
		# print(bi == bList[i])
	
		if bi != bList[i]:
			thirdCond = False

	
	return firstCond and secondCond and thirdCond


def fake_vote_gen(p, q):
	G, _ = setup.Verifiably_Random_Generator(p, q)
	return G

