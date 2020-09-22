import tkinter as tk
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)


class FrameContent:
    """ Right frame of the window"""

    def __init__(self, p_parent, p_title, p_background):
        window_width = settings['dimensions']['window_width']
        window_height = settings['dimensions']['window_height']
        top_menu_height = settings['dimensions']['top_menu_height']
        left_menu_width = settings['dimensions']['left_menu_width']
        self.frame_width = window_width - left_menu_width
        self.frame_height = window_height - top_menu_height
        self.frame = tk.Frame(p_parent, bg=p_background, width=self.frame_width, height=self.frame_height)
        self.frame.grid_propagate(False)
        self.frame.grid(row=1, column=0)
        self.frame.columnconfigure(0, weight=1)

        # Label page title
        self.label_page_title = tk.Label(self.frame, bg=p_background, text=p_title)
        self.label_page_title.grid(row=0, column=0, sticky='nw', padx=10, pady=(5, 5))
        font_right_frame_title = settings['font']['font_right_frame_title']
        font_size_right_frame_title = settings['font_size']['font_size_right_frame_title']
        self.label_page_title.config(font=(font_right_frame_title, font_size_right_frame_title))


class ButtonLeftText:
    """ Text buttons located in the left of the window """

    def __init__(self, p_text, p_row, p_parent, p_bg, p_pady, p_command):
        self.init_bg = p_bg
        self.button = tk.Button(p_parent, text=p_text, bg=p_bg, fg="white", activebackground="green", borderwidth=1, command=p_command)
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
        self.button.grid(row=0, column=p_col, sticky="e",  pady=(5, 5), padx=(10, 10), ipadx=15)
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