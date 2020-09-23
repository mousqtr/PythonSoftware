import tkinter as tk
import json
from functools import partial
from tkinter import ttk
import pandas as pd

# xlsx = pd.ExcelFile('excel/Gestion_Parc_Relyens.xlsx')
# df1 = pd.read_excel(xlsx, 'Laptop')
# df2 = pd.read_excel(xlsx, 'Desktop')
#
# def display_data():
#     print(df1.shape)
#     print(df1["Site"])
#     df1.at['C', 'x', ]

def display_data():
    df = pd.read_csv('csv/csv_test.csv')
    print(df['Nom'])
    df.at[0, 'Prenom'] =  'Alice'
    print(df)
    df.to_csv('csv/csv_test.csv')

