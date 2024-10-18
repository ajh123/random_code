import tkinter as tk

# Create a window called "Calculator 2"
root = tk.Tk()
root.title("Calculator 2")

# Create the layout of our buttons
buttons = [
    ["1", "2", "3", "+"],
    ["4", "5", "6", "-"],
    ["7", "8", "9", "*"],
    ["C", "0", "=", "/"]
]


# Create our own App class to better organise our code (we don't need to use a class, but we will end up with a mess)
class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.output = tk.StringVar() # Create a StringVar to hold the output of our calculator
        tk.Label(self, textvariable=self.output).grid(row=0, column=0, columnspan=5) # Create a label to display the output
        
        # Iterate over each button row
        for x in range(0, len(buttons)):
            row = buttons[x] # Get each row
            for y in range(0, len(row)): # Iterate over each row column
                symbol = row[y] # Get the current symbol inside the column
                if symbol == None: # If this symbol is None, then skip to the next one
                    continue
                # If the symbol is not None, then create a buttton displaying the symbol
                # and bind the button to the perform function, whilst making sure the current symbol is passed
                tk.Button(self, text=symbol, command=lambda symbol=symbol: self.perform(symbol)).grid(row=x+1, column=y+1)
        self.pack()

    # The perform function is responsible for ensuring the output is updated corectlly and doing the actual maths
    def perform(self, symbol):
        # Retrive the current output
        operation = self.output.get()
        # Check if the clear button is pressed
        if symbol == "C":
            self.output.set("") # if so, clear the output
            return # then finish the function
        if symbol != "=": # if the button is not an equals then update the ouput containig the button's symbol
            self.output.set(f"{operation}{symbol}")
        # if the symbol is an equals
        if symbol == "=":
            # then perform the maths by using the Python eval function
            result = eval(operation)
            # then set the output to the result
            self.output.set(result)

# Firstly, start our app
App(root)
tk.mainloop()