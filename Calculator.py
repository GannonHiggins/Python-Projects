from tkinter import *


expr = "" #global expression variable

def button_click(key):
    global expr
    expr += str(key)
    display.set(expr)

def equal():
    global expr
    try:
        resault = str(eval(expr))
        display.set(resault)
        expr = ""
    except:
        display.set("Error")
        expr = ""

def clear():
    global expr
    expr = ""
    display.set("")

if __name__ == "__main__":
    root = Tk()
    root.title("Calculator")
    root.geometry("600x700")


    root.mainloop()
