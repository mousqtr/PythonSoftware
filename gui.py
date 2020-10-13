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

initial_configuration_widget_height = 500

bg_left_menu = settings['colors']['bg_left_menu']
bg_top_menu = settings['colors']['bg_top_menu']
bg_left_menu = settings['colors']['bg_left_menu']

company_name = settings['company_name']
font_company_name = settings['font']['font_company_name']
font_size_company_name = settings['font_size']['font_size_company_name']
bg_company_name = settings['colors']['bg_company_name']


class MainWindow:
    """ Main window class, includes gui elements as top frame and middle frame"""

    def __init__(self):
        """ Main window class, includes gui elements as top frame and middle frame"""

        # Creation of the frame
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

        # Boolean that indicates if the window has to be resized or not
        self.resized = True


class TopFrame:
    """ Top frame class, includes all gui elements located in the top of the window """

    def __init__(self, p_main_window, p_icon):
        """ Top frame class, includes all gui elements located in the top of the window """

        # Transform parameters into class variables
        self.main_window = p_main_window
        self.company_icon = p_icon

        # Creation of the frame
        self.frame = tk.Frame(self.main_window.frame, bg=bg_top_menu, width=window_width_initial, height=top_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=0)

        # Creation of the first frame (1/3) - company logo, company name
        self.width_first_frame = 50
        self.first_top_frame = tk.Frame(self.frame, width=self.width_first_frame, height=top_menu_height_initial)
        self.first_top_frame.grid(row=0, column=0)
        self.first_top_frame.grid_propagate(False)
        self.first_top_frame.columnconfigure(0, weight=1)
        self.first_top_frame.rowconfigure(0, weight=1)

        # Creation of the second frame (2/3)
        self.width_second_frame = 250
        self.second_top_frame = tk.Frame(self.frame, bg=bg_top_menu, width=self.width_second_frame, height=top_menu_height_initial)
        self.second_top_frame.grid(row=0, column=1)

        # Creation of the third frame (3/3) - buttons
        width_3 = 500
        self.third_top_frame = tk.Frame(self.frame, bg=bg_top_menu, width=width_3, height=top_menu_height_initial)
        self.third_top_frame.grid(row=0, column=2)

        # Company name in the first frame
        self.label_company_title = tk.Label(self.first_top_frame, text=company_name, bg=bg_company_name, fg="white")
        self.label_company_title.config(font=(font_company_name, font_size_company_name))

        # Company icon in the first frame
        self.company_icon = self.company_icon.zoom(4)
        self.company_icon = self.company_icon.subsample(32)
        self.button_company = tk.Button(self.first_top_frame, image=self.company_icon, height=50, borderwidth=0, command=None)
        self.button_company.grid(row=0)

        self.window_open = True

    def resize(self):
        """ Function that resizes the frame and the second frame """

        # Difference between the initial window width and the resized window width
        offset_width = self.main_window.frame.winfo_width() - window_width_initial

        # Resize the top frame
        self.frame["width"] = window_width_initial + offset_width

        # Resize the second top frame
        self.second_top_frame["width"] = self.width_second_frame + offset_width

    def open(self, p_bool):
        """ Function that draw the company icon or the company name depending on the p_bool value """

        # The left window is opened
        if p_bool == True:
            self.width_first_frame = 250
            self.first_top_frame["width"] = 250
            self.width_second_frame = 50
            self.resize()
            self.label_company_title.grid(row=0, column=0, sticky='news')
            self.button_company.grid_forget()

        # The left window is closed
        else:
            self.width_first_frame = 50
            self.first_top_frame["width"] = 50
            self.width_second_frame = 250
            self.resize()
            self.label_company_title.grid_forget()
            self.button_company.grid(row=0, column=0, sticky='news')


