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


class StrStyle():
    GRAY = '\033[90m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

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


"""
BLACK = '\033[30m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
BRIGHT_RED = '\033[91m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'

RESET = '\033[0m' # called to return to standard terminal text color

print(BLACK + "black" + RESET)
print(GREEN + "green" + RESET)
print(YELLOW + "yellow" + RESET)
print(BLUE + "blue" + RESET)
print(MAGENTA + "magenta" + RESET)
print(CYAN + "cyan" + RESET)
print(LIGHT_GRAY + "light gray" + RESET)
print(BRIGHT_RED + "bright red" + RESET)
print(BRIGHT_YELLOW + "bright yellow" + RESET)
print(BRIGHT_BLUE + "bright blue" + RESET)
print(BRIGHT_MAGENTA + "bright magenta" + RESET)
print(BRIGHT_CYAN + "bright cyan" + RESET)
print(WHITE + "white" + RESET)
"""