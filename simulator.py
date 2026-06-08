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

        self.created_pieces = 0

        for cycle in range(max_cycles):

            entrada = self.machines[0]
            proceso = self.machines[1]
            salida = self.machines[2]
            

            entrada.update()
            if entrada.status == "RUNNING":
                # If no error in first machine, add to queue for the second one
                self.queue_1.add_piece()
                self.created_pieces += 1

            print(entrada)
            
            proceso.update()
            if proceso.status != "ERROR":

                if self.queue_1.size() == 0:
                    proceso.status = "IDLE"
                
                else:
                    proceso.status = "RUNNING"
                    # If no error, take a piece from queue_1
                    piece = self.queue_1.remove_piece()

                    # If a piece is taken (no errors), it moves to next queue
                    if piece:
                        self.queue_2.add_piece()
                
            print(proceso)
            
            salida.update()
            if salida.status != "ERROR":

                if self.queue_2.size() == 0:
                    salida.status = "IDLE"
                
                else:
                    salida.status = "RUNNING"
                    # If no error take a piece from queue_2
                    piece = self.queue_2.remove_piece()

                    if piece:
                        # If last machine is successful, process is completed and we add 1 to production count
                        salida.production_count += 1
                
            print(salida)


            print("----------------------------------------")

            print(
                f"Created:{self.created_pieces}\n"
                f"Q1:{self.queue_1.size()}\n"
                f"Q2:{self.queue_2.size()}\n"
                f"Completed:{salida.production_count}"
            )
            print("-------------")
            time.sleep(2)

        print("Number of cycles achieved")
        print(
            f"Pieces created: "
            f"{self.created_pieces}"

        )
        print(
            f"Pieces completed during simulation: "
            f"{salida.production_count}"
        )
        print(
            f"Pieces left on first queue: {self.queue_1.size()}, {self.queue_1}\n"
            f"Pieces left on second queue: {self.queue_2.size()}, {self.queue_2}"
        )
                
        # Test if any piece is miss during process
        print("Process completed without missing pieces?")
        print(self.created_pieces == salida.production_count + self.queue_1.size() + self.queue_2.size())

    def reset(self): 
        reset_db()
        