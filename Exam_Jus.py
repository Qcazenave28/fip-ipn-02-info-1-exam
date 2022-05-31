from argparse import ArgumentError, ArgumentTypeError
from enum import Enum

total = 0 # Variable globale pour l'addition

class TailleJus(Enum): 
    Small = 0
    Medium = 1
    Large = 2

class JusType():
    _type = TailleJus.Medium

    def __init__(self, type):
        self._type = type

    @property
    def type(self):
        return self._type

class Jus(): 
    _nom = ""
    _ingredient = ""
    _prix = 5

    def __init__(self, nom, ingredient, prix):
        self._nom = nom
        self._ingredient = ingredient
        self._prix = prix

    @property
    def nom(self):
        return self._nom

    @property
    def ingredient(self):
        return self._ingredient

    @property
    def prix(self):
        return self._prix

class Barmaid():
    _listeJus = list()
    _JusSelectionnee = None
    _TailleSelectionnes = list()
    _estPayee = False
    _estValidee = False

    @property
    def facture(self): #Création de la feuille pour l'addition (AJout de boissson a chaque passage)
        global total
        Boisson = JusSelection.prix
        for Justype in self._TailleSelectionnes:
            if Justype.type == TailleJus.Small:
                Boisson += 0
            elif Justype.type == TailleJus.Medium:
                Boisson += 0.5
            elif Justype.type == TailleJus.Large:
                Boisson += 1
            else:
                raise ArgumentTypeError("TypeJus unknown!")
        total += Boisson
        print("total =", total)    
        return Boisson

    @property
    def estAnnulee(self): 
        return self._JusSelectionnee == None and self._TailleSelectionnes == []

    @property
    def estValide(self): 
        return self._JusSelectionnee != None and len(self._TailleSelectionnes) > 0

    @property
    def estPayee(self): 
        return self._estPayee

    @property
    def estValidee(self): 
        return self._estValidee

    def __init__(self, listeJus):
        if isinstance(listeJus, list):
            if not all(isinstance(elem, Jus) for elem in listeJus):
              raise ArgumentTypeError("must be a list of Jus!")
        else:
            raise ArgumentTypeError("must be a list!")

        self._listeJus = listeJus

    def consulterJus(self):
        return self._listeJus

    def selectionnerJus(self, JusSelection):
        if not isinstance(JusSelection, Jus):
            raise ArgumentTypeError("JusSelection must be a Jus!")
        self._JusSelectionnee = (JusSelection)
        return True

    def selectionnerTaille(self, Taille):
        if isinstance(Taille, list):
            if not all(isinstance(elem, JusType) for elem in Taille):
              raise ArgumentTypeError("must be a list of Taille!")
        else:
            raise ArgumentTypeError("must be a list!")
        
        self._TailleSelectionnes = Taille
        return True

    def valider(self):
        if self.estValide: 
            self._estValidee = True
        else:
            self._estValidee = False
        return self._estValidee

    def annulerCommande(self):
        self._TailleSelectionnes = list()
        self._JusSelectionnee = None
        self._estPayee = False
        self._estValidee = False

    def payer(self, somme):
        global total
        if not self.estValidee:
            raise BaseException("command must be confirmed!")
        reste = somme - total
        if reste < 0:
            self._estPayee = False
        if reste == 0 or reste > 0:
            self._estPayee = True
        return (self._estPayee, reste)

    def imprimer(self):
        if not self.estValidee or not self.estPayee:
            raise BaseException("command must be confirmed and payed!")

        return True



if __name__ == '__main__':
    initJus = [
        Jus("The Boost", "0.5:Mango,2:Oranges,1:Guajana", 4.5),
        Jus("The Fresh", "3:Apples, 1:Ginger, 1:Lemon", 3.5),
        Jus("The Fusion","1:Guava, 0.25:Pineapple, 0.5:Banana", 4.5),
        Jus("The Detox", "3:Carrots, 1:Celery Stick, 1:Guajana", 3)
    ]

    # init Barmaid
    barmaid = Barmaid(initJus)
    print("Barmaid initialisee!")

    # consultation
    jus = barmaid.consulterJus()
    print("consultation Jus:")
    for JusSelection in jus:
        print("- %s / %s / %.2f " %(JusSelection.nom, JusSelection.ingredient, JusSelection.prix))
    choix = 'o'
    #selection jus
    i = input ("Saissir le chiffre correspondant au jus (0/1/2/3): ")
    JusSelection = initJus[int(i)] #Selectionner a la main la valeur = choix jus
    JusChoisi = barmaid.selectionnerJus(JusSelection)
    print("Le jus choisi est :",JusSelection.nom)
    print("Jus Choisi ? %s" % JusChoisi)

    #selection Taille
    Taille = list()
    Taille.append(JusType(TailleJus.Medium))
    TailleSelectionne = barmaid.selectionnerTaille(Taille)
    print("Taille selectionne ? %s" % TailleSelectionne)

    #Augmenter l'addition avec la nouvelle boisson
    barmaid.facture    
    choix = input ("Voulez-vous commander autre chose ? o/n")
    if choix =="o": 
        # selection jus
        i = input("Saissir le chiffre correspondant au jus (0/1/2/3): ")
        JusSelection = initJus[int(i)] #Selectionner a la main la valeur = choix jus
        JusChoisi = barmaid.selectionnerJus(JusSelection)
        print("Le jus choisi est :",JusSelection.nom)
        print("Jus Choisi ? %s" % JusChoisi)

        # selection Taille
        Taille = list()
        Taille.append(JusType(TailleJus.Large))
        TailleSelectionne = barmaid.selectionnerTaille(Taille)
        print("Taille selectionne ? %s" % TailleSelectionne)

        # Augmenter l'addition avec la nouvelle boisson 
        barmaid.facture 

    # while choix != "n" :
    #     # selection jus
    #     i = input ("Saissir le chiffre correspondant au jus (0/1/2/3): ")
    #     JusSelection = initJus[int(i)] #Selectionner a la main la valeur = choix jus
    #     JusChoisi = barmaid.selectionnerJus(JusSelection)
    #     print("Le jus choisi est :",JusSelection.nom)
    #     print("Jus Choisi ? %s" % JusChoisi)

    #     # selection Taille
    #     Taille = list()
    #     Taille.append(JusType(TailleJus.Medium))
    #     TailleSelectionne = barmaid.selectionnerTaille(Taille)
    #     print("Taille selectionne ? %s" % TailleSelectionne)

    #     # Augmenter l'addition avec la nouvelle boisson
    #     barmaid.facture    
    #     choix = input ("Voulez-vous commander autre chose ? o/n")
    #     while choix != 'n' and choix != 'o' :
    #         choix = input ("erreur de saissie, selectionner o ou n")
    
    # validation
    estValidee = barmaid.valider()
    print("commande validee ? %s" % estValidee)

    # payer
    (estPayee, reste) = barmaid.payer(5)
    print("commande payee (%.1f euros) ? %s" % (reste, estPayee))

'''
TO DO LIST : 
AJouter une boucle avec un test "oui/non" pour repondre à la question "Souhaitez vous autre chose" 
Le tout dans une boucle "while test = oui" et lorsqu'on mettra "non" on sortira de la boucle, a chaque passage
ajout des boissons dans l'addition
Ajouter une fonction input

'''