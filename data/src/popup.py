import tkinter as tk
from tkinter import messagebox

"""def popUp(title, txt):
    root = tk.Tk()
    root.title(title)
    root.iconbitmap('icon.ico')

    message = tk.Label(root, text=txt, pady=20, bg="#ffffff")
    message.grid(row=0, column=0)

    frame = tk.Frame(root, bg='#f0f0f0')
    frame.columnconfigure(0, weight=1)

    close = tk.Button(frame, text="OK", padx=20, command=root.destroy, borderwidth=3)
    close.grid(row=0, column=0, pady=7, padx=10, sticky='e')
    frame.grid(row=1, column=0, ipadx=120)

    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.configure(bg="#ffffff")
    
    root.mainloop()
"""

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