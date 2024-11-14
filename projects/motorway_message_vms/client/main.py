import tkinter as tk
from tkinter import messagebox, simpledialog, Menu, Toplevel, Listbox, MULTIPLE
from typing import List
from requests.exceptions import RequestException
from api import *

class SmartMotorwayGUI:
    def __init__(self, root, client: SmartMotorwayClient):
        self.root = root
        self.client = client
        self.root.title("Smart Motorway Manager")

        # Menu bar for create and delete actions
        menu_bar = Menu(root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Create Message Board", command=self.create_message_board_popup)
        file_menu.add_command(label="Delete Message Board", command=self.delete_message_board_popup)
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)

        # Message board list
        tk.Label(root, text="Message Boards:").grid(row=0, column=0, columnspan=2)
        self.board_listbox = Listbox(root, selectmode=MULTIPLE, width=50, height=15)
        self.board_listbox.grid(row=1, column=0, columnspan=2)

        # Controls for selected boards
        tk.Button(root, text="Display Message", command=self.display_message).grid(row=2, column=0)
        tk.Button(root, text="Display End", command=self.display_end).grid(row=2, column=1)
        tk.Button(root, text="Update Speed Limit", command=self.update_speed_limit).grid(row=3, column=0)
        tk.Button(root, text="Set Lane Status", command=self.set_lane_status).grid(row=3, column=1)
        tk.Button(root, text="Refresh", command=self.refresh).grid(row=4, column=0, columnspan=1)
        tk.Button(root, text="Reset", command=self.reset).grid(row=4, column=1, columnspan=1)

        # Initial load of all message boards
        self.load_all_message_boards()

    def load_all_message_boards(self):
        """Loads all message boards and populates the listbox."""
        try:
            boards = self.client.get_all_message_boards()
            self.board_listbox.delete(0, tk.END)
            for board in boards:
                self.board_listbox.insert(tk.END, f"{board['location']} (x: {board['x']}, z: {board['z']})")
        except RequestException as e:
            messagebox.showerror("Error", f"Failed to load message boards: {e}")

    def get_selected_locations(self) -> List[str]:
        """Gets the locations of selected message boards."""
        selected_indices = self.board_listbox.curselection()
        selected_locations = [self.board_listbox.get(i).split()[0] for i in selected_indices]
        return selected_locations

    def create_message_board_popup(self):
        """Opens a popup to create a new message board."""
        popup = Toplevel(self.root)
        popup.title("Create Message Board")
        
        tk.Label(popup, text="Location:").grid(row=0, column=0)
        location_entry = tk.Entry(popup)
        location_entry.grid(row=0, column=1)
        
        tk.Label(popup, text="X Coordinate:").grid(row=1, column=0)
        x_entry = tk.Entry(popup)
        x_entry.grid(row=1, column=1)

        tk.Label(popup, text="Z Coordinate:").grid(row=2, column=0)
        z_entry = tk.Entry(popup)
        z_entry.grid(row=2, column=1)
        
        tk.Label(popup, text="Number of Lanes:").grid(row=3, column=0)
        lanes_entry = tk.Entry(popup)
        lanes_entry.grid(row=3, column=1)

        def create_message_board():
            location = location_entry.get()
            try:
                x = int(x_entry.get())
                z = int(z_entry.get())
                num_lanes = int(lanes_entry.get() or 3)
                self.client.create_message_board(location, x, z, num_lanes)
                messagebox.showinfo("Success", f"Message board created at {location}.")
                self.load_all_message_boards()
                popup.destroy()
            except (ValueError, RequestException) as e:
                messagebox.showerror("Error", f"Failed to create message board: {e}")

        tk.Button(popup, text="Create", command=create_message_board).grid(row=4, column=0, columnspan=2)

    def delete_message_board_popup(self):
        """Opens a popup to delete a message board."""
        selected_locations = self.get_selected_locations()
        if not selected_locations:
            messagebox.showerror("Error", "Select one or more message boards to delete.")
            return

        response = messagebox.askyesno("Confirm Deletion", f"Delete selected message boards: {', '.join(selected_locations)}?")
        if response:
            for location in selected_locations:
                try:
                    self.client.delete_message_board(location)
                except RequestException as e:
                    messagebox.showerror("Error", f"Failed to delete {location}: {e}")
            self.load_all_message_boards()

    def display_message(self):
        selected_locations = self.get_selected_locations()
        if not selected_locations:
            messagebox.showerror("Error", "Select one or more message boards to update.")
            return
        message = simpledialog.askstring("Message", "Enter message to display:")
        for location in selected_locations:
            board = MessageBoard(self.client, location)
            board.display_message(message)

    def display_end(self):
        selected_locations = self.get_selected_locations()
        if not selected_locations:
            messagebox.showerror("Error", "Select one or more message boards to update.")
            return
        for location in selected_locations:
            board = MessageBoard(self.client, location)
            board.display_end()

    def update_speed_limit(self):
        selected_locations = self.get_selected_locations()
        if not selected_locations:
            messagebox.showerror("Error", "Select one or more message boards to update.")
            return
        try:
            speed_limit = int(simpledialog.askstring("Speed Limit", "Enter new speed limit:"))
            for location in selected_locations:
                board = MessageBoard(self.client, location)
                board.speed_limit = speed_limit
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for speed limit.")

    def set_lane_status(self):
        selected_locations = self.get_selected_locations()
        if not selected_locations:
            messagebox.showerror("Error", "Select one or more message boards to update.")
            return
        lane = simpledialog.askstring("Lane", "Enter lane number:")
        status = messagebox.askyesno("Lane Status", "Set lane status to open?")
        for location in selected_locations:
            board = MessageBoard(self.client, location)
            board.set_lane_status(lane, status)

    def refresh(self):
        self.load_all_message_boards()

    def reset(self):
        selected_locations = self.get_selected_locations()
        if not selected_locations:
            messagebox.showerror("Error", "Select one or more message boards to update.")
            return
        for location in selected_locations:
            self.client.reset_message_board(location)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    client = SmartMotorwayClient("https://6rnxhbsz-5000.uks1.devtunnels.ms/message_boards")  # Replace with your API's base URL
    app = SmartMotorwayGUI(root, client)
    root.mainloop()
