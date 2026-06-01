"""En el simulador se generarán los datos producidos por las máquinas en cada ciclo"""

import time
from machine import Machine

class FactorySim():

    def __init__(self):

        self.machines = [
            Machine("Entrada"),
            Machine("Proceso"),
            Machine("Salida")
        ]
    
    def run(self):
        cycles = 0
        while True:
            
            for machine in self.machines:
                machine.update()
                print(f"{machine.name} | Status:{machine.status} | Production Count:{machine.prduction_count} | Errors:{machine.errors_count}")
                
            cycles += 1
            print("---------")
            time.sleep(2)
            
            if cycles == 5:
                print("Numero de ciclos alcanzado")
                break


