"""La línea que vamos a simular tendra 3 máquinas, Entrada, Proceso y Salida, cada una de las máquinas tendrá funcionalidades básicas que se engloban en la clase Machine"""

import random

class Machine():

    def __init__(self,name):

        self.name = name
        self.status = "RUNNING"
        self.production_count = 0
        self.errors_count = 0 # Total failures occur
        self.error_type = None # Minor, Moderate or Major

        self.running_cycles = 0
        self.idle_cycles = 0
        self.error_cycles = 0 # Total rows on ERROR state during simulation
        self.current_error_duration = 0 # Actual error
        self.required_error_duration = 0 # Actual error duration
        self.errors_since_maintenance = 0

        # Duration in cycles of maintenance
        self.maintenance_cycles = 0
        self.maintenance_time = 0
        self.maintenance_type = None 
        # Preventive or Corrective
        self.preventive_maintenance = 0
        self.corrective_maintenance = 0

        self.running_cycles = 0
        self.idle_cycles = 0
        self.error_cycles = 0

    def update(self):

        # Status monitor 

        # 1. MAINTENANCE

        if self.status == "MAINTENANCE":
            
            self.maintenance_cycles -= 1
            self.maintenance_time += 1

            if self.maintenance_cycles <= 0:

                self.status = "RUNNING"
                self.maintenance_cycles = 0
                self.maintenance_type = None
                self.error_type = None
            
            return

        # 2. ERROR

        if self.status == "ERROR":

            self.error_cycles += 1
            self.current_error_duration += 1

            if self.current_error_duration >= self.required_error_duration:

                self.status = "MAINTENANCE"
                self.maintenance_type = "CORRECTIVE"
                self.corrective_maintenance += 1

                self.current_error_duration = 0

                print(f"{self.name} going on {self.maintenance_type} Maintenance for {self.maintenance_cycles} cycles.\n")

            return

        # 3. PREVENTIVE

        if self.errors_since_maintenance >= 5:

            self.status = "MAINTENANCE"
            self.maintenance_type = "PREVENTIVE"
            self.preventive_maintenance += 1
            self.errors_since_maintenance = 0

            print(f"{self.name} going on {self.maintenance_type} Maintenance for {self.maintenance_cycles} cycles.\n")
        
            return

        # 4. COUNTERS

        if self.status == "RUNNING":
            self.running_cycles += 1
            self.maintenance_type = None
            self.error_type = None

        elif self.status == "IDLE":
            self.idle_cycles += 1


        # 5. FAILURE
        
        # If it's running or idle, there are failures chances
        if random.random() < 0.1: 
            
            self.errors_count += 1
            self.errors_since_maintenance += 1

            severity = random.randint(1,10)

            if severity <= 3:
                self.required_error_duration = 1
                self.error_type = "MINOR"
                self.maintenance_cycles = 1
            elif severity <= 7:
                self.required_error_duration = 2
                self.error_type = "MODERATE"
                self.maintenance_cycles = 2
            else:
                self.required_error_duration = 4
                self.error_type = "MAJOR"
                self.maintenance_cycles = 3

            self.status = "ERROR"

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