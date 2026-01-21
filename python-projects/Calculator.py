from tkinter import *


expr = "" #global expression variable
just_evaluated = False #global variable to track if we just calculated


def button_click(key):
    global expr, just_evaluated
    #if we calculated and the user presses a number, start fresh
    if just_evaluated and str(key).isdigit():
        expr = str(key)
        just_evaluated = False
    #if we calculated and the user presses an operator, add the operator to the expression
    elif just_evaluated and str(key) in ["+", "-", "*", "/"]:
        expr = display.get() + str(key)
        just_evaluated = False
    else:
        expr += str(key)
        just_evaluated = False
    display.set(expr)

def equal():
    global expr, just_evaluated


    try:
        resault = str(eval(expr))
        display.set(resault)
        expr = resault
        just_evaluated = True
    except:
        display.set("Error")
        expr = ""
        just_evaluated = False

def clear():
    global expr
    expr = ""
    just_evaluated = False
    display.set("")

if __name__ == "__main__":

    #Main Window
    root = Tk()
    root.title("Calculator")
    root.configure(bg = "dark gray")
    root.geometry("600x700")

    # Define font for buttons and display
    button_font = ("Arial", 20, "bold")
    display_font = ("Arial", 24, "bold")

    display = StringVar()
    entry = Entry(root, textvariable = display, font=display_font)
    entry.grid(columnspan=4, ipadx=70, ipady=20, padx=10, pady=10, sticky="ew")

    # Configure grid columns to have equal weight
    for i in range(4):
        root.grid_columnconfigure(i, weight=1, uniform="equal")
    
    # Configure grid rows to have equal weight
    for i in range(1, 6):
        root.grid_rowconfigure(i, weight=1, uniform="equal")

    #Number Buttons
    btn_1 = Button(root, text = "1", command = lambda: button_click(1), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_1.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
    btn_2 = Button(root, text = "2", command = lambda: button_click(2), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_2.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
    btn_3 = Button(root, text = "3", command = lambda: button_click(3), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_3.grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
    btn_4 = Button(root, text = "4", command = lambda: button_click(4), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_4.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
    btn_5 = Button(root, text = "5", command = lambda: button_click(5), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_5.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
    btn_6 = Button(root, text = "6", command = lambda: button_click(6), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_6.grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
    btn_7 = Button(root, text = "7", command = lambda: button_click(7), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_7.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
    btn_8 = Button(root, text = "8", command = lambda: button_click(8), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_8.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
    btn_9 = Button(root, text = "9", command = lambda: button_click(9), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_9.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
    btn_0 = Button(root, text = "0", command = lambda: button_click(0), bg = "light gray", padx=10, pady=10, font=button_font)
    btn_0.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)

    #Operator Buttons
    btn_plus = Button(root, text = "+", command = lambda: button_click("+"), bg = "light gray",padx=10, pady=10, font=button_font)
    btn_plus.grid(row=1,column=3, sticky="nsew", padx=2, pady=2)
    btn_minus = Button(root, text = "-", command = lambda: button_click("-"), bg = "light gray",padx=10, pady=10, font=button_font)
    btn_minus.grid(row=2,column=3, sticky="nsew", padx=2, pady=2)
    btn_multiply = Button(root, text = "*", command = lambda: button_click("*"), bg = "light gray",padx=10, pady=10, font=button_font)
    btn_multiply.grid(row=3,column=3, sticky="nsew", padx=2, pady=2)
    btn_divide = Button(root, text = "/", command = lambda: button_click("/"), bg = "light gray",padx=10, pady=10, font=button_font)
    btn_divide.grid(row=4,column=3, sticky="nsew", padx=2, pady=2)
    btn_equal = Button(root, text = "=", command = equal, bg = "light gray",padx=10, pady=10, font=button_font)
    btn_equal.grid(row=4,column=2, sticky="nsew", padx=2, pady=2)

    #Other Button
    btn_clear = Button(root, text = "Clear", command = clear, bg = "light gray",padx=10, pady=10, font=button_font)
    btn_clear.grid(row=4,column=0, sticky="nsew", padx=2, pady=2)
    btn_dot = Button(root, text = ".", command = lambda: button_click("."), bg = "light gray",padx=10, pady=10, font=button_font)
    btn_dot.grid(row=5,column=1, sticky="nsew", padx=2, pady=2)




    
    root.mainloop()
