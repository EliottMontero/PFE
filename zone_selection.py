import tkinter as tk
from PIL.Image import *
from PIL import ImageTk

topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None
path = "test.jpg"
tmp=open(path)
(l,h)=tmp.size
WIDTH, HEIGHT = l, h

#:TODO:FLO:1202:essayer que ca fasse quelque chose quand on appuie sur une touche du clavier...
def save_position(event):
	print(c)
	print("je save")

def end_position(event):
	print(topx, topy, botx, boty)

def get_mouse_posn(event):
    global topy, topx

    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty

    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.


window = tk.Tk()
window.title("Object selection")
window.geometry('%sx%s' % (WIDTH, HEIGHT))
window.configure(background='black')

img = ImageTk.PhotoImage(open(path))
canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                   borderwidth=0, highlightthickness=0)
canvas.pack(expand=False)
canvas.img = img  # Keep reference in case this code is put into a function.
canvas.create_image(0, 0, image=img, anchor=tk.NW)

# Create selection rectangle (invisible since corner points are equal).
rect_id = canvas.create_rectangle(topx, topy, topx, topy,
                                  dash=(2,2), fill='', outline='red')

canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)
canvas.bind('<ButtonRelease-1>',end_position)
canvas.bind('<KeyPress-s>',save_position)

window.mainloop()