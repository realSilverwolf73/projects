from tkinter import Tk, Button, Listbox, Scrollbar, Text, PhotoImage, Label
import math

inv = True
sin = math.sin
cos = math.cos
tan = math.tan
fact = math.factorial
log = math.log10
ln = math.log
pi = math.pi
e = math.exp(1)
sqrt = math.sqrt
prcnt = 1/100
arcsin = math.asin
arccos = math.acos
arctan = math.atan

class GUI:
    def __init__(self):
        self.simple = True
        self.invas = True
        self.root = Tk()
        self.root.title("Calculator for smart people (in radians)")
        self.root.geometry("200x375")
        image_path = "E:\CalculatorOfShame\Ryo Yamada _ Bocchi The Rock! (2).png"
        self.background_image = PhotoImage(file=image_path)

        # Create a Label widget to hold the background image
        self.background_label = Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Set the background color to match the image
        self.background_label.configure(bg="#74A12E")

        # Create and place Listbox at the top
        self.listbox = Listbox(self.root, width=30, height=2)
        self.listbox.grid(row=0, column=0, columnspan=4, pady=10)

        # Create number buttons below the Listbox with an awesome loop
        self.create_buttons()

    def create_buttons(self):
        # Clear existing buttons
        for widget in self.root.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()

        # Create and place number buttons with an awesome loop
        if self.simple:
            buttons_text = ["(", ") ", "prcnt", "DEL", "1", "2", "3", "/", "4", "5", "6", "*", "7", "8", "9", "-", "0", ".", "=", "+", "Fx"]
        else:
            if self.invas:
                buttons_text = ["sin", "cos", "tan", "inv", "log", "ln", "e", "pi", "**", "sqrt", "fact", "ANS", "Fx"]
            else:
                buttons_text = ["arcsin", "arccos", "arctan", "inv", "10**", "e**", "e", "pi", "**(1/", "**2", "fact", "ANS", "Fx"]
        row, col = 1, 0
        for button_text in buttons_text:
            button = Button(self.root, text=button_text, width=4, height=2, command=lambda text=button_text: self.inputButton(text))
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def inputButton(self, button_text):
        try:
            
            match button_text:
                case "Fx":
                    self.simple = not self.simple
                    self.create_buttons()  # Update buttons
                case '=':
                    threshold = 1e-15
                    expression = self.listbox.get(0)
                    result = eval(expression) 
                    if abs(result) < threshold: 
                        self.listbox.insert(1, f"{float(0)}") 
                    else: 
                        self.listbox.insert(1, f"{float(result)}")
                case "DEL":
                    equation = self.listbox.get(0)
                    equation = equation[:-1]
                    self.listbox.delete(0, "end")
                    self.listbox.insert(0, equation)
                case "ANS":
                    answer = self.listbox.get(1)
                    self.listbox.delete(0, "end")
                    self.listbox.insert(0, answer)
                case "inv":
                    self.invas = not self.invas
                    self.create_buttons()
                case default:
                    equation = self.listbox.get(0)
                    equation = equation + button_text
                    self.listbox.delete(0, "end")
                    self.listbox.insert(0, equation)
                    
        except SyntaxError:
            self.listbox.delete(0, "end")
            self.listbox.insert(0, "SyntaxError")

if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()