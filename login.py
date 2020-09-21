import tkinter as tk

class Login:
    def __init__(self, p_parent):
        

    def create_login_window():
        """ Creation of the login window """

        # Window handle
        login_window = tk.Toplevel(root)
        login_window_width = 500
        login_window_height = 250
        x_cord = int((screen_width / 2) - (login_window_width / 2))
        y_cord = int((screen_height / 2) - (login_window_height / 2))
        login_window.geometry("{}x{}+{}+{}".format(login_window_width, login_window_height, x_cord, y_cord))
        login_window.columnconfigure(0, weight=1)

        # Title of the login window
        label_login_title = tk.Label(login_window, text="Identification", bg=bg_identification, fg="white")
        label_login_title.grid(row=0, sticky='new', pady=(0, 20))
        label_login_title.config(font=menu_font)

        # Username label
        label_username = tk.Label(login_window, text="Username")
        label_username.grid(row=1, sticky='new', pady=(0, 10))
        label_username.config(font=username_font)

        # Username entry
        var_username = tk.StringVar(value='')
        entry_username = tk.Entry(login_window, bg="white", width=30, textvariable=var_username, font=("Consolas", 15))
        entry_username.grid(row=2, pady=(0, 20))

        # Password label
        label_password = tk.Label(login_window, text="Password")
        label_password.grid(row=3, sticky='new', pady=(0, 10))
        label_password.config(font=username_font)

        # Password entry
        var_password = tk.StringVar(value='')
        entry_password = tk.Entry(login_window, bg="white", width=30, textvariable=var_password, font=("Consolas", 15))
        entry_password.grid(row=4, pady=(0, 20))