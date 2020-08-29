# coding: utf-8
# author: Raoul HATTERER
# date: fevrier 2020

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# installer tksheet avec pip
from tksheet import Sheet

# pour debugger
# import pdb
# pdb.set_trace()

# dans emacs activer l'environnement virtuel python3.8

# Au préalable:
# -------------
# À partir du Terminal se rendre dans le dossier où se trouve les scripts
# Se connecter en tant que root à mysql avec                           
# mysql -u root -p                                                     
# Dans l'invite de commande MariaDB> entrer:                             
# SOURCE ./initdb_gestiondesnotes.sql;                                 
# pour créer la base de données et les utlisateurs stil et gestionnaire
# et initialiser les tables de la BD.

# ------------------------------------------------------------------------------
# MariaDB
# ------------------------------------------------------------------------------
GN_host = 'localhost'
GN_database = 'bd_gestion_des_notes'
GN_user = None
user_role = None

# ------------------------------------------------------------------------------
# SÉLECTIONS
# ------------------------------------------------------------------------------

annee_selected = None
periode_selected = None
classe_selected = None
professeur_selected = None
discipline_selected = None
    
def select_annee(response):
    """
    Mémorise l'année par clic dans la case du tableau des années scolaires 
    """
    global annee_selected
    index = response[1]
    annee_selected = (annee_id[index], annee_Name[index][0])
    print(annee_selected)

def select_periode(response):
    """
    Mémorise la période scolaire par clic dans la case du tableau des périodes scolaires 
    """
    global periode_selected
    index = response[1]
    periode_selected = (periode_id[index], periode_Name[index][0])
    print(periode_selected)
    appliquer_selections()


def deselect_periode():
    """
    Désélectionne la période
    """
    global periode_selected
    periode_selected = None
    appliquer_selections()


def select_enseignement(response):
    """
    Mémorise  le professeur, la discipline et la classe par clic dans la case du tableau des enseignements 
    """
    global annee_selected, classe_selected, professeur_selected, discipline_selected
    index = response[1]
    print(index)
    enseignements_traduits = sql_traduis_enseignements()
    enseignement_selected = enseignements_traduits[index]
    print(enseignement_selected)
    nom_professeur, prenom_professeur, nom_classe, annee_classe, nom_discipline = enseignement_selected
    selected_professeur_id = sql_professeur_id(nom_professeur, prenom_professeur)
    professeur_selected = (selected_professeur_id, nom_professeur)
    selected_discipline_id = sql_discipline_id(nom_discipline)
    discipline_selected = (selected_discipline_id, nom_discipline)
    selected_classe_id = sql_classe_id(nom_classe, annee_classe)
    classe_selected = (selected_classe_id, nom_classe)
    appliquer_selections()

    
def select_classe(response):
    """
    Mémorise la classe par clic dans la case du tableau des classes
    """
    global classe_selected
    index = response[1]
    classe_selected = (classe_id[index], classe_Name[index])
    appliquer_selections()

    
def deselect_classe():
    """
    Désélectionne la classe 
    """
    global classe_selected
    classe_selected = None
    appliquer_selections()    


def select_professeur(response):
    """
    Mémorise le professeur par clic dans la case du tableau des professeurs
    """
    global professeur_selected
    print(response)
    index = response[1]  # index dans le tableau affiché pas dans la table Professeur
    professeur_selected = (professeur_id[index], prof_Name[index])
    appliquer_selections()

    
def deselect_prof():
    """
    Désélectionne le professeur
    """
    global professeur_selected
    professeur_selected = None
    appliquer_selections()

    
def select_discipline(response):
    """
    Mémorise la discipline par clic dans la case du tableau des disciplines
    """
    global discipline_selected
    index = response[1]
    discipline_selected = (discipline_id[index], disc_Name[index][0])
    appliquer_selections()

    
def deselect_discipline():
    """
    Désélectionne la discipline 
    """
    global discipline_selected
    discipline_selected = None
    appliquer_selections()


def appliquer_selections():
    """
    Rafraîchi l'affichage des onglets Enseignements et Evaluations suivant les sélections en cours
    """
    frame_selection_enseignements.destroy()    
    afficher_selections_enseignements()
    sheet_enseignements.destroy()
    afficher_enseignements()
    frame_selection_evaluations.destroy()
    afficher_selections_evaluations()
    sheet_evaluations.destroy()
    afficher_evaluations()
    
# ------------------------------------------------------------------------------
# AFFICHAGE NOTEBOOK
# ------------------------------------------------------------------------------

def afficher_notebook_professeur():
    """
    Affiche le notebook avec tous les onglets
    """
    afficher_compte_professeur()
    notebook.add(f1, text="Disciplines")
    notebook.add(f2, text="Professeurs")
    notebook.add(f3, text="Élèves")
    notebook.add(f4, text="Classes")
    notebook.add(f5, text="Enseignements")
    notebook.add(f6, text="Périodes")
    notebook.add(f7, text="Évaluations")    
    afficher_disciplines()
    afficher_professeurs()
    afficher_eleves()
    afficher_classes()
    afficher_annees_et_periodes()
    afficher_selections_enseignements()
    afficher_enseignements()
    afficher_selections_evaluations()
    afficher_evaluations()





# ------------------------------------------------------------------------------
# GESTION COMPTE
# ------------------------------------------------------------------------------

def connexion(event=None):
    """
    Tente la connexion à la base de données avec les identifiants que l'utilisateur a saisis dans l'IHM
    """
    global cursor, GN_user, GN_password
    GN_user = user_entry_text.get()
    GN_password = pwd_entry_text.get()
    role = sql_read_role()
    if role == 'role_professeur':
        frame_connexion.destroy()
        afficher_notebook_professeur()
    elif role == 'role_gestionnaire':
        messagebox.showwarning("Connexion refusée", "Cette application est réservée aux enseignants enregistrés.\n\nVeuillez utiliser l'application: gestionnaire.py")        


