import pandas as pd
import json


# Initialization of the dataframe
df = pd.read_csv('csv/csv_test.csv')
nb_row_df = df.shape[0]
nb_column_df = df.shape[1]

# Open the data file
with open('widgets/summary/summary_data.json') as json_file:
    widgets_data = json.load(json_file)


def fill_file():
    nb_computer = get_nb_iterations_1_word("materiel", "ordinateur")
    nb_phone = get_nb_iterations_1_word("materiel", "téléphone")
    nb_user_in_paris = get_nb_iterations_1_word("site", "paris")
    nb_computer_and_phone = get_nb_iterations_2_words("materiel", "ordinateur", "téléphone")

    save_data("Ordinateurs", nb_computer)
    save_data("Telephones", nb_phone)
    save_data("Utilisateurs sur Paris", nb_user_in_paris)
    save_data("Ordinateurs et telephones", nb_computer_and_phone)


def save_data(p_name, p_data):
    #

    # Build the data that will be add to the saving file
    value_data = {p_name: p_data}

    # Update the saving file (.json) with these data
    widgets_data['data'].update(value_data)
    with open('widgets/summary/summary_data.json', 'w') as outfile:
        json.dump(widgets_data, outfile, indent=4)


def get_nb_iterations_1_word(p_column, p_word):

    # Get the index of p_column
    headers_list = list(df.columns.values)
    col = -1
    for i in headers_list:
        if i.lower() == p_column.lower():
            col = headers_list.index(i)

    # Get nb of iteration of p_word
    iterations = 0
    for i in range(0, nb_row_df):
        if df.iloc[i][col].lower() == p_word.lower() :
            iterations += 1

    return iterations


def get_nb_iterations_2_words(p_column, p_word_1, p_word_2):

    # Get nb of iteration of p_word
    iterations_1 = get_nb_iterations_1_word(p_column, p_word_1)
    iterations_2 = get_nb_iterations_1_word(p_column, p_word_2)

    return iterations_1 + iterations_2
