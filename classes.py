from utils import StrStyle

class Book():
    def __init__(self, id, title=None, author=None, year=None, status=None):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def get_id(self):
        return self.id
    
    def isAvailable(self):
        return self.status
    
    def __str__(self):
        return self.title + " - " + self.author
    
    def show_card(self, show_status=True) : 
        card =  "Titre  : {titre}\n".format(titre = self.title if self.title else "Non renseigné")
        card += "Auteur : {author}\n".format(author = self.author if self.author else "Non renseigné")
        card += "Année  : {year}\n".format(year = self.year if self.year else "Non renseignée")
        if show_status : 
            card += "\nStatut : {status}".format(status=StrStyle.GREEN + "Disponible" + StrStyle.RESET if self.status
                                                    else StrStyle.RED + "Non disponible" + StrStyle.RESET)
        print(card)

class User():
    def __init__(self, id, username, password) : 
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id
    
    def __str__(self) : 
        return self.username
    
class Loan():
    def __init__(self, id, date, book):
        self.id = id
        self.date = date
        self.book = book

    def __str__(self):
        return str(self.book)
    
    def get_id(self):
        return self.id
    
    def get_book(self):
        return self.book
    
    def get_date(self):
        return self.date
    
    def show_card(self):
        self.book.show_card(show_status=False)
        card = "Emprunté le : {date}".format(date = self.date)
        print(card)


#TODO
class Filter():
    def __init__(self, author="", year="" , available_only=False) : 
        self.author = author
        self.year = year
        self.available_only = available_only

    def __str__(self) : 
        filter_str = []
        if self.author : 
            filter_str += ["auteur : {}".format(self.author)]
        if self.year :
            filter_str += ["année : {}".format(self.year)]
        if self.available_only : 
            filter_str += ["Disponible"]
        return "{" + " | ".join(filter_str) + "}"
    
    def set_value(self, column, value):
        if column == "author" : 
            self.author = value
        elif column == "year" : 
            self.year = value
        elif column == "available_only":
            self.available_only = value

    def erase(self):
        self.author = ""
        self.year = ""
        self.genre = ""
        self.available_only = False

    def to_sql(self) :
        filter_str = []
        if self.author : 
            filter_str += ["author='{}'".format(self.author)]
        if self.year:
            filter_str += ["publish_year='{}'".format(self.year)]     
        if self.available_only:
            filter_str += ["status=1"]

        if filter_str : 
            return "WHERE " + " AND ".join(filter_str)
        else : 
            return ""
