import tkinter as tk
import json
from gui import FrameContent, ButtonLeftText

with open('settings.json') as json_file:
    settings = json.load(json_file)

window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
left_menu_width_initial = 50
left_menu_height_initial = window_height_initial
bg_identification = settings['colors']['bg_identification']

class NewPage:
    """ Create a new page window """

    def __init__(self, p_parent, p_left_frame, p_right_frame):
        """ Initialization of create page window """

        # Parameters
        self.parent = p_parent
        self.nb_row = 5
        self.nb_column = 5
        self.left_frame = p_left_frame
        self.right_frame = p_right_frame

        # Window handle
        self.window_new_page = tk.Toplevel(self.parent)
        self.window_new_page.resizable(False, False)
        self.window_new_page.title("Ajouter une page")
        window_new_page_icon = tk.PhotoImage(file="img/add.png")
        self.window_new_page.iconphoto(False, window_new_page_icon)
        width_new_page_window = 700
        height_login_window = 410
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x_cord = int((screen_width / 2) - (width_new_page_window / 2))
        y_cord = int((screen_height / 2) - (height_login_window / 2))
        self.window_new_page.grid_propagate(False)
        self.window_new_page.geometry("{}x{}+{}+{}".format(width_new_page_window, height_login_window, x_cord, y_cord))
        self.window_new_page.columnconfigure((0, 1, 2, 3), weight=1)

        # Left part of the window
        self.part_left = tk.Frame(self.window_new_page, bg="#DCDCDC", width=200, height=400)
        self.part_left.grid(row=0, column=0, columnspan=1, padx=(5,5), pady=(5,5))
        self.part_left.columnconfigure(0, weight=1)
        self.part_left.rowconfigure((1, 4), weight=10)
        self.part_left.rowconfigure((2, 3), weight=1)
        self.part_left.grid_propagate(False)
        self.label = tk.Label(self.part_left, text="Paramètres", bg=bg_identification, fg="white")
        self.label.grid(row=0, sticky='new')
        self.label.config(font=("Calibri bold", 12))

        # Left part of the window - First frame
        self.first_left_frame = tk.Frame(self.part_left, bg="#e8e8e8", width=400, height=150)
        self.first_left_frame.grid(row=1, column=0)

        # Left part of the window - First frame - Label page name
        self.label_page_name = tk.Label(self.first_left_frame, text="Nom de la page", bg="#DCDCDC", fg="black")
        self.label_page_name.grid(row=0, sticky='nwe')
        self.label_page_name.config(font=("Calibri bold", 12))

        # Left part of the window - First frame - Entry page name
        self.entry_page_name = tk.Entry(self.first_left_frame, width=18)
        self.entry_page_name.grid(row=1, sticky='nwe')
        self.entry_page_name.config(font=("Calibri bold", 12))

        # Left part of the window - Second frame
        self.second_left_frame = tk.Frame(self.part_left, bg="#e8e8e8", width=400, height=150)
        self.second_left_frame.grid(row=2, column=0)

        # Left part of the window - Second frame - Label nb line
        self.label_grid = tk.Label(self.second_left_frame, text="Nombre de lignes", bg="#DCDCDC", fg="black")
        self.label_grid.grid(row=0, sticky='nwe')
        self.label_grid.config(font=("Calibri bold", 12))

        # Left part of the window - Second frame - Entry nb line
        str_nb_row = tk.StringVar()
        str_nb_row.set(str(self.nb_row))
        self.entry_page_row = tk.Entry(self.second_left_frame, width=18, textvariable=str_nb_row)
        self.entry_page_row.grid(row=1, sticky='nwe')
        self.entry_page_row.config(font=("Calibri bold", 12))

        # Left part of the window - Third frame
        self.third_left_frame = tk.Frame(self.part_left, bg="#e8e8e8", width=400, height=150)
        self.third_left_frame.grid(row=3, column=0)

        # Left part of the window - Third frame - Label nb column
        self.label_grid = tk.Label(self.third_left_frame, text="Nombre de colonnes", bg="#DCDCDC", fg="black")
        self.label_grid.grid(row=0, sticky='nwe')
        self.label_grid.config(font=("Calibri bold", 12))

        # Left part of the window - Third frame - Entry nb column
        str_nb_column = tk.StringVar()
        str_nb_column.set(str(self.nb_column))
        self.entry_page_column = tk.Entry(self.third_left_frame, width=18, textvariable=str_nb_column)
        self.entry_page_column.grid(row=1, sticky='nwe')
        self.entry_page_column.config(font=("Calibri bold", 12))

        # Left part of the window - Fourth frame
        self.fourth_left_frame = tk.Frame(self.part_left, bg="#e8e8e8", width=400, height=150)
        self.fourth_left_frame.grid(row=4, column=0)

        # Left part of the window - Fourth frame - Button
        self.button_apply = tk.Button(self.fourth_left_frame, text="Actualiser la grille", width=18, command=self.update_grid)
        self.button_apply.grid(row=0, sticky='nwe')

        # Center part of the window
        self.part_center = tk.Frame(self.window_new_page, width=400, height=400, bg="#DCDCDC")
        self.part_center.grid(row=0, column=1, columnspan=2)
        self.part_center.columnconfigure(0, weight=1)
        self.part_center.rowconfigure((0, 1, 2), weight=1)
        self.part_center.grid_propagate(False)

        # Center part of the window - Label title
        self.label = tk.Label(self.part_center, text="Personnaliser la grille", bg=bg_identification, fg="white")
        self.label.grid(row=0, sticky='new')
        self.label.config(font=("Calibri bold", 12))

        # Center part of the window - Frame sections
        self.frame_sections = tk.Frame(self.part_center, bg="#DCDCDC", width=280, height=280)
        self.frame_sections.grid(row=1)
        self.frame_sections.grid_propagate(False)

        # Adapt the grid format to nb of row/column
        t_row = []
        t_column = []
        for i in range(self.nb_row):
            t_row.append(i)
        for i in range(self.nb_column):
            t_column.append(i)
        self.frame_sections.columnconfigure(tuple(t_column), weight=1)
        self.frame_sections.rowconfigure(tuple(t_row), weight=1)

        # Calculate the dimensions of a mono section
        section_width = int(self.frame_sections["width"] / self.nb_column)
        section_height = int(self.frame_sections["width"] / self.nb_row)

        # Lists which will contain sections
        self.mono_sections = []
        self.poly_sections = []
        self.selected_sections = []
        self.disappeared_sections = []  # Sections that will disappear
        self.disappeared_sections_group = []

        # Create all ButtonSections
        section_id = 0
        for i in range(self.nb_row):
            for j in range(self.nb_column):
                ButtonSection(self, i, j, 1, 1, section_width, section_height, section_id)
                section_id += 1

        # Center part of the window - Label 1
        self.label = tk.Label(self.part_center, text="Clique gauche sur deux cases pour construire \n une zone plus large", bg="#DCDCDC", fg="black")
        self.label.grid(row=2, sticky='new')
        self.label.config(font=("Calibri", 12, "bold italic"))

        # Center part of the window - Label 2
        self.label = tk.Label(self.part_center, text="Clique droit sur une zone pour la subdiviser", bg="#DCDCDC", fg="black")
        self.label.grid(row=3, sticky='new', pady=(0, 10))
        self.label.config(font=("Calibri", 12, "bold italic"))

        # Right part of the window
        self.part_right = tk.Frame(self.window_new_page, bg="#DCDCDC", width=200, height=400)
        self.part_right.grid(row=0, column=3, columnspan=1, padx=(5, 5), pady=(5, 5))
        self.part_right.rowconfigure(1, weight=1)
        self.part_right.grid_propagate(False)

        # Right part of the window - Label confirmation
        self.label = tk.Label(self.part_right, text="Confirmation", bg=bg_identification, fg="white")
        self.label.grid(row=0, sticky='new')
        self.label.config(font=("Calibri bold", 12))

        # Right part of the window - Button confirmation
        self.button_apply = tk.Button(self.part_right, text="Créer la page", width=15, command=self.apply)
        self.button_apply.grid(row=1, padx=30)

    def apply(self):
        """ Runs the creation of a page """

        # Create a widget frame for each frame content
        moving_part_widgets = tk.Frame(self.left_frame.frame, bg="#42526C", height=left_menu_height_initial, width=200)
        moving_part_widgets.columnconfigure(0, weight=1)
        moving_part_widgets.grid_propagate(False)
        self.left_frame.moving_widgets_page.append(moving_part_widgets)

        # Get the name of the page
        name = self.entry_page_name.get()
        new_frame_content = FrameContent(self.right_frame, name, "#e8e8e8", self.nb_row, self.nb_column, self)
        new_frame_content.change_page()

        # Create the left button
        row = len(self.left_frame.buttons_page) + 1
        new_button_left = ButtonLeftText(name, row, self.left_frame.moving_frames[0], "white", new_frame_content.change_page)
        self.left_frame.buttons_page.append(new_button_left)

        # Destroy the new page window
        self.window_new_page.destroy()

        # Add the page name in the widget page
        text = "Page : " + new_frame_content.name
        label_page = tk.Label(moving_part_widgets, text=text, bg="#333333", fg="white")
        label_page.grid(row=0, sticky='nwe')
        label_page.config(font=("Calibri bold", 12))

    def update_grid(self):
        """ Updates the grid when dimensions are changed """

        # Destroy previous sections buttons
        for x in self.mono_sections:
            x.button.grid_forget()

        for x in self.poly_sections:
            x.button.grid_forget()

        # Get the dimensions in the entries
        self.nb_row = int(self.entry_page_row.get())
        self.nb_column = int(self.entry_page_column.get())

        # Configure row/column of the window to receive the grid
        t_row = []
        t_column = []
        for i in range(self.nb_row):
            t_row.append(i)
        for i in range(self.nb_column):
            t_column.append(i)
        self.frame_sections.columnconfigure(tuple(t_column), weight=1)
        self.frame_sections.rowconfigure(tuple(t_row), weight=1)

        # Calculate the size of a button section
        section_width = int(self.frame_sections["width"] / self.nb_column)
        section_height = int(self.frame_sections["width"] / self.nb_row)

        # List of sections
        self.mono_sections = []              # Initial sections (rowspan = 1 and columnspan = 1)
        self.poly_sections = []          # Sections created after a merge of initial sections
        self.selected_sections = []     # Sections selected by a click (green ones)

        # Creation of initial sections
        section_id = 0
        for i in range(self.nb_row):
            for j in range(self.nb_column):
                ButtonSection(self, i, j, 1, 1, section_width, section_height, section_id)
                section_id += 1

    def get_id_by_pos(self, p_row, p_col):
        """ Returns the id of a button section from its row and column number """

        return p_row * self.nb_column + p_col

    def merge_sections(self, p_section1, p_section2):
        """ Merges two initial sections """

        # Coordnates of both sections
        x1, x2 = p_section1.row, p_section2.row
        y1, y2 = p_section1.column, p_section2.column

        # Calculate position extremums
        if x1 > x2:
            x_max = x1
            x_min = x2
        else:
            x_max = x2
            x_min = x1

        if y1 > y2:
            y_max = y1
            y_min = y2
        else:
            y_max = y2
            y_min = y1

        # Detect all sections between these extremums
        detected_sections = []
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                id = self.get_id_by_pos(i, j)
                section = self.mono_sections[id]
                detected_sections.append(section)

        self.disappeared_sections_group.append(detected_sections)

        # Calculate the gap of this selection
        row_gap = x_max - x_min + 1
        col_gap = y_max - y_min + 1

        # Calculate the parameters of the new section
        section3_width = col_gap * p_section1.width
        section3_height = row_gap * p_section1.height
        rowspan = row_gap
        columnspan = col_gap
        section3_id = len(self.poly_sections)

        # Create the new section
        ButtonSection(self, x_min, y_min, rowspan, columnspan, section3_width, section3_height, section3_id)

    def merge(self):
        """ Merges only when two sections are selected """

        if len(self.selected_sections) == 2:
            self.merge_sections(self.selected_sections[0], self.selected_sections[1])
            self.selected_sections[0].button["bg"] = bg_identification
            self.selected_sections[1].button["bg"] = bg_identification
            self.selected_sections = []


