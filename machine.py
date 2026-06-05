"""La línea que vamos a simular tendra 3 máquinas, Entrada, Proceso y Salida, cada una de las máquinas tendrá funcionalidades básicas que se engloban en la clase Machine"""

import random

class Machine():

    def __init__(self,name):

        self.name = name
        self.status = "RUNNING"
        self.production_count = 0
        self.errors_count = 0

    def update(self):

        # Status monitor for possible failures
    
        if random.random() < 0.1: 
            self.status = "ERROR"
            self.errors_count += 1
        
        # Machine no longer produces by itself
        # if self.status == "RUNNING":
        #     self.production_count += 1

        elif self.status == "ERROR":
            # Recuperarse de un error
            if random.random() < 0.3:
                self.status = "RUNNING"

    def __str__(self):

        return (
        f"{self.name}:\n"
        f"Status:{self.status} | "
        # f"Production:{self.production_count} | "
        f"Errors:{self.errors_count}"
        )