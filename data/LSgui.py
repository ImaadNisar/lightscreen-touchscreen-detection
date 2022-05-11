import tkinter as tk
#from LSmain import selectPoints

def mainWin():
    root = tk.Tk()
    root.geometry("1280x720")
    root.title("Lightscreen")

    root.mainloop()

def validateSettings():

    settings = ("theme", "wsize", "hsize")
    default = "theme: light\nwsize: 1280\nhsize: 720"
    valid = True

    with open("LS/data/config.txt", "r") as f:
        contents = f.readlines()
        cur_settings = [entry.split(":")[0] in settings for entry in contents]
        if len(cur_settings) != len(settings) or False in cur_settings:
            valid = False
    if not valid:
       with open("LS/data/config.txt", "w") as f:
           f.write(default)
    mainWin()



validateSettings()
