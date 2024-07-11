import customtkinter
from tkinter import *
from googletrans import Translator


# 11 создадим функцию для перевода
def translate():
    for launguage, suffix in languages.items():
        if comboTwo.get() == launguage:
            text = t_input.get('1.0', END)
            translation = translator.translate(text, dest=suffix)  # принимает текст и суффикс языка
            t_output.delete('1.0', END)
            t_output.insert('1.0', translation.text)


# 1 окно
app = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
app.geometry('500x300')
app.title('Translate_1')
app.resizable(width=False, height=False)
translator = Translator()

# 2 создадим словарь с языками
languages = {'Русский': 'ru', 'English': 'en'}  # можно и другие языки добавлять

# 3 создаем рамку
header_frame = customtkinter.CTkFrame(app, )
header_frame.pack(fill=X)  # fill=x - растяжение рамки по X

# 4 создадим внутри рамки сталбцы
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=1)
header_frame.grid_columnconfigure(2, weight=1)

# 5 создание виджета comboOne для отображения языков первого значения
comboOne = customtkinter.CTkComboBox(header_frame,
                                     font=('Caveat', 20),
                                     values=[lang for lang in languages],
                                     state='readonly')  # state=readonly запрещает изменять размеры в виджите
comboOne.set(languages['Русский'])   # curent(0) по умолчанию вывод элемента с индексом 0
comboOne.grid(row=0, column=0, pady=5)  # вывод виджета в нулевой строке в нулевом столбце

# # 6 создание кнопки при нажатии на которую будет производиться перевод
btn = customtkinter.CTkButton(header_frame, text='Перевести', font=('Caveat', 20), fg_color='green', command=translate)
btn.grid(row=0, column=1, pady=5)

# 7 создание виджета comboOne для отображения языков второго значения
comboTwo = customtkinter.CTkComboBox(header_frame,
                                     font=('Caveat', 20),
                                     values=[lang for lang in languages],
                                     state='readonly')  # state=readonly запрещает изменять размеры в виджите
comboTwo.set(languages['English'])  # curent(1) по умолчанию вывод элемента с индексом 1
comboTwo.grid(row=0, column=2, pady=5)  # вывод виджета в нулевой строке втором столбце

# 8 рамка с полями с текстом
translate_frame = customtkinter.CTkFrame(app)
translate_frame.pack(fill=X)

# 9 разделяем поля на два столбца
translate_frame.grid_columnconfigure(0, weight=1)
translate_frame.grid_columnconfigure(1, weight=1)

# 10 создание текстового поля для вводимого текста
t_input = customtkinter.CTkTextbox(translate_frame, font=('Caveat', 20))
t_input.grid(row=0, column=0, pady=5)

# 11 создание второго текстового поля для отображения перевода
t_output = customtkinter.CTkTextbox(translate_frame, font=('Caveat', 20))
t_output.grid(row=0, column=1, pady=5)

# 12 текстовое поле для отображения последних переводов
db_enter = customtkinter.CTkTextbox(app, font=('Caveat', 20))
db_enter.pack(pady=5)

app.mainloop()
