#!/usr/bin/python2
import psycopg2
from Tkinter import *
import Tkinter as tk

root = tk.Tk()
def search_actor(search_word):
    query='''SELECT name FROM actors WHERE lower(name) % lower(\'{0}\') OR
    lower(name) % lower(\'{0}\') OR name ILIKE \'%{0}%\' OR name @@ \'{0} \'
    ORDER BY levenshtein(lower(\'{0}\'),
    lower(name));'''.format(search_word.get())
    create_window(query,' ' )

def search_movie(search_word):
    query='''SELECT title FROM movies WHERE lower(title) % lower(\'{0}\') OR
    lower(title) % lower(\'{0}\') OR title ILIKE \'%{0}%\' OR title @@ \'{0} \'
    ORDER BY levenshtein(lower(\'{0}\'),
    lower(title));'''.format(search_word.get())
    create_window(query,' ' )

def search_near_actor(search_word):
    query='''SELECT name FROM actors WHERE metaphone(name, 6) =
    metaphone(\'{0}\', 6) OR metaphone(name, 6) % metaphone(\'{0}\', 6)
    ;'''.format(search_word.get())
    create_window(query,' ' )

def search_near_movie(search_word):
    query='''SELECT title FROM movies WHERE metaphone(title, 6) =
    metaphone(\'{0}\', 6) OR metaphone(title, 6) % metaphone(\'{0}\',
    6);'''.format(search_word.get())
    create_window(query,' ' )

def search_all_movie(search_word):
    query='''SELECT name, title FROM actors NATURAL JOIN movies_actors NATURAL
    JOIN movies WHERE name IN ( SELECT name FROM actors WHERE lower(name) %
    lower(\'{0}\') OR lower(name) % lower(\'{0}\') OR name ILIKE \'%{0}%\' OR
    name @@ \'{0} \' ORDER BY levenshtein(lower(\'{0}\'), lower(name))) ORDER
    BY name, title;'''.format(search_word.get())
    create_window(query, ' in ')

def search_all_actors(search_word):
    query='''SELECT name, title FROM actors NATURAL JOIN movies_actors NATURAL
    JOIN movies WHERE title IN ( SELECT title FROM movies WHERE lower(title) %
    lower(\'{0}\') OR lower(title) % lower(\'{0}\') OR title ILIKE
    \'%{0}%\' OR
    title @@ \'{0} \' ORDER BY levenshtein(lower(\'{0}\'), lower(title))) ORDER
    BY title, name;'''.format(search_word.get())
    create_window(query, ' in ')

def create_window(query, result_columns):
    cur.execute(query)
    result = cur.fetchall()

    toplevel = Toplevel()
    toplevel.title('Result')
    toplevel.resizable(height=True, width=True)
    scrollbar = Scrollbar(toplevel)
    scrollbar.pack(side=RIGHT, fill =Y)
    
    mylist = Listbox(toplevel, yscrollcommand = scrollbar.set)
    mylist.config(width=0)

    for item in result:
        mylist.insert(END, result_columns.join(item))
    mylist.pack()
    scrollbar.config(command = mylist.yview)
    toplevel.focus_set()

def connect_to_db():
    return psycopg2.connect(dbname='vorlesung', user='student',
            password='student', host='localhost', port='54321')

root.title("Datenbank")
root.geometry('250x200')

label = tk.Label(root, text="Hello Datenbank!", width=30) 
entry = tk.Entry(root)
button_actor = tk.Button(root, text='fuzzy search actor', 
        command=(lambda e=entry: search_actor(e)))
button_movie = tk.Button(root, text='fuzzy search movie', 
        command=(lambda e=entry: search_movie(e)))
button_near_actor = tk.Button(root, text='near search actor', 
        command=(lambda e=entry: search_near_actor(e)))
button_near_movie = tk.Button(root, text='near search movie', 
        command=(lambda e=entry: search_near_movie(e)))
button_all_movie = tk.Button(root, text='search all movies for actor', 
        command=(lambda e=entry: search_all_movie(e)))
button_all_actor = tk.Button(root, text='search all actors in movie', 
        command=(lambda e=entry: search_all_actors(e)))

label.pack()

button_actor.pack()
button_movie.pack()
button_near_actor.pack()
button_near_movie.pack()
button_all_movie.pack()
button_all_actor.pack()

entry.pack()

conn = connect_to_db()
cur = conn.cursor()

root.mainloop()

