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
        width_window = 400
        height_window = 395
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x_cord = int((screen_width / 2) - (width_window / 2))
        y_cord = int((screen_height / 2) - (height_window / 2))
        self.window_new_page.grid_propagate(False)
        self.window_new_page.geometry("{}x{}+{}+{}".format(width_window, height_window, x_cord, y_cord))
        self.window_new_page.columnconfigure((0, 1), weight=1)

        # Left part of the window
        self.frame = tk.Frame(self.window_new_page, bg="#DCDCDC", width=390, height=385)
        self.frame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_propagate(False)

        self.label_title = tk.Label(self.frame, text="Ouvrir un fichier", bg=bg_identification, fg="white")
        self.label_title.grid(row=0, sticky='news')
        self.label_title.config(font=("Calibri bold", 12))

        self.frame_extensions = tk.Frame(self.frame, bg="#DCDCDC", height=360)
        self.frame_extensions.grid(row=1, sticky='news')
        self.frame_extensions.grid_propagate(False)

        self.frame_open = [[tk.Frame() for i in range(3)] for j in range(3)]
        self.button_open = [[tk.Button() for i in range(3)] for j in range(3)]
        id = 0
        for i in range(3):
            for j in range(3):
                self.frame_open[i][j] = tk.Frame(self.frame_extensions, bg="white", height=100, width=100)
                self.frame_open[i][j].grid(row=i, column=j, padx=(15, 15), pady=(10, 10))
                self.frame_open[i][j].grid_propagate(False)
                self.button_open[i][j] = tk.Button(self.frame_open[i][j], width=95, height=95, command=partial(self.create_table, id))
                self.button_open[i][j].grid(row=0)
                id += 1

        self.button_open[0][0].config(image=self.extension_images[0])
        self.button_open[0][1].config(image=self.extension_images[1])
        self.button_open[0][2].config(image=self.extension_images[2])
        self.button_open[1][0].config(image=self.extension_images[3])
        self.button_open[1][1].config(image=self.extension_images[4])

    def openfilename(self):
        """ Open file dialog box to select file
        :return: the name of the file
        """

        filename = filedialog.askopenfilename(title='Ouvrir un fichier')
        return filename

    def create_table(self, p_id):

        if p_id == 0:
            filename = self.openfilename()
            df = pd.read_csv(filename)
            print(df)

        if p_id == 1:
            filename = self.openfilename()
            df = pd.read_excel(filename)
            print(df)

        row = len(self.left_frame.buttons_table) + 1
        new_button_left = ButtonLeftText(str(filename), row, self.left_frame.moving_frames[3], "white", None)
        self.left_frame.buttons_table.append(new_button_left)








