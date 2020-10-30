import tkinter as tk
from tkinter import filedialog
import json

from gui import ButtonLeftText
from tables.page_table import PageTable
from pages.edit_page import EditPage

with open('settings.json') as json_file:
    settings = json.load(json_file)

window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']


class Menu:
    """ Top menu """

    def __init__(self, p_main_window, p_widget_images):
        """ Top menu """

        # Transform parameters into class variables
        self.main_window = p_main_window
        self.frame_left = self.main_window.childrens[0]
        self.frame_right = self.main_window.childrens[1]
        self.widget_images = p_widget_images

        # Creation of the menu
        menu_bar = tk.Menu(self.main_window.frame)

        # File button
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Nouveau fichier", command=None)
        menu_file.add_command(label="Ouvrir un fichier", command=self.open_file)
        menu_file.add_command(label="Enregistrer", command=self.save)
        menu_file.add_command(label="Enregistrer sous", command=None)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=None)
        menu_bar.add_cascade(label="Fichier", menu=menu_file)

        # Edit button
        menu_edit = tk.Menu(menu_bar, tearoff=0)
        menu_edit.add_command(label="Ouvrir la configuration des widgets", command=self.open_edit_widgets_mode)
        menu_edit.add_command(label="Quitter la configuration des widgets", command=self.close_edit_widgets_mode)
        menu_edit.add_separator()
        menu_edit.add_command(label="Editer la page", command=self.edit_page)
        menu_bar.add_cascade(label="Edition", menu=menu_edit)

        # Preferences button
        menu_preferences = tk.Menu(menu_bar, tearoff=0)
        menu_preferences.add_command(label="Paramètres", command=None)
        menu_preferences.add_command(label="Thèmes", command=None)
        menu_bar.add_cascade(label="Préférences", menu=menu_preferences)

        # User button
        menu_user = tk.Menu(menu_bar, tearoff=0)
        menu_user.add_command(label="Se connecter", command=None)
        menu_user.add_command(label="Se déconnecter", command=None)
        menu_user.add_command(label="Propriétés", command=None)
        menu_bar.add_cascade(label="Utilisateurs", menu=menu_user)

        # Help button
        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="À propos", command=None)
        menu_bar.add_cascade(label="Aide", menu=menu_help)

        # Add the bar to the window
        self.main_window.frame.config(menu=menu_bar)

        # Correct the window position
        screen_width = p_main_window.frame.winfo_screenwidth()
        screen_height = p_main_window.frame.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width_initial / 2))
        y_cordinate = int((screen_height / 2) - (window_height_initial / 2))
        p_main_window.frame.geometry("{}x{}+{}+{}".format(window_width_initial, window_height_initial, x_cordinate, y_cordinate))

    def open_edit_widgets_mode(self):
        """ Function call when we click on 'Configure widgets' button """

        # If there is at least one PageContent
        if len(self.frame_right.pages_content) > 0:

            # Get the id of the current PageContent
            page_content_id = self.frame_right.current_frame

            # Get the current PageContent
            page_content = self.frame_right.pages_content[page_content_id]

            # Get images to the current PageContent
            page_content.send_img_lists(self.widget_images)

            # Pass the current PageContent to edit_widgets mode
            page_content.open_edit_widgets()

    def close_edit_widgets_mode(self):
        """ Function call when we click on 'Close edit widgets' button """

        # If there is at least one PageContent
        if len(self.frame_right.pages_content) > 0:

            # Get the id of the current PageContent
            page_content_id = self.frame_right.current_frame

            # Get the current PageContent
            page_content = self.frame_right.pages_content[page_content_id]

            # Pass the current PageContent to edit_widgets mode
            page_content.close_edit_widgets()

    def save(self):
        """ Function call when we click on 'Save' button """

        print("Saving ...")

        with open('save/save1.json') as json_file:
            save_json = json.load(json_file)

        # Save the tables
        for table in self.frame_right.pages_table:
            # Build the data that will be add to the saving file
            table_data = {str(table.name): str(table.filename)}

            # Update the saving file (.json) with these data
            save_json['tables'].update(table_data)

        # Save the pages
        for page in self.frame_right.pages_content:

            # Save the dimensions
            nb_row = {"nb_row": page.nb_row}
            nb_column = {"nb_column": page.nb_column}

            # Save the polysections
            # print(page.disappeared_sections_group)

            page_data = {page.name: [nb_row, nb_column]}

            # Update the saving file (.json) with these data
            save_json['pages'].update(page_data)

        with open('save/save1.json', 'w') as outfile:
            json.dump(save_json, outfile, indent=4)

    def open_file(self):
        """ Function call when we click on 'Open' button """

        filename = filedialog.askopenfilename(title='Ouvrir un fichier')

        with open(filename) as json_file:
            save_json = json.load(json_file)

        # Load the tables
        for table_name in save_json['tables']:
            filename = save_json['tables'][table_name]
            page_table = PageTable(self.frame_right, filename, table_name)

            # Create a left button
            row = len(self.frame_left.buttons_table) + 1
            new_button_left = ButtonLeftText(table_name, row, self.frame_left.moving_frames[3], "white",
                                             page_table.change_page)
            self.frame_left.buttons_table.append(new_button_left)

        for page_name in save_json['pages']:
            print(page_name)

    def edit_page(self):
        if len(self.frame_right.pages_content) > 0:
            EditPage(self.main_window.frame, self.frame_left, self.frame_right)