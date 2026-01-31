import tkinter as tk
from tkvideo import tkvideo
import threading
import random


root = tk.Tk()
root.resizable(False, False)
root.withdraw()
count = 10

def closed2():
    root.quit()


def closed():
    root3 = tk.Toplevel()
    root3.attributes('-fullscreen', True)
    lbl = tk.Label(root3, bg="black")
    player = tkvideo("sprites/video/death.mp4", lbl, loop=1, size = (root3.winfo_screenwidth(), root3.winfo_screenheight()))
    player.play()
    lbl.pack(fill="both", expand=1)
    threading.Timer(4, closed2).start()


def window():
    root2 = tk.Toplevel()
    lbl = tk.Label(root2, bg="black")
    player = tkvideo("sprites/video/eyes.mp4", lbl, loop=1)
    player.play()
    root2.overrideredirect(True)
    lbl.pack(fill="both", expand=1)
    root2.wm_attributes('-transparentcolor', 'black')
    root2.resizable(False, False)
    w1_x, w1_y = random.randint(0, root2.winfo_screenwidth() - 600), \
        random.randint(0, root2.winfo_screenheight() - 400)
    root2.geometry(f"+{w1_x}+{w1_y}")


def okno():
    global count
    if count > 1:
        window()
        threading.Timer(1, okno).start()
        count -= 1

okno()
threading.Timer(10, closed).start()
root.mainloop()