"""Util methods."""

import functools
from charm.core.math.integer import reduce as reduce_int

class Poly:
  """Polynomial

  poly = Poly(coeffs)
  poly(x) -> val
  """

  def __init__(self, coeffs):
    self.coeffs = coeffs

  def __call__(self, block):
    return functools.reduce(lambda prev, curr: curr * block + prev, self.coeffs)

  def __setitem__(self, attr, value):
    self.coeffs[attr] = value

  def __getitem__(self, attr):
    return self.coeffs[attr]

def product(iterable):
  return functools.reduce(lambda x, y: x * y, iterable)

def lagrange_interpolate(argument, interpolation_set):
  return product((
      grtag ** (product(
          (argument - m_prim) / (m - m_prim)
          for m_prim, _ in interpolation_set if m_prim != m))
  ) for m, grtag in interpolation_set)

# TODO: Fix the function above!

def sum(A):
  return functools.reduce(lambda x, y: x + y, A)

def LI(points, xc):
  return reduce_int(sum([
      yj * product([(xc - xm) / (xj - xm) for xm, _ in points if xm != xj])
      for xj, yj in points
  ]))