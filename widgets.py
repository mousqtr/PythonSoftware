import tkinter as tk
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)

class Summary:
    def __init__(self, p_parent, p_row):
        frame_height = 200
        frame_width = 780
        frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        frame.grid_propagate(False)
        frame.config(highlightbackground="grey")
        frame.grid(row=p_row, column=0, pady=(5, 5))
        frame.update_idletasks()  # to display good dimensions with .winfo_width()
        frame.columnconfigure((0, 1, 2, 3), weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure((1, 2), weight=4)



        self.title = tk.Label(frame,text="Summary", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, columnspan=5, sticky="nwe", ipadx=10, ipady=5)
        font_top_menu = settings['font']['font_top_menu']
        font_size_top_menu = settings['font_size']['font_size_top_menu']
        self.title.config(font=(font_top_menu, 12))


        # print(frame.winfo_width())
        # print(frame.winfo_height())

        pixelVirtual = tk.PhotoImage(width=1, height=1)  # to have pixel measure of button size

        self.nb_column = 4
        self.nb_row = 2
        self.buttons = [[tk.Button() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.button_width = int(frame_width/self.nb_column)
        self.button_height = int(frame_height/self.nb_row)
        for i in range(0, self.nb_row):
            for j in range(0, self.nb_column):
                self.buttons[i][j] = tk.Label(frame, image=pixelVirtual, width=self.button_width, height=self.button_height, text="ok", compound="c")
                # self.buttons[i][j].grid_propagate(False)
                self.buttons[i][j].grid(row=i+1, column=j,  padx=(10,10), pady=(10,10))

