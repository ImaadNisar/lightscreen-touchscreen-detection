import tkinter as tk
from LSmain import selectPoints
from PIL import Image, ImageTk
import webbrowser
from platform import system
import popup

def mainWin():
    config = validateSettings()
    print(config)
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: quitProgram(root))
    root.geometry("1280x720")
    root.title("Lightscreen")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()


    icon = "data/images/winIcon.ico"
    if system() == "Linux":
        icon = "@data/images/linuxIcon.xbm"
    root.iconbitmap(icon)
    #root.resizable(False, False)
    
    theme = ''.join([set.split(":")[1] for set in config if set.split(":")[0] == "theme"])[:-1].strip()
    color = {
        "p": "#121212",
        "s": "#333333",
        "t": "#adadad",
        "c": "#FFFFFF"
        }
    imglocation = "data/images/spandark.png"

    if theme == "light":
        color["p"] = "#bae4e2"
        color["s"] = "#e5f4f3"
        color["t"] = "#89abad"
        color["c"] = "#4f4f4e"
        imglocation = "data/images/spanlight.png"
    

    spanimg = Image.open(imglocation)
    resized = spanimg.resize((360, 72), Image.ANTIALIAS)
    resizedspan = ImageTk.PhotoImage(resized)

    sidebar = tk.Frame(root, bg = color["p"])
    main = tk.Frame(root, bg=color["s"])
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    main.rowconfigure(0, weight=1)


    btnfont = ("Roboto Mono Light", 15, "bold")

    span = tk.Label(sidebar, image=resizedspan, borderwidth=0)

    howtouse = tk.Button(sidebar, text=">> HOW TO USE", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=lambda: webbrowser.open("https://www.google.com"), highlightthickness=0)

    calibration = tk.Button(sidebar, text=">> CALIBRATION", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=selectPoints, highlightthickness=0)

    settings = tk.Button(sidebar, text=">> SETTINGS", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, cursor="hand2", command=lambda: viewSettings(main, color, (f"{w}",f"{h}"), config), highlightthickness=0)

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

    keys = ("theme", "wsize", "hsize", "startup", "minimizeToTray")

    default = "theme: dark\nwsize: 1920\nhsize: 1080\nstartup: False\nminimizeToTray: False"
    valid = True

    with open("data/src/settings.txt", "r") as f:
        contents = f.readlines()
        cur_settings = [entry.split(":")[0] in keys for entry in contents]
        if len(cur_settings) != len(keys) or False in cur_settings:
            valid = False

        for entry in contents:
            key, val = entry.split(":")[0].strip(), entry.split(":")[1].strip()
            if ((key == keys[0] and val.lower() not in("dark", "light")) or 
            (key in keys[1:3] and not val.isnumeric()) or 
            (key in keys[3:] and val.lower() not in ("true", "false"))):
                valid = False


    if not valid:
       with open("data/src/settings.txt", "w") as f:
           f.write(default)
    with open("data/src/settings.txt", "r") as f:
        config = f.readlines()
        return config




def viewSettings(main, color, res, config):
    print(config)



    #  create widgets
    mainContent = tk.Frame(main, bg=color["s"])

    darkMode = tk.BooleanVar()
    startup = tk.BooleanVar()
    minTray = tk.BooleanVar()

    text = {
        "t": "Enables dark mode - requires restart",
        "s": "Run on startup - requires restart",
        "m": "Minimize to system tray when closed - requires restart" 
    }

    font = ("Roboto Mono Light", 12)

    setTitle = tk.Label(mainContent, text="SETTINGS", font=("Roboto Mono Light", 26, "bold"), bg=color["s"], fg=color["t"])

    themeChk = tk.Checkbutton(mainContent, variable=darkMode, onvalue=True, offvalue=False, bg=color["s"], fg=color["t"], text=text["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], font=font, justify="left", command=lambda: enableSave(save))
    themeChk.variable = darkMode  # prevents garbage collection
    
    
    startupChk = tk.Checkbutton(mainContent, variable=startup, onvalue=True, offvalue=False, text=text["s"], bg=color["s"], fg=color["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], font=font, justify="left", command=lambda: enableSave(save))
    startupChk.variable = startup

    minTrayChk = tk.Checkbutton(mainContent, variable=minTray, onvalue=True, offvalue=False, text=text["m"], bg=color["s"], fg=color["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], font=font, justify="left", command=lambda: enableSave(save))
    minTrayChk.variable = minTray


    for entry in config:
        key, val = entry.split(":")[0].strip(), entry.split(":")[1].strip()
        print(val)
        if key == "theme" and val == "dark":
            themeChk.select()
        elif key == "startup" and val == "True":
            startupChk.select()
        elif key == "minimizeToTray" and val == "True":
            minTrayChk.select()
    
    resFrm = tk.Frame(mainContent, bg=color["s"])
    wlbl = tk.Label(resFrm, text="Width:", bg=color["s"], font=font, fg=color["t"], highlightthickness=0)
    wtxt = tk.Entry(resFrm, width=10, bg=color["s"], font=font, fg=color["t"], highlightthickness=0, borderwidth=2, relief="groove")
    hlbl = tk.Label(resFrm, text="Height:", bg=color["s"], font=font, fg=color["t"], highlightthickness=0)
    htxt = tk.Entry(resFrm, width=10, bg=color["s"], font=font, fg=color["t"], highlightthickness=0, borderwidth=2, relief="groove")
    resBtn = tk.Button(resFrm, command=lambda: showRes(wlbl, wtxt, hlbl, htxt), text="text here")
    
    wtxt.insert(tk.END, res[0])  # insert file res
    htxt.insert(tk.END, res[1])

    img = Image.open("data/images/save.png")
    resize = img.resize((125,50), Image.ANTIALIAS)
    imgscaled = ImageTk.PhotoImage(resize)

    save = tk.Button(mainContent, image=imgscaled, bg=color["s"], borderwidth=0, cursor="hand2", activebackground=color["s"], width=85, height=30, command=lambda: onSave(save), highlightthickness=0)
    save.image = imgscaled
    #  create widgets



    #  place on screen
    setTitle.grid(row=0, column=0, sticky="n", padx=(230, 0), pady=(20,0))
    themeChk.grid(row=1, column= 0, sticky="w", padx=(50,0), pady=(75, 25))
    startupChk.grid(row=2, column= 0, sticky="w", padx=(50,0), pady=25)
    minTrayChk.grid(row=3, column= 0, sticky="w", padx=(50,0), pady=25)

    resFrm.grid(row=4, column=0, sticky="w", padx=(50,0), pady=25)
    resBtn.grid(row=0, column=0, sticky="w", padx=(10,20), pady=25)

    

    
    mainContent.grid(row=0, column=0, sticky="nsew")
    #  place on screen


def enableSave(save):
    save.grid(row=5, column=1, sticky="e", ipadx=20, ipady=10, padx=(50, 0), pady=(150, 0))


def onSave(btn):
    #save here
    popup.popUp("Changes Saved", "Changes have been saved.\nPlease restart to apply changes.", 1)
    btn.grid_forget()


def showRes(wlbl, wtxt, hlbl, htxt):
    wlbl.grid(row=0, column=1, sticky="w", padx=(0,5))
    wtxt.grid(row=0, column=2, sticky="w", padx=(0,20))
    hlbl.grid(row=0, column=3, sticky="w", padx=(0,5))
    htxt.grid(row=0, column=4, sticky="w")



mainWin()
