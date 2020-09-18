class Product:

    def __init__(self, type, modele, ref):
        self.type = type
        self.modele = modele
        self.ref = ref


    def __repr__(self):
        return "Product('{}', '{}', {})".format(self.type, self.modele, self.ref)