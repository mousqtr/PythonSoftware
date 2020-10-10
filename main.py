import tkinter as tk
import json
from functools import partial

from gui import MainWindow, LeftFrame, RightFrame, TopFrame, ButtonLeftText, ButtonTopText, MiddleFrame
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
left_menu_height_initial = window_height_initial - top_menu_height_initial
frame_right_width_initial = window_width_initial - left_menu_width_initial
frame_right_height_initial = window_height_initial


bg_connect = settings['colors']['bg_connect']
bg_left_menu = settings['colors']['bg_left_menu']

# Root initialization
main_window = MainWindow()
root = main_window.frame

# The window is splitted into 2 frames
img_pages = tk.PhotoImage(file="img/pages2.png")
img_widgets = tk.PhotoImage(file="img/widgets2.png")
img_settings = tk.PhotoImage(file="img/setting2.png")

img_pages2 = tk.PhotoImage(file="img/pages3.png")
img_widgets2 = tk.PhotoImage(file="img/widgets3.png")
img_settings2 = tk.PhotoImage(file="img/setting3.png")

img_summary = tk.PhotoImage(file="img/widgets/summary.png")
img_graph = tk.PhotoImage(file="img/widgets/graph.png")
img_donut_chart = tk.PhotoImage(file="img/widgets/donut_chart.png")
img_histogram = tk.PhotoImage(file="img/widgets/histogram.png")
img_table = tk.PhotoImage(file="img/widgets/table.png")
img_histogram_graph = tk.PhotoImage(file="img/widgets/histogram_graph.png")
img_map = tk.PhotoImage(file="img/widgets/map.png")

list_img_1 = [img_pages, img_widgets, img_settings]
list_img_2 = [img_pages2, img_widgets2, img_settings2]
list_img_widgets = [img_summary, img_donut_chart, img_table, img_map, img_graph, img_histogram, img_histogram_graph]
list_title_widgets = ["Sommaire", "Graphique\nen anneau", "Table", "Carte", "Graphique", "Histogramme", "Graphe\nHistogramme"]

img_logo = tk.PhotoImage(file="img/logo.png")
img_logo = img_logo.zoom(4)
img_logo = img_logo.subsample(32)

frame_top = TopFrame(root, img_logo)
frame_middle = MiddleFrame(root)

frame_left = LeftFrame(frame_middle, frame_top, list_img_1, list_img_2)
frame_right = RightFrame(frame_middle, frame_left)


# Initialization of the buttons
def edit_widgets(p_right_frame, p_list_img_widgets, p_list_title_widgets):
    if len(frame_right.frames_content) > 0:
        frame_content_id = p_right_frame.current_frame
        frame_content = p_right_frame.frames_content[frame_content_id]
        frame_content.edit_widgets(p_list_img_widgets, p_list_title_widgets)


button_configure_widgets = ButtonTopText("Configurer les widgets", 1, frame_top.third_top_frame, bg_connect,
                                         partial(edit_widgets, frame_right, list_img_widgets, list_title_widgets))

window_login = Login(root)
button_login = ButtonTopText("Se connecter", 2, frame_top.third_top_frame, bg_connect, window_login.create_login_window)



def edit_page():
    if len(frame_right.frames_content) > 0:
        EditPage(root, frame_left, frame_right, frame_top)
    # print(frame_left.widgets_frames)



button_edit_page = ButtonTopText("Editer la page", 0, frame_top.third_top_frame, bg_connect, edit_page)


def create_page():
    nb_buttons_max = 11
    if len(frame_left.buttons_left) < nb_buttons_max:
        NewPage(root, frame_left, frame_right, frame_top)


button_create_page = ButtonLeftText(" + ", 20, frame_left.moving_frames[0], "white", create_page)


# Detect the window resize
def window_resize(event):
    width = main_window.frame.winfo_width()
    height = main_window.frame.winfo_height()

    if width != main_window.width or height != main_window.height:
        main_window.width = width
        main_window.height = height

    """ Resize the window and intern elements """
    frame_top.resize()
    frame_middle.resize()




root.bind("<Configure>", window_resize)

# Launch the GUI
root.mainloop()





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