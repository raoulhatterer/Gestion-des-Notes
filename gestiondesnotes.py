# coding: utf-8
# author: Raoul HATTERER
# date: fevrier 2020


import mysql.connector 
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
# installer tksheet avec pip
from tksheet import Sheet


# pour debugger
# import pdb
# pdb.set_trace()

# activer l'environnement virtuel python3.8

# Au préalable:
# -------------
# créer la base de données et les utlisateurs stil et gestionnaire 
# et initialiser les tables de la BD grâce au script initdb_gestiondesnotes.SQL
# par la commande
# source ./initdb_gestiondesnotes.SQL


class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.sheet_demo = Sheet(self,
                                data = [[f"{r}, {c}" for c in range(30)] for r in range(2000)], #to set sheet data at startup
                                #set_all_heights_and_widths = True, #to fit all cell sizes to text at start up
                                #headers = 0, #to set headers as first row at startup
                                #row_index = 0, #to set row_index as first column at startup
                                #total_rows = 2000, #if you want to set empty sheet dimensions at startup
                                #total_columns = 30, #if you want to set empty sheet dimensions at startup
                                height = 500, #height and width arguments are optional
                                width = 700) #For full startup arguments/parameters see DOCUMENTATION.md
        self.sheet_demo.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                         "drag_select",   #enables shift click selection as well
                                         "column_drag_and_drop",
                                         "row_drag_and_drop",
                                         "column_select",
                                         "row_select",
                                         "column_width_resize",
                                         "double_click_column_resize",
                                         "row_width_resize",
                                         "column_height_resize",
                                         "arrowkeys",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
                                         "rc_select",
                                         "rc_insert_column",
                                         "rc_delete_column",
                                         "rc_insert_row",
                                         "rc_delete_row",
                                         "copy",
                                         "cut",
                                         "paste",
                                         "delete",
                                         "undo",
                                         "edit_cell"))
        #self.sheet_demo.enable_bindings("enable_all")
        #self.sheet_demo.disable_bindings() #uses the same strings
        self.sheet_demo.grid(row = 0, column = 0, sticky = "nswe")
        



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
    print("All attributes of Professeurs (", cursor.rowcount, "): ")
    for row in records:
        print("\t", row)

    cursor = connection.cursor()
    cursor.execute("select * from Professeurs;")
    records = cursor.fetchall()
    print("All professeur of Professeurs (", cursor.rowcount, "): ")
    for row in records:
        print("\t", row)

    cursor = connection.cursor()
    cursor.execute("desc Disciplines;")
    records = cursor.fetchall()
    print("All attributes of Disciplines (", cursor.rowcount, "): ")
    for row in records:
        print("\t", row)

    cursor = connection.cursor()
    cursor.execute("select Disc_Name from Disciplines;")
    records = cursor.fetchall()
    print("All discipline of Disciplines (", cursor.rowcount, "): ")
    disciplines = list()
    for row in records:
        print("\t", row)
        disciplines.append(list(row))
    print(disciplines)


        
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")




def ajouter_discipline():
    sheet_disciplines.insert_row() # an empty row at the end
    sheet_disciplines.refresh()

def cell_select(self, response):
    print (response)

def enregistrer_disciplines():
    print(disciplines)
    
root = tk.Tk()
root.title("Gestion des notes")
root.resizable(False, False)
style = ttk.Style(root)
style.configure("lefttab.TNotebook", tabposition="n")
 
notebook = ttk.Notebook(root, style="lefttab.TNotebook")
 
f1 = tk.Frame(notebook, width=800, height=600)
f2 = tk.Frame(notebook, width=800, height=600)
f3 = tk.Frame(notebook, width=800, height=600)
f4 = tk.Frame(notebook, width=800, height=600)





sheet_disciplines = Sheet(f1,
                         data = disciplines, #to set sheet data at startup
                         height = 600, 
                         width = 800) 
sheet_disciplines.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                         "copy",
                                         "cut",
                                         "paste",
                                         "delete",
                                         "undo",
                                         "edit_cell"))

#sheet_disciplines.hide("row_index")
sheet_disciplines.hide("top_left")
sheet_disciplines.hide("header")
#sheet_disciplines.total_rows(4) #will delete rows if set to less than current data rows


button_add_discipline = tk.Button(f1, text='Ajouter', command=ajouter_discipline)
button_save_disciplines = tk.Button(f1, text='Enregistrer', command=enregistrer_disciplines)

notebook.add(f1, text="Disciplines")
notebook.add(f2, text="Enseignants")
notebook.add(f3, text="Élèves")
notebook.add(f4, text="Classes")

notebook.grid(row=0, column=0, sticky="nw")
# f1.rowconfigure(0, weight =0)
# f1.rowconfigure(1, weight =1)
# f1.rowconfigure(2, weight =0)
# f1.columnconfigure(0, weight =0)
# f1.columnconfigure(1, weight =1)
# f1.columnconfigure(2, weight =0)
# sheet_disciplines.grid(row=1, column=1)
sheet_disciplines.grid(row = 0, column = 0, columnspan=2, sticky = "nswe")
button_add_discipline.grid(row=1, column=0)
button_save_disciplines.grid(row=1, column=1)
root.mainloop()
