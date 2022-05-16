import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk


def popUp(title, txt, type):
    root = tk.Tk()
    root.withdraw()
    if type == 1: 
        messagebox.showinfo(title, txt)
    else:
        return messagebox.askyesno(title, txt)


def warning(title, txt):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, txt)


def quitProgram(root, icon=False, min=False):
    if min:
        icon.stop()
    root.quit()
    root.destroy()



def showProgram(root, icon=False, item=None):
    icon.stop()
    root.after(0, root.deiconify)


def minToTray(root):
    root.withdraw()
    image = Image.open("data/images/winIcon.ico")
    menu = (item("Quit", lambda: quitProgram(root, icon, min=True)), item("Show", lambda: showProgram(root, icon)))
    icon = pystray.Icon("Lightscreen", image, "Lightscreen", menu)
    icon.run()