import tkinter as tk
from tkinter import messagebox  # display pop-up boxes
import pystray  # used to create taskbar tray icon
from pystray import MenuItem as item
from PIL import Image, ImageTk  # used to generate accepted image format
from threading import Thread


def popUp(title, txt, type):  # function creates pop-up
    root = tk.Tk()
    root.withdraw()
    if type == 1:  # creates info/yesno pop-up depending on passed arguments
        messagebox.showinfo(title, txt)
    else:
        return messagebox.askyesno(title, txt)


def warning(title, txt):  # displays errorbox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, txt)


def quitProgram(root, icon=False, min=False):  # quits program (also stops icon if used to quit)
    if min:
        icon.stop()
    root.quit()
    root.destroy()



def showProgram(root, icon=False, item=None):
    icon.stop()
    root.after(0, root.deiconify)  # displays the root window when show is selected


def minToTray(root):
    root.withdraw()
    image = Image.open("data/images/winIcon.ico")  # opens image in acceptable format
    menu = (item("Quit", lambda: quitProgram(root, icon, min=True)), item("Show", lambda: showProgram(root, icon)))  # creates items in menu for show and quit functions
    icon = pystray.Icon("Lightscreen", image, "Lightscreen", menu)  # creates systray icon with image, icons and titlename
    icon.run()  # runs the icon