import tkinter as tk
import json

from gui import MainWindow, LeftFrame, RightFrame, TopFrame, ButtonLeftText, ButtonTopText
from new_page import NewPage
from edit_page import EditPage
from login import Login
from widgets.summary.summary import Summary
from widgets.filters.filters import Filters
from widgets.modifiers.modifiers import Modifiers
from widgets.table.table import Table
from widgets.donut_chart.donut_chart import DonutChart

# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Custom settings
window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
top_menu_height_initial = settings['dimensions']['top_menu_height']
left_menu_width_initial = settings['dimensions']['left_menu_width']
left_menu_height_initial = window_height_initial
frame_right_width_initial = window_width_initial - left_menu_width_initial
frame_right_height_initial = window_height_initial

bg_connect = settings['colors']['bg_connect']
bg_left_menu = settings['colors']['bg_left_menu']

# Root initialization
main_window = MainWindow()
root = main_window.frame

# The window is splitted into 2 frames
frame_left = LeftFrame(root)
frame_right = RightFrame(root)
frame_top = TopFrame(frame_right)

# Initialization of the top menu buttons (include in frame_top_menu)


button_configure_widgets = ButtonTopText("Configurer les widgets", 1, frame_top.second_top_frame, bg_connect, None)
button_settings = ButtonLeftText("Paramètres", 0, frame_left.third_left_frame, bg_connect, None)

window_login = Login(root)
button_login = ButtonTopText("Se connecter", 2, frame_top.second_top_frame, bg_connect, window_login.create_login_window)


# # Widget group
# Widget_group_1 = WidgetGroup(1)
# Widget_group_2 = WidgetGroup(2)
#
# # Widgets
# Widget_summary = Summary(Frame_dashboard, Widget_group_1, 1)
# Widget_donut_chart = DonutChart(Frame_dashboard, Widget_group_1, 2)
# Widget_research = Filters(Frame_research, Widget_group_1, 1)
# Widget_table_1 = Table(Frame_research, Widget_group_1, 2)
# Widget_modifier = Modifiers(Frame_modification, Widget_group_1, 1)
# Widget_table_2 = Table(Frame_modification, Widget_group_2, 2)


def edit_page():
    # print(frame_right.frames_content)
    # print(frame_right.current_frame)
    if len(frame_right.frames_content) > 0:
        EditPage(root, frame_left, frame_right, frame_top)


button_edit_page = ButtonTopText("Editer la page", 0, frame_top.second_top_frame, bg_connect, edit_page)


def create_page():
    nb_buttons_max = 8
    if len(frame_left.buttons_left) < nb_buttons_max:
        NewPage(root, frame_left, frame_right, frame_top)


button_create_page = ButtonLeftText(" + ", 20, frame_left.second_left_frame, bg_left_menu, create_page)


# Detect the window resize
def window_resize(event):
    width = main_window.frame.winfo_width()
    height = main_window.frame.winfo_height()

    if width != main_window.width or height != main_window.height:
        main_window.width = width
        main_window.height = height

    """ Resize the window and intern elements """
    offset_width = root.winfo_width() - window_width_initial
    frame_top.frame["width"] = frame_right_width_initial + offset_width
    frame_left.frame["height"] = root.winfo_height()
    frame_right.resize()
    frame_left.resize()


root.bind("<Configure>", window_resize)

# Launch the GUI
root.mainloop()
