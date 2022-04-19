import pandas as pd
import math
from scipy.stats import ttest_ind_from_stats
from prettytable import PrettyTable

# read the file
data = pd.read_csv('ab_test.csv', parse_dates=['time'])


def general_info_original(data):
    show_sample = data.head(5)
    length = len(data)

    print(show_sample)
    print("The dataset size is ", length)

    return data


def data_cleaning(data):
    if data.isnull().sum().any():  # remove missing values
        data.dropna(axis=0, how='any')

    data.drop_duplicates(subset='id')  # remove duplicate values

    # remove mistreated variables
    miss1 = data.query('page == "new_page" and con_treat == "control"').index
    miss2 = data.query('page == "old_page" and con_treat == "treatment"').index
    data2 = data.drop(index=miss1, axis=0)
    data2 = data2.drop(index=miss2, axis=0)

    return data2


def split_data(data):
    grouped = data.groupby(data.con_treat)
    con_data = grouped.get_group("control")
    tre_data = grouped.get_group("treatment")

    return con_data, tre_data


def cleaned_dataset_info(data):
    test_size = data.id.nunique()
    show_sample = data.head(5)
    data_mean = data.converted.mean()
    time_dur = data.time.max(), data.time.min()

    return test_size, show_sample, data_mean, time_dur

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
        p_value = float(p_value)
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
            print("The P_value is ", p_value, ", which is bigger than 0.05, we cannot reject the null hypothesis.")


def main():
    starter = int(input("Enter 1 to start the A/B testing result analysis: "))
    if starter != 1:
        return
    else:
        print("First, let's take a look at the original dataset:")
        general_info_original(data)

    data2 = data_cleaning(data)
    con_data, tre_data = split_data(data2)
    con_test_size, con_show_sample, con_data_mean, con_time_dur = cleaned_dataset_info(con_data)
    tre_test_size, tre_show_sample, tre_data_mean, tre_time_dur = cleaned_dataset_info(tre_data)
    remove_val = len(data) - len(data2)
    print("\n", remove_val, "data has been removed\n")

    print("\nNow, let's sum up the information of cleaned control group and treatment group: \n")
    table = PrettyTable(['Group', 'Data Size', 'Mean', 'Time Duration'])
    table.add_row(['Control', con_test_size, con_data_mean, con_time_dur])
    table.add_row(['Treatment', tre_test_size, tre_data_mean, tre_time_dur])
    print(table)

    hy_starter = int(input("Enter 2 to verify hypothesis testing: "))
    if hy_starter == 2:
        ci_level = input("Please choose the confidence interval level: ")
    else:
        print("Program End")
        return

    CI_level(pvalue(con_data,tre_data),ci_level)


if __name__ == '__main__':
    main()
