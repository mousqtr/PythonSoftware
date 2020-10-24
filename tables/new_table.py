import tkinter as tk
import json
from gui import ButtonLeftText, FrameSection
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
        self.window_new_table = tk.Toplevel(self.parent)
        self.window_new_table.resizable(False, False)
        self.window_new_table.title("Ajouter un tableau")
        window_new_table_icon = tk.PhotoImage(file="img/add.png")
        self.window_new_table.iconphoto(False, window_new_table_icon)
        width_window = 600
        height_window = 395
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x_cord = int((screen_width / 2) - (width_window / 2))
        y_cord = int((screen_height / 2) - (height_window / 2))
        self.window_new_table.grid_propagate(False)
        self.window_new_table.geometry("{}x{}+{}+{}".format(width_window, height_window, x_cord, y_cord))
        self.window_new_table.columnconfigure((0, 1), weight=1)
        self.window_new_table.rowconfigure((0, 1), weight=1)

        # First part of the window
        self.first_frame = tk.Frame(self.window_new_table, bg="#DCDCDC", width=390, height=385)
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
                self.button_open[i][j] = tk.Button(self.frame_open[i][j], width=95, height=95, command=partial(self.open_table, id))
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

        self.label_filename = tk.Label(self.first_frame, text="Aucun fichier chargé", bg="#DCDCDC", fg="black", width=40, relief="groove")
        self.label_filename.grid(row=3)
        self.label_filename.config(font=("Calibri", 10))

        self.filename = " "
        self.extension = -1

        # Second part of the window
        self.second_frame = tk.Frame(self.window_new_table, bg="#DCDCDC", width=200, height=200)
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
        self.third_frame = tk.Frame(self.window_new_table, bg="#DCDCDC", width=200, height=185)
        self.third_frame.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))
        self.third_frame.columnconfigure(0, weight=1)
        self.third_frame.grid_propagate(False)

        self.third_label_title = tk.Label(self.third_frame, text="Confirmation", bg=bg_identification, fg="white")
        self.third_label_title.grid(row=0, sticky='news')
        self.third_label_title.config(font=("Calibri bold", 12))

        self.button_confirmation = tk.Button(self.third_frame, text="Confirmer", width=20, command=self.confirm)
        self.button_confirmation.grid(row=1, pady=(50, 0))
        self.button_confirmation.config(font=("Calibri bold", 10))

        self.frame_table = tk.Frame()

    def open_table(self, p_id):

        # TODO : avoid the error when we close the document window

        # Get the filename of selected file
        filename = filedialog.askopenfilename(title='Ouvrir un fichier')

        # Put the window new_table in top
        self.window_new_table.lift()

        # TODO : verify the filename extension

        # Save the filename
        self.filename = str(filename)

        # Show the name of the openened file
        self.label_filename.config(text=self.filename)

        # Save the extension of the file
        self.extension = p_id

    def confirm(self):

        print("ok")

        # Get the new table name
        table_name = self.entry_name.get()

        # Create a table with the new dataframe
        if self.extension == 0:
            if self.filename != '':
                df = pd.read_csv(self.filename)
                print(df)

        if self.extension == 1:
            if self.filename != '':
                df = pd.read_excel(self.filename)
                print(df)

        page_table = PageTable(self.right_frame, self.filename, table_name)

        # Create a left button
        row = len(self.left_frame.buttons_table) + 1
        new_button_left = ButtonLeftText(str(table_name), row, self.left_frame.moving_frames[3], "white", partial(self.change_page, page_table.frame))
        self.left_frame.buttons_table.append(new_button_left)

        self.right_frame.pages_table.append(page_table)



    def change_page(self, p_frame):
        p_frame.lift()


