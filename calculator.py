import tkinter
import threading
import math

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Scientific Calculator")
        self.mode = "radians"  # Initial mode
        
        # Configure colors
        self.bg_color = "#ffc1cc"
        self.display_bg_color = "#ffd1dc"  
        self.button_bg_color = "#de5d83"  
        self.button_fg_color = "#ffffff"
        self.label_fg_color = "#000000"  

        
        # Entry widget to display input and output
        self.display = tkinter.Entry(master, width=30, font=("Helvetica", 14), bd=10, insertwidth=4, bg=self.display_bg_color)
        self.display.grid(row=0, column=0, columnspan=8)
        
        # Label to display current mode
        self.mode_label = tkinter.Label(master, text="Mode: " + self.mode, font=("Helvetica", 10), fg=self.label_fg_color, bg=self.bg_color)
        self.mode_label.grid(row=5, column=0, columnspan=8)
        
        # Buttons for numbers and operations
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("x", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("sin", 1, 4), ("cos", 2, 4), ("tan", 3, 4), ("(", 1, 5),
            (")", 2, 5), ("√", 3, 5), ("^", 1, 6), ("%", 2, 6),
            ("π", 4, 4), ("log", 4, 5), ("C", 3, 6), ("deg/rad", 4, 6)
        ]
        
        # Create number and operation buttons
        for (text, row, column) in buttons:
            btn = tkinter.Button(master, text=text, width=5, height=2, font=("Helvetica", 12), bg=self.button_bg_color, fg=self.button_fg_color, command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=column, padx=5, pady=5)
        
        # Set background color for the entire calculator
        master.configure(bg=self.bg_color)
        
    def on_button_click(self, value):
        # Handle button clicks
        if value == "=":
            self.calculate()
        elif value == "C":
            self.display.delete(0, tkinter.END)
        elif value == "deg/rad":
            self.toggle_mode()
        else:
            self.display.insert(tkinter.END, value)
    
    def toggle_mode(self):
        # Toggle between radians and degrees mode
        self.mode = "degrees" if self.mode == "radians" else "radians"
        self.mode_label.config(text="Mode: " + self.mode)
    
    def calculate(self):
        # Perform calculation in a separate thread
        expression = self.display.get()
        calc_thread = threading.Thread(target=self.evaluate_expression, args=(expression,))
        calc_thread.start()
    
    def evaluate_expression(self, expression):
        # Evaluate mathematical expression and update display
        try:
            if self.mode == "degrees":
                expression = self.convert_degrees_to_radians(expression)
                
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("√", "math.sqrt")
            expression = expression.replace("^", "**")
            expression = expression.replace("x", "*")
            expression = expression.replace("%", "/100")
            expression = expression.replace("π", "math.pi")
            expression = expression.replace("log", "math.log10")
            
            result = eval(expression)           
        
            
            self.display.delete(0, tkinter.END)
            self.display.insert(tkinter.END, str(result))
        except Exception as e:
            self.display.delete(0, tkinter.END)
            self.display.insert(tkinter.END, "Error")
    
    def convert_degrees_to_radians(self, expression):
        # Convert degrees to radians in trigonometric functions
        trig_functions = ["sin", "cos", "tan"]
        for trig_func in trig_functions:
            start_index = expression.find(trig_func + "(")
            while start_index != -1:
                end_index = self.find_matching_parenthesis(expression, start_index + len(trig_func) + 1)
                angle = expression[start_index + len(trig_func) + 1:end_index]
                angle_in_radians = str(math.radians(float(angle)))
                expression = expression[:start_index + len(trig_func) + 1] + angle_in_radians + expression[end_index:]
                start_index = expression.find(trig_func + "(", end_index)
        return expression
    
    def find_matching_parenthesis(self, expression, start_index):
        # Find the matching closing parenthesis for a given opening parenthesis
        count = 0
        for i in range(start_index, len(expression)):
            if expression[i] == "(":
                count += 1
            elif expression[i] == ")":
                count -= 1
                if count == 0:
                    return i
        return -1

root = tkinter.Tk()
calculator = ScientificCalculator(root)
root.mainloop()


