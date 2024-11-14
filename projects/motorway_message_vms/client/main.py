import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from api import *

client = SmartMotorwayClient("https://jdps73nn-5000.uks1.devtunnels.ms/message_boards")


# Update a message board

# response = client.update_message_board("M1_J2_A", speed_limit=60, lane_statuses={"3": False}, message="Exit closed")
# print(response)

# response = client.reset_message_board("M1_J2_A")
# print(response)

# response = client.update_message_board("M1_J2_A", speed_limit=-1, lane_statuses={"3": True}, message="")
# print(response)

# Sample data
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Create the main window
root = tk.Tk()
root.title("X-Y Position Graph")

# Create a figure
fig = Figure(figsize=(5, 4), dpi=100)
plot = fig.add_subplot(111)
plot.plot(x, y, marker='o')

# Create a canvas to display the plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a toolbar for the plot
toolbar = ttk.Frame(root)
toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Start the Tkinter main loop
root.mainloop()