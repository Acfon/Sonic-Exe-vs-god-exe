import tkinter as tk
from tkvideo import tkvideo
import threading
import random

root = tk.Tk()
root.resizable(False, False)
root.withdraw()

def closed():
    root.quit()


def window():
    root2 = tk.Toplevel()
    lbl = tk.Label(root2)
    player = tkvideo("sprites/video/eyes.mp4", lbl, loop=1)
    player.play()
    lbl.pack()
    root2.wm_attributes('-transparentcolor', 'black')
    root2.resizable(False, False)
    w1_x, w1_y = random.randint(0, root2.winfo_screenwidth() - 600), \
        random.randint(0, root2.winfo_screenheight() - 400)
    root2.geometry(f"+{w1_x}+{w1_y}")
    threading.Timer(1, closed).start()
    root2.mainloop()


for i in range(10):
    window()
threading.Timer(4, closed).start()
root.mainloop()