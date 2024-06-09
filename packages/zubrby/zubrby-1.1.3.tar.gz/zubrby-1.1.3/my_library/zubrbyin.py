import tkinter as tk


def create_grid(canvas, width, height, interval):
    # Рисование вертикальных линий
    for x in range(interval, width, interval):
        canvas.create_line(x, 0, x, height, fill='gray', dash=(2, 2))

    # Рисование горизонтальных линий
    for y in range(interval, height, interval):
        canvas.create_line(0, y, width, y, fill='gray', dash=(2, 2))

    # Рисование осей
    canvas.create_line(0, height // 2, width, height // 2, fill='black')
    canvas.create_line(width // 2, 0, width // 2, height, fill='black')


def main():
    # Создание главного окна
    root = tk.Tk()
    root.title("Координатная сетка")

    # Размеры окна
    width = 200
    height = 200
    interval = 50  # Единичный отрезок

    # Создание холста
    canvas = tk.Canvas(root, width=width, height=height, bg='white')
    canvas.pack()

    # Создание сетки
    create_grid(canvas, width, height, interval)

    # Запуск главного цикла
    root.mainloop()


if __name__ == "__main__":
    main()