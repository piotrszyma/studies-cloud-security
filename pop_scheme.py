# pylint: disable=invalid-name
"""Implementation Proof of possession algorithm for Cloud Storage."""
import random
import hashlib

from charm.core.math.integer import integer  # pylint: disable=no-name-in-module
from charm.toolbox.integergroup import IntegerGroupQ

from utils import Poly, LI_exp

SECURITY_PARAM = 5
G = IntegerGroupQ()
G.paramgen(SECURITY_PARAM)
g = G.randomG()
SECRET_KEY = G.random()
NUM_OF_BLOCKS = 4
NUM_OF_SUBBLOCKS = 4
z = NUM_OF_SUBBLOCKS

def ID(block):
  return hashlib.sha512(str(block).encode('utf-8')).hexdigest()

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
  Pf = LI_exp(xc, interpolation_set)
  return Pf

def gen_proofs(challenges, blocks_of_subblocks_with_tags):
  for challenge, blocks_with_tags in zip(challenges,
                                         blocks_of_subblocks_with_tags):
    yield gen_proof(challenge, blocks_with_tags)

def main():
  message = [[integer(random.randrange(0, G.q), G.q) for _ in range(NUM_OF_SUBBLOCKS)]
             for _ in range(NUM_OF_BLOCKS)]
  # Message generated.
  tags = tag_blocks(SECRET_KEY, message) # [t, ...]
  # Tags generated.
  Kfs_Hs = tuple(gen_challenges(SECRET_KEY, (ID(block) for block in message))) # [(Kf, H), ...]
  # Challenges generated.
  Kfs = tuple(K for K, _ in Kfs_Hs)
  Hs = tuple(H for _, H in Kfs_Hs)
  Pfs = gen_proofs(Hs, tags)
  # Proofs generated.
  for Kf, Pf in zip(Kfs, Pfs):
    assert Kf == Pf
  print('Validated!')




if __name__ == '__main__':
  main()
