import tkinter as tk
from functools import partial
from tkinter import messagebox

from gui import MainWindow, Menu, LeftFrame, RightFrame, ButtonLeftText, PageInitial
from pages.new_page import NewPage
from pages.edit_page import EditPage
from tables.new_table import NewTable
from login import Login

# Main window initialization
main_window = MainWindow()




# Images used in the left static frame (color 1/2)
img_pages = tk.PhotoImage(file="img/pages4.png")
img_widgets = tk.PhotoImage(file="img/widgets4.png")
img_settings = tk.PhotoImage(file="img/setting4.png")
img_tables = tk.PhotoImage(file="img/table4.png")
list_img_1 = [img_pages, img_widgets, img_settings, img_tables]

# Images used in the left static frame (color 2/2)
img_pages2 = tk.PhotoImage(file="img/pages5.png")
img_widgets2 = tk.PhotoImage(file="img/widgets5.png")
img_settings2 = tk.PhotoImage(file="img/setting5.png")
img_tables2 = tk.PhotoImage(file="img/table5.png")
list_img_2 = [img_pages2, img_widgets2, img_settings2, img_tables2]

# Images used as widgets icons
img_image = tk.PhotoImage(file="img/widgets/image.png")
img_summary = tk.PhotoImage(file="img/widgets/summary.png")
img_graph = tk.PhotoImage(file="img/widgets/graph.png")
img_donut_chart = tk.PhotoImage(file="img/widgets/donut_chart.png")
img_histogram = tk.PhotoImage(file="img/widgets/histogram.png")
img_table = tk.PhotoImage(file="img/widgets/table.png")
img_histogram_graph = tk.PhotoImage(file="img/widgets/histogram_graph.png")
img_map = tk.PhotoImage(file="img/widgets/map.png")
list_title_widgets = ["Image", "Sommaire", "Table", "Graphique\nen anneau", "Carte", "Graphique", "Histogramme", "Graphe\nHistogramme"]
list_img_widgets = [img_image, img_summary, img_table, img_donut_chart,  img_map, img_graph, img_histogram, img_histogram_graph]
list_img_widgets2 = []
for img in list_img_widgets:
    img = img.zoom(15)
    img = img.subsample(30)
    list_img_widgets2.append(img)

# Images used in configuration mode
img_add = tk.PhotoImage(file="img/add.png")
img_delete = tk.PhotoImage(file="img/minus.png")
img_empty = tk.PhotoImage(file="img/empty.png")
list_buttons_widget = [img_add, img_delete, img_empty]

# List containing all widget images
list_widgets = [list_img_widgets, list_title_widgets, list_buttons_widget, list_img_widgets2]

# Images used during the addition of a table
img_csv = tk.PhotoImage(file="img/extensions/csv.png")
img_xls = tk.PhotoImage(file="img/extensions/xls.png")
img_sql = tk.PhotoImage(file="img/extensions/sql.png")
img_txt = tk.PhotoImage(file="img/extensions/txt.png")
img_docx = tk.PhotoImage(file="img/extensions/docx.png")
list_extensions_icon = [img_csv, img_xls, img_sql, img_txt, img_docx]
list_extensions_icon2 = []
for img in list_extensions_icon:
    img = img.zoom(30)
    img = img.subsample(30)
    list_extensions_icon2.append(img)



# Logo of the company
img_logo = tk.PhotoImage(file="img/logo.png")

# Creation of each frame of the window
frame_left = LeftFrame(main_window, list_img_1, list_img_2)
frame_right = RightFrame(main_window, frame_left)

page_initial = PageInitial(frame_right)


menu = Menu(main_window, list_widgets)

# Initialization of the login button
window_login = Login(main_window.frame)
# button_login = ButtonTopText("Se connecter", 2, frame_top.third_top_frame, window_login.create_login_window)


# Initialization of the edit button
# def edit_page():
#     if len(frame_right.frames_content) > 0:
#         EditPage(main_window.frame, frame_left, frame_right, frame_top)

    # print(frame_left.widgets_frames)


# button_edit_page = ButtonTopText("Editer la page", 0, frame_top.third_top_frame, edit_page)


# Initialization of the create page button
def add_page():
    """ Function called when the user clicks on the add_page button """
    print("New Page")
    nb_buttons_max = 11
    if len(frame_left.buttons_page) < nb_buttons_max:
        NewPage(main_window.frame, frame_left, frame_right)


button_add_page = ButtonLeftText(" + ", 20, frame_left.moving_frames[0], "white", add_page)


# Initialization of the add_table button
def add_table():
    print("New Table")
    nb_tables_max = 11
    if len(frame_left.buttons_table) < nb_tables_max:
        NewTable(main_window.frame, frame_left, frame_right, list_extensions_icon2)


button_add_table = ButtonLeftText(" + ", 20, frame_left.moving_frames[3], "white", add_table)


# Stop the window resize
def stop_window_resize():
    """ Function called to stop the resized of the window """

    main_window.resized = False


# When the user closes the window
def on_closing():
    """ Function called when the user try to close the window """

    if messagebox.askokcancel("Fermer", "Voulez-vous vraiment quitter ?"):
        stop_window_resize()
        main_window.frame.destroy()


# Bind the on_closing function to the main_window protocol
main_window.frame.protocol("WM_DELETE_WINDOW", on_closing)

# Launch the GUI
main_window.frame.mainloop()





# # Widget group
# Widget_group_1 = WidgetGroup(1)
# Widget_group_2 = WidgetGroup(2)

# # Widgets
# Widget_summary = Summary(Frame_dashboard, Widget_group_1, 1)
# Widget_donut_chart = DonutChart(Frame_dashboard, Widget_group_1, 2)
# Widget_research = Filters(Frame_research, Widget_group_1, 1)
# Widget_table_1 = Table(Frame_research, Widget_group_1, 2)
# Widget_modifier = Modifiers(Frame_modification, Widget_group_1, 1)
# Widget_table_2 = Table(Frame_modification, Widget_group_2, 2)