
class myClass():

    # cette fonction est le constructeur de la classe. 
    # Elle est appelée lors de l'instanciation.
    # Elle définit la variable maVariable de la classe. 
    # Les variables de la classe sont accessibles par self.maVariable
    # self représente l'instance de la classe
    def __init__(self):
        print("conrtucteur de la classe")
        self.maVariable = 3

    # Dans une classe, le 1er paramètre est toujours self. 
    # Cela permet d'acceder aux données de la classe
    def changeMaVariable(self,newValue):
        self.maVariable2 = newValue

    def print(self):
        print("valeur: {}".format(self.maVariable))

# crée une instance de la classe. Il ne faut pas oublier les parenthèses !
my = myClass()

# quand on appelle une fonction de la classe, on ne passe pas le 1er paramètre (self)
# Par exemple, pour appeller la fonction print de la classe
my.print()

# pour appeller la fonction changeMaVariable de la classe
my.changeMaVariable(5)

my.print()