def sql_read_role():
    """
    Se connecte à MySQL et retourne le rôle de l'utilisateur parmi : role_gestionnaire...
    """
    global cursor, GN_user, GN_password
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_read_role")
        cursor = connection.cursor()
        sql = "SELECT CURRENT_ROLE();"
        cursor.execute(sql)
        records = cursor.fetchall()
        user_role = records[0][0]
        print(f"User role: {user_role}")
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return user_role
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "Identifiant ou mot de passe non valide")

    
def sql_read_professeur():
    """
    Se connecte à Mysql et retourne les données concernant le professeur à partir de la table Professeur. 
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_read_professeur")
        cursor = connection.cursor()
        sql = "SELECT prenom, nom, titre, professeur_id FROM Professeur WHERE  CONCAT(prenom, nom)=%s"
        tuple_login=(GN_user,)
        cursor.execute(sql, tuple_login)
        records = cursor.fetchall()
        print(records)
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records)
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")


def sql_professeur_id(nom, prenom):
    """
    Se connecte à Mysql et retourne le numéro d'enregistrement d'un professeur à partir de la table Professeur. 
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_professeur_id")
        cursor = connection.cursor()
        sql = "SELECT professeur_id FROM Professeur WHERE  nom=%s AND prenom=%s"
        tuple_data = (nom, prenom)
        cursor.execute(sql, tuple_data)
        records = cursor.fetchall()
        # print(records)
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records[0][0])
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")


def afficher_compte_professeur():
    """
    Affiche l'IHM du compte professeur
    """
    global prenom_entry_text, nom_entry_text, combobox_titre, naissance_entry_text, login_entry_text, frame_compte, current_user_id
    records = sql_read_professeur()
    current_user_id = records[0][3]
    
    frame_compte = tk.Frame(f0)
     # row0 column0
    frame_compte.grid_rowconfigure(0, minsize=100)
    frame_compte.grid_columnconfigure(0, minsize=100)    
    # column1
    button_deconnect = tk.Button(frame_compte, text='Déconnexion',
                                 command=deconnexion)
    button_deconnect.grid(row=1,column=2, sticky=tk.W)
    frame_compte.grid_rowconfigure(2, minsize=20)    
    lbl_login = tk.Label(frame_compte, text="Login")
    lbl_login.grid(row=3, column=1, sticky=tk.E)
    lbl_prenom = tk.Label(frame_compte, text="Prénom")
    lbl_prenom.grid(row=4, column=1, sticky=tk.E)
    lbl_nom = tk.Label(frame_compte, text="Nom")
    lbl_nom.grid(row=5, column=1, sticky=tk.E)
    lbl_genre = tk.Label(frame_compte, text="Titre")
    lbl_genre.grid(row=6, column=1, sticky=tk.E)
    
    # column2
    login_entry_text = tk.StringVar()
    login_entry_text.set(GN_user)
    entry_login = tk.Entry(frame_compte, textvariable=login_entry_text, state='disabled')
    entry_login.grid(row=3, column=2, sticky=tk.W)

    prenom_entry_text = tk.StringVar()
    prenom_entry_text.set(records[0][0])
    entry_prenom = tk.Entry(frame_compte, textvariable=prenom_entry_text)
    entry_prenom.grid(row=4, column=2, sticky=tk.W)

    nom_entry_text = tk.StringVar()
    nom_entry_text.set(records[0][1])
    entry_nom = tk.Entry(frame_compte, textvariable=nom_entry_text)
    entry_nom.grid(row=5, column=2, sticky=tk.W)

    combobox_titre = ttk.Combobox(frame_compte, values=['M','Mme'], width=4)
    if records[0][2]=="M":
        combobox_titre.current(0)
    else:
        combobox_titre.current(1)        
    combobox_titre.grid(row=6, column=2, sticky=tk.W)

    frame_compte.grid_rowconfigure(9, minsize=20)    
    button_save = tk.Button(frame_compte, text='Enregistrer',
                             command=sql_save_compte_admin)
    button_save.grid(row=10,column=2, sticky=tk.W)

    # column4
    button_change_pwd = tk.Button(frame_compte, text='Changer de mot de passe',
                                  command=change_password)
    button_change_pwd.grid(row=3,column=4, sticky=tk.W)
    # column5
    frame_compte.grid_columnconfigure(5, minsize=100)        
    
    frame_compte.grid()
    # row
    frame_compte.grid_rowconfigure(11, minsize=100)    


