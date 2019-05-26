"""Util methods."""

import functools
import operator
from charm.core.math.integer import reduce as reduce_modulus

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

def product_modulus(iterable):
  return functools.reduce(operator.mul, iterable)

def sum_modulus(A):
  return functools.reduce(operator.add, A)

def LI(argument, interpolation_set):
  return reduce_modulus(sum_modulus(
      yj * product_modulus((argument - xm) / (xj - xm) for xm, _ in interpolation_set if xm != xj)
      for xj, yj in interpolation_set
  ))

def LI_exp(argument, interpolation_set):
  return product_modulus((
      grtag ** (product_modulus(
          (argument - m_prim) / (m - m_prim)
          for m_prim, _ in interpolation_set if m_prim != m))
  ) for m, grtag in interpolation_set)
