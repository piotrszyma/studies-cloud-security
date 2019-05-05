"""Implementation of Privacy Set Intersection protocol.

It is used when two parties want to get common elements without knowledge
about all elements they possess.
"""
from charm.toolbox.integergroup import IntegerGroupQ

NUMBER_OF_MESSAGES = 5
SECURITY_PARAM = 20
G = IntegerGroupQ()
G.paramgen(SECURITY_PARAM)
g = G.randomGen()


def main():
  # Elements generation phase, AnB contains similar elements.
  common = [g ** G.random() for _ in range(3)]

  # A generates hashes H_a and sends them to B.
  A = [g ** G.random() for _ in range(7)] + common
  a_k = G.random()
  H_a = [G.hash(a) ** a_k for a in A]


  # B generates hashes H_b and sends them to A.
  B = [g ** G.random() for _ in range(7)] + common
  b_k = G.random()
  H_b = [G.hash(b) ** b_k for b in B]


  # B powers hashes of A to his secret b.
  H_a_b = [a ** b_k for a in H_a]

  # A powers hashes of B to his secret a.
  H_b_a = [b ** a_k for b in H_b]

  # A computes common.
  a_common = [o for o, e in zip(A, H_a_b) if e in H_b_a]

  # B computes common.
  b_common = [o for o, e in zip(A, H_a_b) if e in H_b_a]

  assert a_common == b_common == common

if __name__ == "__main__":
  main()
