


def change_vote(p, q, g, G, x, y, r, j, k):
	x_ = pow(g, r, p)
	# y = pow(h, r, p) * G[j-1]
	GjInv = pow(G[j-1], p-2, p)
	y_ = y * GjInv * G[k-1]
	y_ %= p
	return x_, y_