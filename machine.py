"""La línea que vamos a simular tendra 3 máquinas, Entrada, Proceso y Salida, cada una de las máquinas tendrá funcionalidades básicas que se engloban en la clase Machine"""

import random

class Machine():

    def __init__(self,name):

        self.name = name
        self.status = "RUNNING"
        self.production_count = 0
        self.errors_count = 0

    def update(self):

        # Simulación de un posible fallo
        # random() devuelve un float entre 0.0 y 1.0, que equivaldría a dar un porcentaje de que se produzca un fallo
        if random.random() < 0.1: 
            self.status = "ERROR"
            self.errors_count += 1
        
        if self.status == "RUNNING":
            self.production_count += 1 # La maquina procesa una pieza con exito

        elif self.status == "ERROR":
            # Recuperarse de un error
            if random.random() < 0.3:
                self.status = "RUNNING"

    def __str__(self):
        return (
        f"{self.name} | "
        f"Status:{self.status} | "
        f"Production:{self.production_count} | "
        f"Errors:{self.errors_count}"
        )