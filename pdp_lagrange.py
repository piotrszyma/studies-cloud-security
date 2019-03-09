# pylint: disable=invalid-name
"""Implementation Proof of possession algorithm for Cloud Storage."""
import random
import hashlib

from charm.core.math.integer import integer  # pylint: disable=no-name-in-module
from charm.toolbox.integergroup import IntegerGroupQ

from utils import Poly, lagrange_interpolate

SECURITY_PARAM = 5
G = IntegerGroupQ()
G.paramgen(SECURITY_PARAM)
g = G.randomG()
SECRET_KEY = G.random()
NUM_OF_BLOCKS = 1
NUM_OF_SUBBLOCKS = 4
z = NUM_OF_SUBBLOCKS

def ID(block):
  return hashlib.sha512(str(block).encode('utf-8')).hexdigest()

# def setup(security_param=1024):
#   """Setup defines system parameters for a user.

#   1. Choose G supgroup of Zp* of order q, s. t. q, p are prime, q | p - 1
#     and DLP is hard to G
#   2. SKc <-- r Zq

#   Args:
#     security_param: minmum number of bits of q.

#   Returns:
#     Master secret key SKc of the user.
#   """
#   group.paramgen(security_param)
#   secret_key = group.random()
#   return secret_key


def poly(secret_key, block_id):
  """Yields an secret polynomial Lf over Zq for a given block f."""
  random.seed(str(secret_key) + block_id)
  return Poly([integer(random.randrange(G.q), G.q) for _ in range(NUM_OF_SUBBLOCKS)])  # pylint: disable=not-callable

def tag_block(secret_key, block):
  """Tag generating procedure."""
  generated_poly = poly(secret_key, ID(block))
  sub_blocks_with_tags = [(message, generated_poly(message)) for message in block]
  return sub_blocks_with_tags

def tag_blocks(secret_key, message):
  for block in message:
    yield tag_block(secret_key, block)

def gen_challenge(secret_key, block_id):
  Lf = poly(secret_key, block_id)
  r = G.random()
  xc = G.random()
  Kf = g ** (r * Lf(xc))
  H = (g**r, xc, g ** (r * Lf(integer(0, G.q))))
  return Kf, H

def gen_challenges(secret_key, block_ids):
  for block_id in block_ids:
    yield gen_challenge(secret_key, block_id)

def gen_proof(challenge, blocks_with_tags):
  g_r, xc, g_lf0 = challenge
  interpolation_set = [(integer(0, G.q), g_lf0)] + [(message, g_r ** tag)
                        for message, tag in blocks_with_tags]
  Pf = lagrange_interpolate(xc, interpolation_set)
  return Pf

def gen_proofs(challenges, blocks_of_subblocks_with_tags):
  for challenge, blocks_with_tags in zip(challenges,
                                         blocks_of_subblocks_with_tags):
    yield gen_proof(challenge, blocks_with_tags)

def main():
  message = [[integer(random.randrange(0, G.q), G.q) for _ in range(NUM_OF_SUBBLOCKS)]
             for _ in range(NUM_OF_BLOCKS)]
  print('Message generated.')
  t = tag_block(SECRET_KEY, message[0])
  print('Tags generated.')
  Kf, H = gen_challenge(SECRET_KEY, ID(message[0]))
  print('Challenge generated.')
  Pf = gen_proof(H, t)
  print('Proof generated.')
  assert Kf == Pf

if __name__ == '__main__':
  main()
