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
                child.frame["width"] = child.width + offset_width/child_page.nb_column
                child.frame["height"] = frame_right_height_initial + (self.parent.winfo_height() - top_menu_height_initial) / child_page.nb_row

            # Resize sections
            for child in child_page.childrens2:
                child.frame["width"] = child.width + child.columspan*(offset_width/child_page.nb_column)
                child.frame["height"] = frame_right_height_initial + (self.parent.winfo_height() - top_menu_height_initial) / child_page.nb_row




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

        # # Label page title
        # self.label_page_title = tk.Label(self.frame, bg=p_background, text=p_title)
        # self.label_page_title.grid(row=0, column=0, sticky='nw', padx=10, pady=(5, 5))
        # font_right_frame_title = settings['font']['font_right_frame_title']
        # font_size_right_frame_title = settings['font_size']['font_size_right_frame_title']
        # self.label_page_title.config(font=(font_right_frame_title, font_size_right_frame_title))


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

        self.row = p_row
        self.column = p_column
        self.rowspan = p_rowspan
        self.columspan = p_columnspan
        self.width = p_w
        self.height = p_h
        self.id = p_id

        self.frame = tk.Frame(p_parent.frame, bg="red", width=p_w, height=p_h)
        self.frame.grid(row=p_row, column=p_column, rowspan=p_rowspan, columnspan=p_columnspan, padx=(5, 5), pady=(5, 5))
        self.frame.grid_propagate(False)

        text = str(p_row) + "/" + str(p_column)
        self.label = tk.Label(self.frame, fg="white", bg="blue", text=text)
        self.label.grid(row=0, column=0)
        self.label.config(font=("Calibri bold", 14))

        if p_rowspan == 1 and p_columnspan == 1:
            p_parent.childrens.append(self)
        else:
            p_parent.childrens2.append(self)
