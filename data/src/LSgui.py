import tkinter as tk
from LSmain import selectPoints
from PIL import Image, ImageTk
import webbrowser
from platform import system

def mainWin():
    config = validateSettings()
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: quitProgram(root))
    root.geometry("1280x720")
    root.title("Lightscreen")

    icon = "data/images/winIcon.ico"
    if system() == "Linux":
        icon = "@data/images/linuxIcon.xbm"
    root.iconbitmap(icon)
    root.minsize(840, 400)
    
    theme = ''.join([set.split(":")[1] for set in config if set.split(":")[0] == "theme"])[:-1].strip()
    color = {
        "p": "#bae4e2",
        "s": "#e5f4f3",
        "t": "#89abad",
        "c": "#4f4f4e"
        }
    imglocation = "data/images/spanlight.png"

    if theme == "dark":
        color["p"] = "#121212"
        color["s"] = "#333333"
        color["t"] = "#adadad"
        color["c"] = "#FFFFFF"
        imglocation = "data/images/spandark.png"
    

    spanimg = Image.open(imglocation)
    resized = spanimg.resize((360, 72), Image.ANTIALIAS)
    resizedspan = ImageTk.PhotoImage(resized)

    sidebar = tk.Frame(root, bg = color["p"])
    main = tk.Frame(root, bg=color["s"])
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    main.rowconfigure(0, weight=1)

    """root.columnconfigure(0, weight=1)
    root.columnconfigure()"""

    btnfont = ("Roboto Mono Light", 15, "bold")

    span = tk.Label(sidebar, image=resizedspan, borderwidth=0)
    howtouse = tk.Button(sidebar, text=">> HOW TO USE", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=lambda: webbrowser.open("https://www.google.com"), highlightthickness=0)
    calibration = tk.Button(sidebar, text=">> CALIBRATION", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=selectPoints, highlightthickness=0)
    settings = tk.Button(sidebar, text=">> SETTINGS", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, cursor="hand2", command=lambda: viewSettings(main, color), highlightthickness=0)
    bottomleft = tk.Frame(root, bg=color["p"])
    bottomright= tk.Frame(root, bg=color["s"])
    bottomtext = tk.Button(bottomleft, text="GitHub: @ImaadNisar", font = ("Roboto Mono Light", 7), bg=color["p"], fg=color["t"], highlightthickness=0, borderwidth=0, activeforeground=color["c"], activebackground=color["p"], cursor="hand2", command=lambda: webbrowser.open("https://github.com/ImaadNisar"))


    span.grid(row=0, column=0, padx=20, pady=20)
    howtouse.grid(row=1, column=0, sticky="ew", pady=30)
    calibration.grid(row=2, column=0, sticky="ew", pady=10)
    settings.grid(row=3, column=0, sticky="ew", pady=30)
    bottomtext.grid(row=4, column=0, sticky="sw")
    bottomleft.grid(row=1, column=0, sticky="nsew")
    bottomright.grid(row=1, column=1, sticky="nsew")


    main.grid(row=0, column=1, sticky="nsew")
    sidebar.grid(row=0, column=0, sticky="nsew")


    root.mainloop()


def quitProgram(root):
    root.quit()
    root.destroy()


def validateSettings():

    settings = ("theme", "wsize", "hsize", "startup", "minimizeToTray")
    default = "theme: dark\nwsize: 1280\nhsize: 720\nstartup: False\nminimizeToTray: False"
    valid = True

    with open("data/src/config.txt", "r") as f:
        contents = f.readlines()
        cur_settings = [entry.split(":")[0] in settings for entry in contents]
        if len(cur_settings) != len(settings) or False in cur_settings:
            valid = False
    if not valid:
       with open("data/src/config.txt", "w") as f:
           f.write(default)
    with open("data/src/config.txt", "r") as f:
        config = f.readlines()
        return config




def viewSettings(main, color):
    mainContent = tk.Frame(main, bg=color["s"])

    darkMode = tk.BooleanVar()
    startup = tk.BooleanVar()
    minTray = tk.BooleanVar()

    text = {
        "t": "Enables dark mode - requires restart for effect to take place.",
        "s": "Enables program to run on startup. Will only work correctly if position of camera and mouse isn'nt changed. Requires restart for effect to take place.",
        "m": "Enables program to be minimized to tray when closed. Allows the program to run in the background without taking up a slot in the taskbar. Requires restart for effect to take place." 


    }

    themeChk = tk.Checkbutton(mainContent, variable=darkMode, onvalue=True, offvalue=False, bg=color["s"], fg=color["t"], text=text["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], command=lambda: save.config(state="normal", bg="#1ca30d", activebackground="#126e08", activeforeground="#FFFFFF", cursor="hand2"))

    startupChk = tk.Checkbutton(mainContent, variable=startup, onvalue=True, offvalue=False, text=text["s"], bg=color["s"], fg=color["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], command=lambda: save.config(state="normal", bg="#1ca30d", activebackground="#126e08", activeforeground="#FFFFFF", cursor="hand2"))

    minTrayChk = tk.Checkbutton(mainContent, variable=minTray, onvalue=True, offvalue=False, text=text["m"], bg=color["s"], fg=color["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], command=lambda: save.config(state="normal", bg="#1ca30d", activebackground="#126e08", activeforeground="#FFFFFF", cursor="hand2"))

    save = tk.Button(mainContent, text="Save Changes", command=lambda: saveChanges(darkMode),bg="#a3a3a3", fg="#FFFFFF", borderwidth=0, highlightthickness=0, activeforeground="#FFFFFF", activebackground="#a3a3a3", state="disabled")

    


    themeChk.grid(row=0, column= 0, sticky="w")
    startupChk.grid(row=1, column= 0, sticky="w")
    minTrayChk.grid(row=2, column= 0, sticky="w")

    save.grid(row=3, column= 0, sticky="w", ipadx=20, ipady=10)


    
    mainContent.grid(row=0, column=0, sticky="nsew")


def saveChanges(darkMode):
    print(darkMode.get())




mainWin()
