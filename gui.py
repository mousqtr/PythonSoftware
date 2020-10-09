import tkinter as tk
import json
from functools import partial
from widgets.summary.new_summary import Summary

with open('settings.json') as json_file:
    settings = json.load(json_file)

window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
top_menu_height_initial = settings['dimensions']['top_menu_height']
left_menu_width_initial = 50
left_menu_height_initial = window_height_initial - top_menu_height_initial

frame_right_height_initial = left_menu_height_initial

bg_left_menu = settings['colors']['bg_left_menu']
bg_top_menu = settings['colors']['bg_top_menu']
bg_left_menu = settings['colors']['bg_left_menu']

company_name = settings['company_name']
font_company_name = settings['font']['font_company_name']
font_size_company_name = settings['font_size']['font_size_company_name']
bg_company_name = settings['colors']['bg_company_name']


class MainWindow:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.title("Gestionnaire d'inventaire")
        self.frame.resizable(True, True)
        self.frame.minsize(800, 600)
        window_icon = tk.PhotoImage(file="img/box.png")
        self.frame.iconphoto(False, window_icon)
        self.frame.grid_propagate(False)

        # Window dimension
        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width_initial / 2))
        y_cordinate = int((screen_height / 2) - (window_height_initial / 2))
        self.frame.geometry("{}x{}+{}+{}".format(window_width_initial, window_height_initial, x_cordinate, y_cordinate))

        # Window size
        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()


class TopFrame:
    def __init__(self, p_parent, p_icon):

        self.parent = p_parent

        # top_menu_width = window_width_initial - left_menu_width_initial
        self.frame = tk.Frame(p_parent, bg=bg_top_menu, width=window_width_initial, height=top_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=0)

        # width_1 = 250
        # self.first_top_frame = tk.Frame(self.frame, bg="blue", width=width_1, height=top_menu_height_initial)
        # self.first_top_frame.grid(row=0, column=0)
        # self.first_top_frame.grid_propagate(False)
        # self.first_top_frame.columnconfigure(0, weight=1)
        # self.first_top_frame.rowconfigure(0, weight=1)

        self.width_first_frame = 50
        self.first_top_frame = tk.Frame(self.frame, bg="blue", width=self.width_first_frame, height=top_menu_height_initial)
        self.first_top_frame.grid(row=0, column=0)
        self.first_top_frame.grid_propagate(False)
        self.first_top_frame.columnconfigure(0, weight=1)
        self.first_top_frame.rowconfigure(0, weight=1)

        self.width_second_frame = 250
        self.second_top_frame = tk.Frame(self.frame, bg=bg_top_menu, width=self.width_second_frame, height=top_menu_height_initial)
        self.second_top_frame.grid(row=0, column=1)

        width_3 = 500
        self.third_top_frame = tk.Frame(self.frame, bg=bg_top_menu, width=width_3, height=top_menu_height_initial)
        self.third_top_frame.grid(row=0, column=2)

        # Company title

        self.label_company_title = tk.Label(self.first_top_frame, text=company_name, bg=bg_company_name, fg="white")
        self.label_company_title.config(font=(font_company_name, font_size_company_name))

        self.button_company = tk.Button(self.first_top_frame, image=p_icon, height=50, borderwidth=0, command=None)
        self.button_company.grid(row=0)

    def resize(self):
        offset_width = self.parent.winfo_width() - window_width_initial
        self.frame["width"] = window_width_initial + offset_width
        self.second_top_frame["width"] = self.width_second_frame + offset_width

    def open(self, p_bool):
        if p_bool == True:
            self.width_first_frame = 250
            self.first_top_frame["width"] = 250
            self.width_second_frame = 50
            self.resize()
            self.label_company_title.grid(row=0, column=0, sticky='news')
            self.button_company.grid_forget()
        else:
            self.width_first_frame = 50
            self.first_top_frame["width"] = 50
            self.width_second_frame = 250
            self.resize()
            self.label_company_title.grid_forget()
            self.button_company.grid(row=0, column=0, sticky='news')



