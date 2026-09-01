import fastf1
import pandas as pd
import matplotlib


def main():
    print("F1 Race Strategy Analyzer")
    print("-------------------------")

    print("Cache enabled.")

    # Store downloaded FastF1 data in the local cache folder.
    fastf1.Cache.enable_cache("cache")

    print("Loading race data...")

    # Get the 2024 Bahrain Grand Prix race session.
    session = fastf1.get_session(2024, "Bahrain", "R")

    # Download/load the timing data for the session.
    session.load()

    print("\nRace loaded successfully!")
    print(f"Event: {session.event['EventName']}")
    print(f"Session: {session.name}")
    print(f"Date: {session.date}")
    print(f"Drivers: {len(session.drivers)}")


if __name__ == "__main__":
    main()