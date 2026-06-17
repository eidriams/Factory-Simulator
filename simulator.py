"""En el simulador se generarán los datos producidos por las máquinas en cada ciclo"""

import time
from machine import Machine
from database import create_table, insert_data, reset_db, insert_simulation_data
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

    
    def run_queues(self, max_cycles):
        
        # Pieces that enter the first queue with no errors
        self.created_pieces = 0

        for cycle in range(1,max_cycles+1):

            entrada = self.machines[0]
            proceso = self.machines[1]
            salida = self.machines[2]
            
            print(f"\n** Cycle Nº {cycle} **\n")

            # MACHINE 1 ENTRADA

            entrada.update()

            if entrada.status == "RUNNING":
                # If no error in first machine, add to queue for the second one
                self.queue_1.add_piece()
                self.created_pieces += 1

            insert_data(entrada,cycle)

            print(
                f"{entrada.name}\n"
                f"Utilization: {entrada.utilization()}\n"
                f"MTBF: {entrada.mtbf()} cycles\n"
                f"Status: {entrada.status}\n"
                f"Errors: {entrada.errors_count}\n"
                
                )
            
            print(f"Cycles: Run: {entrada.running_cycles} | Idle: {entrada.idle_cycles} | Error: {entrada.error_cycles} | Maintenance: {entrada.maintenance_time}\n")

            # MACHINE 2 PROCESO
            
            if proceso.status not in ["ERROR", "MAINTENANCE"]:

                if self.queue_1.size() == 0:
                    proceso.status = "IDLE"
                else:
                    proceso.status = "RUNNING"

            proceso.update()

            if proceso.status == "RUNNING":

                # If no error, take a piece from queue_1
                piece = self.queue_1.remove_piece()
                # If a piece is taken (no errors), it moves to next queue
                if piece:
                    self.queue_2.add_piece()

            elif proceso.status == "IDLE":
                pass

            insert_data(proceso,cycle)
            
            print(
                f"{proceso.name}\n"
                f"Utilization: {proceso.utilization()}\n"
                f"MTBF: {proceso.mtbf()} cycles\n"
                f"Status: {proceso.status}\n"
                f"Errors: {proceso.errors_count}\n"
                
                )
            
            print(f"Cycles: Run: {proceso.running_cycles} | Idle: {proceso.idle_cycles} | Error: {proceso.error_cycles} | Maintenance: {proceso.maintenance_time}\n")

            # MACHINE 3 SALIDA
            
            if salida.status not in ["ERROR", "MAINTENANCE"]:

                if self.queue_2.size() == 0:
                    salida.status = "IDLE"
                else:
                    salida.status = "RUNNING"

            salida.update()

            if salida.status == "RUNNING":

                piece = self.queue_2.remove_piece()
                # If last machine is successful, process is completed and we add 1 to production count
                if piece:
                    salida.production_count += 1

            elif salida.status == "IDLE":
                pass

            insert_data(salida,cycle)
            
            print(
                f"{salida.name}\n"
                f"Utilization: {salida.utilization()}\n"
                f"MTBF: {salida.mtbf()} cycles\n"
                f"Status: {salida.status}\n"
                f"Errors: {salida.errors_count}\n"
                
                )
            
            print(f"Cycles: Run: {salida.running_cycles} | Idle: {salida.idle_cycles} | Error: {salida.error_cycles} | Maintenance: {salida.maintenance_time}\n")


            print("----------------------------------------")

            print(
                f"Created:{self.created_pieces}\n"
                f"Q1:{self.queue_1.size()}\n"
                f"Q2:{self.queue_2.size()}\n"
                f"Completed:{salida.production_count}"
            )
            print("-------------")

            insert_simulation_data(
                cycle,
                self.queue_1.size(),
                self.queue_2.size(),
                self.created_pieces,
                salida.production_count)
            
            
            time.sleep(2)

        print("\nNumber of cycles achieved")
        
        print(
            f"Items on process: "
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
                
        # # Test if any piece is miss during process
        # print("Process completed without missing pieces?")
        # print(self.created_pieces == salida.production_count + self.queue_1.size() + self.queue_2.size())

    def reset(self): 
        reset_db()
    


    # def run(self, max_cycles=5):
        
    #     cycles = 0
    #     while cycles < max_cycles:
            
    #         for machine in self.machines:
    #             machine.update()
    #             insert_data(machine)
    #             print(machine)
                
    #         cycles += 1
    #         print("----------------------------------")
    #         time.sleep(2)

    #     print("Numero de ciclos alcanzado")