def fonctionLorsqueEvenementSeProduit(result):
    print("resultat: {}".format(result))

class maClasse():

    # cette fonction est le constructeur de la classe. 
    # Elle definit un pointeur vers la fonction qui est zero
    def __init__(self):
        self.pointeurFunction = 0

    # Permet d'enregistrer ce qu'il faut faire quand l'evenement se produit
    def definitPointeur(self,fct):
        self.pointeurFunction = fct

    # Permet de simuler un evenement
    def evenement(self,x):
        # si le pointeur de fonction est definit
        if (not self.pointeurFunction==0):
            # on appelle la fonction
            self.pointeurFunction(x)
        else:
            print("pas de fonction definie")


my = maClasse()
my.evenement(3) # affichera "pas de fonction definie"
my.definitPointeur(fonctionLorsqueEvenementSeProduit) # on definit la fonction à appeler
my.evenement(3) # la fonction fonctionLorsqueEvenementSeProduit est appelée
