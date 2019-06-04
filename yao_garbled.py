import random

from charm.toolbox import symcrypto




def random_bytes(size):
  with open('/dev/random', 'rb') as f:
    return f.read(size)


def encrypt(k1, k2, m1):
  c1 = symcrypto.SymmetricCryptoAbstraction(k1).encrypt(m1)
  c2 = symcrypto.SymmetricCryptoAbstraction(k2).encrypt(c1)
  return c2


def decrypt(k1, k2, c2):
  c1 = symcrypto.SymmetricCryptoAbstraction(k2).decrypt(c2)
  m = symcrypto.SymmetricCryptoAbstraction(k1).decrypt(c1)
  return m

keys = dict((k, random_bytes(128)) for k in ['A_0', 'A_1', 'B_0', 'B_1', 'C_0', 'C_1'])
Alice_keys = {k: v for k, v in keys.items() if 'A' in k}
Bob_keys = {k: v for k, v in keys.items() if 'B' in k}


Table = [
    encrypt(keys['A_0'], keys['B_0'], keys['C_0']),
    encrypt(keys['A_0'], keys['B_1'], keys['C_0']),
    encrypt(keys['A_1'], keys['B_0'], keys['C_0']),
    encrypt(keys['A_1'], keys['B_1'], keys['C_1'])
]

random.shuffle(Table)

Alice_A = random.choice(tuple(Alice_keys.values()))
Bob_B = random.choice(tuple(Bob_keys.values()))

print(f'Alice has chosen {Alice_A}')
print(f'Bob has chosen {Bob_B}')


# for i, t in enumerate(Table):
#   try:
#     a = decrypt(Alice_A, Bob_b, t)
#   except UnicodeDecodeError:
#     pass
#   else:
#     print(a == keys['C_0'])