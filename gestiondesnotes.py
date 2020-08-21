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
# AFFICHAGE NOTEBOOK
# ------------------------------------------------------------------------------

def afficher_notebook_gestionnaire():
    """
    Affiche le notebook avec tous les onglets
    """
    afficher_compte_admin()
    notebook.add(f1, text="Disciplines")
    notebook.add(f2, text="Enseignants")
    notebook.add(f3, text="Élèves")
    notebook.add(f4, text="Classes")
    afficher_disciplines()
    afficher_professeurs()
    afficher_eleves()
    afficher_classes()





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
    if role == 'role_gestionnaire':
        frame_connexion.destroy()
        afficher_notebook_gestionnaire()


def sql_read_role():
    """
    Se connecte à MySQL et retourne le rôle de l'utilisateur parmi : role_gestionnaire...
    """
    global cursor, GN_user, GN_password
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
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
    
        
def sql_read_admin():
    """
    Se connecte à Mysql et retourne les données concernant le gestionnaire à partir de la jonction des deux tables Àdministraterus`et `Fonctions`. 
    """
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        print("sql_read_admin")
        cursor = connection.cursor()
        sql = "SELECT FirstName, LastName, Gender ,Birthday , Func_Name, Login FROM Administrateurs INNER JOIN Fonctions WHERE Administrateurs.Func_Id=Fonctions.Func_Id AND Login=%s;"
        tuple_login =  (GN_user,)
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


def afficher_compte_admin():
    """
    Affiche l'IHM du compte administrateur
    """
    global prenom_entry_text, nom_entry_text, combobox_genre, naissance_entry_text, login_entry_text, frame_compte
    records = sql_read_admin()
    
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
    lbl_genre = tk.Label(frame_compte, text="Genre")
    lbl_genre.grid(row=6, column=1, sticky=tk.E)
    lbl_naissance = tk.Label(frame_compte, text="Date de naissance")
    lbl_naissance.grid(row=7, column=1, sticky=tk.E)
    lbl_fonction = tk.Label(frame_compte, text="Fonction")
    lbl_fonction.grid(row=8, column=1, sticky=tk.E)

    # column2
    login_entry_text = tk.StringVar()
    login_entry_text.set(records[0][5])
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

    combobox_genre = ttk.Combobox(frame_compte, values=['M','F'], width=4)
    if records[0][2]=="M":
        combobox_genre.current(0)
    else:
        combobox_genre.current(1)        
    combobox_genre.grid(row=6, column=2, sticky=tk.W)

    naissance_entry_text = tk.StringVar()
    naissance_entry_text.set(records[0][3].strftime("%d/%m/%Y"))
    entry_naissance = tk.Entry(frame_compte, textvariable=naissance_entry_text)
    entry_naissance.grid(row=7, column=2, sticky=tk.W)

    fonction_entry_text = tk.StringVar()
    fonction_entry_text.set(records[0][4])
    entry_fonction = tk.Entry(frame_compte, textvariable=fonction_entry_text) 
    entry_fonction.grid(row=8, column=2, sticky=tk.W)

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
                print(f"Try to connected to MySQL Server as {GN_user}")
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
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_save_compte_admin")
        cursor = connection.cursor()
        sql = "UPDATE Administrateurs SET FirstName=%s, LastName=%s, Gender=%s, Birthday=%s WHERE Login=%s "
        date = datetime.strptime(naissance_entry_text.get(),'%d/%m/%Y').strftime('%Y-%m-%d')
        administrateur = (prenom_entry_text.get(), nom_entry_text.get(), combobox_genre.get(), date, login_entry_text.get())
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
    Retourne un tupple conteant 'discipline_id' et 'disc_Name'.
    discipline_id : liste contenant tous les index générés de façon automatique de
    la table Discipline de la base de données 'bd_gestion_des_notes'.
    disc_Name : liste contenant tous les noms des disciplines (dans l'ordre
    alphabétique) contenus dans la table Discipline de la base de données
    'bd_gestion_des_notes'.
    """
    global GN_password
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_read_disciplines")
        cursor = connection.cursor()
        cursor.execute("select discipline_id, Disc_Name from Discipline ORDER BY Disc_Name ASC;")
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




def afficher_disciplines():
    """
    Affiche un tableau de type tableur avec toutes les disciplines (IHM)
    """
    global sheet_disciplines, discipline_id, disc_Name
    discipline_id, disc_Name = sql_read_disciplines()
    sheet_disciplines = Sheet(f1,
                              data=disc_Name,  # to set sheet data at startup
                              column_width = 250,
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
    Met à jour la base de données en y ajoutant d'éventuelles nouvelles
    disciplines puis rafraîchi l'ÌHM 
    """
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("enregistrer_disciplines")
        cursor = connection.cursor()
        for index in range(len(disc_Name)):
            sql = "UPDATE Discipline SET Disc_Name = %s WHERE discipline_id = %s"
            discipline = (disc_Name[index][0], discipline_id[index])
            cursor.execute(sql, discipline)
            connection.commit()
        # déconnexion
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        # rafraîchissement IHM
        sheet_disciplines.destroy()
        afficher_disciplines()

    except Error as e:
        print("Error while connecting to MySQL", e)



