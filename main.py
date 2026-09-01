import fastf1


def main():
    print("F1 Race Strategy Analyzer")
    print("-------------------------")

    fastf1.Cache.enable_cache("cache")

    print("Loading race data...")

    session = fastf1.get_session(2024, "Bahrain", "R")
    session.load()

    print("\nRace loaded successfully!")
    print(f"Event: {session.event['EventName']}")
    print(f"Session: {session.name}")
    print(f"Drivers: {len(session.drivers)}")

    # Select Max Verstappen's laps.
    driver_laps = session.laps.pick_drivers("VER")

    print("\nDriver: VER")
    print(f"Number of laps: {len(driver_laps)}")

    # Show a few useful columns from the first 10 laps.
    columns_to_show = [
        "LapNumber",
        "LapTime",
        "Compound",
        "Stint",
        "Position",
        "PitInTime",
        "PitOutTime",
    ]

    print("\nFirst 10 laps:")
    print(driver_laps[columns_to_show].head(10))


if __name__ == "__main__":
    main()