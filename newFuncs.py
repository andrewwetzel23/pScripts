from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename

# GUI search for directory
def browseForDir():
    Tk().withdraw()
    return askdirectory()

# GUI search for a file
def browseForFile():
    Tk().withdraw()
    return askopenfilename()