import sqlite3 as sql



class Analysis():

    def __init__(self):
        self.conn = sql.connect("factory.db")
        self.cursor = self.conn.cursor()

    def prod_by_machine(self):

        self.cursor.execute("""
            SELECT machine, MAX(production)
            FROM machine_data
            GROUP BY machine
            """)

        return self.cursor.fetchall()

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


    def total_production(self):        

        data = self.prod_by_machine()
        total = 0

        for machine, production in data:
            total += production
        
        return total
        # Could be only one line of code
        # return sum(production for _,production in data)
    
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

        return self.cursor.fetchone()

    def errors_by_machine(self):

        self.cursor.execute("""
        SELECT machine, COUNT(*)
        FROM machine_data WHERE status = 'ERROR'
        GROUP BY machine                                                     
        """)

        return self.cursor.fetchall()

    def summary(self):

        print("\n===» FACTORY REPORT «===\n")

        print(
            f"Cycles run on database: "
            f"{self.total_cycles()}"
        )

        print(
            f"Total production: "
            f"{self.total_production()}"
        )

        print(
            f"Total Errors: "
            f"{self.total_errors()}\n"
            f"Error rate: "
            f"{self.error_rate():.2f}%"
        )

        print(f"\nProduction by Machine: ")
        for machine, production in self.prod_by_machine():
            print(f" • {machine}: {production}")
        

        print(f"\nErrors by Machine: ")
        for machine, error in self.errors_by_machine():
            print(f" • {machine}: {error}")

        print(
            f"\nMost Problematic Machine: "
            f"{self.most_prob_machine()[0]} → {self.most_prob_machine()[1]}"
        )

        