class MiddleFrame:
    def __init__(self, p_parent):

        self.parent = p_parent

        self.frame = tk.Frame(p_parent, bg="red", width=window_width_initial, height=window_height_initial - top_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.children_frames = []

    def resize(self):
        self.frame["width"] = self.parent.winfo_width()
        self.frame["height"] = self.parent.winfo_height() - top_menu_height_initial

        for x in self.children_frames:
            x.resize()

class RightFrame:
    """ Right frame of the window"""

    def __init__(self, p_parent, p_left):

        self.parent = p_parent.frame
        self.frame_left = p_left

        self.frame_right_width_initial = 800 - self.frame_left.frame_initial_width
        self.frame = tk.Frame(self.parent, width=self.frame_right_width_initial, height=frame_right_height_initial)
        self.frame.grid(row=1, column=1, sticky='n')

        self.frames_content = []
        self.current_frame = 0

        p_parent.children_frames.append(self)

    def resize(self):
        offset_width = self.parent.winfo_width() - window_width_initial
        offset_height = self.parent.winfo_height() - window_height_initial

        self.frame_right_width_initial = 800 - self.frame_left.frame_initial_width
        self.frame["width"] = self.frame_right_width_initial + offset_width
        self.frame["height"] = self.parent.winfo_height()

        # Resize the frameContent part
        for child_page in self.frames_content:
            child_page.frame["width"] = self.frame_right_width_initial + offset_width
            child_page.frame["height"] = self.parent["height"]

            # Resize sections
            for child in child_page.mono_sections:
                child.frame["width"] = int(child_page.frame["width"]/child_page.nb_column)
                child.frame["height"] = int(child_page.frame["height"] / child_page.nb_row)

            # Resize sections
            for child in child_page.poly_sections:
                child.frame["width"] = int(child_page.frame["width"]/child_page.nb_column)*child.columspan
                child.frame["height"] = int(child_page.frame["height"]/child_page.nb_row)*child.rowspan



class LeftFrame:
    def __init__(self, p_middle, p_top_frame, p_list_img_1, p_list_img_2):
        self.middle = p_middle
        self.frame_top = p_top_frame
        self.frame_middle = p_middle.frame
        self.list_img_1 = p_list_img_1
        self.list_img_2 = p_list_img_2

        for i in range(len(self.list_img_1)):
            self.list_img_1[i] = self.list_img_1[i].zoom(10)
            self.list_img_1[i] = self.list_img_1[i].subsample(32)
            self.list_img_2[i] = self.list_img_2[i].zoom(10)
            self.list_img_2[i] = self.list_img_2[i].subsample(32)


        bg_left = "#42526C"

        self.frame_initial_width = 50
        self.frame = tk.Frame(self.frame_middle, bg=bg_left, width=left_menu_width_initial, height=left_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=1, column=0)

        self.static_part = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=50)
        self.static_part.grid(row=1, column=0)
        self.static_part.columnconfigure(0, weight=1)
        self.static_part.grid_propagate(False)

        self.moving_part_pages = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=0)
        self.moving_part_pages.grid(row=1, column=1)
        self.moving_part_pages.columnconfigure(0, weight=1)
        self.moving_part_pages.grid_propagate(False)

        self.moving_part_widgets = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=0)
        self.moving_part_widgets.grid(row=1, column=1)
        self.moving_part_widgets.columnconfigure(0, weight=1)
        self.moving_part_widgets.grid_propagate(False)

        self.moving_part_settings = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=0)
        self.moving_part_settings.grid(row=1, column=1)
        self.moving_part_settings.columnconfigure(0, weight=1)
        self.moving_part_settings.grid_propagate(False)

        self.part_pages_opened = [False, False, False]

        self.buttons = [tk.Button() for i in range(3)]

        self.buttons[0] = tk.Button(self.static_part, image=self.list_img_1[0], height=50, borderwidth=0, command=partial(self.show, self.moving_part_pages, 0))
        self.buttons[0].grid(row=0)

        self.buttons[1] = tk.Button(self.static_part, image=self.list_img_1[1], height=50, borderwidth=0, command=partial(self.show, self.moving_part_widgets, 1))
        self.buttons[1].grid(row=1)

        self.buttons[2] = tk.Button(self.static_part, image=self.list_img_1[2], height=50, borderwidth=0, command=partial(self.show, self.moving_part_settings, 2))
        self.buttons[2].grid(row=2)

        label_page = tk.Label(self.moving_part_pages, text="Pages", bg=bg_left, fg="white")
        label_page.grid(row=0, sticky='nwe')
        label_page.config(font=("Calibri bold", 12))

        label_widget = tk.Label(self.moving_part_widgets, text="Widgets", bg=bg_left, fg="white")
        label_widget.grid(row=0, sticky='nwe')
        label_widget.config(font=("Calibri bold", 12))

        label_setting = tk.Label(self.moving_part_settings, text="Paramètres \ngénéraux", bg=bg_left, fg="white")
        label_setting.grid(row=0, sticky='nwe')
        label_setting.config(font=("Calibri bold", 12))


        # List which contains the buttons in the left menu
        self.buttons_left = []

        self.middle.children_frames.append(self)

    def resize(self):
        offset = self.frame_middle.winfo_height() - left_menu_height_initial
        self.frame["height"] = self.frame_middle.winfo_height()
        self.static_part["height"] = left_menu_height_initial + offset
        self.moving_part_pages["height"] = left_menu_height_initial + offset
        self.moving_part_widgets["height"] = left_menu_height_initial + offset
        self.moving_part_settings["height"] = left_menu_height_initial + offset

    def show(self, p_frame, p_id):
        if not self.part_pages_opened[p_id]:
            self.frame_initial_width = 250
            self.frame["width"] = 250
            p_frame["width"] = 200
            p_frame.lift()
            for i in range(len(self.part_pages_opened)):
                if i == p_id:
                    self.part_pages_opened[i] = True
                    self.buttons[i]["image"] = self.list_img_2[i]
                else:
                    self.part_pages_opened[i] = False
                    self.buttons[i]["image"] = self.list_img_1[i]
            self.part_pages_opened[p_id] = True
            self.frame_top.open(True)
        else:
            self.frame_initial_width = 50
            self.frame["width"] = 50
            p_frame["width"] = 0
            self.part_pages_opened[p_id] = False
            self.frame_top.open(False)

            for i in range(len(self.buttons)):
                self.buttons[i]["image"] = self.list_img_1[i]

        self.middle.resize()





