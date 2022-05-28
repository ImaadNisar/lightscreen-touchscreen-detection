import tkinter as tk
from LScalibrate import selectPoints
from LStrack import start
from PIL import Image, ImageTk
import webbrowser  # used to open webpage
from platform import system # used to identify os
import LSsharedmodules

def mainWin():
    version = "v1.0"
    config, default, startup, minimizeToTray = validateFiles()  # obtains values from files
    root = tk.Tk()

    if minimizeToTray.lower() == "true":  # changes what happens when the window is closed
        root.protocol("WM_DELETE_WINDOW", lambda: LSsharedmodules.minToTray(root))  # minimize the window the tray is setting is selected
    else:
        root.protocol("WM_DELETE_WINDOW", lambda: LSsharedmodules.quitProgram(root))  # otherwise quit

    root.geometry("1280x720")  # changes window properties
    root.title("Lightscreen")
    root.resizable(False, False)

    # applies the appropriate icon depending on os
    icon = "data/images/winIcon.ico"
    if system() == "Linux":
        icon = "@data/images/linuxIcon.xbm" 
    root.iconbitmap(icon)
    
    
    theme = ''.join([set.split(":")[1] for set in config if set.split(":")[0] == "theme"])[:-1].strip()  # obtains theme from file contents
    
    global mainimage
    global mainimglbl
    # dark theme color scheme
    color = {
        "p": "#111111",
        "s": "#232323",
        "t": "#adadad",
        "c": "#202020"
        }
    imglocation = "data/images/spandark.png"
    mainimg = Image.open("data/images/maindark.png")
    mainimage = ImageTk.PhotoImage(mainimg)

    # light theme color scheme
    if theme == "light":
        color["p"] = "#ffffff"
        color["s"] = "#f3f3ff"
        color["t"] = "#665ab5"
        color["c"] = "#857a87"
        imglocation = "data/images/spanlight.png"
        mainimg = Image.open("data/images/mainlight.png")
        mainimage = ImageTk.PhotoImage(mainimg)
    
    # opens image in correct format
    spanimg = Image.open(imglocation)
    resized = spanimg.resize((360, 72), Image.ANTIALIAS)
    resizedspan = ImageTk.PhotoImage(resized)

    # creates frames and configures layout for each
    sidebar = tk.Frame(root, bg = color["p"])
    main = tk.Frame(root, bg=color["s"])
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    main.rowconfigure(0, weight=1)


    btnfont = ("Roboto Mono Light", 15, "bold")  # font used in widgets

    span = tk.Button(sidebar, image=resizedspan, borderwidth=0, cursor="hand2", highlightthickness=0, activebackground=color["p"], command=lambda: homepage(main, mainimglbl))  # label used for image

    # creates widgets >

    mainimglbl = tk.Label(main, image=mainimage, highlightthickness=0, borderwidth=0)

    start = tk.Button(sidebar, text=">> START", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, cursor="hand2", highlightthickness=0, command=lambda: startTracking(root))
    
    calibration = tk.Button(sidebar, text=">> CALIBRATION", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=lambda: startCalibration(main, color, mainimglbl), highlightthickness=0)

    settings = tk.Button(sidebar, text=">> SETTINGS", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, cursor="hand2", command=lambda: viewSettings(main, color, config, default), highlightthickness=0)

    howtouse = tk.Button(sidebar, text=">> MORE INFO", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=lambda: howToUse(main, color), highlightthickness=0)

    bottomleft = tk.Frame(root, bg=color["p"])
    bottomright= tk.Frame(root, bg=color["s"])
    credit = tk.Button(bottomleft, text="GitHub: @ImaadNisar", font = ("Roboto Mono Light", 7), bg=color["p"], fg=color["c"], highlightthickness=0, borderwidth=0, activeforeground=color["t"], activebackground=color["p"], cursor="hand2", command=lambda: webbrowser.open("https://github.com/ImaadNisar"))
    version = tk.Label(bottomleft, text=version, font=("Roboto Mono Light", 7), bg=color["p"], fg=color["c"], highlightthickness=0, borderwidth=0)

    
    

    # < creates widgets

    # puts widgets on screen
    span.grid(row=0, column=0, padx=20, pady=20)
    start.grid(row=1, column=0, sticky="ew", pady=30)
    calibration.grid(row=2, column=0, sticky="ew", pady=10)
    settings.grid(row=3, column=0, sticky="ew", pady=30)
    howtouse.grid(row=4, column=0, sticky="ew", pady=10)
    credit.grid(row=5, column=0, sticky="sw", padx=(3,0))
    version.grid(row=5, column=0, sticky="se", padx=(375,0))
    bottomleft.grid(row=1, column=0, sticky="nsew")
    bottomright.grid(row=1, column=1, sticky="nsew")
    mainimglbl.grid()

    #  puts frames on screen
    main.grid(row=0, column=1, sticky="nsew")
    sidebar.grid(row=0, column=0, sticky="nsew")

    # immediately starts if setting is selected
    if startup.lower() == "true":
        startTracking(root)



    root.mainloop()




