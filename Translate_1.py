import customtkinter
import sqlite3
from datetime import date
from googletrans import Translator
from CTkListbox import *


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


def translate():
    """Функция для перевода м сохранения в db"""

    for launguage, suffix in languages.items():
        if comboTwo.get() == suffix:
            date_now = str(date.today())
            text = t_input.get('1.0', 'end')
            translation = translator.translate(text, dest=suffix)  # принимает текст и суффикс языка
            t_output.delete('1.0', 'end')
            t_output.insert('0.0', translation.text)
            cur.execute("INSERT INTO translate_list (text, translation, date_now) VALUES (?,?,?)",
                        (text, translation.text.rstrip(), date_now))
            conn.commit()
            list_display()


def delete_translate():
    """Функция для удаления переведенных запросов"""
    index = list_translate.curselection()
    if index:
        selected_list_display = list_translate.get(index[0])
        cur.execute("DELETE FROM translate_list WHERE id=?", (selected_list_display[0],))
        list_display()


def list_display():
    """ Метода для обнавления данных из таблиуы 'translation' и отображения в list_translate"""
    list_translate.delete(0, customtkinter.END)
    cur.execute("SELECT * FROM translate_list")
    title = cur.fetchall()
    for t in reversed(title):
        list_translate.insert(customtkinter.END, (t[0], f"Текст: {t[1]}\n"
                                                        f"Перевод: {t[2]}\n"
                                                        f"Дата: {t[3]}\n"
                                                        f"{'=' * 30}\n"))


app = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
app.geometry('500x450')
app.title('Translate_1')
app.resizable(width=False, height=False)
translator = Translator()

languages = {'Русский': 'ru', 'English': 'en'}  # можно и другие языки добавлять

header_frame = customtkinter.CTkFrame(app, )
header_frame.pack()  # fill=x - растяжение рамки по X

header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=1)
header_frame.grid_columnconfigure(2, weight=1)

comboOne = customtkinter.CTkComboBox(header_frame,
                                     font=('Caveat', 20),
                                     values=[lang for lang in languages.values()],
                                     state='readonly',
                                     width=165
                                     )  # state=readonly запрещает изменять размеры в виджите
comboOne.set(languages['Русский'])   # curent(0) по умолчанию вывод элемента с индексом 0
comboOne.grid(row=0, column=0, pady=5, padx=5)  # вывод виджета в нулевой строке в нулевом столбце

btn = customtkinter.CTkButton(header_frame,
                              text='Перевести',
                              font=('Caveat', 20),
                              fg_color='green',
                              command=translate,
                              width=165,
                              )
btn.grid(row=0, column=1, pady=5, padx=5)

comboTwo = customtkinter.CTkComboBox(header_frame,
                                     font=('Caveat', 20),
                                     values=[lang for lang in languages.values()],
                                     state='readonly',
                                     width=165
                                     )  # state=readonly запрещает изменять размеры в виджите
comboTwo.set(languages['English'])
comboTwo.grid(row=0, column=2, pady=5, padx=5)

translate_frame = customtkinter.CTkFrame(app)
translate_frame.pack()

translate_frame.grid_columnconfigure(0, weight=1)
translate_frame.grid_columnconfigure(1, weight=1)

t_input = customtkinter.CTkTextbox(translate_frame,
                                   font=('Caveat', 15),
                                   width=245
                                   )
t_input.grid(row=0, column=0, pady=5, padx=5)

t_output = customtkinter.CTkTextbox(translate_frame,
                                    font=('Caveat', 15),
                                    width=245
                                    )
t_output.grid(row=0, column=1, pady=5, padx=5)

db_frame = customtkinter.CTkFrame(app, )
db_frame.pack()

list_translate = CTkListbox(db_frame,
                            font=('Caveat', 15),
                            width=450,
                            height=130,
                            multiple_selection=True,
                            )
list_translate.grid(row=0, column=0, padx=5, pady=5)

db_del_frame = customtkinter.CTkFrame(app, )
db_del_frame.pack()

db_del_frame.grid_columnconfigure(0, weight=1)
db_del_frame.grid_columnconfigure(1, weight=1)

# del_label = customtkinter.CTkLabel(db_del_frame,
#                                    text='None',
#                                    font=('Caveat', 15),
#                                    width=350)
# del_label.grid(row=0, column=1, pady=5)

del_btn = customtkinter.CTkButton(db_del_frame,
                                  text='Удалить',
                                  font=('Caveat', 20),
                                  fg_color='green',
                                  command=delete_translate
                                  )
del_btn.grid(row=0, column=0, pady=1)

db_start()

list_display()

app.mainloop()

conn.close()
