import tkinter as tk
from tkinter import scrolledtext
from turtle import *

def create_grid(turtle_obj, width, height, interval):
    turtle_obj.speed(0)
    turtle_obj.penup()
    turtle_obj.hideturtle()

    # Рисование вертикальных линий и меток
    for x in range(-width//2, width//2 + 1, interval):
        turtle_obj.goto(x, -height//2)
        turtle_obj.pendown()
        turtle_obj.goto(x, height//2)
        turtle_obj.penup()
        if x != 0:
            turtle_obj.goto(x, -height//2 - 10)
            turtle_obj.write(x, align="center")

    # Рисование горизонтальных линий и меток
    for y in range(-height//2, height//2 + 1, interval):
        turtle_obj.goto(-width//2, y)
        turtle_obj.pendown()
        turtle_obj.goto(width//2, y)
        turtle_obj.penup()
        if y != 0:
            turtle_obj.goto(-width//2 - 20, y - 5)
            turtle_obj.write(y, align="right")

    # Рисование осей
    turtle_obj.goto(0, -height//2)
    turtle_obj.pendown()
    turtle_obj.goto(0, height//2)
    turtle_obj.penup()
    turtle_obj.goto(-width//2, 0)
    turtle_obj.pendown()
    turtle_obj.goto(width//2, 0)
    turtle_obj.penup()

def execute_code():
    code = code_input.get("1.0", tk.END)
    exec(code, globals())

def start_gui():
    root = tk.Tk()
    root.title("Python Code Executor with Grid")

    # Создание фрейма для ввода кода и кнопки
    frame = tk.Frame(root)
    frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    global code_input
    code_input = scrolledtext.ScrolledText(frame, width=40, height=20)
    code_input.pack(padx=10, pady=10)

    execute_button = tk.Button(frame, text="Запуск", command=execute_code)
    execute_button.pack(pady=10)

    # Создание холста для turtle
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack(side=tk.RIGHT, padx=10, pady=10)

    screen = TurtleScreen(canvas)
    screen.setworldcoordinates(-200, -200, 200, 200)

    turtle_obj = RawTurtle(screen)
    create_grid(turtle_obj, 400, 400, 25)

    root.mainloop()

if __name__ == "__main__":
    start_gui()