class MiddleFrame:
    """ Middle frame class, includes all gui elements located in the second part of the window (after the top) """

    def __init__(self, p_main_window):
        """ Middle frame class, includes all gui elements located in the second part of the window (after the top) """

        # Transform parameters into class variables
        self.main_window = p_main_window

        # Creation of the frame
        self.frame = tk.Frame(self.main_window.frame, width=window_width_initial, height=window_height_initial - top_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def resize(self):
        """ Function that resizes the frame and children frames (LeftFrame and RightFrame) """

        # Resize the frame
        self.frame["width"] = self.main_window.frame.winfo_width()
        self.frame["height"] = self.main_window.frame.winfo_height() - top_menu_height_initial


class RightFrame:
    """ Right frame of the window, includes FrameContent """

    def __init__(self, p_middle, p_left):
        """ Right frame of the window, includes FrameContent """

        # Transform parameters into class variables
        self.frame_middle = p_middle
        self.frame_left = p_left

        # Creation of the frame
        self.frame_right_width_initial = 800 - self.frame_left.frame_initial_width
        self.frame = tk.Frame(self.frame_middle.frame, width=self.frame_right_width_initial, height=frame_right_height_initial)
        self.frame.grid(row=1, column=1, sticky='n')

        # List containig of pages (= each FrameContent)
        self.frames_content = []

        # Current page (= current FrameContent)
        self.current_frame = 0

    def resize(self):
        """ Function that resizes the RightFrames, FrameContents and Sections """

        # Difference between the initial window width and the resized window width
        offset_width = self.frame_middle.frame.winfo_width() - window_width_initial
        offset_height = self.frame_middle.frame.winfo_height() - window_height_initial

        # Resize the right part
        self.frame_right_width_initial = 800 - self.frame_left.frame_initial_width
        self.frame["width"] = self.frame_right_width_initial + offset_width
        self.frame["height"] = self.frame_middle.frame.winfo_height()

        # Resize the frameContent part
        for page in self.frames_content:
            page.frame["width"] = self.frame_right_width_initial + offset_width
            page.frame["height"] = self.frame_middle.frame["height"]

            # Resize mono sections
            for section in page.mono_sections:
                section.frame["width"] = int(page.frame["width"]/page.nb_column)
                section.frame["height"] = int(page.frame["height"] / page.nb_row)

            # Resize poly sections
            for section in page.poly_sections:
                section.frame["width"] = int(page.frame["width"]/page.nb_column)*section.columspan
                section.frame["height"] = int(page.frame["height"]/page.nb_row)*section.rowspan

            for widget_config_frame in page.frames_configuration_widgets:
                widget_config_frame["height"] = initial_configuration_widget_height + offset_height

    def update_values(self):
        """ Function to send values to other classes """

        # Send some values to left frame
        self.frame_left.current_frame = self.current_frame
        self.frame_left.frames_content = self.frames_content


class LeftFrame:
    """ Left frame of the window, included in the MiddleFrame """

    def __init__(self, p_middle, p_top_frame, p_list_img_1, p_list_img_2):
        """ Left frame of the window, included in the MiddleFrame """

        # Transform parameters into class variables
        self.middle = p_middle
        self.frame_top = p_top_frame
        self.frame_middle = p_middle.frame
        self.list_img_1 = p_list_img_1
        self.list_img_2 = p_list_img_2

        # Current page in the screen
        self.current_frame = 0

        # Current selected widget
        self.current_widget = 0

        # List of pages (= FrameContent)
        self.frames_content = []

        # Resize and modify the left icons
        for i in range(len(self.list_img_1)):
            self.list_img_1[i] = self.list_img_1[i].zoom(10)
            self.list_img_1[i] = self.list_img_1[i].subsample(32)
            self.list_img_2[i] = self.list_img_2[i].zoom(10)
            self.list_img_2[i] = self.list_img_2[i].subsample(32)

        # Color of the left menu
        bg_left = "#42526C"

        # Creation of the left frame
        self.frame_initial_width = 50
        self.frame = tk.Frame(self.frame_middle, bg=bg_left, width=left_menu_width_initial, height=left_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=1, column=0)

        # Creation of the left static frame
        self.static_part = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=50)
        self.static_part.grid(row=1, column=0)
        self.static_part.columnconfigure(0, weight=1)
        self.static_part.grid_propagate(False)

        # Creation of the left moving frames
        self.moving_frames = [tk.Frame for i in range(3)]
        self.buttons = [tk.Button() for i in range(3)]
        self.frames_opened = [False for i in range(3)]
        self.texts = ["Pages", "Widgets", "Paramètres"]

        for i in range(3):
            self.moving_frames[i] = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=0)
            self.moving_frames[i].grid(row=1, column=1)
            self.moving_frames[i].columnconfigure(0, weight=1)
            self.moving_frames[i].grid_propagate(False)

            self.buttons[i] = tk.Button(self.static_part, image=self.list_img_1[i], height=50, borderwidth=0, command=partial(self.show, i))
            self.buttons[i].grid(row=i)

            label_page = tk.Label(self.moving_frames[i], text=self.texts[i], bg="#333333", fg="white")
            label_page.grid(row=0, sticky='nwe')
            label_page.config(font=("Calibri bold", 12))

        # List containing the widget frames configuration
        self.moving_widgets_page = []

        # List which contains the buttons in the left menu
        self.buttons_left = []

    def resize(self):
        """ Function that resizes the LeftFrame, StaticPart and MovingPart """

        # Difference between the initial window height and the resized window height
        offset = self.frame_middle.winfo_height() - left_menu_height_initial

        # Resize the entire frame
        self.frame["height"] = self.frame_middle.winfo_height()

        # Resize the static part
        self.static_part["height"] = left_menu_height_initial + offset

        # Resire each frame included in moving_frames list
        for mf in self.moving_frames:
            mf["height"] = left_menu_height_initial + offset

        # Resire each widget frame included in widgets_frames list
        for wf in self.moving_widgets_page:
            wf["height"] = left_menu_height_initial + offset

    def show(self, p_id):
        """ Function that shows the left frame when it is closed """

        # When the p_id frame is closed
        if not self.frames_opened[p_id]:

            # Update sizes
            self.frame_initial_width = 250
            self.frame["width"] = 250
            self.moving_frames[p_id]["width"] = 200

            # If it is the widget moving frame
            if p_id == 1 and self.frames_content != []:
                self.moving_widgets_page[self.current_frame].grid(row=1, column=1, sticky="news")
                self.moving_widgets_page[self.current_frame].lift()
            else:
                self.moving_frames[p_id].lift()

            # Indicate that the frame is open and change the color of the button
            for i in range(len(self.frames_opened)):
                if i == p_id:
                    self.frames_opened[i] = True
                    self.buttons[i]["image"] = self.list_img_2[i]
                else:
                    self.frames_opened[i] = False
                    self.buttons[i]["image"] = self.list_img_1[i]

            # Indicate that the p_id frame is opened
            self.frames_opened[p_id] = True

            # Open the company name frame
            self.frame_top.open(True)

        # When the p_id frame is open
        else:

            # Change the widths of the frame and the moving frame
            self.frame_initial_width = 50
            self.frame["width"] = 50
            self.moving_frames[p_id]["width"] = 0

            # Indicate that the window is closed
            self.frames_opened[p_id] = False

            # Close the company name frame
            self.frame_top.open(False)

            # Change color of left buttons
            for i in range(len(self.buttons)):
                self.buttons[i]["image"] = self.list_img_1[i]

            # If it is the widget moving frame, close it
            if p_id == 1 and self.frames_content != []:
                self.moving_widgets_page[self.current_frame].grid_forget()

        # Resize the middle frame
        self.middle.resize()

    def display(self):
        """ Function called when we click on a widget """
        # print(self.current_widget)
        # print(self.current_frame)

        self.frames_content[self.current_frame].frames_configuration_widgets[self.current_widget].lift()


