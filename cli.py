from InquirerPy import inquirer, prompt, get_style
from InquirerPy.base import Choice
from queries import *
from sqlite3 import IntegrityError
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-" * 40)
    print(" " * 10 + StrStyle.BOLD + "📚 T i n y L i b 📚" + StrStyle.RESET)
    print("-" * 40)

#style_dict = {"questionmark":"hidden", "answermark":"hidden", "pointer": "#61afef", "input": "#98c379"}
style = get_style({"questionmark":"hidden", "answermark":"hidden", "pointer": "#61afef", "input": "#98c379", "answer":"hidden"})


def menu():
    clear_screen()
    choice = inquirer.select(message="", 
                             choices=[Choice(0, "Se connecter"), Choice(1, "Créer un compte"), Choice(2, "Quitter")], 
                             style=style).execute()
    if choice == 1 : 
        try :
            sign_up()
        except KeyboardInterrupt:
            pass
        return 1
    
    elif choice == 0 :
        try :
            user = sign_in()
        except KeyboardInterrupt :
            return 1
        if user:
            user_board(user)
        return 1

    else : 
        return 0

# Créer un compte
def sign_up():
    print(StrStyle.BOLD + " Créer un compte " + StrStyle.RESET + StrStyle.GRAY + "(retour : ctrl-C)\n" + StrStyle.RESET)
    while True:
        name = inquirer.text(message="Nom d'utilisateur :", style=style).execute()
        password = inquirer.text(message="Mot de passe :", style=style).execute()
        if inquirer.confirm("Confirmer ?", style=style).execute():
            try :
                add_user(name, password)
                inquirer.select(message="L'utilisateur a bien été créé", choices=["(Retour)"], style=style).execute()
                return
            except(IntegrityError) : 
                print("Ce nom d'utilisateur n'est pas disponible")
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

# menu utilisateur
def user_board(user):
    while True : 
        clear_screen()
        print(StrStyle.BOLD  + "\n  Bienvenue " + StrStyle.MAGENTA + user.username + StrStyle.RESET + StrStyle.BOLD + " !" + StrStyle.RESET)
        choice = inquirer.select(message="", choices=["Voir les livres empruntés", "Parcourir la bibliothèque", "Se déconnecter"], style=style).execute()
        if choice == "Voir les livres empruntés" :
            user_books(user)
        elif choice == "Parcourir la bibliothèque": 
            library_books(user, Filter())
        elif choice == "Se déconnecter" :
            if inquirer.confirm(message="Déconnexion?", style=style).execute() : 
                return


def user_books(user):
    books = get_user_books(user.id)
    while True :
        clear_screen()
        print(StrStyle.BOLD + "\n Livres empruntés" + StrStyle.RESET)
        book = inquirer.fuzzy(message="", choices=books+["(Retour)"], style=style).execute()
        if book == "(Retour)" :
            return
        else : 
            if book_card(book, user, "board"):
                books = get_user_books(user.id)


def library_books(user, filter):
    books = get_books(filter)
    all_books = True
    while True: 
        clear_screen()
        print(StrStyle.BOLD + "\n Bibliothèque" + StrStyle.RESET)
        book = inquirer.fuzzy(message="", choices=["(Filtre : {})".format(filter)]+books+["(Retour)"], style=style).execute()
        if book == "(Retour)" : 
            return
        elif book == "(Filtre : {})".format(filter):
            filter_menu(user, filter)
            books = get_books(filter)
        else : 
            if book_card(book, user, "library"):
                books = get_books(filter)


def book_card(book, user, source):
    while True: 
        clear_screen()
        book.show_card(source == "library")

        if source == "board" : 
            options = ["(Rendre ce livre)", "(Retour)"]
        elif source == "library" : 
            options = ["(Emprunter)", "(Retour)"] if book.status else ["(Retour)"]

        choice = inquirer.select(message="", choices=options, style=style).execute()

        if choice == "(Rendre ce livre)":
            if inquirer.confirm(message="Rendre " + book.title + " ?", style=style).execute():
                return_book(user.id, book.id)
                inquirer.select(message="Livre retourné", choices=["(Retour)"], style=style).execute()
                return 1

        elif choice == "(Emprunter)" :
            if inquirer.confirm(message="Emprunter " + book.title + " ?", style=style).execute():
                add_loan(user.id, book.id)
                inquirer.select(message="Livre emprunté", choices=["(Retour)"], style=style).execute()
                return 1

        elif choice == "(Retour)" :
            return 0



def filter_menu(user, filter):
    #TODO
    print("not implemented yet")
    return

"""
def filter_menu(user, filter):
    while True :
        clear_screen()
        choice = inquirer.select(message="Filtrer : ",
                                choices=["Auteur [{}]".format(filter.author), 
                                        "Année de publication [{}]".format(filter.year), 
                                        "Livres disponibles uniquement [{}]".format("Oui" if filter.available_only else "Non"),
                                        "(Effacer)",
                                        "(Valider)"], style=style).execute()
        
        if choice[:2] in ["Au", "An", "Ge"] :
            category = "author" if (choice[:2]=="Au") else ("year" if choice[:2]=="An" else "genre")
            selection = inquirer.select(message=choice, choices=get_list(category)+["(Effacer)", "(Retour)"]).execute()

            if selection == "(Effacer)":
                filter.set_value(category, "")
            elif selection == "(Retour)" :
                continue
            else :
                filter.set_value(category, selection)

        elif choice[0] == "L":
                filter.set_value("available_only", not filter.available_only)

        elif choice == "(Effacer)" :
            filter.erase()

        elif choice == "(Valider)" :
            break
"""
       
            





if __name__ == "__main__":
    while menu(): 
        continue
