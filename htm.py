import tkinter as tk
from tkinter import font, ttk
import json
import random
import os


class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.styles = self.load_styles()  # Загрузка стилей
        self.apply_window_styles()
        # self.root.attributes("-fullscreen", True)

        # Загрузка вопросов
        self.load_questions()

        # Переменная для отслеживания состояния игры
        self.current_question = None
        self.selected_button = None
        self.first_click_done = False

        # Привязка клавиш
        self.bind_keys()

        # Показать стартовое окно
        self.show_start_screen()

    def load_styles(self):
        # Загружаем стили из JSON-файла
        with open("styles.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def apply_window_styles(self):
        # Применяем стили к окну приложения
        self.root.title(self.styles["window"]["title"])
        self.root.geometry(self.styles["window"]["geometry"])
        self.root.configure(bg=self.styles["window"]["bg_color"])

        # Создаём шрифты на основе стилей
        self.question_font = font.Font(**self.styles["fonts"]["question_font"])
        self.option_font = font.Font(**self.styles["fonts"]["option_font"])

        # Настройка стилей для ttk-кнопок
        style = ttk.Style(self.root)
        style.theme_use("clam")  # Устанавливаем тему "clam" для корректной работы кастомных стилей
        # Обычные кнопки
        style.configure(
            "Rounded.TButton",
            background=self.styles["button"]["bg_color"],
            foreground=self.styles["button"]["fg_color"],
            font=(self.styles["fonts"]["option_font"]["family"], self.styles["fonts"]["option_font"]["size"]),
            padding=self.styles["button"]["padding"],
            borderwidth=self.styles["button"]["borderwidth"],
            width=self.styles["button"]["width"],  # Фиксированная ширина кнопки
            height=self.styles["button"]["height"]   # Фиксированная высота кнопки
        )
        style.map(
            "Rounded.TButton",
            background=[("active", self.styles["button"]["active_bg"])],
            foreground=[("active", self.styles["button"]["active_fg"])]
        )
        # Кнопка выхода (Уже, чем остальные)
        style.configure(
            "Exit.TButton",
            background=self.styles["exit_button"]["bg_color"],
            foreground=self.styles["exit_button"]["fg_color"],
            font=(self.styles["fonts"]["option_font"]["family"], self.styles["fonts"]["option_font"]["size"]),
            padding=self.styles["exit_button"]["padding"],
            borderwidth=self.styles["exit_button"]["borderwidth"],
            width=self.styles["exit_button"]["width"],  # Фиксированная ширина кнопки
            height=self.styles["exit_button"]["height"]  # Фиксированная высота кнопки
        )
        style.map(
            "Exit.TButton",
            background=[("active", self.styles["exit_button"]["active_bg"])],
            foreground=[("active", self.styles["exit_button"]["active_fg"])]
        )
        # Добавляем стили для различных состояний кнопок
        # Жёлтый - ответ выбран, время на обсуждение выбранного варианта. ИЗМЕНИТЬ СОСТОЯНИЕ НЕЛЬЗЯ
        style.configure(
            "Yellow.TButton",
            background=self.styles["button"]["option_bg"],
            foreground="black",
            font=(self.styles["fonts"]["option_font"]["family"], self.styles["fonts"]["option_font"]["size"]),
            padding=self.styles["button"]["padding"],
            borderwidth=self.styles["button"]["borderwidth"],
            width=self.styles["button"]["width"],  # Фиксированная ширина кнопки
            height=self.styles["button"]["height"]   # Фиксированная высота кнопки
        )
        # Убираем уветную подсветку при наведении курсора на кнопку
        style.map(
            "Yellow.TButton",
            background=[],  # Пустой список убирает изменение цвета при наведении
            foreground=[]   # Оставляем цвет текста неизменным
        )
        # Неправильный ответ
        style.configure(
            "Red.TButton",
            background=self.styles["button"]["incorrect_bg"],
            foreground="white",
            font=(self.styles["fonts"]["option_font"]["family"], self.styles["fonts"]["option_font"]["size"]),
            padding=self.styles["button"]["padding"],
            borderwidth=self.styles["button"]["borderwidth"],
            width=self.styles["button"]["width"],  # Фиксированная ширина кнопки
            height=self.styles["button"]["height"]   # Фиксированная высота кнопки
        )
        # Убираем уветную подсветку при наведении курсора на кнопку
        style.map(
            "Red.TButton",
            background=[],  # Пустой список убирает изменение цвета при наведении
            foreground=[]   # Оставляем цвет текста неизменным
        )
        # Правильный ответ
        style.configure(
            "Green.TButton",
            background=self.styles["button"]["correct_bg"],
            #foreground="white",
            font=(self.styles["fonts"]["option_font"]["family"], self.styles["fonts"]["option_font"]["size"]),
            padding=self.styles["button"]["padding"],
            borderwidth=self.styles["button"]["borderwidth"],
            width=self.styles["button"]["width"],  # Фиксированная ширина кнопки
            height=self.styles["button"]["height"]   # Фиксированная высота кнопки
        )
        # Убираем уветную подсветку при наведении курсора на кнопку
        style.map(
            "Green.TButton",
            background=[],  # Пустой список убирает изменение цвета при наведении
            foreground=[]   # Оставляем цвет текста неизменным
        )

    def load_questions(self):
        # Загружаем вопросы из JSON-файла
        with open("questions.json", "r", encoding="utf-8") as file:
            self.questions = json.load(file)

    def show_start_screen(self):
        self.clear_screen()

        welcome_label = tk.Label(
            self.root,
            text="Welcome to the Guess game!",
            font=self.question_font,
            bg=self.styles["window"]["bg_color"],
            fg=self.styles["label"]["fg_color"],
            wraplength=self.styles["label"]["wraplength"],
            justify=self.styles["label"]["justify"]
        )
        welcome_label.pack(pady=100)

        start_button = ttk.Button(
            self.root,
            text="Start game",
            style="Rounded.TButton",
            command=self.start_game
        )
        start_button.pack(pady=20)

    def setup_ui(self):
        # Картинка
        self.image_label = tk.Label(self.root, bg=self.styles["window"]["bg_color"])
        self.image_label.pack(pady=10)

        # Вопрос
        self.question_label = tk.Label(
            self.root,
            text="",
            font=self.question_font,
            bg=self.styles["window"]["bg_color"],
            fg=self.styles["label"]["fg_color"],
            wraplength=self.styles["label"]["wraplength"],
            justify=self.styles["label"]["justify"]
        )
        self.question_label.pack(pady=20)

        # Кнопки для ответов
        self.buttons_frame = tk.Frame(self.root, bg=self.styles["window"]["bg_color"])
        self.buttons_frame.pack(pady=20)

        self.buttons = []
        for i in range(4):
            button = ttk.Button(
                self.buttons_frame,
                text="",
                style="Rounded.TButton",
                command=lambda i=i: self.handle_first_click(i)
            )
            self.buttons.append(button)

            # Расположение кнопок в сетке (2x2)
            row, col = divmod(i, 2)
            button.grid(row=row, column=col, padx=10, pady=10)

        # Кнопка для следующего вопроса
        self.next_button = ttk.Button(
            self.root,
            text="Next question",
            style="Rounded.TButton",
            command=self.load_next_question
        )
        self.next_button.place(relx=0.5, rely=0.9, anchor="center")  # Центрирование кнопки
        self.next_button.pack_forget()  # Скрыть кнопку до ответа

        # Кнопка для выхода из игры
        self.exit_button = ttk.Button(
            self.root,
            text="Exit game",
            style="Exit.TButton",
            command=self.root.quit
        )
        self.exit_button.pack(side="right", anchor="se", padx=10, pady=10)

    def load_next_question(self):
        # Сброс состояния кнопок
        for button in self.buttons:
            button.config(text="", state="normal", style="Rounded.TButton")
        self.next_button.place_forget()  # Скрыть кнопку "Следуюший вопрос" до ответа
        self.selected_button = None
        self.first_click_done = False

        if not self.questions:
            self.end_game()
            return

        self.current_question = random.choice(self.questions)
        self.questions.remove(self.current_question)

        # Загрузка картинки, если она есть
        image_path = self.current_question.get("image")
        if image_path and os.path.exists(f"images/{image_path}"):
            photo = tk.PhotoImage(file=f"images/{image_path}")
            # Ограничение размеров изображения через subsample (например, уменьшить в 2 раза)
            max_width, max_height = 400, 300  # Максимальная ширина и высота в пикселях
            width, height = photo.width(), photo.height()
            scale_x = max(1, width // max_width)  # Вычисляем коэффициент уменьшения
            scale_y = max(1, height // max_height)
            scale = max(scale_x, scale_y)  # Используем максимальный коэффициент

            photo = photo.subsample(scale, scale)

            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            self.image_label.config(image="")

        self.question_label.config(text=self.current_question["question"])
        for i, option in enumerate(self.current_question["options"]):
            self.buttons[i].config(
                text=option,
                state="normal",
                command=lambda i=i: self.handle_first_click(i)
            )

        self.correct_option = self.current_question["correct"]
        self.result_image_path = self.current_question.get("result_image")

    def bind_keys(self):
        """Привязка клавиш 1, 2, 3, 4 к кнопкам."""
        self.root.bind("1", lambda event: self.handle_first_click(0))
        self.root.bind("2", lambda event: self.handle_first_click(1))
        self.root.bind("3", lambda event: self.handle_first_click(2))
        self.root.bind("4", lambda event: self.handle_first_click(3))
        self.root.bind("s", lambda event: self.start_game())
        self.root.bind("n", lambda event: self.load_next_question())
        self.root.bind("e", lambda event: self.root.quit())

    def handle_first_click(self, index):
        if not self.first_click_done:
            self.first_click_done = True
            self.selected_button = index
            # Подсвечиваем выбранную кнопку в жёлтый
            self.buttons[index].config(style="Yellow.TButton")
            for i, button in enumerate(self.buttons):
                if i != index:
                    button.state(["disabled"])
        else:
            self.handle_second_click(index)

    def handle_second_click(self, index):
        if index != self.correct_option:
            # Окрашиваем выбранную кнопку в красный
            self.buttons[index].config(style="Red.TButton")
        # Сбрасываем состояние кнопки, чтобы применить стиль
        self.buttons[self.correct_option].config(state="normal")
        # Подсвечиваем правильный ответ в зелёный
        self.buttons[self.correct_option].config(style="Green.TButton")

        # Замена картинки на результат, если указано
        if self.result_image_path and os.path.exists(f"images/{self.result_image_path}"):
            photo = tk.PhotoImage(file=f"images/{self.result_image_path}")
            self.image_label.config(image=photo)
            self.image_label.image = photo

        # Если вопросов больше нет, показать финальное окно с задержкой
        if not self.questions:
            self.root.after(2000, self.end_game)  # Задержка 2 секунды
        else:
            # Показать кнопку "Следующий вопрос" Центрирование кнопки
            self.next_button.place(relx=0.5, rely=0.9, anchor="center")

    def start_game(self):
        self.clear_screen()
        self.setup_ui()
        self.load_next_question()

    def end_game(self):
        self.clear_screen()
        end_label = tk.Label(
            self.root,
            text="Game over! Thanks for playing",
            font=self.question_font,
            bg=self.styles["window"]["bg_color"],
            fg=self.styles["label"]["fg_color"],
            wraplength=self.styles["label"]["wraplength"],
            justify=self.styles["label"]["justify"]
        )
        end_label.pack(pady=100)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = MillionaireGame(root)
    root.mainloop()