def validateFiles():

    temp = tk.Tk()
    temp.withdraw()
    w, h = temp.winfo_screenwidth(), temp.winfo_screenheight()  # obtains screen res
    temp.destroy()

    keys = ("theme", "wsize", "hsize", "startup", "minimizeToTray")

    default = f"theme: dark\nwsize: {w}\nhsize: {h}\nstartup: False\nminimizeToTray: False"
    validSettings = True
    validProfile = True

    with open("data/src/settings.txt", "r") as f:  # reads files contents
        contents = f.readlines()
        try:  # validates settings
            cur_settings = [entry.split(":")[0] in keys for entry in contents]
            if len(cur_settings) != len(keys) or False in cur_settings:
                validSettings = False

            for entry in contents:
                key, val = entry.split(":")[0].strip(), entry.split(":")[1].strip()
                if ((key == keys[0] and val.lower() not in("dark", "light")) or 
                (key in keys[1:3] and not val.isnumeric()) or 
                (key in keys[3:] and val.lower() not in ("true", "false"))):
                    validSettings = False
        except IndexError:
            validSettings = False

    with open("data/src/profile.txt", "r") as f:  # validates profile
        contents = f.readlines()
        if len(contents) != 2:
            validProfile = False
        for entry in contents:
            if ("points: " not in entry) and ("maskparams: " not in entry):
                validProfile = False

    # resets external files to their default state if invalid
    if not validProfile:  
        with open("data/src/profile.txt", "w") as f:
            f.write("points: \nmaskparams: ")
    if not validSettings:
       with open("data/src/settings.txt", "w") as f:
           f.write(default)

    with open("data/src/settings.txt", "r") as f:
        config = f.readlines()
        for entry in config:  # obtains setting values and returns them
            if entry.split(":")[0].strip() == "startup":
                startup = entry.split(":")[1].strip()
            elif entry.split(":")[0].strip() == "minimizeToTray":
                minimizeToTray = entry.split(":")[1].strip()
        return config, default, startup, minimizeToTray 


