import MineSweeper

import tkinter as tk
from tkinter import messagebox
from collections import Counter
from time import time, sleep
import random

# Constants
SQUARE_SIZE         = 20
SQUARE_SPACING      = 1
SQUARE_TOTAL        = SQUARE_SIZE + 2 * SQUARE_SPACING

DEFAULT_HEIGHT      = 16
MIN_HEIGHT          = 8
MAX_HEIGHT          = 40

DEFAULT_WIDTH       = 32
MIN_WIDTH           = 8
MAX_WIDTH           = 60

DEFAULT_BOMBS_LIMIT = 1
MIN_BOMBS_LIMIT     = 1
MAX_BOMBS_LIMIT     = 8

DEFAULT_BOMBS_RATIO = 5
MIN_BOMBS_RATIO     = 1
MAX_BOMBS_RATIO     = 10


# Globals
height      = DEFAULT_HEIGHT
width       = DEFAULT_WIDTH
bombs_limit = DEFAULT_BOMBS_LIMIT
bombs_ratio = DEFAULT_BOMBS_RATIO
board       = None


# Initialize the random number generator
random.seed()


# GUI elements
root             = tk.Tk()
minefield_canvas = None
squares          = []
numbers          = []
status_label     = None
bombs_label      = None
bombs_counter    = 0
flags_label      = None
flags_counter    = 0


# GUI construction
def create_main_window():
    global button_canvas
    root.title("MineSweeper")
    control_canvas = tk.Canvas(root, bg="#aaaaaaaaa")
    add_configuration_canvas(control_canvas)
    add_information_canvas(control_canvas)
    add_extra_funcionality_canvas(control_canvas)
    control_canvas.pack()
    create_minefield_canvas()

def offset(val):
    return 10 + val * 20


def add_slider(canvas, xoffset, yoffset, val, min, max, eventh, text):
    slider = tk.Scale(canvas, from_=min, to=max, orient=tk.HORIZONTAL, command=eventh)
    slider.set(val)
    label = tk.Label(canvas, text=text)
    canvas.create_window(offset(xoffset), offset(yoffset), anchor=tk.NW, window=label)
    canvas.create_window(10 + offset(xoffset), 25 + offset(yoffset), anchor=tk.NW, window=slider)


def add_button(canvas, xoffset, yoffset, command, text):
    button = tk.Button(canvas, text=text, bg="#bbbbbbbbb", command=command)
    canvas.create_window(offset(xoffset), offset(yoffset), anchor=tk.NW, window=button)


def add_configuration_canvas(control_canvas):
    global status_label
    c = tk.Canvas(control_canvas, bg="#ccccccccc", height=210, width=340)
    add_slider(c, 0, 0, height,      MIN_HEIGHT,      MAX_HEIGHT,      on_h_slider,  "Height:")
    add_slider(c, 0, 4, width,       MIN_WIDTH,       MAX_WIDTH,       on_v_slider,  "Width:")
    add_slider(c, 8, 0, bombs_ratio, MIN_BOMBS_RATIO, MAX_BOMBS_RATIO, on_br_slider, "# squares / # bombs:")
    add_slider(c, 8, 4, bombs_limit, MIN_BOMBS_LIMIT, MAX_BOMBS_LIMIT, on_bl_slider, "Max # bombs per Square:")
    add_button(c, 0, 8, create_minefield_canvas, "Restart")
    add_button(c, 4, 8, root.destroy, "Quit")
    status_label = tk.Label(c, bg="blue", fg="white")
    c.create_window(offset(8), offset(8), width=150, height=28, anchor=tk.NW, window=status_label)
    c.pack(side=tk.LEFT)


def add_information_canvas(control_canvas):
    global bombs_label, flags_label
    c = tk.Canvas(control_canvas, bg="#ccccccccc", height=90, width=200)
    b_label = tk.Label(c, text="# Bombs:")
    f_label = tk.Label(c, text="# Flags:")
    bombs_label = tk.Label(c, text="000", bg="red", fg="white")
    flags_label = tk.Label(c, text="000", bg="green", fg="white")
    c.create_window(10, 20, anchor=tk.NW, window=b_label)
    c.create_window(10, 50, anchor=tk.NW, window=f_label)
    c.create_window(90, 20, anchor=tk.NW, window=bombs_label)
    c.create_window(90, 50, anchor=tk.NW, window=flags_label)
    c.pack(side=tk.TOP)
    
    
