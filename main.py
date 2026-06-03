from simulator import FactorySim
from analysis import Analysis


def main():

    simulador = FactorySim()
    simulador.run()

    analysis = Analysis()
    analysis.summary()


if __name__ == "__main__":
    main()
