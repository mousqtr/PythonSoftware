import tkinter as tk
import tkinter.font as font
import json
import Pmw
from functools import partial

with open('settings.json') as json_file:
    settings = json.load(json_file)

window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
left_menu_width_initial = 50
left_menu_height_initial = window_height_initial


initial_configuration_widget_height = 550

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

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

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

        # When the left menu state changes, this boolean is set to True
        self.left_menu_changed = False

        # List which contains LeftFrame and RightFrame
        self.childrens = []

        # Bind the resize function to the main_window
        self.frame.bind("<Configure>", self.window_resize)

    # Detect the window resize
    def window_resize(self, event):
        """ Function called for each iteration of the loop """

        # If the main window is opened and resized is allowed
        if self.resized:
            width = self.frame.winfo_width()
            height = self.frame.winfo_height()

            # Resize the dimensions have changed
            if width != self.width or height != self.height or self.left_menu_changed:
                self.width = width
                self.height = height
                self.left_menu_changed = False

                # Resize the window and internal elements
                for child in self.childrens:
                    child.resize()


class RightFrame:
    """ Right frame of the window, includes PageInitial, PageContent, PageTable """

    def __init__(self, p_main_frame, p_left):
        """ Right frame of the window, includes PageInitial, PageContent, PageTable """

        # Transform parameters into class variables
        self.frame_main = p_main_frame
        self.frame_left = p_left

        # Set this class available from MainWindow
        self.frame_main.childrens.append(self)

        # Creation of the frame
        self.frame_right_width_initial = 800 - self.frame_left.frame_initial_width
        self.frame = tk.Frame(self.frame_main.frame, width=self.frame_right_width_initial, height=window_height_initial, bg="#e8e8e8")
        self.frame.grid(row=0, column=1, sticky='n')
        self.frame.grid_propagate(False)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # List containing initial pages (= each PageInitial)
        self.frames_initial = []

        # List containing pages (= each PageContent)
        self.pages_content = []

        # List containing tables (= each NewTable)
        self.pages_table = []

        # Current page (= current PageContent)
        self.current_frame = 0

        # Current page (= current PageTable)
        self.current_table = 0

        # Current mode
        # mode 0 : PageInitial mode
        # mode 1 : PageContent mode
        # mode 2 : PageTable mode
        self.mode = 0

    def resize(self):
        """ Function that resizes the RightFrame, PageInitial/PageContent/PageTable and Sections """

        # Difference between the initial window width and the resized window width
        offset_width = self.frame_main.frame.winfo_width() - window_width_initial
        offset_height = self.frame_main.frame.winfo_height() - window_height_initial

        # Resize the right part
        self.frame_right_width_initial = 800 - self.frame_left.frame_initial_width
        self.frame["width"] = self.frame_right_width_initial + offset_width
        self.frame["height"] = self.frame_main.frame.winfo_height()

        # Resize the PageInitial part
        if self.mode == 0:

            print("Resize initial frame")

            page = self.frames_initial[0]
            page.frame["width"] = self.frame_right_width_initial + offset_width
            page.frame["height"] = self.frame_main.frame.winfo_height()

        # Resize the PageContent part
        if self.mode == 1:

            if self.pages_content != []:

                print("Resize PageContent ", self.current_frame)

                page = self.pages_content[self.current_frame]
                page.frame["width"] = self.frame_right_width_initial + offset_width
                page.frame["height"] = self.frame_main.frame.winfo_height()

                # Resize mono sections
                for section in page.mono_sections:
                    section.frame["width"] = (page.frame["width"] / page.nb_column) * section.columnspan - 10
                    section.frame["height"] = (page.frame["height"] / page.nb_row) * section.rowspan - 10

                # Resize poly sections
                for section in page.poly_sections:
                    section.frame["width"] = int(page.frame["width"]/page.nb_column)* section.columnspan - 10
                    section.frame["height"] = int(page.frame["height"]/page.nb_row)* section.rowspan - 10

                for widget_config_frame in page.frames_configuration_widgets:
                    widget_config_frame["height"] = initial_configuration_widget_height + offset_height

        # Resize the PageTable part
        if self.mode == 2:

            if self.pages_table != []:

                print("Resize PageTable ", self.current_table)

                page = self.pages_table[self.current_table]

                page.frame["width"] = self.frame_right_width_initial + offset_width
                page.frame["height"] = self.frame_main.frame.winfo_height()

                page.frame_table["width"] = page.frame["width"] - 10
                page.frame_table["height"] = page.frame["height"] - 10


    def update_values(self):
        """ Function to send values to other classes """

        # Send some values to left frame
        self.frame_left.current_frame = self.current_frame
        self.frame_left.pages_content = self.pages_content


