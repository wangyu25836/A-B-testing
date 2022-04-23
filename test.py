import pandas as pd
from prettytable import PrettyTable
from sig_data import pvalue
from sig_data import CI_level
from review import general_info_original
from review import data_cleaning
from review import split_data
from review import cleaned_dataset_info


data = pd.read_csv('ab_test.csv', parse_dates=['time'])

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
