import tkinter as tk
from LSmain import selectPoints
from PIL import ImageTk, Image
import webbrowser

def mainWin():
    config = validateSettings()
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: quitProgram(root))
    root.geometry("1280x720")
    root.title("Lightscreen")
    root.iconbitmap("images\selectPoints.ico")
    root.minsize(840, 400)
    
    
    theme = ''.join([set.split(":")[1] for set in config if set.split(":")[0] == "theme"])[:-1].strip()
    color = {
        "p": "#bae4e2",
        "s": "#e5f4f3",
        "t": "#89abad"
        }
    imglocation = "images\spanlight.png"

    if theme == "dark":
        color["p"] = "#121212"
        color["s"] = "#333333"
        color["t"] = "#adadad"
        imglocation = "images\spandark.png"
    

    spanimg = Image.open(imglocation)
    resized = spanimg.resize((360, 72), Image.ANTIALIAS)
    resizedspan = ImageTk.PhotoImage(resized)

    sidebar = tk.Frame(root, bg = color["p"])
    main = tk.Frame(root, bg=color["s"])
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    """root.columnconfigure(0, weight=1)
    root.columnconfigure()"""

    btnfont = ("Roboto Mono Light", 15, "bold")

    span = tk.Label(sidebar, image=resizedspan, borderwidth=0)
    howtouse = tk.Button(sidebar, text=">> HOW TO USE", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=lambda: webbrowser.open("https://www.google.com"))
    configuration = tk.Button(sidebar, text=">> CONFIGURATION", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, padx=50, cursor="hand2", command=selectPoints)
    settings = tk.Button(sidebar, text=">> SETTINGS", fg=color["t"], font=btnfont, bg=color["p"], borderwidth=0, cursor="hand2", command=lambda: viewSettings(main))
    bottomleft = tk.Frame(root, bg=color["p"])
    bottomright= tk.Frame(root, bg=color["s"])
    bottomtext = tk.Label(bottomleft, text="GitHub: @ImaadNisar", font = ("Roboto Mono Light", 7), bg=color["p"], fg=color["t"])


    span.grid(row=0, column=0, padx=20, pady=20)
    howtouse.grid(row=1, column=0, sticky="ew", pady=30)
    configuration.grid(row=2, column=0, sticky="ew", pady=10)
    settings.grid(row=3, column=0, sticky="ew", pady=30)
    bottomtext.grid(row=4, column=0, sticky="sw")
    bottomleft.grid(row=1, column=0, sticky="nsew")
    bottomright.grid(row=1, column=1, sticky="nsew")


    main.grid(row=0, column=1, sticky="nsew")
    sidebar.grid(row=0, column=0, sticky="nsew")



    viewSettings(main)
    root.mainloop()


def quitProgram(root):
    root.quit()
    root.destroy()


def validateSettings():

    settings = ("theme", "wsize", "hsize", "startup", "minimizeToTray")
    default = "theme: dark\nwsize: 1280\nhsize: 720\nstartup: False\nminimizeToTray: False"
    valid = True

    with open("src\config.txt", "r") as f:
        contents = f.readlines()
        cur_settings = [entry.split(":")[0] in settings for entry in contents]
        if len(cur_settings) != len(settings) or False in cur_settings:
            valid = False
    if not valid:
       with open("src\config.txt", "w") as f:
           f.write(default)
    with open("src\config.txt", "r") as f:
        config = f.readlines()
        return config




def viewSettings(main):
    theme_var = tk.IntVar
    tick_theme = tk.Checkbutton(main, variable=theme_var, onvalue=1, offvalue=0, command="lambda: select(theme_var)")

    tick_theme.pack()


def select(var):
    print(var.get())


mainWin()
