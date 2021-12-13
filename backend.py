import sqlite3
import os

path = "C:/ProgramData/mahab_db"
if not os.path.isdir(path) is True:
    if os.path.isdir("C:/ProgramData") is True:
        os.mkdir(path)
    else:
        os.mkdir("C:/ProgramData")
        os.mkdir(path)

path = f"{path}/mahab.db"

def connect_user():
    conn = sqlite3.connect(path)
    cor = conn.cursor()
    cor.execute(
        'CREATE TABLE IF NOT EXISTS table_user (first_name text,last_name text,user_name text,password text,image text DEFAULT icon, login text, count_see text )'
    )
    conn.commit()
    conn.close()

def connect_seeting():
    conn = sqlite3.connect(path)
    cor = conn.cursor()
    cor.execute(
        'CREATE TABLE IF NOT EXISTS setting (max_amount INTEGER , min_amount Integer , font text, font_size INTEGER ,start_with_win text, bg text, fg text, path_di text)'
    )
    conn.commit()
    conn.close()


def insert_user(first_name, last_name, user_name, password, image, login, count_see):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO table_user VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name,user_name, password, image, login, count_see)
    )
    conn.commit()
    conn.close()


def insert_setting(max_amount, min_amount, font, font_size, start_with_win, bg, fg, path_di):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO setting VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (max_amount, min_amount, font, font_size, start_with_win, bg, fg, path_di)
    )
    conn.commit()
    conn.close()


def view_user():
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM table_user"
    )
    info = cur.fetchall()
    conn.commit()
    conn.close()
    return info


def view_setting():
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM setting"
    )
    setting = cur.fetchall()
    conn.commit()
    conn.close()
    return setting


def update_user(first_name, last_name,user_name, password, image, login, count_see):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE table_user SET first_name=?, last_name=?,user_name=?,password=?, image=?, login=?, count_see=?", (first_name, last_name,user_name,password, image, login, count_see)
    )
    conn.commit()
    conn.close()


def update_setting(max_amount, min_amount, font, font_size, start_with_win, bg, fg):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE setting SET max_amount=?, min_amount=?, font=?, font_size=?, start_with_win=?, bg=?, fg=?", (max_amount, min_amount, font, font_size, start_with_win, bg, fg)
    )
    conn.commit()
    conn.close()


def delete():
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM table_user"
    )
    cur.execute(
        "DELETE FROM setting"
    )
    conn.commit()
    conn.close()

connect_user()
connect_seeting()
