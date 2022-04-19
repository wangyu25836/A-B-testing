import math
from scipy.stats import ttest_ind_from_stats


def variance(data):
    n = len(data.converted)
    mean = data.converted.mean()

    deviations = [((float(x) - mean)**2) for x in data.converted]
    var = sum(deviations) / n
    return var


def std(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev


def pvalue(data1, data2):
    n1 = len(data1.converted)
    n2 = len(data2.converted)
    mean1 = data1.converted.mean()
    mean2 = data2.converted.mean()
    std1 = std(data1)
    std2 = std(data2)

    p_value = ttest_ind_from_stats(mean1, std1, n1, mean2, std2, n2).pvalue

    return p_value



def CI_level(p_value, ci_level):
    if ci_level == "90%":
        if p_value < 0.10:
            print("The P_value is ", p_value, ", we can reject the null hypothesis.")
        else:
            print("The P_value is ", p_value, ", which is bigger than 0.10, we cannot reject the null hypothesis.")
    if ci_level == "95%":
        if p_value < 0.05:
            print("The P_value is ", p_value, ", we can reject the null hypothesis.")
        else:
            print("The P_value is ", p_value, ", which is bigger than 0.05, we cannot reject the null hypothesis.")
    if ci_level == "99%":
        if p_value < 0.01:
            print("The P_value is ", p_value, ", we can reject the null hypothesis.")
        else:
            print("The P_value is ", p_value, ", which is bigger than 0.01, we cannot reject the null hypothesis.")





            

