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

# Random input of Bob.
Alice_index = random.choice(['A_0', 'A_1'])
Alice_key = keys[Alice_index]

# Random input (Bob chooses) of Bob
Bob_index = random.choice(['B_0', 'B_1'])
Bob_key = keys[Bob_index]

# A garbled table is being created that obfuscates the truth table.
#
#   F: (A, B) -> C
#
#  #=================#
#  |  A  |  B  |  C  |
#  #=================#
#  |  0  |  0  |  0  |
#  |  0  |  1  |  0  |
#  |  1  |  0  |  0  |
#  |  1  |  1  |  1  |
#  #=================#
# Parties don't trust each other but want to get value C based on their A & B.

values_mapping = {
    (keys['A_0'], keys['B_0']): keys['C_0'],
    (keys['A_0'], keys['B_1']): keys['C_0'],
    (keys['A_1'], keys['B_0']): keys['C_0'],
    (keys['A_1'], keys['B_1']): keys['C_1'],
}

# A garbled circuit is being generated that masks function F.
garbled_table = [
    encrypt(keys['A_0'], keys['B_0'], keys['C_0']),
    encrypt(keys['A_0'], keys['B_1'], keys['C_0']),
    encrypt(keys['A_1'], keys['B_0'], keys['C_0']),
    encrypt(keys['A_1'], keys['B_1'], keys['C_1'])
]
random.shuffle(garbled_table)

print(f'Alice has chosen {Alice_index}')
print(f'Bob has chosen {Bob_index}')

# They can get only single value at that interesting point.
for t in garbled_table:
  try:
    a = decrypt(Alice_key, Bob_key, t)
    if a == values_mapping[(Alice_key, Bob_key)]:
      print(f'Valid value of F({Alice_index}, {Bob_index}) found.')
      break
  except UnicodeDecodeError:
    pass
else:
  print('Valid value not found...')