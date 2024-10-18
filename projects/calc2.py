import tkinter as tk

root = tk.Tk()
root.title("Calculator 2")

buttons = [
    ["1", "2", "3", "+"],
    ["4", "5", "6", "-"],
    ["7", "8", "9", "*"],
    ["C", "0", "=", "/"]
]


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.var = tk.StringVar()
        tk.Label(self, textvariable=self.var).grid(row=0, column=0, columnspan=5)
        
        for x in range(0, len(buttons)):
            row = buttons[x]
            for y in range(0, len(row)):
                element = row[y]
                if element == None:
                    continue
                tk.Button(self, text=element, command=lambda element=element: self.perform(element)).grid(row=x+1, column=y+1)
        self.pack()

    def perform(self, element):
        operation = self.var.get()
        if element == "C":
            self.var.set("")
            return
        if element != "=":
            self.var.set(f"{operation}{element}")
        if element == "=":
            result = eval(operation)
            self.var.set(result)

App(root)
tk.mainloop()