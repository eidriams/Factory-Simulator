"""La línea que vamos a simular tendra 3 máquinas, Entrada, Proceso y Salida, cada una de las máquinas tendrá funcionalidades básicas que se engloban en la clase Machine"""

import random

class Machine():

    def __init__(self,name):

        self.name = name
        self.status = "RUNNING"
        self.production_count = 0
        self.errors_count = 0 # Total

        self.running_cycles = 0
        self.idle_cycles = 0
        self.error_cycles = 0
        self.current_error_duration = 0 # Actual error
        self.required_error_duration = 0 # Actual error duration
        self.errors_since_maintenance = 0
        # Duration in cycles of maintenance
        self.maintenance_cycles = 3
        self.maintenance_time = 0
        self.maintenance_type = None # Preventive or Corrective
        self.preventive_maintenance = 0
        self.corrective_maintenance = 0

        self.running_cycles = 0
        self.idle_cycles = 0
        self.error_cycles = 0
        # Duration in cycles of maintenance
        self.maintenance_cycles = 3
        self.maintenance_time = 0

    def update(self):

        # Status monitor 

        if self.status == "ERROR":
            # Number of cycles with status = ERROR
            self.error_cycles += 1
            self.current_error_duration += 1

            if self.current_error_duration >= self.required_error_duration:
                self.status = "MAINTENANCE"
                self.maintenance_type = "CORRECTIVE"
                self.corrective_maintenance += 1
                self.current_error_duration = 0
            return

        elif self.status == "IDLE":
            self.idle_cycles += 1

        elif self.status == "RUNNING":
            self.running_cycles += 1

        elif self.status == "MAINTENANCE":

            self.maintenance_cycles -= 1
            self.maintenance_time += 1

            if self.maintenance_cycles <= 0:

                self.status = "RUNNING"
                self.maintenance_cycles = 3
            
            return
        
        # If it is running, there are failures chances 
        if random.random() < 0.1: 
            
            self.errors_count += 1
            self.errors_since_maintenance += 1
            # Nº of cycles on error status
            self.required_error_duration = random.randint(1,3)

            self.status = "ERROR"

            return
        
        if self.errors_since_maintenance >= 5:

            self.status = "MAINTENANCE"
            self.maintenance_type = "PREVENTIVE"
            self.preventive_maintenance += 1
            self.errors_since_maintenance = 0
            
        return

    def __str__(self):

        return (
        f"{self.name}:\n"
        f"Status:{self.status} | "
        f"Errors:{self.errors_count}"
        )
    
    def utilization(self):

        total = (
            self.running_cycles +
            self.idle_cycles +
            self.error_cycles +
            self.maintenance_time
        )

        if total == 0:
            return 0
        
        # % of running time 
        util = self.running_cycles / total * 100
        return f"{util:.2f}%"
    
    def mtbf(self):
        # Mean time between failures
        if self.errors_count == 0:
            return 0
        
        # Failures for every X number of cycles
        fail = self.running_cycles / self.errors_count
        return f"{fail:.2f}"