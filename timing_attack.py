import time
import random
import contextlib
import itertools

@contextlib.contextmanager
def time_check():
  start = time.time()
  try:
    yield
  finally:
    print(time.time() - start)


def odd(n):
  return n % 2 != 0

def time_benchmark(func):
  def benchmarked(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print(end - start)
    return result
  return benchmarked

def fast_exp(a: int, n: int, m: int, delays=False) -> int:
  x = a

  if odd(n):
    if delays:
      time.sleep(0.01)
    y = a
  else:
    y = 1

  n_prim = n // 2
  while n_prim > 0:
    x = (x ** 2) % m
    if odd(n_prim):
      if delays:
        time.sleep(0.01)
      y = x if y == 1 else (y * x) % m
    n_prim = n_prim // 2
  return y

a = 2
n = random.randint(128, 255)
print(f'Random number to find is... {n}')
m = 630899156147664284829166865938701721337


start = time.time()
result = fast_exp(a, n, m, delays=True)
end = time.time() - start
num_of_ones = int(end // 0.01)

perms = itertools.permutations(
  (1,) * (num_of_ones - 1) + (0,) * (8 - num_of_ones))

for perm in perms:
  repr = '1'+ ''.join(map(str, perm))
  num = int(repr, base=2)
  if result == fast_exp(a, num, m):
    print(f"Found number: {num}")
    break
