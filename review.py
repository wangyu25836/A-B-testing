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
