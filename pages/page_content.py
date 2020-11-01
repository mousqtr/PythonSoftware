import tkinter as tk
import Pmw
import json
from functools import partial

from widgets.summary.summary import WidgetSummary
from widgets.image.image import WidgetImage
from widgets.table.table import WidgetTable

from gui import ButtonLeftText

with open('settings.json') as json_file:
    settings = json.load(json_file)

initial_configuration_widget_height = 550
window_height_initial = settings['dimensions']['window_height']


class PageContent:
    """ Page /or Frame content of the window, included in the RightFrame """

    def __init__(self, p_frame_right, p_name, p_background, p_nb_row, p_nb_column, p_sections):
        """ Page /or Frame content of the window, included in the RightFrame """

        # Transform parameters to class variables
        self.nb_row = p_nb_row
        self.nb_column = p_nb_column
        self.right_frame = p_frame_right
        self.frame_left = p_frame_right.frame_left
        self.name = p_name
        self.bg = p_background
        self.sections = p_sections

        # Create a widget frame for each frame content
        moving_part_widgets = tk.Frame(self.frame_left.frame, bg="#005dac", height=window_height_initial, width=200)
        moving_part_widgets.columnconfigure(0, weight=1)
        moving_part_widgets.grid_propagate(False)
        self.frame_left.moving_widgets_page.append(moving_part_widgets)

        # Add the page name in the widget page
        text = self.name
        label_page = tk.Label(moving_part_widgets, text=text, bg="#333333", fg="white")
        label_page.grid(row=0, sticky='nwe')
        label_page.config(font=("Calibri bold", 12))

        # Set parameters to the RightFrame class (add the frame in frame_content list/ set current_frame)
        self.right_frame.pages_content.append(self)
        self.right_frame.update_values()
        self.id = len(self.right_frame.pages_content) - 1
        self.right_frame.current_frame = self.id

        # Creation of the main frame
        self.frame_width = self.right_frame.frame["width"]
        self.frame_height = self.right_frame.frame["height"]
        self.frame = tk.Frame(self.right_frame.frame, bg=p_background, width=self.frame_width, height=self.frame_height)
        self.frame.grid(row=0, column=0)
        self.frame.grid_propagate(False)

        # Lists which will contain sections
        self.frame_sections = []
        self.disappeared_sections_group = []    # Sections located behind a poly_sections (they will disappeared)

        # Elements that will be used during the "widget configuration" mode
        self.frame_edit_mode = []
        self.buttons_widget = []
        self.buttons_sections_add = []
        self.buttons_sections_delete = []

        # List of images used
        self.list_img_widgets = []
        self.list_img_widgets2 = []
        self.list_title_widgets = []
        self.list_buttons_widget = []

        # List containing the widgets
        self.widgets = []

        # List containing the widgets configuration objects
        self.configuration_widgets = []

        # List containing the widgets configuration objects frames
        self.frames_configuration_widgets = []

        # Creation of the sections
        self.create_sections()

        # Boolean who indicated if the "widget configuration" mode is open or not
        self.edit_widget_mode_is_activate = False

        # Text which appear when a mouse over something
        self.message = Pmw.Balloon(self.frame)  # Calling the tooltip

        # Create the left button
        row = len(self.frame_left.buttons_page) + 1
        new_button_left = ButtonLeftText(self.name, row, self.frame_left.moving_frames[0], "white", self.change_page)
        self.frame_left.buttons_page.append(new_button_left)

    def create_sections(self):
        """ Creation of the sections included in the PageContent page """

        self.frame_sections = []
        self.configuration_widgets = []
        self.frames_configuration_widgets = []

        # Adapt the configuration of the frame to number of row/col of sections
        t_row = []
        t_column = []
        for i in range(self.nb_row):
            t_row.append(i)
        for i in range(self.nb_column):
            t_column.append(i)
        self.frame.columnconfigure(tuple(t_column), weight=1)
        self.frame.rowconfigure(tuple(t_row), weight=1)

        # Creation of all FrameSections
        section_id = 0
        for s in self.sections:
            FrameSection(self, s.row, s.column, s.rowspan, s.columnspan, section_id)
            section_id += 1

        # Lists containing the labels & buttons used for "widgets configuration mode"
        self.frame_edit_mode = [tk.Frame() for i in range(len(self.frame_sections))]
        self.buttons_widget = [tk.Button() for i in range(len(self.frame_sections))]
        self.buttons_sections_add = [tk.Button() for i in range(len(self.frame_sections))]
        self.buttons_sections_delete = [tk.Button() for i in range(len(self.frame_sections))]

    def change_page(self):
        """ Change the page (= PageContent) """

        # Set this frame as current_frame
        self.right_frame.current_frame = self.id

        # Indicates that we are in the PageContent mode
        self.right_frame.mode = 1

        # Update values in others class (in left_frame for example)
        self.right_frame.update_values()

        # Resize the frame
        self.right_frame.resize()

        # Hide all PageTable pages
        for page in self.right_frame.pages_table:
            page.frame.grid_forget()

        # Hide all PageContent pages
        for page in self.right_frame.pages_content:
            page.frame.grid_forget()

        # Show the page
        self.frame.grid(row=1)

        # Change the page - put frame in forward
        self.frame.lift()

    def destroy_sections(self):
        """ Destroy all sections """

        # Destroy all FrameSection
        for s in self.frame_sections:
            s.frame.grid_forget()

    def send_img_lists(self, p_img_widgets):
        """ Get images lists from main file """

        # List of images used for widgets icons
        self.list_img_widgets = p_img_widgets[0]

        # List of images used as widgets title
        self.list_title_widgets = p_img_widgets[1]

        # List of images used for buttons during the widget configuration mode
        self.list_buttons_widget = p_img_widgets[2]

        # List of images used for widgets icons 2
        self.list_img_widgets2 = p_img_widgets[3]

    def open_edit_widgets(self):
        """ Function called from the edit_widgets_mode function in the Menu class """

        # If the edit_widgets_mode is enable
        if not self.edit_widget_mode_is_activate:
            self.frame["bg"] = "#e8e8e8"
            self.hide_widgets()
            self.show_edit_widgets_mode()
            self.edit_widget_mode_is_activate = True

    def close_edit_widgets(self):
        """ Function called from the close_widgets_mode function in the Menu class """

        # If the edit_widgets_mode is disable
        if self.edit_widget_mode_is_activate:
            self.frame["bg"] = self.bg
            self.show_widgets()
            self.hide_edit_widgets_mode()
            self.edit_widget_mode_is_activate = False

    def show_edit_widgets_mode(self):
        """ Show the edit widget mode, in each section you have labels and buttons (add, delete) """

        # For each section of the page (= PageContent)
        for i in range(len(self.frame_sections)):

            # Get the section
            s = self.frame_sections[i]

            self.frame_edit_mode[i] = tk.Frame(s.frame, bg="white")
            self.frame_edit_mode[i].grid(sticky="news")
            self.frame_edit_mode[i].columnconfigure((0, 1), weight=1)
            self.frame_edit_mode[i].rowconfigure((0, 1), weight=1)
            self.frame_edit_mode[i].grid_propagate(False)

            # Change the background color
            s.frame["bg"] = "#005dac"

            # Fix the dimensions of paddings
            padx = 2
            pady = 2

            # Button to add a widget in the section
            self.buttons_widget[i] = tk.Label(self.frame_edit_mode[i])
            self.buttons_widget[i]["command"] = None
            self.buttons_widget[i].grid(row=0, rowspan=1, columnspan=2, sticky='news', padx=(padx, padx), pady=(pady, pady))
            if s.widget_index == -1:
                # self.buttons_widget[i]["image"] = self.list_buttons_widget[2]
                self.buttons_widget[i]["text"] = "No widget"
                self.buttons_widget[i].config(font=("Calibri bold", 10))
            else :
                self.buttons_widget[i]["image"] = self.list_img_widgets2[s.widget_index]

            # Button to add a widget in the section
            self.buttons_sections_add[i] = tk.Button(self.frame_edit_mode[i], image=self.list_buttons_widget[0])
            self.buttons_sections_add[i]["command"] = partial(self.add_widget, s)
            self.buttons_sections_add[i].grid(row=1, column=0, sticky='news', padx=(padx,padx), pady=(pady, pady))
            self.message.bind(self.buttons_sections_add[i], 'Ajouter un widget')

            # Button to delete a widget in the section
            self.buttons_sections_delete[i] = tk.Button(self.frame_edit_mode[i], image=self.list_buttons_widget[1])
            self.buttons_sections_delete[i]["command"] = None
            self.buttons_sections_delete[i].grid(row=1, column=1, sticky='news', padx=(padx, padx), pady=(pady, pady))
            self.message.bind(self.buttons_sections_delete[i], 'Supprimer le widget')

    def hide_edit_widgets_mode(self):
        """ Hide the edit widget mode """

        # For each section of the page (= PageContent)
        for i in range(len(self.frame_sections)):
            self.frame_edit_mode[i].grid_forget()
            self.frame_sections[i].frame["bg"] = "white"

    def add_widget(self, p_section):
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
        nb_widgets = len(self.list_img_widgets)
        buttons_widgets = [tk.Button() for i in range(nb_widgets)]
        labels_widgets = [tk.Label() for i in range(nb_widgets)]
        j = 0
        for i in range(4):
            labels_widgets[i] = tk.Label(window_widget_choice, text=self.list_title_widgets[i])
            labels_widgets[i].grid(row=1, column=i, padx=(5, 5), pady=(0, 0))
            labels_widgets[i].config(font=("Calibri bold", 12))

            buttons_widgets[i] = tk.Button(window_widget_choice, image=self.list_img_widgets[i], width=100, height=100, borderwidth=2)
            buttons_widgets[i]["command"] = partial(self.apply_widget, i, p_section)
            buttons_widgets[i].grid(row=2, column=i, padx=(5, 5), pady=(0, 0))

        for i in range(nb_widgets - 4):
            labels_widgets[i] = tk.Label(window_widget_choice, text=self.list_title_widgets[i+4])
            labels_widgets[i].grid(row=3, column=i, padx=(5, 5), pady=(0, 0))
            labels_widgets[i].config(font=("Calibri bold", 12))

            buttons_widgets[i] = tk.Button(window_widget_choice, image=self.list_img_widgets[i+4], width=100, height=100, borderwidth=2)
            buttons_widgets[i]["command"] = partial(self.apply_widget, i+4, p_section)
            buttons_widgets[i].grid(row=4, column=i, padx=(5, 5), pady=(0, 0))

    def apply_widget(self, p_id_widget, p_section):
        """ Function called the user validates the widget choice """

        # Get the properties of the current section
        widget_configuration = self.configuration_widgets[p_section.id]

        # If the selected widget is Summary, create a summary widget in the current section
        if p_id_widget == 0:
            widget = WidgetImage(p_section, widget_configuration)

        if p_id_widget == 1:
            widget = WidgetSummary(p_section, widget_configuration)

        if p_id_widget == 2:
            widget = WidgetTable(p_section, widget_configuration)

        self.widgets.append(widget)

        # Bind the index of the widget to the FrameSection
        p_section.widget_index = p_id_widget

        # Change the image of the FrameSection in the configuration mode
        self.buttons_widget[p_section.id]["image"] = self.list_img_widgets2[p_id_widget]

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