class LeftFrame:
    """ Left frame of the window, included in the MiddleFrame """

    def __init__(self, p_main_frame, p_list_img_1, p_list_img_2):
        """ Left frame of the window, included in the MiddleFrame """

        # Transform parameters into class variables
        self.frame_main = p_main_frame
        self.list_img_1 = p_list_img_1
        self.list_img_2 = p_list_img_2

        self.frame_main.childrens.append(self)

        # Current page in the screen
        self.current_frame = 0

        # Current selected widget
        self.current_widget = 0

        # List of pages (= PageContent)
        self.pages_content = []

        # List of tables (= PageTable)
        self.pages_table = []

        # Resize and modify the left icons
        for i in range(len(self.list_img_1)):
            self.list_img_1[i] = self.list_img_1[i].zoom(10)
            self.list_img_1[i] = self.list_img_1[i].subsample(32)
            self.list_img_2[i] = self.list_img_2[i].zoom(10)
            self.list_img_2[i] = self.list_img_2[i].subsample(32)

        # Color of the left menu
        bg_left = "#005dac"

        # Creation of the left frame
        self.frame_initial_width = 50
        self.frame = tk.Frame(self.frame_main.frame, bg=bg_left, width=left_menu_width_initial, height=left_menu_height_initial)
        self.frame.grid_propagate(False)
        self.frame.grid(row=0, column=0)

        # Creation of the left static frame
        self.static_part = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=50)
        self.static_part.grid(row=1, column=0)
        self.static_part.columnconfigure(0, weight=1)
        self.static_part.grid_propagate(False)

        # Creation of the left moving frames
        self.moving_frames = [tk.Frame for i in range(len(self.list_img_1))]
        self.buttons = [tk.Button() for i in range(len(self.list_img_1))]
        self.frames_opened = [False for i in range(len(self.list_img_1))]
        self.texts = ["Pages", "Widgets", "Paramètres", "Tableaux"]

        # Overlay message
        self.message = Pmw.Balloon(self.frame)

        for i in range(len(self.list_img_1)):
            self.moving_frames[i] = tk.Frame(self.frame, bg=bg_left, height=left_menu_height_initial, width=0)
            self.moving_frames[i].grid(row=1, column=1)
            self.moving_frames[i].columnconfigure(0, weight=1)
            self.moving_frames[i].grid_propagate(False)

            self.buttons[i] = tk.Button(self.static_part, image=self.list_img_1[i], height=50, borderwidth=0, command=partial(self.show, i))
            self.buttons[i].grid(row=i)
            self.message.bind(self.buttons[i], self.texts[i])

            label_page = tk.Label(self.moving_frames[i], text=self.texts[i], bg="#333333", fg="white")
            label_page.grid(row=0, sticky='nwe')
            label_page.config(font=("Calibri bold", 12))

        # List containing the widget frames configuration
        self.moving_widgets_page = []

        # List which contains the page buttons in the left menu
        self.buttons_page = []

        # List which contains the table buttons in the left menu
        self.buttons_table = []

    def resize(self):
        """ Function that resizes the LeftFrame, StaticPart and MovingPart """

        # Difference between the initial window height and the resized window height
        offset = self.frame_main.frame.winfo_height() - left_menu_height_initial

        # Resize the entire frame
        self.frame["height"] = self.frame_main.frame.winfo_height()

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
            if p_id == 1 and self.pages_content != []:
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

        # When the p_id frame is open
        else:

            # Change the widths of the frame and the moving frame
            self.frame_initial_width = 50
            self.frame["width"] = 50
            self.moving_frames[p_id]["width"] = 0

            # Indicate that the window is closed
            self.frames_opened[p_id] = False

            # Change color of left buttons
            for i in range(len(self.buttons)):
                self.buttons[i]["image"] = self.list_img_1[i]

            # If it is the widget moving frame, close it
            if p_id == 1 and self.pages_content != []:
                self.moving_widgets_page[self.current_frame].grid_forget()

        self.frame_main.left_menu_changed = True

    def change_config_widget_frame(self):
        """ Function called when we click on a widget """

        self.pages_content[self.current_frame].frames_configuration_widgets[self.current_widget].lift()


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

        self.button['bg'] = '#00aeef'
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


class PageInitial:
    def __init__(self, p_right_frame):

        # Transform parameters into class variables
        self.right_frame = p_right_frame

        # Indicates to the RightFrame class that is it an initial page
        self.right_frame.frames_initial.append(self)

        # Creation of the frame
        frame_width = self.right_frame.frame["width"]
        frame_height = self.right_frame.frame["height"]
        self.frame = tk.Frame(self.right_frame.frame, width=frame_width, height=frame_height)
        self.frame.grid(row=0, column=0)
        self.frame.grid_propagate(False)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.lift()

        # Content of this initial page
        presentation_text = "Bienvenue à vous ! \n \n Pour commencer, rendez-vous dans le premier onglet \n et appuyer sur '+' pour créer une nouvelle page "
        self.label_title = tk.Label(self.frame, text=presentation_text, fg="black", bg="#e8e8e8")
        self.label_title.grid(row=0, column=0, sticky="news")
        init_font = font.Font(size=13, weight="bold")
        self.label_title.config(font=init_font)