def change_password():
    """
    Affichage d'une IHM permettant de changer le mot de passe de l'utilisateur.
    Déconnections du compte à l'issue du changement de mot de passe. 
    """
    global frame_new_password, GN_password

    def sql_change_password_if_valid():
        """
        Contrôle la validité du nouveau mot de passe puis le modifie
        """
        global GN_password
        GN_new_password = new_password_entry_text.get()
        if  GN_new_password == confirmation_entry_text.get():
            try:
                print(f"Try to connect to MySQL Server as {GN_user}")
                connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
                db_Info = connection.get_server_info()
                print(f"Connected to MySQL Server version {db_Info}")
                print("sql_change_password_if_valid")
                cursor = connection.cursor()
                GN_password = GN_new_password
                sql = "SET PASSWORD FOR %s@%s = PASSWORD(%s);"
                data = (GN_user, GN_host, GN_password)
                cursor.execute(sql, data)
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                frame_new_password.destroy()
                afficher_IHM_connexion()

            except Error as e:
                print("Error while connecting to MySQL", e)
                messagebox.showwarning("Erreur de connexion", "Identifiant ou mot de passe non valide")
        else:
            messagebox.showwarning("Erreur de saisie", "Nouveau mot de passe non confirmé")

    # IHM New Password
    frame_compte.destroy()
    bullet = "●"
    frame_new_password = tk.Frame(f0)
     # row0 column0
    frame_new_password.grid_rowconfigure(0, minsize=100)
    frame_new_password.grid_columnconfigure(0, minsize=100)    
    # row1
    lbl_new_password = tk.Label(frame_new_password, text='Nouveau mot de passe')
    lbl_new_password.grid(row=1, column=1, sticky=tk.W)
    # row2
    new_password_entry_text = tk.StringVar()
    new_password = tk.Entry(frame_new_password, show=bullet, textvariable=new_password_entry_text, fg="grey")
    new_password.focus()
    new_password.grid(row=2, column=1)
    # row3
    lbl_confirmation = tk.Label(frame_new_password, text='Confirmation')
    lbl_confirmation.grid(row=3, column=1, sticky=tk.W)
    # row4
    confirmation_entry_text = tk.StringVar()
    confirmation_entry_text.set("")
    confirmation = tk.Entry(frame_new_password, show=bullet, textvariable=confirmation_entry_text, fg="grey")
    confirmation.grid(row=4, column=1)
    # raw5
    frame_new_password.grid_rowconfigure(5, minsize=12)
    # raw6
    frame_boutons = tk.Frame(frame_new_password)
    button_cancel = tk.Button(frame_boutons, text='Annuler',
                              command=annuler_new_password)
    button_cancel.grid(row=0, column=0)
    frame_boutons.grid_columnconfigure(1, minsize=40)    
    button_save = tk.Button(frame_boutons, text='Enregistrer',
                             command=sql_change_password_if_valid)
    button_save.grid(row=0, column=2)
    frame_boutons.grid(row=6, column=1)
    # raw7
    frame_new_password.grid_rowconfigure(7, minsize=100)
    # column3
    frame_new_password.grid_columnconfigure(3, minsize=100)
    
    frame_new_password.grid()

    
def annuler_new_password():
    """
    Annulation du nouveau mot de passe et retour au compte.
    """
    frame_new_password.destroy()
    afficher_notebook_gestionnaire()


    
def sql_save_compte_admin():
    """
    Se connecte à MySQL pour sauvegarder les données du compte administrateur dans la table Administrateurs
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_save_compte_admin")
        cursor = connection.cursor()
        sql = "UPDATE Administrateur SET FirstName=%s, LastName=%s, Gender=%s, Birthday=%s WHERE Login=%s "
        date = datetime.strptime(naissance_entry_text.get(),'%d/%m/%Y').strftime('%Y-%m-%d')
        administrateur = (prenom_entry_text.get(), nom_entry_text.get(), combobox_titre.get(), date, login_entry_text.get())
        print(administrateur)
        cursor.execute(sql, administrateur)
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")        
    except Error as e:
        print("Error while connecting to MySQL", e)


def deconnexion():
    """
    Déconnexion du compte et retour à l'IHM de connexion 
    """
    frame_compte.destroy()
    notebook.hide(1)  # Disciplines
    notebook.hide(2)  # Enseignants
    notebook.hide(3)  # Élèves
    notebook.hide(4)  # Classes
    notebook.hide(5)  # enseignements    
    notebook.hide(6)  # années scolaires 
    afficher_IHM_connexion()


def afficher_IHM_connexion():
    """
    Affiche la page de connexion (IHM) 
    """
    global user_entry_text, pwd_entry_text, frame_connexion
    bullet = "●"

    frame_connexion = tk.Frame(f0)
     # row0 column0
    frame_connexion.grid_rowconfigure(0, minsize=200)
    frame_connexion.grid_columnconfigure(0, minsize=300)    
    # row1
    loginFrame = tk.Frame(frame_connexion)
    loginFrame.grid(row=1, column=1)
    user_entry_text = tk.StringVar()
    user_entry_text.set("Utilisateur")
    user = tk.Entry(loginFrame, textvariable=user_entry_text, fg="grey")
    user.focus()
    user.selection_range(0, tk.END)
    pwd_entry_text = tk.StringVar()
    pwd_entry_text.set("")
    pwd = tk.Entry(loginFrame, show=bullet, textvariable=pwd_entry_text, fg="grey")
    pwd.bind('<Return>', connexion)
    user.grid(row=0)
    pwd.grid(row=1)
    loginFrame.grid_rowconfigure(3, minsize=12)
    button_login = tk.Button(loginFrame, text='Se connecter',
                             command=connexion)
    button_login.grid(row=4)
    # raw2
    frame_connexion.grid_rowconfigure(2, minsize=200)
    frame_connexion.grid_columnconfigure(2, minsize=300)    
    frame_connexion.grid()
    

# ------------------------------------------------------------------------------
# DISCIPLINES
# ------------------------------------------------------------------------------


def sql_read_disciplines():
    """
    Fonction appelée par 'afficher_disciplines()'
    Retourne un tupple contenant 'discipline_id' et 'disc_Name'.
    discipline_id : liste contenant tous les index générés de façon automatique de
    la table Discipline de la base de données 'bd_gestion_des_notes'.
    disc_Name : liste contenant tous les noms des disciplines (dans l'ordre
    alphabétique) contenus dans la table Discipline de la base de données
    'bd_gestion_des_notes'.
    """
    global GN_password
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_read_disciplines")
        cursor = connection.cursor()
        cursor.execute("select discipline_id, nom from Discipline ORDER BY nom ASC;")
        records = cursor.fetchall()
        # print(records)
        print("All discipline of Discipline (", cursor.rowcount, "): ")
        discipline_id, disc_Name = list(), list()
        for row in records:
            # print("\t", row)
            discipline_id += [row[0]]
            disc_Name += [[row[1]]]  # liste de liste requise pour un affichage modifiable avec tksheet

        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return (discipline_id, disc_Name)
    
    except Error as e:
        print("Error while connecting to MySQL", e)


def sql_discipline_id(nom):
    """
    Se connecte à Mysql et retourne le numéro d'enregistrement d'une discipline à partir de la table Discipline. 
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_discipline_id")
        cursor = connection.cursor()
        sql = "SELECT discipline_id FROM Discipline WHERE  nom=%s"
        tuple_data = (nom,)
        cursor.execute(sql, tuple_data)
        records = cursor.fetchall()
        print(records)
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records[0][0])
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")


