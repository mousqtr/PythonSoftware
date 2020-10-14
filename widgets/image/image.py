import tkinter as tk
import json
from PIL import ImageTk, Image
from tkinter import filedialog


with open('settings.json') as json_file:
    settings = json.load(json_file)

class Image_widget:
    """ Widget that shows some label and data """

    def __init__(self, p_section_frame, p_widget_configuration_frame, p_widget_group):
        """
        Initialization of the summary widget that shows some label and data

        :param p_parent: Page that will contain this summary widget
        :param p_row: Row of the page where the widget will be placed
        :param p_widget_group: Group containing this widget
        """

        # Saving the parameters to use them in each function
        self.frame_section = p_section_frame
        self.widget_group = p_widget_group
        self.frame_widget_configuration = p_widget_configuration_frame

        # Add this widget to p_parent widgets
        self.widget_group.widgets.append(self)
        self.type = "Summary"

        # Properties of the widget-
        self.frame = tk.Frame(self.frame_section.frame, bg="white", highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(sticky="news")
        self.frame.update_idletasks()  # to display good dimensions with .winfo_width()
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=10)

        # Title of the page
        self.title = tk.Label(self.frame, text="Image", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, sticky="nwes")
        self.title.config(font=("Calibri bold", 12))

        # # Creation of the buttons that display data
        self.image_tk = Image.open("./img/add.png")
        self.image_pil = Image.open("./img/add.png")

        self.image_panel = tk.Label(self.frame)
        self.image_panel.grid(row=1, column=0, sticky="nwes")
        self.image_is_opened = False

        # User interaction with the button
        self.frame.bind("<Button-1>", self.on_click)
        self.title.bind("<Button-1>", self.on_click)
        self.image_panel.bind("<Button-1>", self.on_click)
        self.image_panel.bind('<Configure>', self.resize_image)


    def update(self):
        print("Update Image")

    def hide(self):
        self.frame.grid_forget()

    def show(self):
        self.frame.grid(row=0, column=0, sticky="news")

    def on_click(self, e):
        """ Function called when the user click on this section """

        self.frame_section.on_click(e)

        # # Label - Choose data to draw
        # label_data = tk.Label(self.frame_widget_configuration, text="Donnée", bg="white")
        # label_data.grid(row=1, sticky='nwe')
        # font_add_label_data = settings['font']['font_login_username']
        # font_size_add_label_data = settings['font_size']['font_size_login_username']
        # label_data.config(font=(font_add_label_data, font_size_add_label_data))

        # Create a button and place it into the window using grid layout
        btn = tk.Button(self.frame_widget_configuration, text='open image', command=self.open_img).grid(
            row=1)

        # # Button - Validation
        # button_validate = tk.Button(self.frame_widget_configuration, text="Valider", width=30)
        # button_validate.grid(row=7, pady=(10, 0), padx=(10, 10))
        # button_validate['command'] = None

    def openfilename(self):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        filename = filedialog.askopenfilename(title='"pen')
        return filename

    def open_img(self):
        # Select the Imagename from a folder
        x = self.openfilename()
        img = Image.open(x)
        self.image_pil = img
        width = self.image_panel.winfo_width()
        height = self.image_panel.winfo_height()
        img = img.resize((width, height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        self.image_panel["image"] = img
        self.image_tk = img

        self.image_is_opened = True

    def resize_image(self, event):
        if self.image_is_opened:
            new_width = self.image_panel.winfo_width()
            new_height = self.image_panel.winfo_height()
            img = self.image_pil
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.image_panel["image"] = img
            self.image_load = img


