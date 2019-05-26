"""Oblivious polynomial evaluation.

Sender has poly P(y) = Sum for i in 0..d_P b_i y^i of degree d_P
Receiver has alpha and wants to get P(alpha)

Sender generates random masking polynomial P_x(X) of degree d, s.t. P_x(0) = 0
P_x(x) = Sum for i in 1..d a_i x^i

Param d equals degree of P multiplied by security parameter k,
i. e. d = k * d_P

Sender defines Q(x, y) = P_x(x) + P(y)


Receiver hides alpha in a univariate polynomial:

Receiver chooses random poly S of degree k such that S(0) = alpha
Receiver's plan is to use R(x) = Q(x, S(x)) to learn P(alpha)
R(0) = Q(0, S(0)) = P(S(0)) = P(alpha)
"""
import random

from charm.toolbox.integergroup import IntegerGroupQ
from charm.core.math.integer import integer
from charm.core.math.integer import reduce as reduce_modulus
from utils import Poly, LI


SECURITY_PARAM = 20
G = IntegerGroupQ()
G.paramgen(SECURITY_PARAM)
g = G.randomGen()

k = 4
m = 4
d_p = 12 # Degree of P
d = d_p * k  # Degree of P_x

def main():
  # Receiver has alpha.
  alpha = G.random()

  # Sender has polynomial P.
  P = Poly([G.random() for _ in range(d_p + 1)])

  # Sender generates random masking poly P_x
  P_x = Poly([G.random() for _ in range(d + 1)])
  P_x[0] = integer(0, G.q) # To hold assumption that P_x(0) == 0

  # Sender defines bivariate polynomial Q(x, y).
  # deg(Q) == deg(P_x) == d == d_p * k
  Q = lambda x, y: reduce_modulus(P_x(x) + P(y))

  # Receiver hides alpha in a univariate polynomial.
  # deg(S) == k
  S = Poly([G.random() for _ in range(k + 1)])
  S[0] = alpha

  # The receiver sets n = dR + 1 = d + 1 = kdP + 1 and chooses N = nm distinct random
  # values x1, . . . , xN ∈ F, all different from 0.
  n = k * d_p + 1
  N = n * m
  X = [G.random() for _ in range(N)]

  # The receiver chooses a random set T of n indices 1 ≤ i1, i2, . . . , in ≤ N.
  T = list(range(N))
  random.shuffle(T)
  T = T[:n]

  # Receiver defines N values yi, for 1 ≤ i ≤ N. The value yi is defined as
  # S(xi) if i is in T, and is a random value if F otherwise.
  # The receiver sends the N points (Y) to the sender
  Y = [(x, S(x) if i in T else G.random()) for i, x in enumerate(X)]
  Qs = [(x, Q(x, y)) for x, y in Y]

  # Receiver calculates values.
  R_values = [v for i, v in enumerate(Qs) if i in T]
  R_0 = LI(integer(0, G.q), R_values)
  P_alpha = P(alpha)

  assert R_0 == P_alpha


if __name__ == "__main__":
  main()
