import tkinter
import random

window=tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("480x520+100+100")
window.resizable(False, False)

row_index=1
col_index=0

for button_text in range (0,400):
    tkinter.Button(window, text=" ", width=2).grid(row=row_index, column=col_index)
    col_index+=1
    if col_index>19:
        row_index+=1
        col_index=0

window.mainloop()
