"""Implementation of Oblivious Transfer 1 of 2 protocol."""
import hashlib

from charm.core.math.integer import integer  # pylint: disable=no-name-in-module
from charm.toolbox.integergroup import IntegerGroupQ

SECURITY_PARAM = 5
G = IntegerGroupQ()
G.paramgen(SECURITY_PARAM)
g = G.randomGen()

def get_hash(number):
  return hashlib.sha256(int(number).to_bytes(256, byteorder='big')).digest()

def xor(otp: bytes, msg: bytes) -> bytes:
  return bytes(hash_byte ^ msg_byte for hash_byte, msg_byte in zip(otp, msg))

def main():
  # A generates random number.
  c = G.random()
  C = g ** c

  # C is being sent to B.
  # A ----- (C) ----> B

  # B receives C and generates k.
  k = G.random()
  PK_0 = g ** k
  PK_1 = C / (g ** k)
  # PK_0 and PK_1 are being sent to A.
  # (first value is chosen message, so b == 0 in this case)
  # A <-(PK_0, PK_1)- B

  # A generates c0 & c1.
  r0 = G.random()
  r1 = G.random()
  m0 = b"message 0"
  m1 = b"message 1"
  c0 = (g ** r0, xor(get_hash(PK_0 ** r0), m0))
  c1 = (g ** r1, xor(get_hash(PK_1 ** r1), m1))
  # A -- (c0, c1) --> B

  # B receives c0 & c1, retreives chosen message.
  w0 = c0[1]
  H = c0[0] ** k
  assert xor(get_hash(H), w0) == m0

if __name__ == "__main__":
  main()
