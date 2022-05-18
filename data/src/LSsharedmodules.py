import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from platform import system
if system() == "Windows":
    import pystray
    from pystray import MenuItem as item



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


def quitProgramIcon(root, icon=False, min=False):
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
    menu = (item("Quit", lambda: quitProgramIcon(root, icon, min=True)), item("Show", lambda: showProgram(root, icon)))
    icon = pystray.Icon("Lightscreen", image, "Lightscreen", menu)
    icon.run()

def quit(root):
    root.quit()
    root.destroy()