class FrameContent:
    """ Page /or Frame content of the window, included in the RightFrame """

    def __init__(self, p_frame_right, p_name, p_background, p_nb_row, p_nb_column, p_source_window):
        """ Page /or Frame content of the window, included in the RightFrame """

        # Transform parameters to class variables
        self.nb_row = p_nb_row
        self.nb_column = p_nb_column
        self.right_frame = p_frame_right
        self.name = p_name
        self.source_window = p_source_window
        self.frame_left = p_frame_right.frame_left

        # Set parameters to the RightFrame class (add the frame in frame_content list/ set current_frame)
        self.right_frame.frames_content.append(self)
        self.right_frame.update_values()
        self.id = len(self.right_frame.frames_content) - 1
        self.right_frame.current_frame = self.id

        # Creation of the main frame
        window_height = settings['dimensions']['window_height']
        top_menu_height = settings['dimensions']['top_menu_height']
        self.frame_width = self.right_frame.frame["width"]
        self.frame_height = window_height - top_menu_height
        self.frame = tk.Frame(self.right_frame.frame, bg=p_background, width=self.frame_width, height=self.frame_height)
        self.frame.grid(row=1)
        self.frame.grid_propagate(False)

        # Lists which will contain sections
        self.mono_sections = []                 # list of 1 x 1 sections
        self.poly_sections = []                 # list of n x m sections
        self.displayed_sections = []            # Addition of mono_sections and poly_sections
        self.disappeared_sections_group = []    # Sections located behind a poly_sections (they will disappeared)

        # Elements that will be used during the "widget configuration" mode
        self.labels_sections = []
        self.buttons_sections_add = []
        self.buttons_sections_delete = []

        # List containing the widgets
        self.widgets = []

        # List containing the widgets configuration frames
        self.frames_configuration_widgets = []

        # Creation of the sections
        self.create_sections()

        # Boolean who indicated if the "widget configuration" mode is open or not
        self.edit_widget_mode_is_activate = False

    def create_sections(self):
        """ Creation of the sections included in the FrameContent page """

        # Lists which will contain sections
        self.mono_sections = []
        self.poly_sections = []
        self.displayed_sections = []
        self.disappeared_sections_group = self.source_window.disappeared_sections_group

        # Adapt the configuration of the frame to number of row/col of sections
        t_row = []
        t_column = []
        for i in range(self.nb_row):
            t_row.append(i)
        for i in range(self.nb_column):
            t_column.append(i)
        self.frame.columnconfigure(tuple(t_column), weight=1)
        self.frame.rowconfigure(tuple(t_row), weight=1)

        # Calculate the dimensions of a mono section
        section_width = int(self.frame["width"] / self.nb_column)
        section_height = int(self.frame["height"] / self.nb_row)

        # Convert "list of list" to list
        disappeared_sections = []
        for x in self.source_window.disappeared_sections_group:
            for y in x:
                disappeared_sections.append(y)

        # Create all mono FrameSection (size 1x1)
        section_id = 0
        for s in self.source_window.mono_sections:
            if s not in disappeared_sections:
                section = FrameSection(self, s.row, s.column, 1, 1, section_width, section_height, section_id, self.frame_left)
                section_id += 1
                self.mono_sections.append(section)

        # Create all poly FrameSection (size nxp)
        for s in self.source_window.poly_sections:
            width = section_width * s.columnspan
            height = section_height * s.rowspan
            section = FrameSection(self, s.row, s.column, s.rowspan, s.columnspan, width, height, section_id, self.frame_left)
            self.poly_sections.append(section)
            section_id += 1

        # List containing all FrameSection
        self.displayed_sections = self.mono_sections + self.poly_sections

        # Create Frame setting widget for each section
        section_id = 0
        for ds in self.displayed_sections:

            # Creation of a widget frame configuration for each section
            widget_setting_frame = tk.Frame(self.frame_left.moving_widgets_page[self.id], bg="white", height=initial_configuration_widget_height,
                                            width=180)
            widget_setting_frame.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))
            widget_setting_frame.columnconfigure(0, weight=1)
            widget_setting_frame.grid_propagate(False)
            self.frames_configuration_widgets.append(widget_setting_frame)

            # Creation of a title in the widget frame configuration
            text = "Widget : " + str(section_id)
            label_widget = tk.Label(widget_setting_frame, text=text, bg="#8989ff", fg="white")
            label_widget.grid(row=0, sticky='nwe')
            label_widget.config(font=("Calibri bold", 12))
            section_id += 1

        # Lists containing the labels & buttons used for "widgets configuration mode"
        self.labels_sections = [tk.Label() for i in range(len(self.displayed_sections))]
        self.buttons_sections_add = [tk.Button() for i in range(len(self.displayed_sections))]
        self.buttons_sections_delete = [tk.Button() for i in range(len(self.displayed_sections))]

    def change_page(self):
        """ Change the page (= FrameContent) """

        # Change the page - put frame in forward
        self.frame.lift()

        # Set this frame as current_frame
        self.right_frame.current_frame = self.id

        # Update values in others class (in left_frame for example)
        self.right_frame.update_values()

    def destroy_sections(self):
        """ Destroy all sections """

        # Destroy mono sections
        for s in self.mono_sections:
            s.frame.grid_forget()

        # Destroy poly sections
        for s in self.poly_sections:
            s.frame.grid_forget()

    def edit_widgets(self, p_list_img_widgets, p_list_title_widgets):
        """ Function called from the edit_widgets_mode function in the main py file """

        # If the edit_widgets_mode is enable
        if not self.edit_widget_mode_is_activate:
            self.hide_widgets()
            self.show_edit_widgets_mode(p_list_img_widgets, p_list_title_widgets)
            self.edit_widget_mode_is_activate = True

        # If the edit_widgets_mode is disable
        else:
            self.show_widgets()
            self.hide_edit_widgets_mode()
            self.edit_widget_mode_is_activate = False

    def show_edit_widgets_mode(self, p_list_img_widgets, p_list_title_widgets):
        """ Show the edit widget mode, in each section you have labels and buttons (add, delete) """

        # For each section of the page (= FrameContent)
        for i in range(len(self.displayed_sections)):

            # Get the section
            s = self.displayed_sections[i]

            # Change the background color
            s.frame["bg"] = "#42526C"

            # Fix the dimensions of paddings
            padx = 5 * s.rowspan
            pady = 5 * s.columspan

            # Name of the widget
            text = "Widget : " + str(i)
            self.labels_sections[i] = tk.Label(s.frame, text=text, bg="#42526C", fg="white")
            self.labels_sections[i].grid(row=0, column=0, sticky='news', padx=(padx,padx), pady=(pady, pady))

            # Button to add a widget in the section
            self.buttons_sections_add[i] = tk.Button(s.frame, text="Ajouter", fg="black")
            self.buttons_sections_add[i]["command"] = partial(self.add_widget, s, p_list_img_widgets, p_list_title_widgets)
            self.buttons_sections_add[i].grid(row=1, column=0, sticky='news', padx=(padx,padx), pady=(pady, pady))

            # Button to delete a widget in the section
            self.buttons_sections_delete[i] = tk.Button(s.frame, text="Supprimer", fg="black")
            self.buttons_sections_delete[i]["command"] = None
            self.buttons_sections_delete[i].grid(row=2, column=0, sticky='news', padx=(padx,padx), pady=(pady, pady))

    def hide_edit_widgets_mode(self):
        """ Hide the edit widget mode """

        # For each section of the page (= FrameContent)
        for i in range(len(self.displayed_sections)):
            self.labels_sections[i].grid_forget()
            self.buttons_sections_add[i].grid_forget()
            self.buttons_sections_delete[i].grid_forget()
            self.displayed_sections[i].frame["bg"] = "white"

    def add_widget(self, p_section, p_list_img_widgets, p_list_title_widgets):
        """ Function called the user click on add a widget during the edit_widget_mode """

        # Creation of the window where the user can choose the widget
        window_widget_choice = tk.Toplevel(self.right_frame.frame)
        window_widget_choice.resizable(False, False)
        window_widget_choice.title("Choix du widget")
        window_widget_choice_icon = tk.PhotoImage(file="img/grid.png")
        window_widget_choice.iconphoto(False, window_widget_choice_icon)
        window_widget_choice_width = 560
        window_widget_choice_height = 400
        screen_width = self.right_frame.frame.winfo_screenwidth()
        screen_height = self.right_frame.frame.winfo_screenheight()
        x_cord = int((screen_width / 2) - (window_widget_choice_width / 2))
        y_cord = int((screen_height / 2) - (window_widget_choice_height / 2))
        window_widget_choice.geometry("{}x{}+{}+{}".format(window_widget_choice_width, window_widget_choice_height, x_cord, y_cord))
        window_widget_choice.columnconfigure((0, 1, 2, 3), weight=1)
        window_widget_choice.rowconfigure((0, 1, 3), weight=1)
        window_widget_choice.rowconfigure((2,4), weight=2)
        window_widget_choice.grid_propagate(False)

        # Title of the login window
        bg_identification = settings['colors']['bg_identification']
        label_login_title = tk.Label(window_widget_choice, text="Choix du widget", bg=bg_identification, fg="white")
        label_login_title.grid(row=0, sticky='new', pady=(0, 0), columnspan=4)
        font_login_title = settings['font']['font_login_title']
        font_size_login_title = settings['font_size']['font_size_login_title']
        label_login_title.config(font=(font_login_title, font_size_login_title))

        # Grid of widgets
        nb_widgets = len(p_list_img_widgets)
        buttons_widgets = [tk.Button() for i in range(nb_widgets)]
        labels_widgets = [tk.Label() for i in range(nb_widgets)]
        j = 0
        for i in range(4):
            labels_widgets[i] = tk.Label(window_widget_choice, text=p_list_title_widgets[i])
            labels_widgets[i].grid(row=1, column=i, padx=(5, 5), pady=(0, 0))
            labels_widgets[i].config(font=("Calibri bold", 12))

            buttons_widgets[i] = tk.Button(window_widget_choice, image=p_list_img_widgets[i], width=100, height=100, borderwidth=2)
            buttons_widgets[i]["command"] = partial(self.apply_widget, i, p_section)
            buttons_widgets[i].grid(row=2, column=i, padx=(5, 5), pady=(0, 0))

        for i in range(nb_widgets - 4):
            labels_widgets[i] = tk.Label(window_widget_choice, text=p_list_title_widgets[i+4])
            labels_widgets[i].grid(row=3, column=i, padx=(5, 5), pady=(0, 0))
            labels_widgets[i].config(font=("Calibri bold", 12))

            buttons_widgets[i] = tk.Button(window_widget_choice, image=p_list_img_widgets[i+4], width=100, height=100, borderwidth=2)
            buttons_widgets[i]["command"] = partial(self.apply_widget, i+4)
            buttons_widgets[i].grid(row=4, column=i, padx=(5, 5), pady=(0, 0))

    def apply_widget(self, p_id_widget, p_section):
        """ Function called the user validates the widget choice """

        # Get the properties of the current section
        s_width = p_section.frame.winfo_width()
        s_height = p_section.frame.winfo_height()
        widget_group_1 = WidgetGroup(1)
        widget_configuration_frame = self.frames_configuration_widgets[p_section.id]

        # If the selected widget is Summary, create a summary widget in the current section
        if p_id_widget == 0:
            widget_summary = Summary(p_section, widget_configuration_frame, widget_group_1, s_width, s_height)
            self.widgets.append(widget_summary)

        # Hide the widget to continue in the edit widget mode
        self.hide_widgets()

    def hide_widgets(self):
        """ Hide the existing widgets to show the edit_widget mode """

        for w in self.widgets:
            w.hide()

    def show_widgets(self):
        """ Show the existing widgets after the edit_widget mode """

        for w in self.widgets:
            w.show()


