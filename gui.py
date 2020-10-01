import tkinter as tk
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)

window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
top_menu_height_initial = settings['dimensions']['top_menu_height']
left_menu_width_initial = settings['dimensions']['left_menu_width']
frame_right_width_initial = window_width_initial - left_menu_width_initial
frame_right_height_initial = window_height_initial

class RightFrame:
    """ Right frame of the window"""

    def __init__(self, p_parent):

        self.parent = p_parent

        self.frame = tk.Frame(p_parent, bg="black", width=frame_right_width_initial, height=frame_right_height_initial)
        # self.frame.grid_propagate(False)
        self.frame.grid(row=0, column=1, sticky='n')

        self.frameContent = []

    def resize(self):
        offset_width = self.parent.winfo_width() - window_width_initial
        self.frame["width"] = frame_right_width_initial + offset_width
        self.frame["height"] = self.parent.winfo_height()

        # Resize the frameContent part
        for child_page in self.frameContent:
            child_page.frame["width"] = frame_right_width_initial + offset_width
            child_page.frame["height"] = self.parent.winfo_height() - top_menu_height_initial

            # Resize sections
            for child in child_page.childrens:
                child.button["width"] = int(child.width + offset_width/child_page.nb_column)
                child.button["height"] = int(frame_right_height_initial + (self.parent.winfo_height() -
                                                                           top_menu_height_initial) / child_page.nb_row)

            # Resize sections
            for child in child_page.childrens2:
                child.button["width"] = int(child.width + child.columspan*(offset_width/child_page.nb_column))
                child.button["height"] = int(frame_right_height_initial + (self.parent.winfo_height() -
                                                                       top_menu_height_initial) / child_page.nb_row)




class FrameContent:
    """ Right frame content of the window"""

    def __init__(self, p_parent, p_title, p_background, p_nb_row, p_nb_column):
        window_height = settings['dimensions']['window_height']
        top_menu_height = settings['dimensions']['top_menu_height']
        self.frame_width = p_parent.frame["width"]
        self.frame_height = window_height - top_menu_height
        self.frame = tk.Frame(p_parent.frame, bg=p_background, width=self.frame_width, height=self.frame_height)
        self.frame.grid(row=1)

        self.frame.grid_propagate(False)
        t_row = []
        t_column = []
        for i in range(p_nb_row):
            t_row.append(i)
        for i in range(p_nb_column):
            t_column.append(i)
        self.frame.columnconfigure(tuple(t_column), weight=1)
        self.frame.rowconfigure(tuple(t_row), weight=1)

        self.childrens = []
        self.childrens2 = []
        self.nb_row = p_nb_row
        self.nb_column = p_nb_column

        p_parent.frameContent.append(self)

        self.selected_sections = []

        # # Label page title
        # self.label_page_title = tk.Label(self.frame, bg=p_background, text=p_title)
        # self.label_page_title.grid(row=0, column=0, sticky='nw', padx=10, pady=(5, 5))
        # font_right_frame_title = settings['font']['font_right_frame_title']
        # font_size_right_frame_title = settings['font_size']['font_size_right_frame_title']
        # self.label_page_title.config(font=(font_right_frame_title, font_size_right_frame_title))

        section_width = int(frame_right_width_initial / self.nb_column)
        section_width2 = int(2 * frame_right_width_initial / self.nb_column)
        section_height = int(self.frame["height"] / self.nb_row)

        self.sections = []
        section_id = 0
        for i in range(self.nb_row):
            for j in range(self.nb_column):
                section = Section(self, i, j, 1, 1, section_width, section_height, section_id)
                self.sections.append(section)
                section_id += 1

    def get_id_by_pos(self, p_row, p_col):
        return p_row * self.nb_column + p_col

    def fusion_sections(self, p_section1, p_section2):
        x1, x2 = p_section1.row, p_section2.row
        y1, y2 = p_section1.column, p_section2.column

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

        detected_sections = []
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                id = self.get_id_by_pos(i, j)
                section = self.sections[id]
                detected_sections.append(section)

        row_gap = x_max - x_min + 1
        col_gap = y_max - y_min + 1

        section3_width = col_gap * p_section1.width
        section3_height = row_gap * p_section1.height
        rowspan = row_gap
        columnspan = col_gap
        section3_id = len(self.childrens2)
        Section(self, x_min, y_min, rowspan, columnspan, section3_width, section3_height, section3_id)

    def fusion(self):
        if len(self.selected_sections) == 2:
            self.fusion_sections(self.selected_sections[0], self.selected_sections[1])
            self.selected_sections[0].button["bg"] = "#1E90FF"
            self.selected_sections[1].button["bg"] = "#1E90FF"
            self.selected_sections = []






