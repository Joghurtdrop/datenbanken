#!/usr/bin/python2
import psycopg2
from Tkinter import *
import Tkinter as tk

root = tk.Tk()
def search_actor(search_word):
    print(search_word)
    cur.execute("SELECT * FROM movies where title %% %s",(search_word))
    fetch = cur.fetchall()
    print(fethc)
    create_window(fetch)

def search_movie(search_word):
    create_window(search_word)


def create_window(result):
    toplevel = Toplevel()
    toplevel.title('result')
    
    for item in result:
        label = tk.Label(toplevel, text=item).pack()

    toplevel.focus_set()

def connect_to_db():
    return psycopg2.connect(dbname='vorlesung', user='student',
            password='student', host='localhost', port='54321')

root.title("Datenbank")

label = tk.Label(root, text="Hello Datenbank!") 
entry = tk.Entry(root)
button_actor = tk.Button(root, text='Search Actor', 
        command=(lambda e=entry: search_actor(e)))
button_movie = tk.Button(root, text='Search Movie', 
        command=(lambda e=entry: search_actor(e)))

label.pack()
button_actor.pack()
button_movie.pack()
entry.pack()

conn = connect_to_db()
cur = conn.cursor()

root.mainloop()