class ButtonLeftText:
    """ Text buttons located in the left of the window """

    def __init__(self, p_text, p_row, p_parent, p_bg, p_command):

        # Creation of the button
        self.button = tk.Button(p_parent, text=p_text, bg=p_bg, fg="black", width=18, activebackground="#8989ff", borderwidth=1, command=p_command)
        self.button.grid(row=p_row, sticky='n', pady=(10, 0), padx=(5, 5))
        self.button.config(font=("Calibri bold", 12))

        # User interaction with the button
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        """ Function called when the mouse is over the button """

        self.button['bg'] = '#8989ff'
        self.button['fg'] = 'white'

    def on_leave(self, e):
        """ Function called when the mouse leaves the button """

        self.button['bg'] = "white"
        self.button['fg'] = 'black'


class ButtonTopText:
    """ Text buttons located in the top of the window """

    def __init__(self, p_text, p_col, p_parent, p_command):
        """ Text buttons located in the top of the window """

        # Creation of the button
        self.bg = settings['colors']['bg_connect']
        self.button = tk.Button(p_parent, text=p_text, bg=self.bg, fg="white", borderwidth=1, command=p_command)
        self.button.grid(row=0, column=p_col, sticky="ne",  pady=(5, 5), padx=(5, 5), ipadx=15)
        font_top_menu = settings['font']['font_top_menu']
        font_size_top_menu = settings['font_size']['font_size_top_menu']
        self.button.config(font=(font_top_menu, font_size_top_menu))

        # User interaction with the button
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        """ Function called when the mouse is over the button """

        self.button['bg'] = '#8989ff'
        self.button['fg'] = 'white'

    def on_leave(self, e):
        """ Function called when the mouse leaves the button """

        self.button['bg'] = self.bg
        self.button['fg'] = 'white'


