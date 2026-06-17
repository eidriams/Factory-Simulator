import sqlite3 as sql
from machine import Machine
from simulator import FactorySim



class Analysis():

    def __init__(self):
        self.conn = sql.connect("factory.db")
        self.cursor = self.conn.cursor()

    # def prod_by_machine(self):

    #     self.cursor.execute("""
    #         SELECT machine, MAX(production)
    #         FROM machine_data
    #         GROUP BY machine
    #         """)
    
        # return self.cursor.fetchall()

    def completed(self):
        self.cursor.execute("""
        SELECT MAX(completed_pieces)
        FROM simulation_data
        """)

        return self.cursor.fetchone()[0]


    def total_cycles(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM machine_data
        """)
        # Total rows of generated table
        cycles = self.cursor.fetchone()[0]

        self.cursor.execute("""
        SELECT COUNT(DISTINCT machine)
        FROM machine_data
        """)

        # Dynamic counting machines to set number of cycles
        machines = self.cursor.fetchone()[0]
        
        return cycles//machines


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

        return created == completed + q1 + q2
    


    def summary(self):

        print("\n===» FACTORY REPORT «===\n")

        print(f"Cycles run on database: {self.total_cycles()}"
        )

        print(f"Total production: {self.completed()}"
        )

        print(f"Production rate: {self.prod_rate():.1f}%")

        print(
            f"Total rows on 'Error' state: "
            f"{self.total_errors()}\n"
            f"Error rate: "
            f"{self.error_rate():.2f}%"
        )

        print(f"\nStatus 'Error' by Machine during simulation: ")
        for machine, error in self.errors_by_machine():
            print(f" • {machine}: {error}")

        print(
            f"\nMost Problematic Machine: "
            f"{self.most_prob_machine()[0]} → {self.most_prob_machine()[1]}"
        )

        print(f"Process completed without missing pieces? → {self.simulation_integrity()}")