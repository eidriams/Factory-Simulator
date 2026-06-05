"""En el simulador se generarán los datos producidos por las máquinas en cada ciclo"""

import time
from machine import Machine
from database import create_table, insert_data, reset_db
from queue_manager import ProductionQueue

class FactorySim():

    def __init__(self):

        create_table()
        self.machines = [
            Machine("Entrada"),
            Machine("Proceso"),
            Machine("Salida")
        ]
        # Queues between machines "Entrada"-"Proceso" and "Proceso"-"Salida"
        self.queue_1 = ProductionQueue()
        self.queue_2 = ProductionQueue()
    
    def run(self, max_cycles=5):
        
        cycles = 0
        while cycles < max_cycles:
            
            for machine in self.machines:
                machine.update()
                insert_data(machine)
                print(machine)
                
            cycles += 1
            print("----------------------------------")
            time.sleep(2)

        print("Numero de ciclos alcanzado")
            
    
    def run_queues(self, max_cycles):

        for cycle in range(max_cycles):

            entrada = self.machines[0]
            proceso = self.machines[1]
            salida = self.machines[2]

            entrada.update()
            if entrada.status == "RUNNING":
                # If no error in first machine, add to queue for the second one
                self.queue_1.add_piece()
            print(entrada)
            
            proceso.update()
            if proceso.status == "RUNNING":
                # If no error, take a piece from queue_1
                piece = self.queue_1.remove_piece()

                # If a piece is taken (no errors), it moves to next queue
                if piece:
                    self.queue_2.add_piece()
            print(proceso)
            
            salida.update()
            if salida.status == "RUNNING":
                # If no error take a piece from queue_2
                piece = self.queue_2.remove_piece()

                print("Piece: ",piece)

                if piece:
                    # If last machine is successful, process is completed and we add 1 to production count
                    salida.production_count += 1
            print(salida)
            print("----------------------------------------")
            time.sleep(2)

        print("Number of cycles achieved") 
        print(
            f"Production during cycles: "
            f"{salida.production_count}"
        )
        print(
            f"Pieces on first queue: {self.queue_1.size()} | "
            f"Pieces on second queue: {self.queue_2.size()}"
        )
                


    def reset(self):
        reset_db()
        