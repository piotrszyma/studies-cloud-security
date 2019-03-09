"""Util methods."""

import functools


class Poly:
  """Polynomial

  poly = Poly(coeffs)
  poly(x) -> val
  """

  def __init__(self, coeffs):
    self.coeffs = coeffs

  def __call__(self, block):
    return functools.reduce(lambda prev, curr: curr * block + prev, self.coeffs)

def product(iterable):
  return functools.reduce(lambda x, y: x * y, iterable)

def lagrange_interpolate(argument, interpolation_set):
  return product((
      grtag ** (product(
          (argument - m_prim) / (m - m_prim)
          for m_prim, _ in interpolation_set if m_prim != m))
  ) for m, grtag in interpolation_set)