def add_extra_funcionality_canvas(control_canvas):
    c = tk.Canvas(control_canvas, bg="#ccccccccc", height=120, width=200)
    add_button(c, 0.7, .3, show_solution, "Show solution")
    add_button(c, 0.7, 2, show_shortest_solution, "Show fastest solution")
    add_button(c, 0.7, 3.7, flag_all_bombs, "Flag all bombs")
    c.pack(side=tk.BOTTOM)


# Minefield canvas construction and updates:
def create_minefield_canvas(initial=None):
    global board, minefield_canvas, flags_counter, flags_counter
    bombs = generate_bombs(height, width, initial)
    bombs_counter = len(bombs)
    bombs_label["text"] = str(bombs_counter)
    flags_counter = 0
    flags_label["text"] = str(flags_counter)
    if board == None or MineSweeper.nb_rows(board) != height or MineSweeper.nb_cols(board) != width:
        if not (minefield_canvas is None):
            minefield_canvas.destroy()
        minefield_canvas = tk.Canvas(root, bg="#aaaaaaaaa", height=height * SQUARE_TOTAL, width=width * SQUARE_TOTAL)
        add_squares_and_numbers(height, width)
        minefield_canvas.pack()
    else:
        for row in range(height):
            for col in range(width):
                pos = (row, col)
                minefield_canvas.itemconfig(get_square_for_position(pos), fill="black")
                minefield_canvas.itemconfig(get_number_for_position(pos), fill="white", text="")
    board = MineSweeper.make_board((height, width), bombs)
    enable_minefield()


def create_square(pos):
    (x, y) = get_xy_for_position(pos)
    return minefield_canvas.create_polygon(
        x, y,
        x + SQUARE_SIZE, y,
        x + SQUARE_SIZE, y - SQUARE_SIZE,
        x, y - SQUARE_SIZE,
        tags="square",
        fill="black"
    )


def create_number(pos):
    (x, y) = get_xy_for_position(pos)
    return minefield_canvas.create_text(
        x + (SQUARE_TOTAL / 2), y + (SQUARE_SPACING - (SQUARE_TOTAL) / 2),
        text="",
        fill="black",
        tags="square",
    )


def add_squares_and_numbers(h, w):
    global squares, numbers
    squares = []
    numbers = []
    for row in range(h):
        squares_row = []
        numbers_row = []
        for col in range(w):
            squares_row.append(create_square((row, col)))
            numbers_row.append(create_number((row, col)))
        squares.append(squares_row)
        numbers.append(numbers_row)

def display_minefield():
    global flags_counter
    total_flags = 0
    for row in range(MineSweeper.nb_rows(board)):
        for col in range(MineSweeper.nb_cols(board)):
            pos = (row, col)
            nb_flags = MineSweeper.nb_flags_at(board, pos)
            total_flags += nb_flags
            if MineSweeper.is_open_at(board, pos):
                minefield_canvas.itemconfig(get_square_for_position(pos), fill="white")
                adjecent_bombs = MineSweeper.nb_adjacent_bombs(board, pos)
                if (adjecent_bombs > 0):
                    minefield_canvas.itemconfig(get_number_for_position(pos),
                                                fill=color_for_number(adjecent_bombs), text=str(adjecent_bombs))
            elif nb_flags > 0:
                minefield_canvas.itemconfig(get_square_for_position(pos), fill="green")
                minefield_canvas.itemconfig(get_number_for_position(pos), fill="white", text=(str(nb_flags)))
            else:
                minefield_canvas.itemconfig(get_square_for_position(pos), fill="black")
                minefield_canvas.itemconfig(get_number_for_position(pos), fill="white", text="")
    flags_label["text"] = str(total_flags)
    minefield_canvas.update_idletasks()


def disable_minefield():
    minefield_canvas.tag_unbind("square", "<Button-1>")
    minefield_canvas.tag_unbind("square", "<Button-2>")
    minefield_canvas.tag_unbind("square", "<Button-3>")
    minefield_canvas.tag_unbind("square", "<Control-Button-1>")
    minefield_canvas.tag_unbind("square", "<M1-Button-1>")
    status_label["text"] = "Calculating ..."
    for row in range(MineSweeper.nb_rows(board)):
        for col in range(MineSweeper.nb_cols(board)):
            pos = (row, col)
            minefield_canvas.itemconfig(get_number_for_position(pos), text="")
            minefield_canvas.itemconfig(get_square_for_position(pos), fill="gray")
    minefield_canvas.update_idletasks()
    

