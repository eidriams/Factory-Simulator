import sqlite3 as sql
from machine import Machine
from simulator import FactorySim



class Analysis():

    def __init__(self):
        self.conn = sql.connect("factory.db")
        self.cursor = self.conn.cursor()

    def rows(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM machine_data
        """)
        # Total rows of generated table
        return self.cursor.fetchone()[0]

    def completed(self):
        self.cursor.execute("""
        SELECT MAX(completed_pieces)
        FROM simulation_data
        """)

        return self.cursor.fetchone()[0]
    
    def created(self):
        self.cursor.execute("""
        SELECT MAX(created_pieces)
        FROM simulation_data
        """)

        return self.cursor.fetchone()[0]


    def total_cycles(self):

        # self.cursor.execute("""
        # SELECT COUNT(*)
        # FROM machine_data
        # """)
        # Total rows of generated table
        rows = self.rows()

        self.cursor.execute("""
        SELECT COUNT(DISTINCT machine)
        FROM machine_data
        """)

        # Dynamic counting machines to set number of cycles
        machines = self.cursor.fetchone()[0]
        
        return rows//machines


    # def total_production(self):        

    #     data = self.completed()
    #     total = 0

    #     for machine, production in data:
    #         total += production
        
    #     return total
    #     # Could be only one line of code
    #     # return sum(production for _,production in data)

    def prod_rate(self):

        cycles = self.total_cycles()
        prod = self.completed()

        if cycles == 0:
            return 0

        rate = prod/cycles * 100

        return rate
    
    def prod_rate2(self):

        cycles = self.total_cycles()
        prod = self.created()

        if cycles == 0:
            return 0

        rate = prod/cycles * 100

        return rate
    
    def total_errors(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM machine_data
            WHERE status = 'ERROR'
            """)

        return self.cursor.fetchone()[0]
    
    
    def error_rate(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM machine_data
        """)
        # Total rows of generated table
        total = self.cursor.fetchone()[0]
        # If no errors occurs
        if total == 0:
            return 0
        errors = self.total_errors()

        # % of records with status = ERROR
        return errors / total * 100
    
    def most_prob_machine(self):

        self.cursor.execute("""
        SELECT machine, COUNT(*)
        FROM machine_data WHERE status = 'ERROR'
        GROUP BY machine ORDER BY COUNT(*) DESC
        LIMIT 1                                                    
        """)

        result = self.cursor.fetchone()
        # Case with no errors
        if result is None:
            return ("None",0)

        return result

    def errors_by_machine(self):

        self.cursor.execute("""
        SELECT machine, COUNT(*)
        FROM machine_data WHERE status = 'ERROR'
        GROUP BY machine                                                     
        """)

        return self.cursor.fetchall()
    
    def error_type_dist(self):

        self.cursor.execute("""
        SELECT machine, error_type, COUNT(*)
        FROM machine_data
        WHERE error_type IS NOT NULL                         
        GROUP BY machine, error_type
        ORDER BY machine
        """)

        return self.cursor.fetchall()

    def error_distribution(self):

        self.cursor.execute("""
        SELECT machine, error_type, COUNT(*)
        FROM error_log 
        GROUP BY machine, error_type
        ORDER BY machine
        """)

        dist = self.cursor.fetchall()
        
        return dist   

    
    def database_ready(self):

        # Check if database has tables in it

        self.cursor.execute("""
        SELECT name 
        FROM sqlite_master
        WHERE type='table'
        """)

        tables = [table[0] for table in self.cursor.fetchall()]

        return ( "machine_data" in tables and "simulation_data" in tables )

    
    def has_data(self):

        # Check if tables has any data on it

        if not self.database_ready():
            return False

        self.cursor.execute("""
        SELECT COUNT(*) FROM machine_data 
        """)
        
        return self.cursor.fetchone()[0] > 0
    
    def simulation_integrity(self):

        self.cursor.execute("""
        SELECT 
        created_pieces,
        MAX(completed_pieces),
        queue_1,
        queue_2
        FROM simulation_data 
        ORDER BY cycle DESC
        LIMIT 1
        """)
        
        result = self.cursor.fetchone()

        if result is None:
            return False

        created, completed, q1, q2 = result

        # print(f"{created} == {completed} + {q1} + {q2}") Check if its picking the right variables
        if created == completed + q1 + q2:
            return "  • PASSED"
        else:
            return "  • FAILED"
    
    # Max queue reached
    def bottleneck(self):

        self.cursor.execute("""
        SELECT MAX(queue_1), MAX(queue_2)
        FROM simulation_data 
        """)

        q1max, q2max = self.cursor.fetchone()

        return f"  • queue_1 = {q1max}\n  • queue_2 = {q2max}"
    
    def avg_queue(self):

        self.cursor.execute("""
        SELECT AVG(queue_1), AVG(queue_2)
        FROM simulation_data
        """)

        avgq1, avgq2 = self.cursor.fetchone()

        print(f"  • AVG Q1 = {avgq1:.2f}\n  • AVG Q2 = {avgq2:.2f}\n")

        if avgq1 > avgq2:
            return f"   Bottleneck on queue 1: {avgq1} pieces on average\n"
        elif avgq1 < avgq2:
            return f"   Bottleneck on queue 2: {avgq2} pieces on average\n"
        else:
            return f"   Queues bottleneck balanced: {avgq1} pieces on average\n"
    

    # def bottleneck_analysis(self):

    #     avg_q1, avg_q2 = self.avg_queue()

    #     if avg_q1 > avg_q2:
    #         return "Queue 1", avg_q1
    #     elif avg_q1 < avg_q2:
    #         return "Queue 2", avg_q2
    #     else:
    #         return "Balanced", avg_q1


    # Time on what type of maintenance
    def tot_maintenance(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM machine_data
        WHERE maintenance_type = 'CORRECTIVE'
        """)
        corrective = self.cursor.fetchone()[0]
    
        self.cursor.execute("""
        SELECT COUNT(*)
        FROM machine_data
        WHERE maintenance_type = 'PREVENTIVE'
        """)
        preventive = self.cursor.fetchone()[0]
    
        return corrective, preventive
    
    # How many type of errors occur
    def severity_dist(self):

        self.cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM machine_data
        WHERE error_type IS NOT NULL
        GROUP BY error_type
        ORDER BY COUNT(*) DESC
        """)

        return self.cursor.fetchall()

    # Time of every machine on state RUNNING during simulation
    def overall_util(self):
        
        self.cursor.execute("""
        SELECT COUNT(*)
        FROM machine_data
        """)
        # Total rows of generated table
        total = self.cursor.fetchone()[0]

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM machine_data
        WHERE status="RUNNING"
        """)

        run = self.cursor.fetchone()[0]

        # If no row with RUNNING occurs
        if total == 0:
            return 0
        
        # % of records with status = RUNNING
        result = run / total * 100
        return f"{result:.2f}"
    
    def state_distribution(self):

        self.cursor.execute("""
        SELECT status, COUNT(*)
        FROM machine_data
        GROUP BY status
        ORDER BY COUNT(*) DESC
        """)

        return self.cursor.fetchall()



    


    def summary(self):

        print("\n===» FACTORY REPORT «===\n")

        print(f"→ Cycles run on database: {self.total_cycles()}"
        )

        print(f"→ Production:")

        print(f"  • Created Pieces: {self.created()}")

        print(f"  • Completed Pieces: {self.completed()}")

        print(f"  • Production rate per simulation cycles: {self.prod_rate():.1f} %")

        print(f"  • Production rate of pieces that entered first queue: {self.prod_rate2():.1f} %")

        print(f"\n→ Overall machine utilization: {self.overall_util()}%")

        print(f"→ Error rate: {self.error_rate():.2f}%"
        )

        print(
            f"\n→ Most Problematic Machine: "
            f"{self.most_prob_machine()[0]} → {self.most_prob_machine()[1]}\n"
        )

        print(f"→ Bottleneck:\n"
            f"{self.avg_queue()}")
        # bottle, avg = self.bottleneck_analysis()
        # print(f"  • {bottle} (AVG {avg:.2f} pieces)\n")
        

        print(f"→ Max queues:\n{self.bottleneck()}\n")

        print(f"→ Maintenances:")
        print(f"  • Corrective: {self.tot_maintenance()[0]}")
        print(f"  • Preventive: {self.tot_maintenance()[1]}")

        print(f"\n→ State distribution:")
        for status, count in self.state_distribution():
            print(f"  • {status}: {count} ({100*count/self.rows():.2f}%)")
        
        print(f"\n→ Status 'Error' by Machine during simulation: ")
        for machine, error in self.errors_by_machine():
            print(f"  • {machine}: {error} ({100*error/self.rows():.2f} %)")

        print(f"\n→ Error Distribution: ")

        data = self.error_distribution()
        downtime_cycles = self.error_type_dist()
        downtime_dict = {}

        for machine,severity,cycles in downtime_cycles:
            downtime_dict[machine,severity] = cycles
        
        
        machines = {
            "Entrada": {"MINOR": 0, "MODERATE": 0, "MAJOR": 0},
            "Proceso": {"MINOR": 0, "MODERATE": 0, "MAJOR": 0},
            "Salida": {"MINOR": 0, "MODERATE": 0, "MAJOR": 0}
        }
        # Take values returned by error_distribution method and insert on dict machines (ir oder to convserve values that are 0)
        for machine,severity, count in data:
            machines[machine][severity] = count

        # Once we have fill the dict, we can write down to show properly
        for machine,values in machines.items():

            minordt = downtime_dict.get((machine,"MINOR"),0)
            moddt = downtime_dict.get((machine,"MODERATE"),0)
            majordt = downtime_dict.get((machine,"MAJOR"),0)

            avg_minor = minordt / values['MINOR'] if values['MINOR'] else 0
            avg_mod   = moddt / values['MODERATE'] if values['MODERATE'] else 0
            avg_maj   = majordt / values['MAJOR'] if values['MAJOR'] else 0

            print(f"\n ♦ {machine}:")

            print(f"    • MINOR: {values['MINOR']} Errors | "
                f"Downtime: {minordt} cycles | "
                f"{100*minordt/self.rows():.2f} % | "
                f"{avg_minor} cycles/error")
            print(f"    • MODERATE: {values['MODERATE']} Errors | "
                f"Downtime: {moddt} cycles | "
                f"{100*moddt/self.rows():.2f} % | "
                f"{avg_mod} cycles/error")
            print(f"    • MAJOR: {values['MAJOR']} Errors | "
                f"Downtime: {majordt} cycles | "
                f"{100*majordt/self.rows():.2f} % | "
                f"{avg_maj} cycles/error")

        print(f"\n→ Distribution of errors cycles:")
        
        for severity, count in self.severity_dist():
            print(f"  • {severity}: {count} | ({100*count/self.rows():.2f} %)")
        
        print(f"\n→ Process integrity:\n{self.simulation_integrity()}")

        