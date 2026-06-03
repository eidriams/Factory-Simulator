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

        errors = self.total_errors()
        # % of records with status = ERROR
        return errors / total * 100
    
    def summary(self):

        print("\n--- FACTORY REPORT ---")

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

        print(
            f"Production by Machine: "
            f"{self.prod_by_machine()}"
        )