def viewSettings(main, color, config, default):
    for widget in main.winfo_children():
        widget.grid_forget()
    mainContent = tk.Frame(main, bg=color["s"])  # create frame

    #  creates tickbox vars
    darkMode = tk.BooleanVar()
    startup = tk.BooleanVar()
    minTray = tk.BooleanVar()

    text = {  # text for tickboxes
        "t": "Enables dark mode - requires restart",
        "s": "Run on startup using saved profile - requires restart",
        "m": "Minimize to system tray when closed - requires restart" 
    }

    font = ("Roboto Mono Light", 12)

    setTitle = tk.Label(mainContent, text="SETTINGS", font=("Roboto Mono Light", 26, "bold"), bg=color["s"], fg=color["t"])  # creates settings title label

    # creates tickboxes
    themeChk = tk.Checkbutton(mainContent, variable=darkMode, onvalue=True, offvalue=False, bg=color["s"], fg=color["t"], text=text["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], font=font, justify="left", command=lambda: enableSave(save))  # command called to display save button
    themeChk.variable = darkMode  # prevents garbage collection
    
    startupChk = tk.Checkbutton(mainContent, variable=startup, onvalue=True, offvalue=False, text=text["s"], bg=color["s"], fg=color["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], font=font, justify="left", command=lambda: enableSave(save))
    startupChk.variable = startup

    minTrayChk = tk.Checkbutton(mainContent, variable=minTray, onvalue=True, offvalue=False, text=text["m"], bg=color["s"], fg=color["t"], highlightthickness=0, activebackground=color["s"], activeforeground=color["t"], font=font, justify="left", command=lambda: enableSave(save))
    minTrayChk.variable = minTray

    #  creates resolution related widgets
    resFrm = tk.Frame(mainContent, bg=color["s"])
    wlbl = tk.Label(resFrm, text="Width:", bg=color["s"], font=font, fg=color["t"], highlightthickness=0)
    wtxt = tk.Entry(resFrm, width=10, bg=color["s"], font=font, fg=color["t"], highlightthickness=0, borderwidth=2, relief="groove")
    hlbl = tk.Label(resFrm, text="Height:", bg=color["s"], font=font, fg=color["t"], highlightthickness=0)
    htxt = tk.Entry(resFrm, width=10, bg=color["s"], font=font, fg=color["t"], highlightthickness=0, borderwidth=2, relief="groove")
    resBtn = tk.Button(resFrm, command=lambda: showRes(wlbl, wtxt, hlbl, htxt, save), text="Change resolution", font=font, bg=color["s"], fg=color["t"], relief="groove", borderwidth=2, highlightthickness=1, cursor="hand2")  # when res button clicked, places widgets
    
    setValues(config, themeChk, startupChk, minTrayChk, wtxt, htxt)  # sets the values of 


    #  creates images for save and reset buttons
    img = Image.open("data/images/save.png")
    resize = img.resize((125,50), Image.ANTIALIAS)
    imgscaled = ImageTk.PhotoImage(resize)
    save = tk.Button(mainContent, image=imgscaled, bg=color["s"], borderwidth=0, cursor="hand2", activebackground=color["s"], width=90, height=35, command=lambda: onSave(save, darkMode.get(), startup.get(), minTray.get(), wtxt.get(), htxt.get()), highlightthickness=0)  # calls save function onclick
    save.image = imgscaled

    img2 = Image.open("data/images/default.png")
    resize2 = img2.resize((125,50), Image.ANTIALIAS)
    imgscaled2 = ImageTk.PhotoImage(resize2)
    setDefault = tk.Button(mainContent, image=imgscaled2, bg=color["s"], borderwidth=0, cursor="hand2", activebackground=color["s"], width=90, height=35, command=lambda: onDefault(save, config, default, themeChk, startupChk, minTrayChk, wtxt, htxt), highlightthickness=0)  # sets default values for widgets and saves
    setDefault.image = imgscaled2
    setDefault.grid(row=5, column=0, sticky="w", ipadx=20, ipady=10, padx=(70, 0), pady=(150, 0))




    #  place on screen >
    setTitle.place(x=350, y=40)
    themeChk.grid(row=1, column= 0, sticky="w", padx=(50,0), pady=(147, 25))
    startupChk.grid(row=2, column= 0, sticky="w", padx=(50,0), pady=25)
    minTrayChk.grid(row=3, column= 0, sticky="w", padx=(50,0), pady=25)

    resFrm.grid(row=4, column=0, sticky="w", padx=(50,0))
    resBtn.grid(row=0, column=0, sticky="w", padx=(0,20), pady=25, ipadx=20, ipady=10)


    
    mainContent.grid(row=0, column=0, sticky="nsew")
    #  < place on screen


def setValues(config, themeChk, startupChk, minTrayChk, wtxt, htxt):  # function to initailly set values for widgets
    for entry in config:
        key, val = entry.split(":")[0].strip(), entry.split(":")[1].strip()
        if key == "theme" and val in ("dark", "light"):
            if val == "dark": themeChk.select()
            else: themeChk.deselect()
        elif key == "startup" and val in ("True", "False"):
            if val == "True": startupChk.select()
            else: startupChk.deselect()
        elif key == "minimizeToTray" and val in ("True", "False"):
            if val == "True": minTrayChk.select()
            else: minTrayChk.deselect()
        elif key == "wsize":
            wtxt.delete(0, tk.END)
            wtxt.insert(0, val)
        elif key == "hsize":
            htxt.delete(0, tk.END)
            htxt.insert(0, val)
    



def enableSave(save):  # places save button on screen
    save.grid(row=5, column=1, sticky="e", ipadx=20, ipady=10, padx=(50, 0), pady=(130, 0))


def onSave(btn, darkMode, startup, minTray, wvar, hvar):
    if not wvar.isnumeric() or not hvar.isnumeric():  # checks entry values are valid
        LSsharedmodules.warning("Invalid Resolution", "Resolution not valid.\n\nPlease re-enter the width and height of your monitor")
        return
    d = "dark" if darkMode else "light"
    toSave = f"theme: {d}\nwsize: {wvar}\nhsize: {hvar}\nstartup: {startup}\nminimizeToTray: {minTray}"
    with open("data/src/settings.txt", "w") as f:  # writes selected and inputted values to file
        f.write(toSave) 
    LSsharedmodules.popUp("Changes Saved", "Changes have been saved.\nPlease restart to apply changes.", 1)  # presents popup
    btn.grid_forget()  # removes save button from screen


def onDefault(save, config, default, themeChk, startupChk, minTrayChk, wtxt, htxt):
    with open("data/src/settings.txt", "w") as f:
        f.write(default)  # writes default settings to file
    with open("data/src/settings.txt", "r") as f:
        config = f.readlines() # reads default contents

    setValues(config, themeChk, startupChk, minTrayChk, wtxt, htxt)  # changes state for all widgets once reset
    save.grid_forget()
    LSsharedmodules.popUp("Changes Saved", "Changes have been saved.\nPlease restart to apply changes.", 1)

def showRes(wlbl, wtxt, hlbl, htxt, save):  # places resolution related widgets on screen
    wlbl.grid(row=0, column=1, sticky="w", padx=(0,5))
    wtxt.grid(row=0, column=2, sticky="w", padx=(0,20))
    hlbl.grid(row=0, column=3, sticky="w", padx=(0,5))
    htxt.grid(row=0, column=4, sticky="w")
    enableSave(save)  # shows the save button


def clearMain(frame):  # removes all widgets from the frame
    for widget in frame.winfo_children():
        widget.grid_forget()


def startCalibration(main, color, lbl):
    lbl.grid_forget()
    if len(main.winfo_children()) > 1: 
        clearMain(main)  # clears the frame (if settings currently displayed)
    calibrateLbl = tk.Label(main, text="Calibration in progress...", font=("Roboto Mono Light", 22, "bold"), bg=color["s"], fg=color["t"])
    calibrateLbl.grid(row=0, column=0, padx=(200, 0))  # displays calibration label
    points, maskparams = False, False
    points, maskparams = selectPoints()  # obtains values from external function
    if not points or not maskparams:
        LSsharedmodules.warning("Aborted", "Calibration Process Aborted")
    else:
        profile = f"points: {points}\nmaskparams: {maskparams}" 
        with open("data/src/profile.txt", "w") as f:
            f.write(profile)  # writes values to profile
    calibrateLbl.destroy()
    lbl.grid()
    
    




def getRes():  # function to obtain the screen resolution from the settings file
    with open("data/src/settings.txt", "r") as f:
        contents = f.readlines()
        for entry in contents:
            key, val = entry.split(":")[0].strip(), entry.split(":")[1].strip()
            if key == "wsize":
                w = int(val)
            elif key == "hsize":
                h = int(val)
    return w, h


def startTracking(root):  # starts tracking
    w, h = getRes()  # obtains resolution
    with open("data/src/profile.txt", "r") as f:  # obtain profile (calibration) contents
        contents = f.readlines()
    if contents == ['points: \n', 'maskparams: ']:  # pop-up error if profile if empty
        LSsharedmodules.warning("Error", "No Profile Detected.\nClick CALIBRATION to create a profile")
        return
    try:
        for entry in contents:
            key , val = entry.split(":")[0].strip(), entry.split(":")[1].strip()  # obtains profile values and store in vars
            if key == "points":
                points = val
            elif key == "maskparams":
                maskparams = val
        
        start(root, points, maskparams, w, h)  # starts

    except Exception as e:  # if invalid profile values used, catches exception and display pop-up
        LSsharedmodules.warning("Error", f"Unexpected Error.\nClick CALIBRATION to create a profile\n\n{e}")
        root.quit()
        root.destroy()


def homepage(main, lbl):  # removes all widgets from main frame
    for widget in main.winfo_children():
        widget.grid_forget()
    lbl.grid()


def howToUse(main, color):
    for widget in main.winfo_children():
        widget.grid_forget()

    # creates github btn
    img = Image.open("data\images\github.png")
    resized = img.resize((256, 256), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    githubbtn = tk.Button(main, image=image, bg=color["s"], activebackground=color["s"], borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: webbrowser.open("https://github.com/ImaadNisar"))
    githubbtn.image = image

    # creates site btn
    img2 = Image.open("data\images\lightscreen.png")
    resized = img2.resize((256, 256), Image.ANTIALIAS)
    image2 = ImageTk.PhotoImage(resized)
    websitebtn = tk.Button(main, image=image2, bg=color["s"], activebackground=color["s"], borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: webbrowser.open("https://imaadnisar.github.io/Lightscreen-Touchscreen-Detection/"))
    websitebtn.image = image2

    githubbtn.grid(column=0, row=0, padx=(120, 0), ipadx=5, ipady=5)
    websitebtn.grid(column=1, row=0, padx=(120, 0), ipadx=5, ipady=5)



mainWin()