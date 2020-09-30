import tkinter as tk
import json
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DonutChart:
    """ Widget that shows some label and data """

    def __init__(self, p_parent, p_widget_group, p_row):
        """
        Initialization of the summary widget that shows some label and data

        :param p_parent: Page that will contain this summary widget
        :param p_row: Row of the page where the widget will be placed
        :param p_widget_group: Group containing this widget
        """

        # Saving the parameters to use them in each function
        self.parent = p_parent
        self.row = p_row
        self.widget_group = p_widget_group

        # Add this widget to p_parent widgets
        self.widget_group.widgets.append(self)
        self.type = "Summary"

        # Properties of the widget-
        frame_height = 400
        frame_width = 780
        frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        frame.grid_propagate(False)
        frame.config(highlightbackground="grey")
        frame.grid(row=self.row, column=0, pady=(5, 5))
        frame.update_idletasks()  # to display good dimensions with .winfo_width()
        frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Title of the page
        title = tk.Label(frame, text="Portion", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        title.grid(row=0, column=0, columnspan=5, sticky="nwe", ipadx=10, ipady=5)
        title.config(font=("Calibri bold", 12))

        fig = matplotlib.figure.Figure(figsize=(3, 3))
        gs = fig.add_gridspec(1, 2)
        ax = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax.pie([20, 30, 50])
        ax2.pie([20, 30, 50])
        ax.legend(["20", "30", "50"], loc='upper right', title='La legende')
        ax2.legend(["20", "30", "50"], loc='upper right', title='La legende')

        # Create the circle for the donut
        circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
        ax.add_artist(circle)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nwe", columnspan=5)

        canvas.draw()

