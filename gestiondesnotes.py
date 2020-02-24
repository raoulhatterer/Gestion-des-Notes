# coding: utf-8

import mysql.connector 
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk

# pour debugger
# import pdb
# pdb.set_trace()

# activer l'environnement virtuel python3.8

# Au préalable:
# -------------
# créer la base de données bd_cinema et l'utilisateur user_cinema
# initialiser les tables de la BD grâce au script createdb_gestiondesnotes.sql avec
# source createdb_gestiondesnotes.sql

try:
    print("Try to connected to MySQL Server")
    connection = mysql.connector.connect(host='localhost',
                                         database='bd_gestion_des_notes',
                                         user='user_gestionnaire',
                                         password='gestionnaire')
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You are connected to database: ", record)

    cursor = connection.cursor()
    cursor.execute("show databases;")
    records = cursor.fetchall()
    print("Databases: ", records)

    cursor = connection.cursor()
    cursor.execute("show tables;")
    records = cursor.fetchall()
    print("All tables: ", records)

    cursor = connection.cursor()
    cursor.execute("desc Professeurs;")
    records = cursor.fetchall()
    print("All attributes of Individu (", cursor.rowcount, "): ")
    for row in records:
        print("\t", row)

    cursor = connection.cursor()
    cursor.execute("select * from Professeurs;")
    records = cursor.fetchall()
    print("All individu of Individu (", cursor.rowcount, "): ")
    for row in records:
        print("\t", row)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")





root = tk.Tk()
 
style = ttk.Style(root)
style.configure("lefttab.TNotebook", tabposition="n")
 
notebook = ttk.Notebook(root, style="lefttab.TNotebook")
 
f1 = tk.Frame(notebook, bg="red", width=800, height=600)
f2 = tk.Frame(notebook, bg="blue", width=800, height=600)
f3 = tk.Frame(notebook, bg="green", width=800, height=600)
f4 = tk.Frame(notebook, bg="orange", width=800, height=600)
 
notebook.add(f1, text="Disciplines")
notebook.add(f2, text="Enseignants")
notebook.add(f3, text="Élèves")
notebook.add(f4, text="Classes")
 
notebook.grid(row=0, column=0, sticky="nw")
 
root.mainloop()
