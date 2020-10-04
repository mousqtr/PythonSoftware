import tkinter as tk
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)

window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
top_menu_height_initial = settings['dimensions']['top_menu_height']
left_menu_width_initial = settings['dimensions']['left_menu_width']
left_menu_height_initial = window_height_initial
frame_right_width_initial = window_width_initial - left_menu_width_initial
frame_right_height_initial = window_height_initial

bg_left_menu = settings['colors']['bg_left_menu']
bg_top_menu = settings['colors']['bg_top_menu']
bg_left_menu = settings['colors']['bg_left_menu']

company_name = settings['company_name']
font_company_name = settings['font']['font_company_name']
font_size_company_name = settings['font_size']['font_size_company_name']
bg_company_name = settings['colors']['bg_company_name']


class TopFrame:
    def __init__(self, p_parent):
        # Top menu (include in right_frame)
        top_menu_width = window_width_initial - left_menu_width_initial
        self.frame = tk.Frame(p_parent.frame, bg=bg_top_menu, width=top_menu_width, height=top_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=0, sticky='new')
        self.frame.columnconfigure((0, 1), weight=1)

        self.first_top_frame = tk.Frame(self.frame, bg=bg_top_menu)
        self.first_top_frame.grid(row=0, column=0, sticky='news')

        self.second_top_frame = tk.Frame(self.frame, bg=bg_top_menu)
        self.second_top_frame.grid(row=0, column=1, sticky='nes')

        self.page_title = tk.Label(self.first_top_frame, text=" ", bg=bg_top_menu, fg="white")
        self.page_title.grid(row=0, column=0, sticky="ns", pady=7, padx=10)
        font_top_menu = settings['font']['font_top_menu']
        font_size_top_menu = settings['font_size']['font_size_top_menu']
        self.page_title.config(font=(font_top_menu, font_size_top_menu))


class RightFrame:
    """ Right frame of the window"""

    def __init__(self, p_parent):

        self.parent = p_parent

        self.frame = tk.Frame(p_parent, bg="black", width=frame_right_width_initial, height=frame_right_height_initial)
        self.frame.grid(row=0, column=1, sticky='n')

        self.frames_content = []

    def resize(self):
        offset_width = self.parent.winfo_width() - window_width_initial
        self.frame["width"] = frame_right_width_initial + offset_width
        self.frame["height"] = self.parent.winfo_height()

        # Resize the frameContent part
        for child_page in self.frames_content:
            child_page.frame["width"] = frame_right_width_initial + offset_width
            child_page.frame["height"] = self.parent.winfo_height() - top_menu_height_initial

            # Resize sections
            for child in child_page.sections:
                child.frame["width"] = int(child_page.frame["width"]/child_page.nb_column)
                child.frame["height"] = int(child_page.frame["height"] / child_page.nb_row)

            # Resize sections
            for child in child_page.new_sections:
                child.frame["width"] = int(child_page.frame["width"]/child_page.nb_column)*child.columspan
                child.frame["height"] = int(child_page.frame["height"]/child_page.nb_row)*child.rowspan


class FrameContent:
    """ Right frame content of the window"""

    def __init__(self, p_frame_right, p_frame_top, p_name, p_background, p_nb_row, p_nb_column, p_new_page):

        self.nb_row = p_nb_row
        self.nb_column = p_nb_column
        self.right_frame = p_frame_right
        self.top_frame = p_frame_top
        self.right_frame.frames_content.append(self)
        self.name = p_name

        window_height = settings['dimensions']['window_height']
        top_menu_height = settings['dimensions']['top_menu_height']
        self.frame_width = self.right_frame.frame["width"]
        self.frame_height = window_height - top_menu_height
        self.frame = tk.Frame(self.right_frame.frame, bg=p_background, width=self.frame_width, height=self.frame_height)
        self.frame.grid(row=1)
        self.frame.grid_propagate(False)

        t_row = []
        t_column = []
        for i in range(self.nb_row):
            t_row.append(i)
        for i in range(self.nb_column):
            t_column.append(i)
        self.frame.columnconfigure(tuple(t_column), weight=1)
        self.frame.rowconfigure(tuple(t_row), weight=1)
        print(tuple(t_column))
        print(tuple(t_row))

        section_width = int(self.frame["width"] / self.nb_column)
        section_height = int(self.frame["height"] / self.nb_row)

        self.sections = []
        self.new_sections = []
        self.displayed_sections = []

        section_id = 0
        for s in p_new_page.sections:
            section = FrameSection(self, s.row, s.column, 1, 1, section_width, section_height, section_id)
            section_id += 1
            if s not in p_new_page.disappeared_sections:
                self.sections.append(section)

        section_id = 0
        for s in p_new_page.new_sections:
            width = section_width * s.columspan
            height = section_height * s.rowspan
            section = FrameSection(self, s.row, s.column, s.rowspan, s.columspan, width, height, section_id)
            self.new_sections.append(section)
            section_id += 1

        self.displayed_sections = self.sections + self.new_sections

        for i in range(len(self.displayed_sections)):
            s = self.displayed_sections[i]
            label = tk.Label(s.frame, text=str(i), bg="blue", fg="white")
            label.grid(row=0, column=0, sticky='news')

    def change_page(self):
        self.frame.lift()
        self.top_frame.page_title["text"] = "Page : " + self.name


class FrameSection:
    """ Sections Frame located in main window """

    def __init__(self, p_parent, p_row, p_column, p_rowspan, p_columnspan, p_w, p_h, p_id):
        """ Initialization of these sections buttons """

        self.parent = p_parent
        self.row = p_row
        self.column = p_column
        self.rowspan = p_rowspan
        self.columspan = p_columnspan
        self.width = p_w
        self.height = p_h
        self.id = p_id

        self.frame = tk.Frame(p_parent.frame, width=p_w, height=p_h)
        self.frame.grid(row=p_row, column=p_column, rowspan=p_rowspan, columnspan=p_columnspan, padx=(5, 5), pady=(5, 5))
        self.frame.config(highlightbackground="black", highlightthickness=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)


class WidgetGroup:
    def __init__(self, p_id):
        self.id = p_id
        self.widgets = []

    def update_widgets(self):
        for w in self.widgets:
            w.update()


class LeftFrame:
    def __init__(self, p_parent):
        self.frame = tk.Frame(p_parent, bg=bg_left_menu, width=left_menu_width_initial, height=left_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=0, column=0, sticky='new')
        self.frame.columnconfigure(0, weight=1)

        # List which contains the buttons in the left menu
        self.buttons_left = []

        # Company title
        label_company_title = tk.Label(self.frame, text=company_name, bg=bg_company_name, fg="white", height=2)
        label_company_title.grid(row=0, sticky='new', pady=(0, 20))
        label_company_title.config(font=(font_company_name, font_size_company_name))


class ButtonLeftText:
    """ Text buttons located in the left of the window """

    def __init__(self, p_text, p_row, p_parent, p_bg, p_pady, p_command):
        self.init_bg = p_bg

        self.button = tk.Button(p_parent.frame, text=p_text, bg=p_bg, fg="white", activebackground="green", borderwidth=1, command=p_command)
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
        self.button.grid(row=0, column=p_col, sticky="ne",  pady=(5, 5), padx=(5, 5), ipadx=15)
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








