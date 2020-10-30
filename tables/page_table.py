import tkinter as tk
import json
import pandas as pd

with open('settings.json') as json_file:
    settings = json.load(json_file)

with open('tables/tables.json') as json_file:
    tables_json = json.load(json_file)


class PageTable:
    def __init__(self, p_right_frame, p_filename, p_name):

        # Transform parameters into class variables
        self.right_frame = p_right_frame
        self.filename = p_filename
        self.name = p_name

        # Create a previsualisation window
        window_height = settings['dimensions']['window_height']
        frame_width = self.right_frame.frame["width"]
        frame_height = window_height
        self.frame = tk.Frame(self.right_frame.frame, bg="white", width=frame_width, height=frame_height)
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

        # Set parameters to the RightFrame class (add the frame in frame_content list/ set current_frame)
        self.right_frame.pages_table.append(self)
        self.id = len(self.right_frame.pages_table) - 1
        self.right_frame.current_table = self.id

        print("table", self.right_frame.pages_table)

    def change_page(self):
        """ Change the page (= FrameContent) """

        # Set this table as current_table
        self.right_frame.current_table = self.id

        # Indicates that we are in the FrameContent mode
        self.right_frame.mode = 2

        # Resize the frame
        self.right_frame.resize()

        for page in self.right_frame.pages_table:
            page.frame.grid_forget()

        for page in self.right_frame.pages_content:
            page.frame.grid_forget()

        self.frame.grid(row=1)

        # Change the page - put frame in forward
        self.frame.lift()


class PrevisualisationTable:
    """ Widget that displays a table """

    def __init__(self, p_table_frame, p_filename, p_table_name):
        """
        Initialization of the table widget that shows a table

        :param p_section: Section that will contain this table widget
        :param p_widget_configuration: Object in the left menu, specific to each widget and used to configure the widget
        :param p_widget_group: Group containing this widget
        """

        self.filename = p_filename
        self.table_name = p_table_name

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

        self.save_table()

    def resize(self, event):
        """ Function called when the parent section is resized"""

        print("Resize Table")

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

    def save_table(self):

        # Build the data that will be add to the saving file
        value_data = {str(self.table_name): str(self.filename)}

        # Update the saving file (.json) with these data
        tables_json['list_tables'].update(value_data)
        with open('tables/tables.json', 'w') as outfile:
            json.dump(tables_json, outfile, indent=4)