class FrameContent:
    """ Right frame content of the window"""

    def __init__(self, p_frame_right, p_name, p_background, p_nb_row, p_nb_column, p_source_window):

        self.nb_row = p_nb_row
        self.nb_column = p_nb_column
        self.right_frame = p_frame_right
        self.name = p_name
        self.source_window = p_source_window

        self.right_frame.frames_content.append(self)
        self.id = len(self.right_frame.frames_content) - 1
        self.right_frame.current_frame = self.id

        window_height = settings['dimensions']['window_height']
        top_menu_height = settings['dimensions']['top_menu_height']
        self.frame_width = self.right_frame.frame["width"]
        self.frame_height = window_height - top_menu_height
        self.frame = tk.Frame(self.right_frame.frame, bg=p_background, width=self.frame_width, height=self.frame_height)
        self.frame.grid(row=1)
        self.frame.grid_propagate(False)

        # Lists which will contain sections
        self.mono_sections = []              # list of 1 x 1 sections
        self.poly_sections = []          # list of n x m sections
        self.displayed_sections = []
        self.disappeared_sections_group = []

        self.labels_sections = []
        self.buttons_sections_add = []
        self.buttons_sections_delete = []

        self.create_sections()

    def create_sections(self):

        self.mono_sections = []
        self.poly_sections = []
        self.displayed_sections = []
        self.disappeared_sections_group = self.source_window.disappeared_sections_group

        t_row = []
        t_column = []
        for i in range(self.nb_row):
            t_row.append(i)
        for i in range(self.nb_column):
            t_column.append(i)
        self.frame.columnconfigure(tuple(t_column), weight=1)
        self.frame.rowconfigure(tuple(t_row), weight=1)

        section_width = int(self.frame["width"] / self.nb_column)
        section_height = int(self.frame["height"] / self.nb_row)

        # Convert list of list to list
        disappeared_sections = []
        for x in self.source_window.disappeared_sections_group:
            for y in x:
                disappeared_sections.append(y)

        section_id = 0
        for s in self.source_window.mono_sections:
            if s not in disappeared_sections:
                section = FrameSection(self, s.row, s.column, 1, 1, section_width, section_height, section_id)
                section_id += 1
                self.mono_sections.append(section)
            # if s in disappeared_sections:
            #     s.button.grid_forget()

        section_id = 0
        for s in self.source_window.poly_sections:
            width = section_width * s.columnspan
            height = section_height * s.rowspan
            section = FrameSection(self, s.row, s.column, s.rowspan, s.columnspan, width, height, section_id)
            self.poly_sections.append(section)
            section_id += 1

        self.displayed_sections = self.mono_sections + self.poly_sections

        self.labels_sections = [tk.Label() for i in range(len(self.displayed_sections))]
        self.buttons_sections_add = [tk.Button() for i in range(len(self.displayed_sections))]
        self.buttons_sections_delete = [tk.Button() for i in range(len(self.displayed_sections))]


    def change_page(self):
        self.frame.lift()
        self.right_frame.current_frame = self.id

    def destroy_sections(self):
        for s in self.mono_sections:
            s.frame.grid_forget()
        for s in self.poly_sections:
            s.frame.grid_forget()

    def edit_widgets(self):
        for i in range(len(self.displayed_sections)):
            s = self.displayed_sections[i]

            if i == 0:
                s_width = s.frame.winfo_width()
                s_height = s.frame.winfo_height()
                print(s_width)
                print(s_height)
                Widget_group_1 = WidgetGroup(1)
                Widget_summary = Summary(s, Widget_group_1, s_width, s_height)
            else:

                s.frame["bg"] = "#42526C"

                padx = 5 * s.rowspan
                pady = 5 * s.columspan

                text = "Widget : " + str(i)
                self.labels_sections[i] = tk.Label(s.frame, text=text, bg="#42526C", fg="white")
                self.labels_sections[i].grid(row=0, column=0, sticky='news', padx=(padx,padx), pady=(pady,pady))

                self.buttons_sections_add[i] = tk.Button(s.frame, text="Ajouter", fg="black")
                self.buttons_sections_add[i].grid(row=1, column=0, sticky='news', padx=(padx,padx), pady=(pady,pady))

                self.buttons_sections_delete[i] = tk.Button(s.frame, text="Supprimer", fg="black")
                self.buttons_sections_delete[i].grid(row=2, column=0, sticky='news', padx=(padx,padx), pady=(pady,pady))


    def destroy_widgets(self):
        for i in range(len(self.displayed_sections)):
            self.labels_sections[i].grid_forget()
            self.buttons_sections_add[i].grid_forget()
            self.buttons_sections_delete[i].grid_forget()


class ButtonLeftText:
    """ Text buttons located in the left of the window """

    def __init__(self, p_text, p_row, p_parent, p_bg, p_command):
        self.init_bg = p_bg

        self.button = tk.Button(p_parent, text=p_text, bg=p_bg, fg="black", width=16, activebackground="green", borderwidth=1, command=p_command)
        self.button.grid(row=p_row, sticky='n', pady=(10, 0), padx=(5, 5))
        self.button.config(font=("Calibri bold", 12))
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.button['bg'] = '#8989ff'
        self.button['fg'] = 'white'

    def on_leave(self, e):
        self.button['bg'] = "white"
        self.button['fg'] = 'black'


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

