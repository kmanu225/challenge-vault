from math import gcd
from random import randint
from matplotlib import pyplot as plt
import numpy as np
from sympy import mod_inverse as invert
from sympy import isprime


def weierstrass(x, y, a, b):
    return pow(y, 2) - pow(x, 3) - a * x - b


def isInvertable(g: int, p: int) -> bool:
    """
    Check if g is invertable in Z/pZ.\n
    @param g: Integer number.
    @param p: Integer number.
    @return: bool
    """
    try:
        invert(g, p)
        return True
    except ValueError:
        return False


def isGenerator(g: int, p: int) -> bool:
    """
    Check if g is a generator of Z/pZ.\n
    @param g: Integer number.
    @param p: Prime number defining the group Z/pZ.
    @return: bool
    """
    if gcd(g, p) != 1:
        return False

    for i in range(1, p - 2):
        if pow(g, i, p) == 1:
            return False
    return True