def ajouter_discipline():
    """
    Ajoute une discipline 'À définir' dans le tableau des disciplines (et dans
    la base de données) et sélectionne la ligne. Commence par enregistrer
    l'état précédent du tableau dans la base de données dans le cas où
    l'utilisateur enchaîne les ajouts.
    """
    enregistrer_disciplines()
    global sheet_disciplines
    sql = "INSERT INTO Discipline (Disc_Name) VALUES ('À définir')"
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("ajouter_discipline")
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    except Error as e:
        print("Error while connecting to MySQL", e)
    sheet_disciplines.destroy()
    afficher_disciplines()
    sheet_disciplines.select_row(disc_Name.index(['À définir']))


# ------------------------------------------------------------------------------
# PROFESSEURS
# ------------------------------------------------------------------------------

def sql_read_professeurs():
    """
    Fonction appelée par 'afficher_professeurs()'
    Retourne un tupple conteant: 'professeur_id', 'prof_Name', 'prof_Print'.
    professeur_id : liste contenant tous les index générés de façon automatique de
    la table 'Professeur' de la base de données 'bd_gestion_des_notes'.
    prof_Name : liste contenant tous les noms des professeurs (dans l'ordre
    alphabétique) contenus dans la table Discipline de la base de données
    'bd_gestion_des_notes'.
    'prof_Print': liste affichée dans l'onglet Professeurs
    """
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
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
                              headers=["Titre", "Nom", "Prénom"],
                              height=600,
                              width=800)
    # sheet_professeurs.hide("row_index")
    sheet_professeurs.hide("top_left")
    #sheet_professeurs.hide("header")
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
    Met à jour la base de données en y ajoutant d'éventuelles modifications puis rafraîchi l'IHM pour une remise dans l'ordre alphabétique.
    """
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("enregistrer_professeurs")
        cursor = connection.cursor()
        for index in range(len(prof_Name)):
            sql = "UPDATE Professeur SET prenom=%s, nom=%s,  titre=%s WHERE professeur_id = %s"
            if prof_Print[index][0] in ['M', 'M.']:
                professeur = (prof_Print[index][1],  # FirstName
                              prof_Print[index][2],  # LastName
                              'M',
                              professeur_id[index])
            elif prof_Print[index][0] in ['Mme', 'Mme.']:
                professeur = (prof_Print[index][1],  # FirstName 
                              prof_Print[index][2],  # LastName  
                              'F',
                              professeur_id[index])
            else:
                professeur = (prof_Print[index][1],  # FirstName 
                              prof_Print[index][2],  # LastName  
                              None,
                              professeur_id[index])
            # print(professeur)
            cursor.execute(sql, professeur)
            connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        # Rafraîchissement IHM
        sheet_professeurs.destroy()
        afficher_professeurs()

    except Error as e:
        print("Error while connecting to MySQL", e)


def ajouter_professeur():
    """
    Ajoute un nouveau professeur dans le tableau des professeurs (et dans
    la base de données) et sélectionne la ligne. Commence par enregistrer
    l'état précédent du tableau dans la base de données dans le cas où
    l'utilisateur enchaîne les ajouts.
    """
    enregistrer_professeurs()
    global sheet_professeurs, disc_Name, discipline_id
    if ['À définir'] not in disc_Name:
        ajouter_discipline()
    sql = "INSERT INTO Professeurs (prenom, nom, discipline_id) VALUES (%s, %s, %s)"
    prof_nouveau = ('* Prénom ? *', '* Nom ? *', discipline_id[disc_Name.index(['À définir'])])
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("ajouter_professeur")
        cursor = connection.cursor()
        cursor.execute(sql, prof_nouveau)
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        sheet_professeurs.destroy()
        afficher_professeurs()
        row_index = prof_Name.index('* Nom ? *')
        sheet_professeurs.select_row(row_index)

    except Error as e:
        print("Error while connecting to MySQL", e)

# ------------------------------------------------------------------------------
# ÉLÈVES
# ------------------------------------------------------------------------------

def sql_read_eleves():
    """
    Fonction appelée par 'afficher_eleves()'
    Retourne un tupple conteant 'eleve_id', 'eleves_Name', eleves_Print.
    eleve_id : liste contenant tous les index générés de façon automatique de
    la table 'Eleve' de la base de données 'bd_gestion_des_notes'.
    eleves_Name : liste contenant tous les noms des élèves (dans l'ordre
    alphabétique) contenus dans la table 'Eleve' de la base de données
    'eleves_Print': liste affichée dans l'onglet élèves sous forme de tableau
    """
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("sql_read_eleves")
        cursor = connection.cursor()
        cursor.execute("select eleve_id, prenom, nom, genre, classe_id FROM Eleve ORDER BY nom ASC")        
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
                         height=600,
                         width=800)
    # sheet_eleves.hide("row_index")
    sheet_eleves.hide("top_left")
    # sheet_eleves.hide("header")
    sheet_eleves.grid(row=0, column=0, columnspan=2, sticky="nswe")
    sheet_eleves.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                       "arrowkeys",
                                       "copy",
                                       "cut",
                                       "paste",
                                       "delete",
                                       "undo",
                                       "edit_cell"))


def enregistrer_eleves():
    """
    Met à jour la base de données en y ajoutant d'éventuelles modifications puis rafraîchi l'IHM
    """
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("enregistrer_eleves")
        cursor = connection.cursor()
        for index in range(len(eleves_Name)):
            sql = "UPDATE Eleve SET prenom=%s, nom=%s, genre=%s, classe_id=%s WHERE eleve_id = %s"
            eleve = (eleves_Print[index][1],  # prenom
                     eleves_Print[index][0],  # nom
                     eleves_Print[index][2],  # genre
                     eleves_Print[index][3],  # classe_id
                     eleve_id[index])
            # print(eleve)
            cursor.execute(sql, eleve)
            connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        # Rafraîchissement
        sheet_eleves.destroy()
        afficher_eleves()

    except Error as e:
        print("Error while connecting to MySQL", e)


def ajouter_eleve():
    """
    Ajoute un nouvel élève dans le tableau des élèves (et dans
    la base de données) et sélectionne la ligne. Commence par enregistrer
    l'état précédent du tableau dans la base de données dans le cas où
    l'utilisateur enchaîne les ajouts.
    """
    enregistrer_eleves()
    global sheet_eleves, disc_Name, discipline_id
    sql = "INSERT INTO Eleve (prenom, nom, genre) VALUES (%s, %s, %s)"
    eleve_nouveau = ('* Prénom ? *', '* Nom ? *', 'M ou F')
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("ajouter_eleve")
        cursor = connection.cursor()
        cursor.execute(sql, eleve_nouveau)
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        # Rafraîchissement
        sheet_eleves.destroy()
        afficher_eleves()
        row_index = eleves_Name.index('* Nom ? *')
        sheet_eleves.select_row(row_index)

    except Error as e:
        print("Error while connecting to MySQL", e)

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
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("_charger_classes")
        cursor = connection.cursor()
        cursor.execute("select classe_id, nom, niveau, annee_id from Classe ORDER BY annee_id DESC, nom;")
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

def afficher_classes():
    """
    Affiche un tableau de type tableur avec toutes les classes
    """
    global sheet_classes, classe_id, classe_Name, classe_Print
    classe_id, classe_Name, classe_Print = _charger_classes()
    sheet_classes = Sheet(f4,
                          data=classe_Print,  # to set sheet data at startup
                          headers=["Classe", "Niveau", "Année scolaire"],
                          height=600,
                          width=800)
    # sheet_classes.hide("row_index")
    sheet_classes.hide("top_left")
    # sheet_classes.hide("header")
    sheet_classes.grid(row=0, column=0, columnspan=2, sticky="nswe")
    sheet_classes.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                   "arrowkeys",
                                   "copy",
                                   "cut",
                                   "paste",
                                   "delete",
                                   "undo",
                                   "edit_cell"))


def enregistrer_classes():
    """
    Met à jour la base de données en y ajoutant d'éventuelles nouvelles
    classes.
    """
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("enregistrer_classes")
        cursor = connection.cursor()
        for index in range(len(classe_Name)):
            sql = "UPDATE Classe SET nom = %s, niveau = %s, annee_id = %s WHERE classe_id = %s"
            classe = (classe_Print[index][0], classe_Print[index][1], classe_Print[index][2],  classe_id[index])
            cursor.execute(sql, classe)
            connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    except Error as e:
        print("Error while connecting to MySQL", e)
    sheet_classes.destroy()
    afficher_classes()


def ajouter_classe():
    """
    Ajoute une 'À définir' dans le tableau des disciplines (et dans
    la base de données) et sélectionne la ligne. Commence par enregistrer
    l'état précédent du tableau dans la base de données dans le cas où
    l'utilisateur enchaîne les ajouts.
    """
    enregistrer_classes()
    global sheet_classes
    sql = "INSERT INTO Classe (nom, niveau, annee_id) VALUES ('À définir', 'À définir', 'À définir')"
    try:
        print(f"Try to connected to MySQL Server as {GN_user}")
        connection = mysql.connector.connect(host=GN_host,
                                             database=GN_database,
                                             user=GN_user,
                                             password=GN_password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version", db_Info)
        print("ajouter_classe")
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        sheet_classes.destroy()
        afficher_classes()
        sheet_classes.select_row(classe_Name.index('À définir'))
    except Error as e:
        print("Error while connecting to MySQL", e)






    
def cell_select(self, response):
    print(response)



# Application 

root = tk.Tk()
root.title("Gestion des notes")
root.resizable(False, False)
style = ttk.Style(root)
style.configure("lefttab.TNotebook", tabposition="n")

notebook = ttk.Notebook(root, style="lefttab.TNotebook")

f0 = tk.Frame(notebook, width=800, height=600)  # frame pour la connexion
f1 = tk.Frame(notebook, width=800, height=600)  # frame pour les disciplines
f2 = tk.Frame(notebook, width=800, height=600)  # frame pour les enseignants
f3 = tk.Frame(notebook, width=800, height=600)  # frame pour les élèves
f4 = tk.Frame(notebook, width=800, height=600)  # frame pour les classes

button_add_discipline = tk.Button(f1, text='Ajouter',
                                  command=ajouter_discipline)
button_save_disciplines = tk.Button(f1, text='Enregistrer',
                                    command=enregistrer_disciplines)
button_add_prof = tk.Button(f2, text='Ajouter',
                            command=ajouter_professeur)
button_save_profs = tk.Button(f2, text='Enregistrer',
                              command=enregistrer_professeurs)
button_add_eleve = tk.Button(f3, text='Ajouter',
                             command=ajouter_eleve)
button_save_eleves = tk.Button(f3, text='Enregistrer',
                               command=enregistrer_eleves)
button_add_classe = tk.Button(f4, text='Ajouter',
                              command=ajouter_classe)
button_save_classes = tk.Button(f4, text='Enregistrer',
                                command=enregistrer_classes)
notebook.add(f0, text="Mon compte")

notebook.grid(row=0, column=0, sticky="nw")

button_add_discipline.grid(row=1, column=0)
button_save_disciplines.grid(row=1, column=1)
button_add_prof.grid(row=1, column=0)
button_save_profs.grid(row=1, column=1)
button_add_eleve.grid(row=1, column=0)
button_save_eleves.grid(row=1, column=1)
button_add_classe.grid(row=1, column=0)
button_save_classes.grid(row=1, column=1)

afficher_IHM_connexion()

root.mainloop()
