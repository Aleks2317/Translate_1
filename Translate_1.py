import tkinter as tk
import customtkinter
import sqlite3
from datetime import date
from googletrans import Translator


def db_start():
    """ Метод для создания таблицы 'translate_list' со столбцами:
     id - id с автоматическим добавлением ключа;
     text - вводимый текст для перевода;
     translation - переведенный текст;
     date_now - дата запроса на перевод (автоматически устанавливается)
     """
    global conn, cur
    conn = sqlite3.connect('translate_list.db')  # 17 подключение к db с помощью connect
    cur = conn.cursor()  # 18 создание объекта курсора
    # 19 запрос создание таблицы только в том случае если в db ее нет
    cur.execute("""CREATE TABLE IF NOT EXISTS translate_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    translation TEXT,
    date_now TEXT)""")


def delete_translate():
    """Функция для удаления переведенных запросов"""
    index = list_translate_display.curselection()
    print(f"{index = }")


def list_translates_display():
    """ Метода для выборки данных из таблиуы 'translation' и отображения в  """
    list_translate_display.delete('1.0', 'end')
    cur.execute("SELECT id, text, translation, date_now FROM translate_list")

    title = cur.fetchall()
    for i, t, tr, d in [titl for titl in reversed(title)]:
        list_translate_display.insert(customtkinter.END, f'{"*" * 10} id = {i}. {"Ввод"}{"*" * 10}\n\n'
                                                         f'{t.strip()}\n\n'
                                                         f'{"*" * 10}{"Перевод"}{"*" * 10}\n\n'
                                                         f'{tr.strip()}\n\n'
                                                         f'{"_" * 10}{"Дата: "}{d}{"_" * 10}\n\n')


# 13 создадим функцию для перевода
def translate():
    """Функция для перевода"""
    for launguage, suffix in languages.items():
        print(comboTwo.get())
        if comboTwo.get() == suffix:
            date_now = str(date.today())
            text = t_input.get('1.0', 'end')
            translation = translator.translate(text, dest=suffix)  # принимает текст и суффикс языка
            print(f'{comboTwo.get() = }'
                  f'\n{text = }'
                  f'\n{date_now = }'
                  f'\n{translation.text = }')
            t_output.delete('1.0', 'end')
            t_output.insert('0.0', translation.text)
            cur.execute("INSERT INTO translate_list (text, translation, date_now) VALUES (?,?,?)",
                        (text, translation.text.rstrip(), date_now))
            conn.commit()
            list_translates_display()




# 1 окно
app = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
app.geometry('500x450')
app.title('Translate_1')
app.resizable(width=False, height=False)
translator = Translator()

# 2 создадим словарь с языками
languages = {'Русский': 'ru', 'English': 'en'}  # можно и другие языки добавлять

# 3 создаем рамку
header_frame = customtkinter.CTkFrame(app, )
header_frame.pack()  # fill=x - растяжение рамки по X

# 4 создадим внутри рамки столбцы
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=1)
header_frame.grid_columnconfigure(2, weight=1)

# 5 создание виджета comboOne для отображения языков первого значения
comboOne = customtkinter.CTkComboBox(header_frame,
                                     font=('Caveat', 20),
                                     values=[lang for lang in languages.values()],
                                     state='readonly',
                                     width=165
                                     )  # state=readonly запрещает изменять размеры в виджите
comboOne.set(languages['Русский'])   # curent(0) по умолчанию вывод элемента с индексом 0
comboOne.grid(row=0, column=0, pady=5, padx=5)  # вывод виджета в нулевой строке в нулевом столбце

# 6 создание кнопки при нажатии на которую будет производиться перевод
btn = customtkinter.CTkButton(header_frame,
                              text='Перевести',
                              font=('Caveat', 20),
                              fg_color='green',
                              command=translate,
                              width=165,
                              )
btn.grid(row=0, column=1, pady=5, padx=5)

# 7 создание виджета comboOne для отображения языков второго значения
comboTwo = customtkinter.CTkComboBox(header_frame,
                                     font=('Caveat', 20),
                                     values=[lang for lang in languages.values()],
                                     state='readonly',
                                     width=165
                                     )  # state=readonly запрещает изменять размеры в виджите
comboTwo.set(languages['English'])  # curent(1) по умолчанию вывод элемента с индексом 1
comboTwo.grid(row=0, column=2, pady=5, padx=5)  # вывод виджета в нулевой строке втором столбце

# 8 рамка с полями с текстом
translate_frame = customtkinter.CTkFrame(app)
translate_frame.pack()

# 9 разделяем поля на два столбца
translate_frame.grid_columnconfigure(0, weight=1)
translate_frame.grid_columnconfigure(1, weight=1)

# 10 создание текстового поля для вводимого текста
t_input = customtkinter.CTkTextbox(translate_frame,
                                   font=('Caveat', 15),
                                   width=245
                                   )
t_input.grid(row=0, column=0, pady=5, padx=5)

# 11 создание второго текстового поля для отображения перевода
t_output = customtkinter.CTkTextbox(translate_frame,
                                    font=('Caveat', 15),
                                    width=245
                                    )
t_output.grid(row=0, column=1, pady=5, padx=5)


# добавим рамку для вывода прошлых запросов с возможностью удаления выбранной строки
db_frame = customtkinter.CTkFrame(app, )
db_frame.pack()

# 12 текстовое поле для отображения последних переводов только для чтения
list_translate_display = customtkinter.CTkTextbox(db_frame,
                                                  font=('Caveat', 15),
                                                  width=490,
                                                  height=130,
                                                  activate_scrollbars=True,  # активация прокрутки
                                                  )
list_translate_display.grid(row=0, column=0, padx=5, pady=5)

db_del_frame = customtkinter.CTkFrame(app, )
db_del_frame.pack()

# внизу текстового поля предыдущих запросов создадим лейбл и кнопку удалить
db_del_frame.grid_columnconfigure(0, weight=1)
db_del_frame.grid_columnconfigure(1, weight=1)

del_label = customtkinter.CTkLabel(db_del_frame,
                                   font=('Caveat', 15),
                                   width=350)
del_label.grid(row=0, column=1, pady=5)

del_btn = customtkinter.CTkButton(db_del_frame,
                                  text='Удалить',
                                  font=('Caveat', 20),
                                  fg_color='green',
                                  command=delete_translate
                                  )
del_btn.grid(row=0, column=0, pady=1)

db_start()
list_translates_display()
app.mainloop()
conn.close()