class FrameSection:
    """ Section frame (mono or poly) located in a page (= FrameContent)"""

    def __init__(self, p_parent, p_row, p_column, p_rowspan, p_columnspan, p_w, p_h, p_id, p_frame_left):
        """ Initialization of these sections buttons """

        # Transform parameters to class variables
        self.parent = p_parent
        self.row = p_row
        self.column = p_column
        self.rowspan = p_rowspan
        self.columspan = p_columnspan
        self.width = p_w
        self.height = p_h
        self.id = p_id
        self.frame_left = p_frame_left

        # Creation of the frame
        self.frame = tk.Frame(p_parent.frame, width=p_w, height=p_h, bg="white")
        self.frame.grid(row=p_row, column=p_column, rowspan=p_rowspan, columnspan=p_columnspan, padx=(5, 5), pady=(5, 5))
        self.frame.config(highlightbackground="black", highlightthickness=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)

        # User interaction with the button
        self.frame.bind("<Button-1>", self.on_click)

    def on_click(self, e):
        """ Function called when the user click on this section """

        self.frame['bg'] = '#8989ff'
        self.frame_left.current_widget = self.id
        self.frame_left.display()


class FrameSettingWidget:
    """  """

    def __init__(self, p_parent):
        """  """

        self.frame = tk.Frame(p_parent.frame, width=50, height=50, bg="white")
        self.frame.grid(row=0, column=0 , padx=(5, 5), pady=(5, 5))
        self.frame.config(highlightbackground="black", highlightthickness=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)


class WidgetGroup:
    """ Group containing some widgets to update these widget in a same time """

    def __init__(self, p_id):
        """ Group containing some widgets to update these widget in a same time """

        self.id = p_id
        self.widgets = []

    def update_widgets(self):
        """ Function that updates all widgets containing in this group """

        for w in self.widgets:
            w.update()

