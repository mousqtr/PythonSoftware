import tkinter as tk
import pandas as pd
from functools import partial
import json
from tkinter import ttk

# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Open the data file
with open('widgets/table/table_data.json') as json_file:
    table_data = json.load(json_file)


class WidgetTable:
    """ Widget that displays a table """

    def __init__(self, p_frame_section, p_widget_configuration):
        """
        Initialization of the table widget that shows a table

        :param p_section: Section that will contain this table widget
        :param p_widget_configuration: Object in the left menu, specific to each widget and used to configure the widget
        :param p_filename: Name of the table file
        """
        # Saving the parameters to use them in each class function
        self.section = p_frame_section
        self.widget_configuration = p_widget_configuration
        self.frame_widget_configuration = p_widget_configuration.frame
        self.frame_right = self.section.page_content.frame_right
        self.filename = " "

        # Dimension of the section
        self.frame_section_width = self.section.frame.winfo_width()
        self.frame_section_height = self.section.frame.winfo_height()

        # Initialization of the dataframe
        self.nb_row_df = 0
        self.nb_column_df = 0
        self.list_rows = []
        self.list_headers = [" "]

        # Initial values
        self.nb_column = 0
        self.nb_column_max = 6
        self.list_columns = []

        # Row selected by the user
        self.selected_row = -1

        # Indicate the widget type
        self.type = "Table"

        # Properties of the widget
        self.frame = tk.Frame(self.section.frame, bg="green", highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(sticky="news")
        self.frame.columnconfigure(0, weight=1)

        # Title - Table
        self.label_title = tk.Label(self.frame, text="", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        self.label_title.grid(row=0, sticky="nwes")
        self.label_title.config(font=("Calibri bold", 12))

        # Frame that contains headers of the table
        self.frame.update_idletasks()
        frame_header_width = self.frame.winfo_width() - 17
        self.frame_containing_headers = tk.Frame(self.frame, bg="green", width=frame_header_width, height=20)
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

        # List of table names and filenames
        self.list_tables_names = [" "]
        self.list_tables_filenames = [" "]
        for table in self.frame_right.pages_table:
            self.list_tables_names.append(table.name)
            self.list_tables_filenames.append(table.filename)

        self.combo_tables = ttk.Combobox()
        self.entry_title = tk.Entry()
        self.combo_column_choice = [ttk.Combobox() for j in range(self.nb_column_max)]

        # Call the on_click function when the user left mouse click on these elements
        self.frame.bind("<Button-1>", self.on_click)
        self.label_title.bind("<Button-1>", self.on_click)
        self.frame_containing_headers.bind("<Button-1>", self.on_click)
        self.frame_containing_cells.bind("<Button-1>", self.on_click)
        for i in range(self.nb_column):
            self.buttons_header[i].bind("<Button-1>", self.on_click)
        for j in range(self.nb_column):
            for i in range(self.nb_row_df):
                self.buttons_cell[i][j].bind("<Button-1>", self.on_click)

        # Link the resize function to the resize event of the frame
        self.frame.bind('<Configure>', self.resize)

        # Widget parameters
        self.widget_parameters = {"title": self.label_title["text"], "filename": self.filename, "list_columns": self.list_columns}

    def create_table(self, p_list_rows):
        """
        Function that creates of the table

        :param p_filename: Name of the table file
        :param p_list_col: List which contains the column name of the table
        :param p_list_rows: List which contains the rows to draw
        """

        df = pd.read_csv(self.filename)
        self.nb_row_df = df.shape[0]
        self.nb_column_df = df.shape[1]
        self.list_headers = list(df.head())
        self.list_headers.insert(0, " ")

        # Update the list of rows
        if p_list_rows:
            self.list_rows = p_list_rows
        else:
            self.list_rows = [i for i in range(0, self.nb_row_df)]

        # Update the list of columns
        if not self.list_columns:
            self.list_columns = [i for i in range(0, self.nb_column_df)]

        nb_column = len(self.list_columns)

        print(self.list_columns)

        # Update the column width
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

            self.buttons_header[current_col] = tk.Button(self.frames_header[current_col], text=list(df)[j])
            self.buttons_header[current_col].config(bg="green", fg="white")
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

                self.buttons_cell[i][current_col] = tk.Button(self.frames_cell[i][current_col], text=(df.iloc[i][j - 1]))
                self.buttons_cell[i][current_col]['command'] = partial(self.color_line, i)
                self.buttons_cell[i][current_col].config(borderwidth=2, relief="groove")

                if i in self.list_rows:

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
        height = self.section.frame.winfo_height() - self.frame_containing_headers.winfo_height() - 25
        self.frame_containing_cells.config(width=first5columns_width + self.vsb.winfo_width(),
                            height=height)

        # Set the canvas scrolling region
        self.canvas_cell.config(scrollregion=self.canvas_cell.bbox("all"))

        # Boolean that indicates the creation of the table
        self.is_table_created = True

        # Bind user interaction with new table
        for i in range(nb_column):
            self.buttons_header[i].bind("<Button-1>", self.on_click)
        for j in range(nb_column):
            for i in range(self.nb_row_df):
                self.buttons_cell[i][j].bind("<Button-1>", self.on_click)

        # Save the widget
        widget = {"type": "Table", "title": self.label_title["text"], "filename": self.filename, "list_columns": self.list_columns}
        self.section.save_widget(widget)

    def on_click(self, e):
        """ Function called when the user click on this section """

        # Called the on_click function of its parent
        self.section.on_click(e)

        self.frame_widget_configuration.grid_columnconfigure((0, 1), weight=1)

        # Modify the configuration widget title
        self.widget_configuration.label_title.grid(row=0, columnspan=2)

        label_table = tk.Label(self.frame_widget_configuration, text="Tableau", width=19, bg="#333333",
                                           fg="white")
        label_table.grid(row=1, columnspan=2, pady=(10, 0))
        label_table.config(font=("Calibri bold", 13))

        self.combo_tables = ttk.Combobox(self.frame_widget_configuration, values=self.list_tables_names, state="readonly")
        self.combo_tables.grid(row=2, columnspan=2)
        self.combo_tables.config(font=("Calibri bold", 10))
        if self.list_tables_names:
            index = list(self.list_tables_filenames).index(self.filename)
            self.combo_tables.current(index)

        self.combo_tables.bind('<<ComboboxSelected>>', self.change_combo_column_choice)

        # Label - Title
        label_title = tk.Label(self.frame_widget_configuration, text="Titre du widget", bg="#333333", fg="white")
        label_title.grid(row=3, columnspan=2, pady=(10, 0))
        label_title.config(font=("Calibri", 13))

        # Entry - Write the title
        self.entry_title = tk.Entry(self.frame_widget_configuration, width=22, textvariable=" ")
        self.entry_title.grid(row=4, columnspan=2)
        self.entry_title.config(font=("Calibri bold", 10))
        self.entry_title.delete(0, tk.END)
        self.entry_title.insert(0, self.label_title["text"])

        # Label - Choose columns
        label_select_column = tk.Label(self.frame_widget_configuration, text="Choix des colonnes", bg="#333333", fg="white")
        label_select_column.grid(row=5, columnspan=2, pady=(10, 0))
        label_select_column.config(font=("Calibri", 13))

        # Column choice label
        labels_column_choice = [tk.Label() for j in range(self.nb_column_max)]
        for j in range(self.nb_column_max):
            label_text = "Colonne " + str(j + 1)
            labels_column_choice[j] = tk.Label(self.frame_widget_configuration, text=label_text, width=19, bg="#333333", fg="white")
            labels_column_choice[j].grid(row=j + 6, column=0, sticky='ne', padx=10, pady=1)
            labels_column_choice[j].config(font=("Calibri bold", 9))

            self.combo_column_choice[j] = ttk.Combobox(self.frame_widget_configuration, values=self.list_headers, state="readonly")
            self.combo_column_choice[j].grid(row=j + 6, column=1, sticky='nw', padx=10, pady=1)
            self.combo_column_choice[j].config(font=("Calibri bold", 9))

            if j < len(self.list_columns):
                value = self.list_columns[j] + 1
                self.combo_column_choice[j].current(value)


        # Button - Validation
        button_validate = tk.Button(self.frame_widget_configuration, text="Valider", width=22, bg="orange", fg="white")
        button_validate.grid(row=30, columnspan=2, pady=(20, 0))
        button_validate['command'] = self.validate
        button_validate.config(font=("Calibri", 10))

    def change_combo_column_choice(self, event):

        # Get the file
        table_index = self.combo_tables.current()
        if table_index != -1:
            filename = self.list_tables_filenames[table_index]
            df = pd.read_csv(filename)
            self.list_headers = list(df.head())
            self.list_headers.insert(0, " ")
            for j in range(self.nb_column_max):
                self.combo_column_choice[j]["values"] = self.list_headers
                self.combo_column_choice[j].current(0)

    def color_line(self, p_row):
        """
        Function that colors a line

        :param p_row: A line of the table
        """
        #Update values
        nb_column = len(self.list_columns)
        self.selected_row = p_row

        for i in range(0, self.nb_row_df):
            for j in range(0, nb_column):
                if i == p_row:
                    self.buttons_cell[i][j].config(bg="beige")
                else:
                    self.buttons_cell[i][j].config(bg="SystemButtonFace")

    def validate(self):
        """
        Functions called when the user clicks on validate button - Change columns
        """

        # Get the file
        table_index = self.combo_tables.current()
        if table_index != -1:
            filename = self.list_tables_filenames[table_index]
            if filename != self.filename:
                self.filename = filename
                self.list_columns = []
            self.list_rows = []
            self.create_table(self.list_rows)

        # Get the title entry
        title = self.entry_title.get()

        # If there is no title
        if title == "" or title == " ":
            self.label_title.grid_forget()
            self.label_title["text"] = " "
        else:
            self.label_title.grid(row=0, column=0, sticky="nwes")
            self.label_title["text"] = title

        # Get the list of combobox indexes selected by the user
        list_columns = []
        for j in range(self.nb_column_max):
            col = self.combo_column_choice[j].current() - 1
            if (col >= 0) and (col not in list_columns):
                list_columns.append(col)

        # Sort columns in order
        list_columns.sort()

        # Replace columns with new ones
        if self.filename != " ":
            self.delete_buttons()
            self.list_rows = []
            self.list_columns = list_columns
            self.create_table(self.list_rows)

        # Update the widget parameters
        self.widget_parameters["title"] = self.label_title["text"]
        self.widget_parameters["filename"] = self.filename
        self.widget_parameters["list_columns"] = self.list_columns

        # Change the frame_containing_cells height
        if self.label_title["text"] != "" or self.label_title["text"] != " ":
            frame_canvas_height = self.frame.winfo_height() - self.frame_containing_headers.winfo_height() - 25
        else:
            frame_canvas_height = self.frame.winfo_height() - self.frame_containing_headers.winfo_height()
        self.frame_containing_cells.config(height=frame_canvas_height)

    def delete_buttons(self):
        """
        Functions that deletes headers and table buttons
        """

        # Destruction of the headers buttons
        for header in self.frame_containing_headers.winfo_children():
            header.destroy()

        # Destruction of the headers buttons
        for cell in self.frame_buttons.winfo_children():
            cell.destroy()

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

            # Change the frame_containing_cells height
            if self.label_title["text"] != " " or self.label_title["text"] != "":
                frame_canvas_height = self.frame.winfo_height() - self.frame_containing_headers.winfo_height() - 25
            else:
                frame_canvas_height = self.frame.winfo_height() - self.frame_containing_headers.winfo_height()
            self.frame_containing_cells.config(height=frame_canvas_height)

    def hide(self):
        """ Hide the widget (during the edit widget mode)"""

        print("Hide ImageWidget")
        self.frame.grid_forget()

    def show(self):
        """ Hide the widget (after the edit widget mode)"""

        print("Show ImageWidget")
        self.frame.grid(row=0, column=0, sticky="news")

    def update(self):
        """
        Functions that create a new table with new rows
        """

        print("Update Table")

        # Update list of tables
        self.list_tables_names = [" "]
        self.list_tables_filenames = [" "]
        for table in self.frame_right.pages_table:
            self.list_tables_names.append(table.name)
            self.list_tables_filenames.append(table.filename)

    def load(self, p_widget_parameters):

        # Load idget parameters
        self.label_title["text"] = p_widget_parameters["title"]
        self.filename = p_widget_parameters["filename"]
        self.list_columns = p_widget_parameters["list_columns"]
        self.create_table(self.list_rows)





        # # Delete the table
        # self.delete_buttons()
        #
        # old_row = self.list_rows
        #
        # # Update the database
        # self.df = pd.read_csv('csv/csv_test.csv')
        # self.nb_row_df = self.df.shape[0]
        # self.nb_column_df = self.df.shape[1]
        # self.list_rows = [i for i in range(0, self.nb_row_df)]
        #
        # # # Update rows to draw
        # rows = self.list_rows
        # for w in self.widget_group.widgets:
        #     if w.type == "Filters":
        #         if w.row_to_draw == old_row or w.row_to_draw == []:
        #             rows = self.list_rows
        #         else :
        #             rows = w.row_to_draw
        #
        # # Recreate the table
        # self.create_table(self.list_columns, rows)





    # def details_window(self):
    #     """
    #     Functions called when the user clicks on details button
    #     """
    #
    #     # Window handle
    #     window_details = tk.Toplevel(self.frame)
    #     window_details.resizable(False, False)
    #     window_details.title("Détails")
    #     window_icon = tk.PhotoImage(file="img/loupe.png")
    #     window_details.iconphoto(False, window_icon)
    #     # login_window_width = settings['dimensions']['window_login_width']
    #     # login_window_height = settings['dimensions']['window_login_height']
    #     window_settings_width = 550
    #     window_settings_height = 260
    #     screen_width = self.frame.winfo_screenwidth()
    #     screen_height = self.frame.winfo_screenheight()
    #     x_cord = int((screen_width / 2) - (window_settings_width / 2))
    #     y_cord = int((screen_height / 2) - (window_settings_height / 2))
    #     window_details.geometry("{}x{}+{}+{}".format(window_settings_width, window_settings_height, x_cord, y_cord))
    #     window_details.columnconfigure((0, 1), weight=1)
    #
    #     # Title - Details
    #     bg_identification = settings['colors']['bg_identification']
    #     label_login_title = tk.Label(window_details, text="Détails", bg=bg_identification, fg="white")
    #     label_login_title.grid(row=0, columnspan=2, sticky='new', pady=(0, 10))
    #     font_login_title = settings['font']['font_login_title']
    #     font_size_login_title = settings['font_size']['font_size_login_title']
    #     label_login_title.config(font=(font_login_title, font_size_login_title))
    #
    #     nb_column = len(self.list_columns)
    #     row_colored = 0
    #     for i in range(0, self.nb_row_df):
    #         for j in range(0, nb_column):
    #             if self.buttons_cell[i][j]['bg'] == "beige":
    #                 row_colored = i
    #
    #     # Label - Details
    #     labels_1 = [tk.Label() for j in range(self.nb_column_max)]
    #     labels_2 = [tk.Label() for j in range(self.nb_column_max)]
    #     list_headers = list(self.df.head())
    #     for j in range(self.nb_column_max):
    #         labels_1[j] = tk.Label(window_details, text=list_headers[j])
    #         labels_1[j].grid(row=j + 2, column=0, sticky='nw', padx=30, pady=1)
    #         labels_1[j].config(font=("Calibri bold", 10))
    #         labels_2[j] = tk.Label(window_details, text=self.df.loc[row_colored][j])
    #         labels_2[j].grid(row=j + 2, column=1, sticky='nw', padx=30, pady=1)
    #         labels_2[j].config(font=("Calibri bold", 10))