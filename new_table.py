import tkinter as tk
import json
from gui import FrameContent, ButtonLeftText
from functools import partial
from tkinter import filedialog
import pandas as pd

with open('settings.json') as json_file:
    settings = json.load(json_file)

window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
top_menu_height_initial = settings['dimensions']['top_menu_height']
left_menu_width_initial = 50
left_menu_height_initial = window_height_initial - top_menu_height_initial
bg_identification = settings['colors']['bg_identification']


class NewTable:
    """ Create a new page window """

    def __init__(self, p_parent, p_left_frame, p_right_frame, p_top_frame, p_extension_images):
        """ Initialization of create page window """

        # Parameters
        self.parent = p_parent
        self.nb_row = 5
        self.nb_column = 5
        self.left_frame = p_left_frame
        self.right_frame = p_right_frame
        self.top_frame = p_top_frame
        self.extension_images = p_extension_images

        # Window handle
        self.window_new_page = tk.Toplevel(self.parent)
        self.window_new_page.resizable(False, False)
        self.window_new_page.title("Ajouter un tableau")
        window_new_page_icon = tk.PhotoImage(file="img/add.png")
        self.window_new_page.iconphoto(False, window_new_page_icon)
        width_window = 600
        height_window = 395
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x_cord = int((screen_width / 2) - (width_window / 2))
        y_cord = int((screen_height / 2) - (height_window / 2))
        self.window_new_page.grid_propagate(False)
        self.window_new_page.geometry("{}x{}+{}+{}".format(width_window, height_window, x_cord, y_cord))
        self.window_new_page.columnconfigure((0, 1), weight=1)
        self.window_new_page.rowconfigure((0, 1), weight=1)

        # First part of the window
        self.first_frame = tk.Frame(self.window_new_page, bg="#DCDCDC", width=390, height=385)
        self.first_frame.grid(row=0, column=0, rowspan=2, padx=(5, 5), pady=(5, 5))
        self.first_frame.columnconfigure(0, weight=1)
        self.first_frame.grid_propagate(False)

        self.first_label_title = tk.Label(self.first_frame, text="Ouvrir un fichier", bg=bg_identification, fg="white")
        self.first_label_title.grid(row=0, sticky='news')
        self.first_label_title.config(font=("Calibri bold", 12))

        self.frame_extensions = tk.Frame(self.first_frame, bg="#DCDCDC", height=260)
        self.frame_extensions.grid(row=1, pady=(10, 0), sticky='news')
        self.frame_extensions.grid_propagate(False)

        self.label_choose = tk.Label(self.frame_extensions, text="Choisir l'extension du fichier", bg="#DCDCDC", fg="black")
        self.label_choose.grid(row=0, columnspan=3)
        self.label_choose.config(font=("Calibri bold", 11))

        self.frame_open = [[tk.Frame() for i in range(3)] for j in range(2)]
        self.button_open = [[tk.Button() for i in range(3)] for j in range(2)]
        id = 0
        for i in range(2):
            for j in range(3):
                self.frame_open[i][j] = tk.Frame(self.frame_extensions, bg="white", height=100, width=100)
                self.frame_open[i][j].grid(row=i+1, column=j, padx=(15, 15), pady=(10, 10))
                self.frame_open[i][j].grid_propagate(False)
                self.button_open[i][j] = tk.Button(self.frame_open[i][j], width=95, height=95, command=partial(self.create_table, id))
                self.button_open[i][j].grid(row=0)
                id += 1

        self.button_open[0][0].config(image=self.extension_images[0])
        self.button_open[0][1].config(image=self.extension_images[1])
        self.button_open[0][2].config(image=self.extension_images[2])
        self.button_open[1][0].config(image=self.extension_images[3])
        self.button_open[1][1].config(image=self.extension_images[4])
        self.button_open[1][2].config(bg="#DCDCDC", state=tk.DISABLED, borderwidth=0)

        self.label_filename = tk.Label(self.first_frame, text="Fichier chargé :", bg="#DCDCDC", fg="black", width=40)
        self.label_filename.grid(row=2, pady=(10, 10))
        self.label_filename.config(font=("Calibri bold", 11))

        self.label_filename = tk.Label(self.first_frame, text=" ", bg="#DCDCDC", fg="black", width=40, relief="groove")
        self.label_filename.grid(row=3)
        self.label_filename.config(font=("Calibri bold", 10))

        # Second part of the window
        self.second_frame = tk.Frame(self.window_new_page, bg="#DCDCDC", width=200, height=200)
        self.second_frame.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))
        self.second_frame.columnconfigure(0, weight=1)
        self.second_frame.grid_propagate(False)

        self.second_label_title = tk.Label(self.second_frame, text="Nommer le fichier", bg=bg_identification, fg="white")
        self.second_label_title.grid(row=0, sticky='news')
        self.second_label_title.config(font=("Calibri bold", 12))

        self.second_label_description = tk.Label(self.second_frame, text="Veuillez fournir un\n nom au tableau", bg="#DCDCDC", fg="black")
        self.second_label_description.grid(row=1, pady=(40, 0), sticky='news')
        self.second_label_description.config(font=("Calibri bold", 11))

        self.entry_name = tk.Entry(self.second_frame, width=20)
        self.entry_name.grid(row=2, pady=(15, 0))
        self.entry_name.config(font=("Calibri bold", 10))

        # Third part of the window
        self.third_frame = tk.Frame(self.window_new_page, bg="#DCDCDC", width=200, height=185)
        self.third_frame.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))
        self.third_frame.columnconfigure(0, weight=1)
        self.third_frame.grid_propagate(False)

        self.third_label_title = tk.Label(self.third_frame, text="Confirmation", bg=bg_identification, fg="white")
        self.third_label_title.grid(row=0, sticky='news')
        self.third_label_title.config(font=("Calibri bold", 12))

        self.button_confirmation = tk.Button(self.third_frame, text="Confirmer", width=20)
        self.button_confirmation.grid(row=1, pady=(50, 0))
        self.button_confirmation.config(font=("Calibri bold", 10))

    def openfilename(self):
        """ Open file dialog box to select file
        :return: the name of the file
        """

        filename = filedialog.askopenfilename(title='Ouvrir un fichier')
        return filename

    def create_table(self, p_id):

        if p_id == 0:
            filename = self.openfilename()
            if filename != '':
                df = pd.read_csv(filename)
                print(df)

        if p_id == 1:
            filename = self.openfilename()
            if filename != '':
                df = pd.read_excel(filename)
                print(df)

        # row = len(self.left_frame.buttons_table) + 1
        # new_button_left = ButtonLeftText(str(filename), row, self.left_frame.moving_frames[3], "white", None)
        # self.left_frame.buttons_table.append(new_button_left)

        self.label_filename.config(text=str(filename))

        self.window_new_page.lift()









