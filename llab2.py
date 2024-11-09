import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import site
print(site.getsitepackages())
original_image = None
contrast_stretched_image = None
original_image2 = None
equalized_image = None
image1 = None
image2 = None

def linear_contrast_stretching(image, alpha=1.5, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def histogram_equalization(image):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    channels = list(cv2.split(ycrcb))
    channels[0] = cv2.equalizeHist(channels[0])
    equalized_ycrcb = cv2.merge(channels)
    equalized_image = cv2.cvtColor(equalized_ycrcb, cv2.COLOR_YCrCb2BGR)
    return equalized_image

def load_image():
    global original_image, contrast_stretched_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = cv2.imread(file_path)
        if original_image is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
            return
        update_contrast()
        update_histogram_equalization()

def update_contrast():
    global original_image, contrast_stretched_image
    if original_image is None:
        return
    alpha = alpha_slider.get()
    beta = beta_slider.get()
    contrast_stretched_image = linear_contrast_stretching(original_image, alpha=alpha, beta=beta)
    show_linear_contrast()

def show_linear_contrast():
    original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    contrast_stretched_rgb = cv2.cvtColor(contrast_stretched_image, cv2.COLOR_BGR2RGB)
    original_photo = ImageTk.PhotoImage(Image.fromarray(original_rgb))
    contrast_photo = ImageTk.PhotoImage(Image.fromarray(contrast_stretched_rgb))
    original_label.config(image=original_photo)
    original_label.image = original_photo
    contrast_label.config(image=contrast_photo)
    contrast_label.image = contrast_photo

def update_histogram_equalization():
    global original_image2, equalized_image
    if original_image2 is None:
        return
    equalized_image = histogram_equalization(original_image2)
    show_histogram_equalization()

def show_histogram_equalization():
    original_rgb2 = cv2.cvtColor(original_image2, cv2.COLOR_BGR2RGB)
    equalized_rgb = cv2.cvtColor(equalized_image, cv2.COLOR_BGR2RGB)
    original_photo2 = ImageTk.PhotoImage(Image.fromarray(original_rgb2))
    equalized_photo = ImageTk.PhotoImage(Image.fromarray(equalized_rgb))
    original_label2.config(image=original_photo2)
    original_label2.image = original_photo2
    equalized_label.config(image=equalized_photo)
    equalized_label.image = equalized_photo

def load_image_for_equalization():
    global original_image2
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image2 = cv2.imread(file_path)
        if original_image2 is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
            return
        update_histogram_equalization()

def load_image1():
    global image1
    file_path = filedialog.askopenfilename()
    if file_path:
        image1 = cv2.imread(file_path)
        if image1 is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
            return
        show_image1()

def load_image2():
    global image2
    file_path = filedialog.askopenfilename()
    if file_path:
        image2 = cv2.imread(file_path)
        if image2 is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
            return
        show_image2()

def show_image1():
    if image1 is not None:
        img_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_photo = ImageTk.PhotoImage(img_pil)
        image1_label.config(image=img_photo)
        image1_label.image = img_photo

def show_image2():
    if image2 is not None:
        img_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_photo = ImageTk.PhotoImage(img_pil)
        image2_label.config(image=img_photo)
        image2_label.image = img_photo

def add_images(image1, image2):
    return cv2.add(image1, image2)

def subtract_images(image1, image2):
    return cv2.subtract(image1, image2)

def multiply_images(image1, image2):
    return cv2.multiply(image1, image2)

def divide_images(image1, image2):
    return cv2.divide(image1, image2)

def perform_operations():
    if image1 is None or image2 is None:
        messagebox.showerror("Ошибка", "Необходимо загрузить два изображения.")
        return
    if image1.shape != image2.shape:
        messagebox.showerror("Ошибка", "Изображения должны иметь одинаковые размеры.")
        return
    added_image = add_images(image1, image2)
    subtracted_image = subtract_images(image1, image2)
    multiplied_image = multiply_images(image1, image2)
    divided_image = divide_images(image1, image2)
    show_operations(added_image, subtracted_image, multiplied_image, divided_image)

def show_operations(added, subtracted, multiplied, divided):
    added_image = Image.fromarray(cv2.cvtColor(added, cv2.COLOR_BGR2RGB))
    subtracted_image = Image.fromarray(cv2.cvtColor(subtracted, cv2.COLOR_BGR2RGB))
    multiplied_image = Image.fromarray(cv2.cvtColor(multiplied, cv2.COLOR_BGR2RGB))
    divided_image = Image.fromarray(cv2.cvtColor(divided, cv2.COLOR_BGR2RGB))
    added_photo = ImageTk.PhotoImage(added_image)
    subtracted_photo = ImageTk.PhotoImage(subtracted_image)
    multiplied_photo = ImageTk.PhotoImage(multiplied_image)
    divided_photo = ImageTk.PhotoImage(divided_image)
    added_label.config(image=added_photo)
    added_label.image = added_photo
    subtracted_label.config(image=subtracted_photo)
    subtracted_label.image = subtracted_photo
    multiplied_label.config(image=multiplied_photo)
    multiplied_label.image = multiplied_photo
    divided_label.config(image=divided_photo)
    divided_label.image = divided_photo

root = tk.Tk()
root.title("Эквализация и контрастирование изображения")

contrast_frame = tk.Frame(root)
contrast_frame.grid(row=0, column=0, padx=10, pady=10)

load_button = tk.Button(contrast_frame, text="Загрузить изображение", command=load_image)
load_button.grid(row=0, column=0, columnspan=2)

original_label = tk.Label(contrast_frame, text="Оригинальное изображение")
original_label.grid(row=1, column=0, padx=5, pady=5)

contrast_label = tk.Label(contrast_frame, text="Контрастированное изображение")
contrast_label.grid(row=2, column=0, padx=5, pady=5)

alpha_slider = tk.Scale(contrast_frame, from_=1, to=5, resolution=0.1, orient=tk.HORIZONTAL, label='Alpha')
alpha_slider.set(1.5)
alpha_slider.grid(row=3, column=0, padx=5, pady=5)

beta_slider = tk.Scale(contrast_frame, from_=-100, to=100, orient=tk.HORIZONTAL, label='Beta')
beta_slider.set(0)
beta_slider.grid(row=4, column=0, padx=5, pady=5)

alpha_slider.bind("<Motion>", lambda event: update_contrast())
beta_slider.bind("<Motion>", lambda event: update_contrast())

histogram_frame = tk.Frame(root)
histogram_frame.grid(row=0, column=1, padx=10, pady=10)

load_equalization_button = tk.Button(histogram_frame, text="Загрузить изображение для эквализации", command=load_image_for_equalization)
load_equalization_button.grid(row=0, column=0, padx=5, pady=5)
original_label2 = tk.Label(histogram_frame, text="Оригинальное изображение")
original_label2.grid(row=1, column=0, padx=5, pady=5)

equalized_label = tk.Label(histogram_frame, text="Эквализированное изображение")
equalized_label.grid(row=2, column=0, padx=5, pady=5)

operations_frame = tk.Frame(root)
operations_frame.grid(row=0, column=2, padx=10, pady=10)

load_button1 = tk.Button(operations_frame, text="Загрузить первое изображение", command=load_image1)
load_button1.grid(row=0, column=0, padx=5, pady=5)

load_button2 = tk.Button(operations_frame, text="Загрузить второе изображение", command=load_image2)
load_button2.grid(row=0, column=1, padx=5, pady=5)

image1_label = tk.Label(operations_frame, text="Первое изображение")
image1_label.grid(row=1, column=0, padx=5, pady=5)

image2_label = tk.Label(operations_frame, text="Второе изображение")
image2_label.grid(row=1, column=1, padx=5, pady=5)

operation_button = tk.Button(operations_frame, text="Выполнить операции", command=perform_operations)
operation_button.grid(row=2, column=0, columnspan=2, pady=10)

results_frame = tk.Frame(operations_frame)
results_frame.grid(row=3, column=0, columnspan=2)

added_label = tk.Label(results_frame, text="Сложение")
added_label.grid(row=0, column=0, padx=5, pady=5)

subtracted_label = tk.Label(results_frame, text="Вычитание")
subtracted_label.grid(row=0, column=1, padx=5, pady=5)

multiplied_label = tk.Label(results_frame, text="Умножение")
multiplied_label.grid(row=1, column=0, padx=5, pady=5)

divided_label = tk.Label(results_frame, text="Деление")
divided_label.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()