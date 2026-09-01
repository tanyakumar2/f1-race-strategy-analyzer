import fastf1


def main():
    print("F1 Race Strategy Analyzer")
    print("-------------------------")

    # Enables FastF1's cache so downloaded data can be reused
    fastf1.Cache.enable_cache("cache")

    print("Loading race data...")

    # Select session to analyze
    year = 2024
    circuit = "Bahrain"
    session_type = "R"

    # Gets the chosen session
    session = fastf1.get_session(year, circuit, session_type)

    # Load lap times, tire data, driver information, and other session data
    session.load()

    print("\nRace loaded successfully!")
    print(f"Event: {session.event['EventName']}")
    print(f"Session: {session.name}")
    print(f"Drivers: {len(session.drivers)}")

    # Select driver to analyze
    driver = "VER"

    # Select driver's laps
    driver_laps = session.laps.pick_drivers(driver)

    # Creates a copy so we can add analysis columns
    driver_laps = driver_laps.copy()

    # Converts lap times from Pandas timedeltas to seconds
    driver_laps["LapTimeSeconds"] = driver_laps["LapTime"].dt.total_seconds()

    print(f"\nDriver: {driver}")
    print(f"Number of laps: {len(driver_laps)}")

    # Selects relevant lap information
    columns_to_show = [
        "LapNumber",
        "LapTime",
        "LapTimeSeconds",
        "Compound",
        "Stint",
        "Position",
        "PitInTime",
        "PitOutTime",
    ]

    # Displays the relevant lap information for driver's first 20 laps
    print("\nFirst 20 laps:")
    print(driver_laps[columns_to_show].head(20))

    # Grouping driver's laps by stint
    print(f"\n{driver} Tire Strategy")
    print("-------------")

    # For each stint, this gives the stint number + all the laps in that stint
    for stint_number, stint_laps in driver_laps.groupby("Stint"):

        # Get the tire compound used during this stint.
        compound = stint_laps["Compound"].iloc[0]

        # Find the first and last lap of the stint
        start_lap = int(stint_laps["LapNumber"].min())
        end_lap = int(stint_laps["LapNumber"].max())

        # Count how many laps were in that stint
        stint_length = len(stint_laps)

        # Prints summary of tire strategy for the race
        print(
            f"Stint {int(stint_number)}: "
            f"{compound} | "
            f"Laps {start_lap}-{end_lap} | "
            f"{stint_length} laps"
        )

# Run main() only when this file is executed directly
if __name__ == "__main__":
    main()