def enable_minefield():
    minefield_canvas.tag_bind("square", "<Button-1>", func=on_left_square_click)
    minefield_canvas.tag_bind("square", "<Button-2>", func=on_middle_square_click)
    minefield_canvas.tag_bind("square", "<Button-3>", func=on_right_square_click)
    minefield_canvas.tag_bind("square", "<Control-Button-1>", func=on_right_square_click)
    minefield_canvas.tag_bind("square", "<M1-Button-1>", func=on_right_square_click)
    status_label["text"] = "Game in progress"
    display_minefield()


# Event handlers
def on_h_slider(val):
    global height
    height = int(val)


def on_v_slider(val):
    global width
    width = int(val)


def on_br_slider(val):
    global bombs_ratio
    bombs_ratio = int(val)


def on_bl_slider(val):
    global bombs_limit
    bombs_limit = int(val)


def on_left_square_click(event):
    w = event.widget.find_closest(event.x, event.y)[0]
    pos = get_position_for_widget(w)
    if MineSweeper.is_open_at(board, pos):
        return
    if MineSweeper.nb_flags_at(board, pos) > 0:
        MineSweeper.remove_flag_from(board, pos)
    else:
        open_square(pos)
    display_minefield()


def on_middle_square_click(event):
    w = event.widget.find_closest(event.x, event.y)[0]
    pos = get_position_for_widget(w)
    if bombs_limit == 1 and MineSweeper.is_open_at(board, pos):
        disable_minefield()
        MineSweeper.disclose_as_far_as_possible(board)
        # TODO: remove if statement?
        enable_minefield()


def on_right_square_click(event):
    w = event.widget.find_closest(event.x, event.y)[0]
    pos = get_position_for_widget(w)
    if not MineSweeper.is_open_at(board, pos):
      MineSweeper.add_flag_at(board, pos)
      display_minefield()


# Conversions (positions - xy - squares - numbers):
def get_xy_for_position(pos):
    return (SQUARE_SPACING + pos[1] * SQUARE_TOTAL,
            SQUARE_SPACING + (1 + pos[0]) * SQUARE_TOTAL)


def get_position_for_widget(widget):
    sequence_number = (widget - 1) // 2
    row = (sequence_number // MineSweeper.nb_cols(board))
    col = (sequence_number % MineSweeper.nb_cols(board))
    return (row, col)


def get_square_for_position(pos):
    return squares[pos[0]][pos[1]]


def get_number_for_position(pos):
    return numbers[pos[0]][pos[1]]


# Auxiliary functions
def generate_bombs(h, w, initial=None):
    allowed_positions = []
    for i in range(h):
        for j in range(w):
            if initial != (i, j):
                for _ in range(bombs_limit):
                    allowed_positions.append((i, j))
    random.shuffle(allowed_positions)
    nb_positions = min(len(allowed_positions), h * w // bombs_ratio)
    return allowed_positions[:nb_positions]


def open_square(pos):
    if MineSweeper.nb_bombs_at(board, pos) > 0:
        if flags_counter == 0 and \
           MineSweeper.nb_rows(board) * MineSweeper.nb_cols(board) == \
           len(MineSweeper.closed_squares(board)):
            create_minefield_canvas(initial=pos)
            open_square(pos)
        else:
            minefield_canvas.itemconfig(get_square_for_position(pos), fill="red")
            messagebox.showwarning("Boom!!!!!", "Game over")
            create_minefield_canvas()
    else:
        MineSweeper.disclose_square(board, pos)
        if MineSweeper.is_fully_disclosed(board):
            display_minefield()
            messagebox.showwarning("Congrats!", "You won!!!!!!!!!!!")
            create_minefield_canvas()


def show_solution():
    disable_minefield()
    positions = MineSweeper.solve_bruteforce(board)
    enable_minefield()
    status_label["text"] = "Solving"
    for p in positions:
        open_square(p)
        display_minefield()
        sleep(0.005)


def show_shortest_solution():
    disable_minefield()
    positions = MineSweeper.shortest_solution(board)
    enable_minefield()
    status_label["text"] = "Solving"
    for p in positions:
        open_square(p)
        display_minefield()
        sleep(0.005)


def flag_all_bombs():
    MineSweeper.flag_all_bombs(board)
    display_minefield()


def color_for_number(num):
    if   num == 1: return "#000000fff"
    elif num == 2: return "#777000fff"
    elif num == 3: return "#000777fff"
    elif num == 4: return "#777777fff"
    elif num == 5: return "#aaa000fff"
    elif num == 6: return "#000aaafff"
    elif num == 7: return "#aaaaaafff"
    else:          return "#000000000"


# Start application
create_main_window()
root.mainloop()