class ButtonSection:
    """ Sections buttons located in the create page window """

    def __init__(self, p_parent, p_row, p_column, p_rowspan, p_columnspan, p_w, p_h, p_id):
        """ Initialization of the create page section buttons """

        # Transform parameters to class variables
        self.parent = p_parent
        self.row = p_row
        self.column = p_column
        self.rowspan = p_rowspan
        self.columnspan = p_columnspan
        self.width = p_w
        self.height = p_h
        self.id = p_id

        # Creation of a button
        bg_identification = settings['colors']['bg_identification']
        self.button = tk.Button(p_parent.frame_sections, bg=bg_identification, width=p_w, height=p_h)
        self.button.grid(row=p_row, column=p_column, rowspan=p_rowspan, columnspan=p_columnspan, padx=(5, 5), pady=(5, 5))

        # User interaction with the button
        self.button.bind("<Button-1>", self.left_click)
        self.button.bind("<Button-3>", self.right_click)

        if p_rowspan == 1 and p_columnspan == 1:
            p_parent.mono_sections.append(self)
        else:
            p_parent.poly_sections.append(self)

    def left_click(self, event):
        """ Function called when the user user left click """

        if self.rowspan == 1 and self.columnspan == 1:
            self.button["bg"] = "green"
            self.parent.selected_sections.append(self)
            self.parent.merge()

    def right_click(self, event):
        """ Function called when the user user right click """

        if self.rowspan != 1 or self.columnspan != 1:
            self.destroy()
            id = self.parent.poly_sections.index(self)
            del self.parent.poly_sections[id]
            del self.parent.disappeared_sections_group[id]

    def destroy(self):
        """ Destruction of a poly section """

        if self.rowspan != 1 or self.columnspan != 1:
            self.button.grid_forget()