class FrameSection:
    """ Section frame (mono or poly) located in a page (= PageContent)"""

    def __init__(self, p_page_content, p_row, p_column, p_rowspan, p_columnspan, p_id):
        """ Initialization of these sections buttons """

        # Transform parameters to class variables
        self.page_content = p_page_content
        self.row = p_row
        self.column = p_column
        self.rowspan = p_rowspan
        self.columnspan = p_columnspan
        self.id = p_id
        self.frame_left = self.page_content.frame_left

        # Calculate the dimensions of a mono section
        section_width = int(self.page_content.frame["width"] / self.page_content.nb_column)
        section_height = int(self.page_content.frame["height"] / self.page_content.nb_row)

        # Calculate width and height
        width = section_width * self.columnspan - 10 # 10 is the padx
        height = section_height * self.rowspan - 10 # 10 is the pady

        # Creation of the frame
        self.frame = tk.Frame(self.page_content.frame, width=width, height=height, bg="white")
        self.frame.grid(row=p_row, column=p_column, rowspan=p_rowspan, columnspan=p_columnspan, padx=(5, 5), pady=(5, 5))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)
        # self.frame.config(highlightbackground="black", highlightthickness=1)

        # Widget index contained in the section
        self.widget_index = -1      # - 1 when there is no widget in the FrameSection

        # Add this section to list of FrameSection
        self.page_content.frame_sections.append(self)

        # Creation of the widget configuration frame
        widget_setting = WidgetFrameConfiguration(self.frame_left.moving_widgets_page[self.page_content.id], self.id)
        self.page_content.configuration_widgets.append(widget_setting)
        self.page_content.frames_configuration_widgets.append(widget_setting.frame)

        # User interaction with the button
        self.frame.bind("<Button-1>", self.on_click)

    def on_click(self, e):
        """ Function called when the user click on this section """

        self.frame_left.current_widget = self.id
        self.frame_left.change_config_widget_frame()


class WidgetFrameConfiguration:
    def __init__(self, p_parent, p_id):

        # Creation of a widget frame configuration for each section
        self.frame = tk.Frame(p_parent, bg="#333333",
                                        height=initial_configuration_widget_height,
                                        width=180)
        self.frame.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_propagate(False)

        # Creation of a title in the widget frame configuration
        text = "Widget : " + str(p_id)
        self.label_title = tk.Label(self.frame, text=text, bg="white", fg="#333333")
        self.label_title.grid(row=0, sticky='nwe')
        self.label_title.config(font=("Calibri bold", 12))

