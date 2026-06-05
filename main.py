from simulator import FactorySim
from analysis import Analysis


def main():

    simulador = FactorySim()
    analysis = Analysis()
    
    while True:
        print("\n===== FACTORY SIMULATOR =====")

        print("1. Run Simulation")
        print("2. Show Statistics")
        print("3. Reset Database")
        print("4. Exit")

        option = input("\nSelect an option: ")

        if option == "1":
            cycles = int(input("\nSelect number of cycles to run: "))
            simulador.run_queues(cycles)

        elif option == "2":
            analysis.summary()

        elif option == "3":
            simulador.reset()            

        elif option == "4":
            # Cierra conexion con base de datos
            analysis.conn.close()
            print("Closing program...")
            break

        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()


# Improve some aspects of the menu behaviour like no existing table when choosing option 2