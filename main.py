import fastf1
import pandas as pd
import matplotlib


def main():
    print("F1 Race Strategy Analyzer")
    print("-------------------------")
    print(f"FastF1 version: {fastf1.__version__}")
    print(f"Pandas version: {pd.__version__}")
    print(f"Matplotlib version: {matplotlib.__version__}")
    print("Project setup is working!")


if __name__ == "__main__":
    main()