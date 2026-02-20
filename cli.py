from InquirerPy import inquirer, get_style
from InquirerPy.base import Choice
from sqlite3 import IntegrityError

from queries import *
from utils import *

import os

style = get_style({"questionmark":"hidden", "answermark":"hidden", "pointer": "#61afef", "input": "#98c379", "answer":"hidden"})
back_choice = Choice(0, "(Retour)")

#Menu de départ
def menu():
    clear_screen()
    choice = inquirer.select(message="", 
                             choices=[Choice(1, "Se connecter"), Choice(2, "Créer un compte"), Choice(0, "Quitter")], 
                             style=style).execute()
    
    if choice == 1 :
        try :
            user = sign_in()
        except KeyboardInterrupt :
            return 1
        if user:
            user_board(user)
        return 1
    
    elif choice == 2 : 
        try :
            sign_up()
        except KeyboardInterrupt:
            pass
        return 1

    else : 
        return 0

# Créer un compte
def sign_up():
    print(StrStyle.BOLD + " Créer un compte " + StrStyle.RESET + StrStyle.GRAY + "(retour : ctrl-C)\n" + StrStyle.RESET)
    while True:
        username = inquirer.text(message="Nom d'utilisateur :", style=style).execute()
        password = inquirer.text(message="Mot de passe :", style=style).execute()
        if inquirer.confirm("Confirmer ?", style=style).execute():
            try :
                add_user(username, password)
            except(IntegrityError) : 
                print("Ce nom d'utilisateur n'est pas disponible")
                continue
            inquirer.select(message="L'utilisateur a bien été créé", choices=[back_choice], style=style).execute()
            return
        else:
            print("L'utilisateur n'a pas été créé")
            
    

# Se connecter
def sign_in():
    print(StrStyle.BOLD + " Se connecter " + StrStyle.RESET + StrStyle.GRAY + "(retour : ctrl-C)\n" + StrStyle.RESET)
    while True:
        username = inquirer.text(message="Nom d'utilisateur : ", style=style).execute()
        user = get_user(username)
        if not user : 
            print("Utilisateur non reconnu")
            continue
        else : 
            password = inquirer.secret(message="Mot de passe : ", validate=lambda pswrd : check_password(pswrd, user.password), style=style).execute()
            return user

# Menu utilisateur
def user_board(user):
    while True : 
        clear_screen()
        print(StrStyle.BOLD  + "\n  Bienvenue " + StrStyle.MAGENTA + user.username + StrStyle.RESET + StrStyle.BOLD + " !" + StrStyle.RESET)
        choice = inquirer.select(message="", 
                                choices=[Choice(1,"Voir les livres empruntés"), Choice(2, "Parcourir la bibliothèque"), Choice(0,"Se déconnecter")], 
                                style=style).execute()
        if choice == 1 :
            user_books(user)
        elif choice == 2 : 
            library_books(user)
        elif choice == 0 :
            if inquirer.confirm(message="Déconnexion?", style=style).execute() : 
                return

# Emprunts (utilisateur)
def user_books(user):
    while True :
        clear_screen()
        print(StrStyle.BOLD + "\n Livres empruntés" + StrStyle.RESET)
        loans = get_loans(user.get_id())
        loan = inquirer.fuzzy(message="", 
                              choices=loans + [back_choice], 
                              style=style).execute() 
        if loan : 
            while True : 
                clear_screen()
                loan.show_card()
                options = [Choice(1, "(Rendre ce livre)")] + [back_choice]
                choice = inquirer.select(message="", choices=options, style=style).execute()
                if choice == 1 : 
                    if inquirer.confirm(message="Rendre " + str(loan) + " ?", style=style).execute():
                        return_book(loan.get_id())
                        inquirer.select(message="Livre retourné", choices=[back_choice], style=style).execute()
                        break  
                    else :
                        continue
                else : 
                    break
        else :
            return

# Bibliothèque
def library_books(user):
    while True: 
        clear_screen()
        print(StrStyle.BOLD + "\n Bibliothèque" + StrStyle.RESET)
        books = get_books()
        book = inquirer.fuzzy(message="", 
                              choices= books + [back_choice], 
                              style=style).execute()
        
        if book: 
            while True: 
                clear_screen()
                book.show_card()
                options = [Choice(1, "Emprunter")] if book.isAvailable() else []
                options += [back_choice]
                choice = inquirer.select(message="", choices=options, style=style).execute()
                if choice == 1 : 
                    if inquirer.confirm(message="Emprunter " + str(book) + " ?", style=style).execute():
                        add_loan(user.get_id(), book.get_id())
                        inquirer.select(message="Livre emprunté", choices=[back_choice], style=style).execute()
                        break
                    else : 
                        continue
                else : 
                    break

        else:
            return

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        print("La base de données n'a pas été trouvée. Exécuter 'db.py' pour la mettre en place.")
        quit()
    while menu(): 
        continue
