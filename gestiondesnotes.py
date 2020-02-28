# coding: utf-8
# author: Raoul HATTERER
# date: fevrier 2020

import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
# installer tksheet avec pip
from tksheet import Sheet
from tkinter import messagebox



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

# ------------------------------------------------------------------------------
# MariaDB
# ------------------------------------------------------------------------------
GN_host = 'localhost'
GN_database = 'bd_gestion_des_notes'
GN_user = 'user_gestionnaire'
GN_password = 'gestionnaire'

# ------------------------------------------------------------------------------
# DISCIPLINES
# ------------------------------------------------------------------------------


def _charger_disciplines():
    """
    Fonction appelée par 'afficher_disciplines()'
    Retourne un tupple conteant 'disc_Id' et 'disc_Name'.
    disc_Id : liste contenant tous les index générés de façon automatique de
    la table Discipline de la base de donnée 'bd_gestion_des_notes'.
    disc_Name : liste contenant tous les noms des disciplines (dans l'ordre
    alphabétique) contenus dans la table Discipline de la base de données
    'bd_gestion_des_notes'.
    """
    try:
        # print("Try to connected to MySQL Server")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        cursor = connection.cursor()
        cursor.execute("select Disc_Id, Disc_Name from Disciplines ORDER BY Disc_Name ASC;")
        records = cursor.fetchall()
        # print(records)
        print("All discipline of Disciplines (", cursor.rowcount, "): ")
        disc_Id, disc_Name = list(), list()
        for row in records:
            # print("\t", row)
            disc_Id += [row[0]]
            disc_Name += [[row[1]]]  # liste de liste requise pour un affichage modifiable avec tksheet
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return (disc_Id, disc_Name)


def afficher_disciplines():
    """
    Affiche un tableau de type tableur avec toutes les disciplines
    """
    global sheet_disciplines, disc_Id, disc_Name
    disc_Id, disc_Name = _charger_disciplines()
    sheet_disciplines = Sheet(f1,
                              data=disc_Name,  # to set sheet data at startup
                              height=600,
                              width=800)
    # sheet_disciplines.hide("row_index")
    sheet_disciplines.hide("top_left")
    sheet_disciplines.hide("header")
    sheet_disciplines.grid(row=0, column=0, columnspan=2, sticky="nswe")
    sheet_disciplines.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))


def enregistrer_disciplines():
    """
    Met à jour la base de donnée en y ajoutant d'éventuelles nouvelles
    disciplines.
    """
    try:
        # print("Try to connected to MySQL Server")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        cursor = connection.cursor()
        for index in range(len(disc_Name)):
            sql = "UPDATE Disciplines SET Disc_Name = %s WHERE Disc_Id = %s"
            discipline = (disc_Name[index][0], disc_Id[index])
            cursor.execute(sql, discipline)
            connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    sheet_disciplines.destroy()
    afficher_disciplines()


def ajouter_discipline():
    """
    Ajoute une 'À définir' dans le tableau des disciplines (et dans
    la base de donnée) et sélectionne la ligne. Commence par enregistrer
    l'état précédent du tableau dans la base de donnée dans le cas où
    l'utilisateur enchaîne les ajouts.
    """
    enregistrer_disciplines()
    global sheet_disciplines
    sql = "INSERT INTO Disciplines (Disc_Name) VALUES ('À définir')"
    try:
        # print("Try to connected to MySQL Server")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    sheet_disciplines.destroy()
    afficher_disciplines()
    sheet_disciplines.select_row(disc_Name.index(['À définir']))


# ------------------------------------------------------------------------------
# PROFESSEURS
# ------------------------------------------------------------------------------

def _charger_professeurs():
    """
    Fonction appelée par 'afficher_professeurs()'
    Retourne un tupple conteant 'disc_Id' et 'disc_Name'.
    disc_Id : liste contenant tous les index générés de façon automatique de
    la table Discipline de la base de donnée 'bd_gestion_des_notes'.
    disc_Name : liste contenant tous les noms des professeurs (dans l'ordre
    alphabétique) contenus dans la table Discipline de la base de données
    'bd_gestion_des_notes'.
    """
    try:
        # print("Try to connected to MySQL Server")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        cursor = connection.cursor()
        cursor.execute("select Prof_Id, FirstName, LastName, Disc_Name, Gender FROM Professeurs INNER JOIN Disciplines WHERE Professeurs.Disc_Id = Disciplines.Disc_Id ORDER BY LastName ASC")        
        records = cursor.fetchall()
        # print(records)
        print("All professeur of Professeurs (", cursor.rowcount, "): ")
        prof_Id, prof_Print, prof_Name = list(), list(), list()
        for row in records:
            # print("\t", row)
            prof_Id += [row[0]]
            prof_Name += [row[2]]
            if row[4] == 'M':
                prof_Print += [['M', row[1], row[2], row[3]]]
            elif row[4] == 'F':
                prof_Print += [['Mme', row[1], row[2], row[3]]]
            else:
                prof_Print += [['M ou Mme', row[1], row[2], row[3]]]
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return (prof_Id, prof_Name, prof_Print)


