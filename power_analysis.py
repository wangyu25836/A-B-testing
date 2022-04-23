# determine how small of a difference needs to be detected
# run power analysis to find out the time and population that need to be runned

import numpy as np
import statsmodels.stats.power as smp
import matplotlib.pyplot as plt

a = input("Please enter the alpha:")
e_size = input("Please enter the effect size:")
p = input("Please enter the input level:")


def power_analysis(a, e_size, p):
    obj = smp.TTestIndPower()
    n = obj.solve_power(effect_size=e_size, alpha=a, power=p, alternative='two-sided')

    return n
