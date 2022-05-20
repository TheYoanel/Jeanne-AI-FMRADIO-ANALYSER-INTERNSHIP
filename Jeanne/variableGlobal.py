class VariableGlobalON(object):
    def __init__(self, GlobalON=True):
        self.GlobalON = GlobalON
        # self.DicoRequet =

    # Début# GlobalON Fonction #Début#
    def getGlobalON(self):
        return self.GlobalON

    def Global_ON(self):
        self.GlobalON = True

    def Global_OFF(self):
        self.GlobalON = False

    def Global_INVERSION(self):
        test = self.getGlobalON()
        if test == True:
            return self.Global_ON()
        elif test == False:
            return self.Global_OFF()
        else:
            return None
    # Fin# GlobalON Fonction #Fin#