class WidgetGroup:
    def __init__(self, p_id):
        self.id = p_id
        self.widgets = []

    def update_widgets(self):
        for w in self.widgets:
            w.update()


class ButtonLeftText:
    """ Text buttons located in the left of the window """

    def __init__(self, p_text, p_row, p_parent, p_bg, p_pady, p_command):
        self.init_bg = p_bg
        self.button = tk.Button(p_parent, text=p_text, bg=p_bg, fg="white", activebackground="green", borderwidth=1, command=p_command)
        self.button.grid(row=p_row, sticky='new', pady=p_pady, padx=(5, 5))
        font_left_menu = settings['font']['font_left_menu']
        font_size_left_menu = settings['font_size']['font_size_left_menu']
        self.button.config(font=(font_left_menu, font_size_left_menu))
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.button['bg'] = 'white'
        self.button['fg'] = 'black'

    def on_leave(self, e):
        self.button['bg'] = self.init_bg
        self.button['fg'] = 'white'


class ButtonTopText:
    """ Text buttons located in the top of the window """

    def __init__(self, p_text, p_col, p_parent, p_bg, p_command):
        self.bg = p_bg
        self.button = tk.Button(p_parent, text=p_text, bg=p_bg, fg="white", borderwidth=1, command=p_command)
        self.button.grid(row=0, column=p_col, sticky="e",  pady=(5, 5), padx=(10, 10), ipadx=15)
        font_top_menu = settings['font']['font_top_menu']
        font_size_top_menu = settings['font_size']['font_size_top_menu']
        self.button.config(font=(font_top_menu, font_size_top_menu))
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.button['bg'] = 'green'
        self.button['fg'] = 'white'

    def on_leave(self, e):
        self.button['bg'] = self.bg
        self.button['fg'] = 'white'


class Section:
    def __init__(self, p_parent, p_row, p_column, p_rowspan, p_columnspan, p_w, p_h, p_id):

        self.parent = p_parent
        self.row = p_row
        self.column = p_column
        self.rowspan = p_rowspan
        self.columspan = p_columnspan
        self.width = p_w
        self.height = p_h
        self.id = p_id

        self.button = tk.Button(p_parent.frame, bg="#1E90FF", width=p_w, height=p_h)
        self.button.grid(row=p_row, column=p_column, rowspan=p_rowspan, columnspan=p_columnspan, padx=(5, 5), pady=(5, 5))

        self.button.bind("<Button-1>", self.left_click)
        self.button.bind("<Button-3>", self.right_click)

        # self.button.grid_propagate(False)

        # text = str(p_row) + "/" + str(p_column)
        # self.label = tk.Label(self.frame, fg="white", bg="blue", text=text)
        # self.label.grid(row=0, column=0)
        # self.label.config(font=("Calibri bold", 14))

        if p_rowspan == 1 and p_columnspan == 1:
            p_parent.childrens.append(self)
        else:
            p_parent.childrens2.append(self)

    def left_click(self, event):
        if self.rowspan == 1 and self.columspan == 1:
            self.button["bg"] = "green"
            self.parent.selected_sections.append(self)
            self.parent.fusion()

    def right_click(self, event):
        if self.rowspan != 1 or self.columspan != 1:
            # self.button["bg"] = "red"
            self.destroy()

    def destroy(self):
        if self.rowspan != 1 or self.columspan != 1:
            self.button.grid_forget()


