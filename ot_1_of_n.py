"""Implementation of Oblivious Transfer 1 of n protocol."""
import random

from charm.core.math.integer import integer  # pylint: disable=no-name-in-module
from charm.toolbox.integergroup import IntegerGroupQ

NUMBER_OF_MESSAGES = 5
SECURITY_PARAM = 20
G = IntegerGroupQ()
G.paramgen(SECURITY_PARAM)
g = integer(G.randomGen(), G.q)

def main():
  # A got messages.
  msgs = [G.random() for _ in range(NUMBER_OF_MESSAGES)]
  rs = [G.random() for _ in msgs]
  Rs = [g ** r for r in rs]
  # A sends Rs to B.

  # B chooses random Alpha & index k
  k = random.choice(range(len(msgs)))
  alpha = G.random()
  X = Rs[k] ** alpha
  # B sends X to A.

  # A calculates Ws.
  ws = [X ** (1/rs_i) for rs_i in rs]
  zs = [m_i * w_i for m_i, w_i in zip(msgs, ws)]
  # A sends cs to B.

  # B checks message.
  msg = zs[k] / integer(g ** alpha, G.q)

  # Verification.
  import pdb; pdb.set_trace()
  assert msg == msgs[k]

if __name__ == "__main__":
  main()
