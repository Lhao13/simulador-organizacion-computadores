
#-Clase que representa una línea dentro de la caché principal del procesador---------------------------------------------------------------------------------------------------------------------

class Line:

    def __init__(self, size):
        self.use = 0
        self.modified = 0
        self.valid = 0
        self.tag = 0
        self.data = [0] * size
