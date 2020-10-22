import tkinter as tk
import json
from functools import partial
from tkinter import ttk
from widgets.summary.summary_functions import fill_file


# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Open the data file
with open('widgets/summary/summary_data.json') as json_file:
    widgets_data = json.load(json_file)


class WidgetSummary:
    """ Widget that shows some label and data """

    def __init__(self, p_section, p_widget_configuration_frame, p_widget_group):
        """
        Initialization of the summary widget that shows some label and data

        :param p_parent: Page that will contain this summary widget
        :param p_widget_configuration_frame: Frame in the left menu, used to edit the widget
        :param p_widget_group: Group containing this widget
        """

        # Saving the parameters to use them in each function
        self.section = p_section
        self.widget_group = p_widget_group
        self.frame_widget_configuration = p_widget_configuration_frame.frame

        # Add this widget to p_parent widgets
        self.widget_group.widgets.append(self)
        self.type = "Summary"

        # Properties of the widget-
        self.frame = tk.Frame(self.section.frame, bg="white", highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(sticky="news")
        self.frame.update_idletasks()  # to display good dimensions with .winfo_width()
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=10)

        # Title of the page
        self.title = tk.Label(self.frame, text=" ", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, sticky="nwes")
        self.title.config(font=("Calibri bold", 12))

        # Creation of the buttons that display data
        self.frame_data = tk.Frame(self.frame)
        self.frame_data.grid(row=1, column=0, sticky="nwes")
        self.frame_data.columnconfigure((0, 1, 2), weight=1)
        self.frame_data.rowconfigure((0, 1, 2), weight=1)

        # Creation of the buttons that display data
        self.label_data = tk.Label(self.frame_data, text=" ", fg="white")
        self.label_data.grid(row=1, column=1)
        self.label_data.config(font=("Calibri bold", 11))

        # Loading and changing the content of the buttons
        self.load()

        # Fill the data file
        fill_file()

        # User interaction with the button
        self.frame.bind("<Button-1>", self.on_click)
        self.frame_data.bind("<Button-1>", self.on_click)
        self.title.bind("<Button-1>", self.on_click)

        # User resize interaction
        self.frame_data.bind('<Configure>', self.resize)

        # lists of differents size and font
        self.list_size = [i*10 for i in range(100)]
        self.list_font = [i*3 for i in range(4, 60)]
        self.current_index_size = 7
        self.current_index_font = 0

        # Boolean that indicates if the image has a title or not
        self.bool_title = True

    def on_click(self, e):
        """
        Function called when the user click on this section
        It is possible to find here all elements to configure the widget
        """

        # Call the parent on_click function
        self.section.on_click(e)

        # Label - Title
        label_title = tk.Label(self.frame_widget_configuration, text="Titre du widget", bg="#333333", fg="white")
        label_title.grid(row=1, sticky='nwe', pady=(10, 0))
        label_title.config(font=("Calibri", 13))

        # Entry - Write the title
        self.entry_title = tk.Entry(self.frame_widget_configuration, width=19, textvariable=" ")
        self.entry_title.grid(row=2)
        self.entry_title.config(font=("Calibri bold", 10))

        # Label - Choose data to draw
        label_data = tk.Label(self.frame_widget_configuration, text="Donnée", bg="#333333", fg="white")
        label_data.grid(row=3, sticky='nwe', pady=(10, 0))
        label_data.config(font=("Calibri", 13))

        # Combobox - Choose data to draw
        list_data = []
        for x in widgets_data['data']:
            list_data.append(x)
        combo_data = ttk.Combobox(self.frame_widget_configuration, values=list_data)
        combo_data.current(0)
        combo_data.grid(row=4)

        # Label - Choose background color
        label_bg_color = tk.Label(self.frame_widget_configuration, text="Couleur du fond", bg="#333333", fg="white")
        label_bg_color.grid(row=5, sticky='n', pady=(10, 0))
        label_bg_color.config(font=("Calibri", 13))

        # Combobox - Choose background color to draw
        list_color = [" ", "black", "white", "red", "orange", "blue", "yellow", "purple", "green", "white"]
        combo_bg_color = ttk.Combobox(self.frame_widget_configuration, values=list_color)
        combo_bg_color.current(0)
        combo_bg_color.grid(row=6)

        # Label - Choose color
        label_color = tk.Label(self.frame_widget_configuration, text="Couleur de la donnée", bg="#333333", fg="white" )
        label_color.grid(row=7, sticky='n', pady=(10, 0))
        label_color.config(font=("Calibri", 13))

        # Combobox - Choose frontground color to draw
        list_color = [" ", "black", "white", "red", "orange", "blue", "yellow", "purple", "green", "white"]
        combo_fg_color = ttk.Combobox(self.frame_widget_configuration, values=list_color)
        combo_fg_color.current(0)
        combo_fg_color.grid(row=8)

        # Label - Choose color
        label_color = tk.Label(self.frame_widget_configuration, text="Taille de la police", bg="#333333", fg="white" )
        label_color.grid(row=9, sticky='n', pady=(10, 0))
        label_color.config(font=("Calibri", 13))

        # Combobox - Choose frontground color to draw
        list_font = [i*3 for i in range(4, 20)]
        combo_font = ttk.Combobox(self.frame_widget_configuration, values=list_font)
        combo_font.current(0)
        combo_font.grid(row=10)

        # Button - Validation
        button_validate = tk.Button(self.frame_widget_configuration, text="Valider", width=19, bg="orange", fg="white")
        button_validate.grid(row=11, pady=(20, 0), padx=(10, 10))
        button_validate.config(font=("Calibri", 10))
        button_validate['command'] = partial(self.validate, 0, 0, combo_data, combo_bg_color, combo_fg_color, combo_font)

    def validate(self, p_row, p_column, p_combo_data, p_combo_bg_color, p_combo_fg_color, p_font):
        """
        Function that update the button in (p_row,p_column) with the content p_combo and p_combo_color

        :param p_row: Row of the button
        :param p_column: Column of the button
        :param p_combo_data: Name of the data
        :param p_combo_bg_color: Combo background color of the data
        :param p_combo_fg_color: Combo background color of the data
        """

        # Get the content of comboboxes
        data = p_combo_data.get()
        bg_color = p_combo_bg_color.get()
        fg_color = p_combo_fg_color.get()

        if data == ' ':
            data_text = data
        else:
            data_text = data + '\n' + str(widgets_data['data'][data])

        if bg_color == ' ':
            background_color = "SystemButtonFace"
        else:
            background_color = bg_color

        if fg_color == ' ':
            frontground_color = "black"
        else:
            frontground_color = fg_color

        # Replace the buttons text with the comboboxes content
        self.frame_data['bg'] = background_color
        self.label_data['text'] = data_text
        self.label_data['bg'] = background_color
        self.label_data['fg'] = frontground_color

        # Change font
        index_font = p_font.current()
        self.label_data.config(font=("Calibri bold", self.list_font[index_font]))
        self.current_index_font = index_font

        width_frame = self.frame_data.winfo_width()
        height_frame = self.frame_data.winfo_height()
        index_w = width_frame//10
        index_h = height_frame//10
        index_size = min(index_w, index_h)
        self.list_size[index_size]

        # Save the data
        self.save(p_row, p_column, data, background_color, frontground_color)

        # Change title
        title = self.entry_title.get()

        if title == " " or title == "" and self.bool_title == True:
            self.title.grid_forget()
            self.bool_title = False
            self.title["text"] = " "
        else:
            self.bool_title = True
            self.title.grid(row=0, column=0, sticky="nwes")
            self.title["text"] = title

    def resize(self, event):
        """ Function called when the parent section is resized"""

        print("Resize SummaryWidget")

        # Get the width and the height of the parent frame
        width_frame = self.frame_data.winfo_width()
        height_frame = self.frame_data.winfo_height()

        # Calculate the index of these dimensions
        index_w = width_frame//10
        index_h = height_frame//10

        # Get the minimum index
        index_size = min(index_w, index_h)

        # Get the difference between this new index and he old one
        diff = index_size - self.current_index_size

        # If the index size has changed
        if diff != 0:

            # Calculate the new font size index
            index_font = self.current_index_font + diff

            # Change the font size of
            self.label_data.config(font=("Calibri bold", self.list_font[index_font]))

            self.current_index_font = index_font
            self.current_index_size = index_size

    def hide(self):
        """ Hide the widget (during the edit widget mode)"""

        print("Hide SummaryWidget")
        self.frame.grid_forget()

    def show(self):
        """ Hide the widget (after the edit widget mode)"""

        print("Show SummaryWidget")
        self.frame.grid(row=0, column=0, sticky="news")

    def save(self, p_row, p_column, p_data, p_bg_color, p_fg_color):
        """
        Function that saves the content of the widget

        :param p_row: Row of the button
        :param p_column: Column of the button
        :param p_data: Name of the data
        :param p_bg_color: Background color of the data
        :param p_fg_color: Frontground color of the data
        """

        print("Save SummaryWidget")

        # # Build the texts that will be add to the saving file
        # key = str(p_row) + ',' + str(p_column)
        # value_data = {key: p_data}
        # value_bg_color = {key: p_bg_color}
        # value_fg_color = {key: p_fg_color}
        #
        # # Update the saving file (.json) with these data
        # widgets_data['summary_data'].update(value_data)
        # widgets_data['summary_bg_color'].update(value_bg_color)
        # widgets_data['summary_fg_color'].update(value_fg_color)
        # with open('widgets/summary/summary_data.json', 'w') as outfile:
        #     json.dump(widgets_data, outfile, indent=4)

    def load(self):
        """ Function that loads the content of the widget"""

        # # Get all the data contain in the "summary section" of the saving file
        # for x in widgets_data['summary_data']:
        #     coord = x.split(',')
        #     row = int(coord[0])
        #     column = int(coord[1])
        #     data = widgets_data['summary_data'][x]
        #     bg_color = widgets_data['summary_bg_color'][x]
        #     fg_color = widgets_data['summary_fg_color'][x]
        #     if data == ' ':
        #         data_text = data
        #     else:
        #         data_text = data + '\n' + str(widgets_data['data'][data])
        #     self.buttons[row][column]['text'] = data_text
        #     self.buttons[row][column]['bg'] = bg_color
        #     self.buttons[row][column]['fg'] = fg_color

        print("Load SummaryWidget")

        self.frame_data['bg'] = "SystemButtonFace"
        self.label_data['text'] = " "
        self.label_data['bg'] = "SystemButtonFace"
        self.label_data['fg'] = "black"

    def update(self):
        """ Function that update some values widget_group is updated"""

        print("Update SummaryWidget")