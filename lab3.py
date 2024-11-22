import tkinter as tk
from tkinter import ttk
import time


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы растеризации")
        self.canvas_size = 800  
        self.pixel_size = 20    
        self.origin = self.canvas_size // 2 
        self.start_point = None  
        self.end_point = None    


        self.line_colors = ["red", "green", "blue", "purple", "orange", "brown"]
        self.color_index = 0

        self.algorithm = tk.StringVar(value="Брезенхем (линия)")

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(main_frame, padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(control_frame, text="Выбор алгоритма:", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        ttk.Combobox(
            control_frame,
            textvariable=self.algorithm,
            values=["Брезенхем (линия)", "ЦДА (линия)", "Пошаговый (линия)", "Брезенхем (окружность)"],
            state="readonly"
        ).pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Инструкция:", font=("Arial", 12)).pack(anchor=tk.W, pady=10)
        tk.Label(control_frame, text="1. Выберите алгоритм.\n"
                                     "2. Линия: выберите 2 точки.\n"
                                            "\n (x — номер столбца пикселя, начиная с левого края"
                                            "\n y — номер строки пикселя, начиная с верхнего края\n)"
                                     "3. Окружность: выберите центр и радиус.",
                                     
                 justify=tk.LEFT, wraplength=200).pack(anchor=tk.W)


        ttk.Button(control_frame, text="Очистить", command=self.clear_canvas).pack(fill=tk.X, pady=10)

        self.canvas = tk.Canvas(main_frame, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        log_frame = tk.Frame(main_frame, padx=10, pady=10)
        log_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(log_frame, text="Журнал отрисовки:", font=("Arial", 12)).pack(anchor=tk.W, pady=5)

        log_scrollbar = ttk.Scrollbar(log_frame)
        self.log_box = tk.Listbox(log_frame, width=60, height=30, yscrollcommand=log_scrollbar.set)
        log_scrollbar.config(command=self.log_box.yview)

        self.log_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        self.draw_grid()
        self.draw_axes()

        self.canvas.bind("<Button-1>", self.select_point)

    def draw_grid(self):
        for i in range(0, self.canvas_size, self.pixel_size):
            self.canvas.create_line(i, 0, i, self.canvas_size, fill="#d3d3d3")
            self.canvas.create_line(0, i, self.canvas_size, i, fill="#d3d3d3")

    def draw_axes(self):
        self.canvas.create_line(0, self.origin, self.canvas_size, self.origin, fill="black", width=2)
        self.canvas.create_line(self.origin, 0, self.origin, self.canvas_size, fill="black", width=2)

        self.canvas.create_text(self.canvas_size - 10, self.origin + 15, text="X", fill="black", font=("Arial", 12))
        self.canvas.create_text(self.origin - 15, 10, text="Y", fill="black", font=("Arial", 12))

        for i in range(0, self.canvas_size, self.pixel_size):
            coord = (i - self.origin) // self.pixel_size
            if coord == 0:
                continue
            self.canvas.create_text(i, self.origin + 10, text=str(coord), fill="black", font=("Arial", 8))
            self.canvas.create_text(self.origin + 10, i, text=str(-coord), fill="black", font=("Arial", 8))

    def canvas_to_grid(self, x, y):
        grid_x = (x - self.origin) // self.pixel_size
        grid_y = -(y - self.origin) // self.pixel_size
        return grid_x, grid_y

    def grid_to_canvas(self, x, y):
        canvas_x = self.origin + x * self.pixel_size
        canvas_y = self.origin - y * self.pixel_size
        return canvas_x, canvas_y

    def draw_pixel(self, x, y, color="black"):
        canvas_x, canvas_y = self.grid_to_canvas(x, y)
        self.canvas.create_rectangle(
            canvas_x, canvas_y, canvas_x + self.pixel_size, canvas_y - self.pixel_size,
            fill=color, outline=color
        )

    def dda_line(self, x1, y1, x2, y2, color):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x1, y1
        for _ in range(int(steps) + 1):
            self.draw_pixel(round(x), round(y), color)
            x += x_inc
            y += y_inc

    def step_by_step_line(self, x1, y1, x2, y2, color):
        if abs(x2 - x1) > abs(y2 - y1):  # Если линия больше по ширине
            if x1 > x2:  # Меняем местами начальную и конечную точки
                x1, x2, y1, y2 = x2, x1, y2, y1
                 
            k = (y2 - y1) / (x2 - x1)
            b = y1 - round(k * x1)
            for x in range(x1, x2 + 1):
                y = k * x + b
                self.draw_pixel(x, round(y), color)
        else:  # Если линия больше по высоте
            if y1 > y2:  # Меняем местами начальную и конечную точки
                x1, x2, y1, y2 = x2, x1, y2, y1

            k = (x2 - x1) / (y2 - y1)
            b = x1 - round(k * y1)
            for y in range(y1, y2 + 1):
                x = k * y + b
                self.draw_pixel(round(x), y, color)

    def bresenham_line(self, x1, y1, x2, y2, color):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            self.draw_pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def bresenham_circle(self, xc, yc, r, color):
        x = 0
        y = r
        d = 3 - 2 * r
        self.draw_circle_points(xc, yc, x, y, color)
        while y >= x:
            x += 1
            if d > 0:
                y -= 1
                d += 4 * (x - y) + 10
            else:
                d += 4 * x + 6
            self.draw_circle_points(xc, yc, x, y, color)

    def draw_circle_points(self, xc, yc, x, y, color):
        points = [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x),
        ]
        for px, py in points:
            self.draw_pixel(px, py, color)

    def log_action(self, message):
        self.log_box.insert(tk.END, message)
        self.log_box.see(tk.END)

    def select_point(self, event):
        grid_x, grid_y = self.canvas_to_grid(event.x, event.y)
        if self.algorithm.get() in {"Брезенхем (линия)", "ЦДА (линия)", "Пошаговый (линия)"}:
            if self.start_point is None:
                self.start_point = (grid_x, grid_y)
                self.draw_pixel(grid_x, grid_y, "blue")
            else:
                self.end_point = (grid_x, grid_y)
                x1, y1 = self.start_point
                x2, y2 = self.end_point
                current_color = self.line_colors[self.color_index]

                start_time = time.perf_counter_ns()

                if self.algorithm.get() == "ЦДА (линия)":
                    self.dda_line(x1, y1, x2, y2, current_color)
                elif self.algorithm.get() == "Пошаговый (линия)":
                    self.step_by_step_line(x1, y1, x2, y2, current_color)
                else:  # Брезенхем (линия)
                    self.bresenham_line(x1, y1, x2, y2, current_color)

                end_time = time.perf_counter_ns()
                elapsed_time_ms = (end_time - start_time) / 1000

                self.log_action(f"Линия: ({x1}, {y1}) -> ({x2}, {y2}), Алгоритм: {self.algorithm.get()}, ")
                self.log_action(f"Время: {elapsed_time_ms:.1f} мкс")

                self.color_index = (self.color_index + 1) % len(self.line_colors)
                self.start_point = None
                self.end_point = None

        elif self.algorithm.get() == "Брезенхем (окружность)":
            if self.start_point is None:
                self.start_point = (grid_x, grid_y)
                self.draw_pixel(grid_x, grid_y, "blue")
            else:
                xc, yc = self.start_point
                radius = int(((grid_x - xc) ** 2 + (grid_y - yc) ** 2) ** 0.5)
                current_color = self.line_colors[self.color_index]

                start_time = time.perf_counter_ns()
                self.bresenham_circle(xc, yc, radius, current_color)
                end_time = time.perf_counter_ns()
                elapsed_time_ms = (end_time - start_time) / 1000

                self.log_action(f"Окружность: Центр ({xc}, {yc}), Радиус: {radius},")
                self.log_action(f"\n Алгоритм: {self.algorithm.get()}, Время: {elapsed_time_ms:.1f} мкс")

                self.color_index = (self.color_index + 1) % len(self.line_colors)
                self.start_point = None


    def clear_canvas(self):
        self.canvas.delete("all")
        self.log_action("--- Очистка холста ---")
        self.draw_grid()
        self.draw_axes()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