def afficher_professeurs():
    """
    Affiche un tableau de type tableur avec toutes les professeurs
    """
    global sheet_professeurs, prof_Id, prof_Name, prof_Print
    prof_Id, prof_Name, prof_Print = _charger_professeurs()
    sheet_professeurs = Sheet(f2,
                              data=prof_Print,  # to set sheet data at startup
                              height=600,
                              width=800)
    # sheet_professeurs.hide("row_index")
    sheet_professeurs.hide("top_left")
    sheet_professeurs.hide("header")
    sheet_professeurs.grid(row=0, column=0, columnspan=2, sticky="nswe")
    sheet_professeurs.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))


def enregistrer_professeurs():
    """
    Met à jour la base de donnée en y ajoutant d'éventuelles modifications.
    """
    try:
        # print("Try to connected to MySQL Server")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        cursor = connection.cursor()
        for index in range(len(prof_Name)):
            if [prof_Print[index][3]] not in disc_Name:
                messagebox.showerror("Erreur", "Cette discipline n'est pas enregistrée: {}".format(prof_Print[index][3]))
            else:
                sql = "UPDATE Professeurs SET FirstName=%s, LastName=%s, Disc_Id=%s, Gender=%s WHERE Prof_Id = %s"
                if prof_Print[index][0] in ['M', 'M.']:
                    professeur = (prof_Print[index][1],  # FirstName
                                  prof_Print[index][2],  # LastName
                                  disc_Id[disc_Name.index([prof_Print[index][3]])],  # from Disc_Name to Disc_Id
                                  'M',
                                  prof_Id[index])
                elif prof_Print[index][0] in ['Mme', 'Mme.']:
                    professeur = (prof_Print[index][1],  # FirstName 
                                  prof_Print[index][2],  # LastName  
                                  disc_Id[disc_Name.index([prof_Print[index][3]])],  # from Disc_Name to Disc_Id
                                  'F',
                                  prof_Id[index])
                else:
                    professeur = (prof_Print[index][1],  # FirstName 
                                  prof_Print[index][2],  # LastName  
                                  disc_Id[disc_Name.index([prof_Print[index][3]])],  # from Disc_Name to Disc_Id
                                  None,
                                  prof_Id[index])
                # print(professeur)
                cursor.execute(sql, professeur)
                connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    sheet_professeurs.destroy()
    afficher_professeurs()


def ajouter_professeur():
    """
    Ajoute une 'Nouvelle discipline' dans le tableau des professeurs (et dans
    la base de donnée) et sélectionne la ligne. Commence par enregistrer
    l'état précédent du tableau dans la base de donnée dans le cas où
    l'utilisateur enchaîne les ajouts.
    """
    enregistrer_professeurs()
    global sheet_professeurs, disc_Name, disc_Id
    if ['À définir'] not in disc_Name:
        ajouter_discipline()
    sql = "INSERT INTO Professeurs (FirstName, LastName, Disc_Id) VALUES (%s, %s, %s)"
    prof_nouveau = ('* Prénom ? *', '* Nom ? *', disc_Id[disc_Name.index(['À définir'])])
    try:
        # print("Try to connected to MySQL Server")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        cursor = connection.cursor()
        cursor.execute(sql, prof_nouveau)
        connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    sheet_professeurs.destroy()
    afficher_professeurs()
    row_index = prof_Name.index('* Nom ? *')
    sheet_professeurs.select_row(row_index)


def cell_select(self, response):
    print(response)


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

afficher_disciplines()
afficher_professeurs()

button_add_discipline = tk.Button(f1, text='Ajouter',
                                  command=ajouter_discipline)
button_save_disciplines = tk.Button(f1, text='Enregistrer',
                                    command=enregistrer_disciplines)
button_add_prof = tk.Button(f2, text='Ajouter',
                            command=ajouter_professeur)
button_save_profs = tk.Button(f2, text='Enregistrer',
                              command=enregistrer_professeurs)

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

button_add_discipline.grid(row=1, column=0)
button_save_disciplines.grid(row=1, column=1)
button_add_prof.grid(row=1, column=0)
button_save_profs.grid(row=1, column=1)
root.mainloop()
