import tkinter as tk
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)


class Login:
    """ In that class, the login window will be managed"""

    def __init__(self, p_parent):
        self.root = p_parent

    def create_login_window(self):
        """ Creation of the login window """

        # Window handle
        window_login = tk.Toplevel(self.root)
        window_login.resizable(False, False)
        window_login.title("Portail de connexion")
        window_login_icon = tk.PhotoImage(file="img/lock.png")
        window_login.iconphoto(False, window_login_icon)
        login_window_width = settings['dimensions']['window_login_width']
        login_window_height = settings['dimensions']['window_login_height']
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cord = int((screen_width / 2) - (login_window_width / 2))
        y_cord = int((screen_height / 2) - (login_window_height / 2))
        window_login.geometry("{}x{}+{}+{}".format(login_window_width, login_window_height, x_cord, y_cord))
        window_login.columnconfigure(0, weight=1)

        # Title of the login window
        bg_identification = settings['colors']['bg_identification']
        label_login_title = tk.Label(window_login, text="Identification", bg=bg_identification, fg="white")
        label_login_title.grid(row=0, sticky='new', pady=(0, 10))
        font_login_title = settings['font']['font_login_title']
        font_size_login_title = settings['font_size']['font_size_login_title']
        label_login_title.config(font=(font_login_title, font_size_login_title))

        # Username label
        label_username = tk.Label(window_login, text="Username")
        label_username.grid(row=1, sticky='new', pady=(0, 5))
        font_login_username = settings['font']['font_login_username']
        font_size_login_username = settings['font_size']['font_size_login_username']
        label_username.config(font=(font_login_username, font_size_login_username))

        # Username entry
        var_username = tk.StringVar(value='')
        font_login_entry_username = settings['font']['font_login_entry_username']
        font_size_login_entry_username = settings['font_size']['font_size_login_entry_username']
        entry_username = tk.Entry(window_login, bg="white", width=30, textvariable=var_username, font=(font_login_entry_username, font_size_login_entry_username))
        entry_username.grid(row=2, pady=(0, 20))

        # Password label
        label_password = tk.Label(window_login, text="Password")
        label_password.grid(row=3, sticky='new', pady=(0, 5))
        font_login_password = settings['font']['font_login_password']
        font_size_login_password = settings['font_size']['font_size_login_password']
        label_password.config(font=(font_login_password, font_size_login_password))

        # Password entry
        var_password = tk.StringVar(value='')
        font_login_entry_password = settings['font']['font_login_entry_password']
        font_size_login_entry_password = settings['font_size']['font_size_login_entry_password']
        entry_password = tk.Entry(window_login, show="*", width=30, textvariable=var_password, font=(font_login_entry_password, font_size_login_entry_password))
        entry_password.grid(row=4, pady=(0, 20))

        # Validate button
        button_validate = tk.Button(window_login, text="Valider", width=10, command=None)
        button_validate.grid(row=5, column=0, pady=(0, 20))