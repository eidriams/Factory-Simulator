"""En el simulador se generarán los datos producidos por las máquinas en cada ciclo"""

import time
from machine import Machine
from database import create_table, insert_data, reset_db

class FactorySim():

    def __init__(self):

        create_table()
        self.machines = [
            Machine("Entrada"),
            Machine("Proceso"),
            Machine("Salida")
        ]
    
    def run(self, max_cycles=5):
        
        cycles = 0
        while cycles < max_cycles:
            
            for machine in self.machines:
                machine.update()
                insert_data(machine)
                print(machine)
                
            cycles += 1
            print("---------")
            time.sleep(2)
            
            
        print("Numero de ciclos alcanzado")
                

    def reset(self):
        reset_db()