def afficher_disciplines():
    """
    Affiche un tableau de type tableur avec toutes les disciplines (IHM)
    """
    global sheet_disciplines, discipline_id, disc_Name
    discipline_id, disc_Name = sql_read_disciplines()
    sheet_disciplines = Sheet(f1,
                              data=disc_Name,  # to set sheet data at startup
                              set_all_heights_and_widths = True,
                              height=600,
                              width=800)
    sheet_disciplines.hide("row_index")
    sheet_disciplines.hide("top_left")
    sheet_disciplines.hide("header")
    sheet_disciplines.grid(row=0, column=0, columnspan=2, sticky="we")
    sheet_disciplines.extra_bindings([ ("cell_select", select_discipline)])        
    sheet_disciplines.enable_bindings(("cell_select",
                                       "single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))







# ------------------------------------------------------------------------------
# PROFESSEURS
# ------------------------------------------------------------------------------

def sql_read_professeurs():
    """
    Fonction appelée par 'afficher_professeurs()'
    Retourne un tupple contenant: 'professeur_id', 'prof_Name', 'prof_Print'.
    professeur_id : liste contenant tous les index générés de façon automatique de
    la table 'Professeur' de la base de données 'bd_gestion_des_notes'.
    prof_Name : liste contenant tous les noms des professeurs (dans l'ordre
    alphabétique) contenus dans la table Discipline de la base de données
    'bd_gestion_des_notes'.
    'prof_Print': liste affichée dans l'onglet Professeurs
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_read_professeurs")
        cursor = connection.cursor()
        cursor.execute("select professeur_id, prenom, nom, titre FROM Professeur  ORDER BY nom ASC")        
        records = cursor.fetchall()
        # print(records)
        print("All professeur of Professeurs (", cursor.rowcount, "): ") 
        professeur_id, prof_Print, prof_Name = list(), list(), list()
        for row in records:
            # print("\t", row)
            professeur_id += [row[0]]
            prof_Name += [row[2]]
            if row[3] == 'M':
                prof_Print += [['M', row[1], row[2]]]
            elif row[3] == 'F':
                prof_Print += [['Mme', row[1], row[2]]]
            else:
                prof_Print += [['M ou Mme', row[1], row[2]]]
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    except Error as e:
        print("Error while connecting to MySQL", e)
    return (professeur_id, prof_Name, prof_Print)


def afficher_professeurs():
    """
    Affiche un tableau de type tableur avec toutes les professeurs (IHM)
    """
    global sheet_professeurs, professeur_id, prof_Name, prof_Print
    professeur_id, prof_Name, prof_Print = sql_read_professeurs()
    sheet_professeurs = Sheet(f2,
                              data=prof_Print,  # to set sheet data at startup
                              headers=["Titre", "Prénom", "Nom"],
                              set_all_heights_and_widths = True,
                              height=600,
                              width=800)
    sheet_professeurs.hide("row_index")
    sheet_professeurs.hide("top_left")
    #sheet_professeurs.hide("header")
    sheet_professeurs.grid(row=0, column=0, columnspan=2, sticky="nswe")
    sheet_professeurs.extra_bindings([ ("cell_select", select_professeur)])        
    sheet_professeurs.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))






    
# ------------------------------------------------------------------------------
# ÉLÈVES
# ------------------------------------------------------------------------------

def sql_read_eleves():
    """
    Fonction appelée par 'afficher_eleves()'
    Retourne un tupple contenant 'eleve_id', 'eleves_Name', eleves_Print.
    eleve_id : liste contenant tous les index générés de façon automatique de
    la table 'Eleve' de la base de données 'bd_gestion_des_notes'.
    eleves_Name : liste contenant tous les noms des élèves (dans l'ordre
    alphabétique) contenus dans la table 'Eleve' de la base de données
    'eleves_Print': liste affichée dans l'onglet élèves sous forme de tableau
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_read_eleves")
        cursor = connection.cursor()
        cursor.execute("select eleve_id, prenom, Eleve.nom, genre, classe.nom FROM Eleve INNER JOIN Classe ON Eleve.classe_id = Classe.classe_id ORDER BY Eleve.nom ASC")        
        records = cursor.fetchall()
        # print(records)
        print("All eleve of Eleves (", cursor.rowcount, "): ")
        eleve_id, eleves_Print, eleves_Name = list(), list(), list()
        for row in records:
            # print("\t", row)
            eleve_id += [row[0]]
            eleves_Name += [row[2]]
            eleves_Print += [[row[2], row[1], row[3], row[4]]]  # nom, prenom, genre, classe_id
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return (eleve_id, eleves_Name, eleves_Print)
    except Error as e:
        print("Error while connecting to MySQL", e)


def afficher_eleves():
    """
    Affiche un tableau de type tableur avec toutes les élèves (IHM)
    """
    global sheet_eleves, eleve_id, eleves_Name, eleves_Print
    eleve_id, eleves_Name, eleves_Print = sql_read_eleves()
    sheet_eleves = Sheet(f3,
                         data=eleves_Print,  # to set sheet data at startup
                         headers=["Nom", "Prénom", "Genre", "Classe"],
                         set_all_heights_and_widths = True,
                         height=600,
                         width=800)
    sheet_eleves.hide("row_index")
    sheet_eleves.hide("top_left")
    # sheet_eleves.hide("header")
    sheet_eleves.grid(row=0, column=0, columnspan=2, sticky="we")
    sheet_eleves.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))






        

# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------

def _charger_classes():
    """
    Fonction appelée par 'afficher_classes()'
    Retourne un tuple contenant 'classe_id', 'nom', 'classe_Print'
    classe_id : liste contenant tous les index générés de façon automatique de
    la table Classes de la base de données 'bd_gestion_des_notes'.
    nom : liste contenant tous les noms des classes (dans l'ordre
    alphabétique) contenus dans la table Classes de la base de données
    'bd_gestion_des_notes'.
    classe_Print :liste affichée dans l'onglet classes sous forme de tableau
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("_charger_classes")
        cursor = connection.cursor()
        cursor.execute("select classe_id, Classe.nom, niveau, Anneescolaire.nom from Classe INNER JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id ORDER BY Classe.annee_id DESC, Classe.nom;")
        records = cursor.fetchall()
        # print(records)
        print("All classe of Classes (", cursor.rowcount, "): ")
        classe_id, classe_Name, classe_Print = list(), list(), list()
        for row in records:
            # print("\t", row)
            classe_id += [row[0]]
            classe_Name += [row[1]]
            classe_Print += [[row[1], row[2], row[3]]]  # liste de liste requise pour un affichage modifiable avec tksheet
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    except Error as e:
        print("Error while connecting to MySQL", e)
    return (classe_id, classe_Name, classe_Print)


def sql_classe_id(nom, annee):
    """
    Se connecte à Mysql et retourne le numéro d'enregistrement d'une classe à partir de la table Classe. 
    """
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_classe_id")
        cursor = connection.cursor()
        sql = "SELECT Classe.classe_id FROM Classe INNER JOIN Anneescolaire WHERE  Classe.nom=%s AND Anneescolaire.nom=%s"
        tuple_data = (nom, annee)
        cursor.execute(sql, tuple_data)
        records = cursor.fetchall()
        # print(records)
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records[0][0])
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")


def afficher_classes():
    """
    Affiche un tableau de type tableur avec toutes les classes
    """
    global sheet_classes, classe_id, classe_Name, classe_Print
    classe_id, classe_Name, classe_Print = _charger_classes()
    sheet_classes = Sheet(f4,
                          data=classe_Print,  # to set sheet data at startup
                          headers=["Classe", "Niveau", "Année scolaire"],
                          set_all_heights_and_widths = True,
                          height=600,
                          width=800)
    sheet_classes.hide("row_index")
    sheet_classes.hide("top_left")
    # sheet_classes.hide("header")
    sheet_classes.grid(row=0, column=0, columnspan=2, sticky="we")
    sheet_classes.extra_bindings([ ("cell_select", select_classe)])    
    sheet_classes.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                   "arrowkeys",
                                   "copy",
                                   "cut",
                                   "paste",
                                   "delete",
                                   "undo",
                                   "edit_cell"))









# ------------------------------------------------------------------------------
# ANNEES SCOLAIRES et PERIODES
# ------------------------------------------------------------------------------


def sql_read_annees():
    """
    Fonction appelée par 'afficher_annees_et_periodes()'
    Retourne un tupple contenant 'annee_id' et 'annee_Name'.
    annee_id : liste contenant tous les index générés de façon automatique de
    la table Anneescolaire de la base de données 'bd_gestion_des_notes'.
    annee_Name : liste contenant tous les noms des annees (dans l'ordre
    alphabétique) contenus dans la table Anneescolaire de la base de données
    'bd_gestion_des_notes'.
    """
    global GN_password
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_read_annees")
        cursor = connection.cursor()
        cursor.execute("select annee_id, nom from Anneescolaire ORDER BY nom ASC;")
        records = cursor.fetchall()
        # print(records)
        print("All annee of Anneescolaire (", cursor.rowcount, "): ")
        annee_id, annee_Name = list(), list()
        for row in records:
            # print("\t", row)
            annee_id += [row[0]]
            annee_Name += [[row[1]]]  # liste de liste requise pour un affichage modifiable avec tksheet

        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return (annee_id, annee_Name)
    
    except Error as e:
        print("Error while connecting to MySQL", e)


def sql_read_periodes():
    """
    Fonction appelée par 'afficher_annees_et_periodes()'
    Retourne un tupple contenant 'periode_id' et 'periode_Name'.
    periode_id : liste contenant tous les index générés de façon automatique de
    la table Periode de la base de données 'bd_gestion_des_notes'.
    periode_Name : liste contenant tous les noms des périodes (dans l'ordre
    alphabétique) contenus dans la table Periode de la base de données
    'bd_gestion_des_notes'.
    """
    global GN_password
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_read_periodes")
        cursor = connection.cursor()
        cursor.execute("select periode_id, nom from Periode ORDER BY nom ASC;")
        records = cursor.fetchall()
        # print(records)
        print("All periode of Periode (", cursor.rowcount, "): ")
        periode_id, periode_Name = list(), list()
        for row in records:
            # print("\t", row)
            periode_id += [row[0]]
            periode_Name += [[row[1]]]  # liste de liste requise pour un affichage modifiable avec tksheet

        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return (periode_id, periode_Name)
    
    except Error as e:
        print("Error while connecting to MySQL", e)


def afficher_annees_et_periodes():
    """
    Affiche un tableau de type tableur avec toutes les années scolaires (IHM)
    """
    global sheet_annees, annee_id, annee_Name, sheet_periodes, periode_id, periode_Name
    annee_id, annee_Name = sql_read_annees()
    frame_annees.grid(row=0, column=0, sticky='we')
    sheet_annees = Sheet(frame_annees,
                         data=annee_Name,  # to set sheet data at startup
                         headers=["Années Scolaires"],
                         set_all_heights_and_widths = True,
                         height=600,
                         width=400)
    sheet_annees.hide("row_index")
    sheet_annees.hide("top_left")
    # sheet_annees.hide("header")
    sheet_annees.grid(row=0, column=0, columnspan=2, sticky="we")
    
    sheet_annees.extra_bindings([ ("cell_select", select_annee)])
    sheet_annees.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))
    periode_id, periode_Name = sql_read_periodes()
    frame_periodes.grid(row=0, column=1, sticky='we')
    sheet_periodes = Sheet(frame_periodes,
                           data=periode_Name,  # to set sheet data at startup
                           headers=["Périodes"],
                           set_all_heights_and_widths = True,
                           height=600,
                           width=400)
    sheet_periodes.hide("row_index")
    sheet_periodes.hide("top_left")
    # sheet_periodes.hide("header")
    sheet_periodes.grid(row=0, column=0, columnspan=2,  sticky="we")
    sheet_periodes.extra_bindings([ ("cell_select", select_periode)])    
    sheet_periodes.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))

# ------------------------------------------------------------------------------
# ENSEIGNEMENTS
# ------------------------------------------------------------------------------

        
def sql_read_enseignements():
    """
    Se connecte à Mysql et retourne les données brutes concernant les Enseignements à partir des sélections en cours.
    """
    if not(professeur_selected) and not(classe_selected) and not(discipline_selected):
        sql = "SELECT *  FROM Enseigner;"
        tuple_selection = "" 
    elif professeur_selected and not(classe_selected) and not(discipline_selected):
        sql = "SELECT *  FROM Enseigner WHERE professeur_id=%s;"
        tuple_selection = (professeur_selected[0],)
    elif not(professeur_selected) and classe_selected and not(discipline_selected):
        sql = "SELECT *  FROM Enseigner WHERE classe_id=%s;"
        tuple_selection = (classe_selected[0],)
    elif professeur_selected and classe_selected and not(discipline_selected):
        sql = "SELECT *  FROM Enseigner WHERE professeur_id=%s AND classe_id=%s;"
        tuple_selection = (professeur_selected[0], classe_selected[0])
    elif not(professeur_selected) and not(classe_selected) and discipline_selected:
        sql = "SELECT *  FROM Enseigner WHERE discipline_id=%s;"
        tuple_selection = (discipline_selected[0],)
    elif professeur_selected and not(classe_selected) and discipline_selected:
        sql = "SELECT *  FROM Enseigner WHERE professeur_id=%s AND discipline_id=%s;"
        tuple_selection = (professeur_selected[0], discipline_selected[0])
    elif not(professeur_selected) and classe_selected and discipline_selected:
        sql = "SELECT *  FROM Enseigner WHERE classe_id=%s AND discipline_id=%s;"
        tuple_selection = (classe_selected[0], discipline_selected[0])
    else:
        sql = "SELECT *  FROM Enseigner WHERE professeur_id=%s AND classe_id=%s AND discipline_id=%s;"
        tuple_selection = (professeur_selected[0], classe_selected[0], discipline_selected[0])
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_read_enseignements")
        cursor = connection.cursor()
        cursor.execute(sql, tuple_selection)
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records)
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")


def sql_traduis_enseignements():
    """
    Se connecte à Mysql et retourne les données traduites concernant les Enseignements
    """
    if not(professeur_selected) and not(classe_selected) and not(discipline_selected):
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id;"
        tuple_selection ="" 
    elif professeur_selected and not(classe_selected) and not(discipline_selected):
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id WHERE Enseigner.professeur_id=%s;"
        tuple_selection = (professeur_selected[0],)
    elif not(professeur_selected) and classe_selected and not(discipline_selected):
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id WHERE Enseigner.classe_id=%s;"
        tuple_selection = (classe_selected[0],)
    elif professeur_selected and classe_selected and not(discipline_selected):
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id WHERE Enseigner.professeur_id=%s AND  Enseigner.classe_id=%s;"
        tuple_selection = (professeur_selected[0], classe_selected[0])
    elif not(professeur_selected) and not(classe_selected) and discipline_selected:
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id WHERE Enseigner.discipline_id=%s;"
        tuple_selection = (discipline_selected[0],)
    elif professeur_selected and not(classe_selected) and discipline_selected:
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id WHERE Enseigner.professeur_id=%s AND  Enseigner.discipline_id=%s;"
        tuple_selection = (professeur_selected[0], discipline_selected[0])
    elif not(professeur_selected) and classe_selected and discipline_selected:
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id WHERE Enseigner.classe_id=%s AND  Enseigner.discipline_id=%s;"
        tuple_selection = (classe_selected[0], discipline_selected[0])
    else:
        sql = "SELECT Professeur.nom,  Professeur.prenom, Classe.nom AS Classe, Anneescolaire.nom AS Annee, Discipline.nom AS Discipline FROM Enseigner JOIN Professeur ON Enseigner.professeur_id = Professeur.professeur_id JOIN Classe ON Enseigner.classe_id = Classe.classe_id JOIN Discipline ON Enseigner.discipline_id = Discipline.discipline_id JOIN Anneescolaire ON Classe.annee_id = Anneescolaire.annee_id WHERE Enseigner.professeur_id=%s AND Enseigner.classe_id=%s AND  Enseigner.discipline_id=%s;"
        tuple_selection = (professeur_selected[0], classe_selected[0], discipline_selected[0])
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_traduis_enseignements")
        cursor = connection.cursor()
        cursor.execute(sql, tuple_selection)
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records)
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")


        
        
def afficher_enseignements():
    """
    Affiche l'IHM des Enseignements
    """
    global sheet_enseignements
    enseignements = sql_read_enseignements()
    # print("Enseignements: (PDC)")
    # for row in enseignements:
    #     print(row)
    enseignements_traduits = sql_traduis_enseignements()
    frame_enseignements = tk.Frame(f5)
    frame_enseignements.grid()
    sheet_enseignements = Sheet(f5,
                                data=enseignements_traduits,
                                headers=["Nom Professeur", "Prénom", "Classe", "Année scolaire", "Discipline"],
                                set_all_heights_and_widths = True,
                                height=500,
                                width=800)
    sheet_enseignements.hide("row_index")
    sheet_enseignements.grid(row=1, column=0)
    sheet_enseignements.extra_bindings([ ("cell_select", select_enseignement)])        
    sheet_enseignements.enable_bindings(("cell_select",
                                       "single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo"))



def afficher_selections_enseignements():
    """
    Affiche le professeur, la classe et la discipline sélectionnées dans l'IHM Enseignements
    """
    global frame_selection_enseignements
    print('Sélection:',(professeur_selected, classe_selected, discipline_selected))
    frame_selection_enseignements = tk.LabelFrame(f5, text=' (id SQL) Sélection ')
    frame_selection_enseignements.grid(row=0, column=0)
    
    lbl_professeur = tk.Label(frame_selection_enseignements, text = 'Professeur:')
    lbl_professeur.grid(row=0, column=0, sticky=tk.E)
    lbl_professeur_selected = tk.Label(frame_selection_enseignements, text = professeur_selected)
    lbl_professeur_selected.grid(row=0, column=1, sticky=tk.W)
    button_deselect_prof = tk.Button(frame_selection_enseignements, text="Désélectionner", command=deselect_prof)
    button_deselect_prof.grid(row=0,column=2)

    lbl_classe = tk.Label(frame_selection_enseignements, text = 'Classe:')
    lbl_classe.grid(row=1, column=0, sticky=tk.E)
    lbl_classe_selected = tk.Label(frame_selection_enseignements, text = classe_selected)
    lbl_classe_selected.grid(row=1, column=1, sticky=tk.W)
    button_deselect_classe = tk.Button(frame_selection_enseignements, text="Désélectionner", command=deselect_classe)
    button_deselect_classe.grid(row=1,column=2)

    lbl_discipline = tk.Label(frame_selection_enseignements, text = 'Discipline:')
    lbl_discipline.grid(row=2, column=0, sticky=tk.E)
    lbl_discipline_selected = tk.Label(frame_selection_enseignements, text = discipline_selected)
    lbl_discipline_selected.grid(row=2, column=1, sticky=tk.W)
    button_deselect_discipline = tk.Button(frame_selection_enseignements, text="Désélectionner", command=deselect_discipline)
    button_deselect_discipline.grid(row=2,column=2)

def filtrer_mes_enseignements():
    """
    Affiche les enseignements du professeur utilisateur en conservant les autres filtres éventuels.
    """
    global professeur_selected
    index = current_user_id-1
    professeur_selected = (professeur_id[index], prof_Name[index])
    appliquer_selections()

# ------------------------------------------------------------------------------
# EVALUATIONS
# ------------------------------------------------------------------------------


def sql_read_evaluations():
    """
    Se connecte à Mysql et retourne les données brutes concernant les Evaluations réalisées par le professeur connecté
    """
    sql = "SELECT * FROM Evaluation WHERE professeur_id=%s;"
    tuple_selection = (current_user_id ,)
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_read_evaluations")
        cursor = connection.cursor()
        cursor.execute(sql, tuple_selection)
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records)
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")

def sql_traduis_evaluations():
    """
    Se connecte à Mysql et retourne les données traduites concernant les évaluations réalisées par le professeur connecté
    """

    sql = "SELECT Evaluation.evaluation_id, Evaluation.date_controle, Evaluation.date_visible, Discipline.nom, Classe.nom, Anneescolaire.nom, Periode.nom FROM Evaluation INNER JOIN Enseigner ON Evaluation.professeur_id=Enseigner.professeur_id INNER JOIN Discipline  ON Evaluation.discipline_id = Discipline.discipline_id INNER JOIN Classe ON Evaluation.classe_id=Classe.classe_id  INNER JOIN Anneescolaire ON Classe.annee_id=Anneescolaire.annee_id  INNER JOIN Periode ON Evaluation.periode_id=Periode.periode_id WHERE Evaluation.professeur_id=%s  AND Evaluation.Classe_id=Enseigner.classe_id ;"
    tuple_selection=(current_user_id,)
    try:
        print(f"Try to connect to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_traduis_evaluations")
        cursor = connection.cursor()
        cursor.execute(sql, tuple_selection)
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        return(records)
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showwarning("Erreur de connexion", "La base de données est inaccessible")

    
def afficher_evaluations():
    """
    Affiche l'IHM des Evaluations
    """
    global sheet_evaluations
    evaluations = sql_read_evaluations()
    print("Evaluations:")
    print("date_controle, date_visible, discipline_id, professeur_id, classe_id, periode_id")
    for row in evaluations:
        print(row)
    evaluations_traduites = sql_traduis_evaluations()
    frame_evaluations = tk.Frame(f7)
    frame_evaluations.grid()
    sheet_evaluations = Sheet(f7,
                              data=evaluations_traduites,
                              # headers=["Nom Professeur", "Prénom", "Classe", "Année scolaire", "Discipline"],
                              set_all_heights_and_widths = True,
                              height=500,
                              width=800)
    sheet_evaluations.hide("row_index")
    sheet_evaluations.grid(row=1, column=0)


def afficher_selections_evaluations():
    """
    Affiche le professeur, la classe et la discipline sélectionnées dans l'IHM Evaluations
    """
    global frame_selection_evaluations
    print('Sélection:',(professeur_selected, classe_selected, discipline_selected))
    frame_selection_evaluations = tk.LabelFrame(f7, text=' (id SQL) Sélection ')
    frame_selection_evaluations.grid(row=0, column=0)
    
    lbl_professeur = tk.Label(frame_selection_evaluations, text = 'Professeur:')
    lbl_professeur.grid(row=0, column=0, sticky=tk.E)
    lbl_professeur_selected = tk.Label(frame_selection_evaluations, text = professeur_selected)
    lbl_professeur_selected.grid(row=0, column=1, sticky=tk.W)
    button_deselect_prof = tk.Button(frame_selection_evaluations, text="Désélectionner", command=deselect_prof)
    button_deselect_prof.grid(row=0,column=2)

    lbl_classe = tk.Label(frame_selection_evaluations, text = 'Classe:')
    lbl_classe.grid(row=1, column=0, sticky=tk.E)
    lbl_classe_selected = tk.Label(frame_selection_evaluations, text = classe_selected)
    lbl_classe_selected.grid(row=1, column=1, sticky=tk.W)
    button_deselect_classe = tk.Button(frame_selection_evaluations, text="Désélectionner", command=deselect_classe)
    button_deselect_classe.grid(row=1,column=2)

    lbl_discipline = tk.Label(frame_selection_evaluations, text = 'Discipline:')
    lbl_discipline.grid(row=2, column=0, sticky=tk.E)
    lbl_discipline_selected = tk.Label(frame_selection_evaluations, text = discipline_selected)
    lbl_discipline_selected.grid(row=2, column=1, sticky=tk.W)
    button_deselect_discipline = tk.Button(frame_selection_evaluations, text="Désélectionner", command=deselect_discipline)
    button_deselect_discipline.grid(row=2,column=2)

    lbl_periode = tk.Label(frame_selection_evaluations, text = 'Période:')
    lbl_periode.grid(row=3, column=0, sticky=tk.E)
    lbl_periode_selected = tk.Label(frame_selection_evaluations, text = periode_selected)
    lbl_periode_selected.grid(row=3, column=1, sticky=tk.W)
    button_deselect_periode = tk.Button(frame_selection_evaluations, text="Désélectionner", command=deselect_periode)
    button_deselect_periode.grid(row=3,column=2)    



def ajouter_evaluation():
    """
    Crée une évaluation à partir d'un enseignement assuré par le professeur connecté
    """
    if professeur_selected and classe_selected and discipline_selected and periode_selected and (professeur_selected[0] == current_user_id) and sql_read_enseignements():
        print(f"Ajout de l'évaluation: {discipline_selected} {professeur_selected} {classe_selected} {periode_selected}")        
    else:
        messagebox.showwarning("Opération non valide", "Veuillez sélectionner un enseignement que vous assurez et une période dans leurs onglets respectifs.")

        
    

    # if professeur_selected and classe_selected and discipline_selected and not(sql_read_enseignements()):
    #     print(f"Ajout de l'enseignement: {professeur_selected} {classe_selected} {discipline_selected}")
    #     sql_add_enseignement()
    #     sheet_enseignements.destroy()
    #     afficher_enseignements()
    # elif professeur_selected and classe_selected and discipline_selected:
    #     messagebox.showerror("Ajout impossible", "Cet enseignement existe déjà")

    
    
        
# ------------------------------------------------------------------------------
# Application
# ------------------------------------------------------------------------------

root = tk.Tk()
root.title("Gestion des notes (R. Hatterer) CLIENT PROFESSEUR")
root.resizable(False, False)
style = ttk.Style(root)
style.configure("lefttab.TNotebook", tabposition="n")

notebook = ttk.Notebook(root, style="lefttab.TNotebook")

f0 = tk.Frame(notebook, width=800, height=600)  # frame pour la connexion
f1 = tk.Frame(notebook, width=800, height=600)  # frame pour les disciplines
f2 = tk.Frame(notebook, width=800, height=600)  # frame pour les enseignants
f3 = tk.Frame(notebook, width=800, height=600)  # frame pour les élèves
f4 = tk.Frame(notebook, width=800, height=600)  # frame pour les classes
f5 = tk.Frame(notebook, width=800, height=600)  # frame pour les enseignements
f6 = tk.Frame(notebook, width=800, height=600)  # frame pour les années scolaires
f7 = tk.Frame(notebook, width=800, height=600)  # frame pour les évaluations

frame_annees = tk.Frame(f6)
frame_periodes = tk.Frame(f6)

button_mes_enseignements = tk.Button(f5, text='Filtrer mes enseignements',
                                    command=filtrer_mes_enseignements)


button_add_evaluation = tk.Button(f7, text='Ajouter',
                                    command=ajouter_evaluation)

notebook.add(f0, text="Mon compte")

notebook.grid(row=0, column=0, sticky="nswe")
button_mes_enseignements.grid(row=2, column=0)
button_add_evaluation.grid(row=2, column=0)

afficher_IHM_connexion()

root.mainloop()
