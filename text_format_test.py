from tkinter import *
from tkinter.ttk import *

root = Tk()


frame = Frame(root, width=300, height=200)
frame.pack()

s = Style()
print(s.theme_use())

s.configure('TButton', font='helvetica 24', foreground='red', padding=10)

print(s.theme_names())
bt2 = Button(frame, text='button')
bt2.pack()
btn = Button(frame, text = 'btn')
btn.pack()

root.mainloop()