class PageTable:
    def __init__(self, p_right_frame, p_filename, p_name):

        # Create a previsualisation window
        window_height = settings['dimensions']['window_height']
        top_menu_height = settings['dimensions']['top_menu_height']
        frame_width = p_right_frame.frame["width"]
        frame_height = window_height - top_menu_height
        self.frame = tk.Frame(p_right_frame.frame, bg="white", width=frame_width, height=frame_height)
        self.frame.grid(row=1)
        self.frame.grid_propagate(False)
        self.frame.lift()

        # Frame_Table
        frame_table_width = frame_width - 10
        frame_table_height = frame_height - 10
        self.frame_table = tk.Frame(self.frame, bg="blue", width=frame_table_width, height=frame_table_height)
        self.frame_table.grid(row=0, padx=(5, 5), pady=(5, 5))
        self.frame_table.columnconfigure(0, weight=1)
        self.frame_table.rowconfigure(0, weight=1)
        self.frame_table.grid_propagate(False)

        # Fill the section with the table
        self.table = PrevisualisationTable(self.frame_table, p_filename, p_name)


class PrevisualisationTable:
    """ Widget that displays a table """

    def __init__(self, p_table_frame, p_filename, p_table_name):
        """
        Initialization of the table widget that shows a table

        :param p_section: Section that will contain this table widget
        :param p_widget_configuration: Object in the left menu, specific to each widget and used to configure the widget
        :param p_widget_group: Group containing this widget
        """

        # Dimension of the section
        self.frame_table = p_table_frame
        self.frame_section_width = self.frame_table.winfo_width()
        self.frame_section_height = self.frame_table.winfo_height()

        # Initialization of the dataframe
        self.df = pd.read_csv(p_filename)
        self.nb_row_df = self.df.shape[0]
        self.nb_column_df = self.df.shape[1]
        self.list_rows = [i for i in range(0, self.nb_row_df)]

        # Initial values
        self.nb_column = self.nb_column_df
        self.nb_column_max = 20
        self.list_columns = [i for i in range(self.nb_column)]

        # Properties of the widget
        self.frame = tk.Frame(p_table_frame, bg="red", highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(sticky="news")
        self.frame.columnconfigure(0, weight=1)

        # Title - Table
        self.title = tk.Label(self.frame, text=str(p_table_name), bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, sticky="nwes")
        self.title.config(font=("Calibri bold", 12))

        # Frame that contains headers of the table
        self.frame.update_idletasks()
        frame_header_width = self.frame.winfo_width() - 17
        self.frame_containing_headers = tk.Frame(self.frame, bg="red", width=frame_header_width, height=20)
        self.frame_containing_headers.grid(row=1, sticky="nws")
        self.frame_containing_headers.update_idletasks()

        # Frame that will contain the table
        self.frame_containing_cells = tk.Frame(self.frame)
        self.frame_containing_cells.grid(row=2, sticky='nwes')
        self.frame_containing_cells.grid_rowconfigure(0, weight=1)
        self.frame_containing_cells.grid_columnconfigure(0, weight=1)
        self.frame_containing_cells.grid_propagate(False)

        # Add a canvas in that frame
        self.canvas_cell = tk.Canvas(self.frame_containing_cells, bg="grey")
        self.canvas_cell.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_containing_cells, orient="vertical", command=self.canvas_cell.yview, width=17)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas_cell.configure(yscrollcommand=self.vsb.set)

        # Frames and Buttons of the header
        self.frames_header = [tk.Button() for j in range(self.nb_column)]
        self.buttons_header = [tk.Button() for j in range(self.nb_column)]

        # Objects that will contained the table content
        self.frame_buttons = tk.Frame(self.canvas_cell, bg="grey")
        self.canvas_cell.create_window((0, 0), window=self.frame_buttons, anchor='nw')

        # Frames and Buttons of the table content
        self.frames_cell = [[tk.Button() for j in range(self.nb_column)] for i in range(self.nb_row_df)]
        self.buttons_cell = [[tk.Button() for j in range(self.nb_column)] for i in range(self.nb_row_df)]

        # Boolean that indicates the creation of the table
        self.is_table_created = False

        # Creation of the table
        self.create_table(self.list_columns, self.list_rows)

        # Link the resize function to the resize event of the frame
        self.frame.bind('<Configure>', self.resize)

    def create_table(self, p_list_col, p_list_rows):
        """
        Function that creates of the table

        :param p_list_col: List which contains the column name of the table
        :param p_list_rows: List which contains the rows to draw
        """

        # Update values
        self.list_rows = p_list_rows
        self.list_columns = p_list_col
        nb_column = len(p_list_col)
        width_column = int(self.frame_containing_headers.winfo_width()/nb_column)

        # Creation of the header
        self.frames_header = [tk.Frame() for j in range(nb_column)]
        self.buttons_header = [tk.Button() for j in range(nb_column)]
        current_col = 0
        for j in self.list_columns:
            self.frames_header[current_col] = tk.Frame(self.frame_containing_headers, width=width_column, height=20)
            self.frames_header[current_col].grid(row=0, column=current_col)
            self.frames_header[current_col].grid_propagate(False)
            self.frames_header[current_col].grid_columnconfigure(0, weight=1)
            self.frames_header[current_col].grid_rowconfigure(0, weight=1)

            self.buttons_header[current_col] = tk.Button(self.frames_header[current_col], text=list(self.df)[j-1])
            self.buttons_header[current_col].config(bg="red", fg="white")
            self.buttons_header[current_col].grid(row=0,column=0, sticky="news")
            current_col += 1

        # Creation of the table content
        self.frames_cell = [[tk.Frame() for j in range(nb_column)] for i in range(self.nb_row_df)]
        self.buttons_cell = [[tk.Button() for j in range(nb_column)] for i in range(self.nb_row_df)]

        current_col = 0
        current_row = len(self.list_rows)
        for j in self.list_columns:
            for i in range(0, self.nb_row_df):
                self.frames_cell[i][current_col] = tk.Frame(self.frame_buttons, width=width_column, height=20)
                self.frames_cell[i][current_col].grid_propagate(False)
                self.frames_cell[i][current_col].grid_columnconfigure(0, weight=1)
                self.frames_cell[i][current_col].grid_rowconfigure(0, weight=1)

                self.buttons_cell[i][current_col] = tk.Button(self.frames_cell[i][current_col], text=(self.df.iloc[i][j - 1]))
                self.buttons_cell[i][current_col]['command'] = None
                self.buttons_cell[i][current_col].config(borderwidth=2, relief="groove")

                if i in p_list_rows:

                    self.frames_cell[i][current_col].grid(row=0, column=current_col)
                    self.frames_cell[i][current_col].grid(row=self.list_rows.index(i), column=current_col)

                    self.buttons_cell[i][current_col].config(fg="black")

                else:
                    self.frames_cell[i][current_col].grid(row=current_row, column=current_col)
                    current_row += 1

                    self.buttons_cell[i][current_col].config(state=tk.DISABLED, disabledforeground="SystemButtonFace")

                self.buttons_cell[i][current_col].grid(row=0, column=0, sticky="news")

            current_row = len(self.list_rows)
            current_col += 1

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum([self.buttons_cell[0][j].winfo_width() for j in range(0, nb_column)])
        height = self.frame_table.winfo_height() - self.frame_containing_headers.winfo_height() - 25
        self.frame_containing_cells.config(width=first5columns_width + self.vsb.winfo_width(),
                            height=height)

        # Set the canvas scrolling region
        self.canvas_cell.config(scrollregion=self.canvas_cell.bbox("all"))

        # Boolean that indicates the creation of the table
        self.is_table_created = True

    def resize(self, event):
        """ Function called when the parent section is resized"""

        print("Resize TableWidget")

        if self.is_table_created:

            # Get the number of column
            nb_column = len(self.list_columns)

            # Change the frame_containing_headers width
            frame_header_width = self.frame.winfo_width() - self.vsb.winfo_width()
            self.frame_containing_headers.config(width=frame_header_width)

            # Calculate the new column width
            new_column_width = int(frame_header_width / nb_column)

            # Change frame_headers width
            current_col = 0
            for j in self.list_columns:
                self.frames_header[current_col].config(width=new_column_width)
                current_col += 1

            # Change the frame_table width
            current_col = 0
            for j in self.list_columns:
                for i in range(0, self.nb_row_df):
                    self.frames_cell[i][current_col].config(width=new_column_width)
                current_col += 1

            # Change the frame_containing_cells height=
            frame_canvas_height = self.frame.winfo_height() - self.frame_containing_headers.winfo_height() - 25
            self.frame_containing_cells.config(height=frame_canvas_height)











