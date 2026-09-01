import fastf1
import pandas as pd

pd.set_option('display.max_columns', None)


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

    # Track how many laps each tire set has completed.
    driver_laps["TireAge"] = driver_laps.groupby("Stint").cumcount() + 1

    # Converts lap times from Pandas timedeltas to seconds
    driver_laps["LapTimeSeconds"] = driver_laps["LapTime"].dt.total_seconds()

    # Flag laps where the driver entered/exited the pit lane.
    driver_laps["IsPitLap"] = (
        driver_laps["PitInTime"].notna() | driver_laps["PitOutTime"].notna()
    )

    # Flag laps affected by abnormal track status.
    driver_laps["IsTrackStatusAffected"] = driver_laps["TrackStatus"] != "1"

    # Select laps that are eligible for outlier detection.
    eligible_outlier_laps = driver_laps[
        (~driver_laps["IsPitLap"]) & (~driver_laps["IsTrackStatusAffected"])
    ]

    # Calculate the first and third quartiles of lap times.
    q1 = eligible_outlier_laps["LapTimeSeconds"].quantile(0.25)
    q3 = eligible_outlier_laps["LapTimeSeconds"].quantile(0.75)

    # Calculate the interquartile range (IQR).
    iqr = q3 - q1

    # Calculate the lower and upper outlier boundaries.
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Flag lap times outside the 1.5 × IQR boundaries.
    driver_laps["IsOutlier"] = (
        (driver_laps["LapTimeSeconds"] < lower_bound) | (driver_laps["LapTimeSeconds"] > upper_bound)
    )

    # Keep only laps that are suitable for pace analysis.
    clean_laps = driver_laps[
        (~driver_laps["IsPitLap"])
        & (~driver_laps["IsTrackStatusAffected"])
        & (~driver_laps["IsOutlier"])
    ].copy()

    print(f"\nDriver: {driver}")
    print(f"Number of laps: {len(driver_laps)}")
    print(f"Clean laps available for pace analysis: {len(clean_laps)}")

    # Selects relevant lap information
    columns_to_show = [
        "LapNumber",
        "LapTime",
        "LapTimeSeconds",
        "Compound",
        "Stint",
        "TireAge",
        "Position",
        "IsPitLap",
        "TrackStatus",
        "IsTrackStatusAffected",
        "IsOutlier",
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

    # Calculate representative pace for each stint using clean laps
    print(f"\n{driver} Representative Stint Pace")
    print("--------------------------------")

    for stint_number, stint_laps in clean_laps.groupby("Stint"):

        # Get the tire compound used during this stint
        compound = stint_laps["Compound"].iloc[0]

        # Calculate the median lap time for the stint
        median_lap_time = stint_laps["LapTimeSeconds"].median()

        # Count how many clean laps were used
        clean_lap_count = len(stint_laps)

        print(
            f"Stint {int(stint_number)}: "
            f"{compound} | "
            f"Median pace: {median_lap_time:.3f} seconds | "
            f"{clean_lap_count} clean laps"
        )

    # Find the median pace of each stint
    stint_median_pace = clean_laps.groupby("Stint")["LapTimeSeconds"].median()

    # Find the fastest median stint pace.
    fastest_stint_pace = stint_median_pace.min()

    print(f"\n{driver} Observed Stint Pace Comparison")
    print("-------------------------------------")

    for stint_number, median_lap_time in stint_median_pace.items():

        # Select the clean laps from this stint
        stint_laps = clean_laps[clean_laps["Stint"] == stint_number]

        # Get the tire compound used during this stint
        compound = stint_laps["Compound"].iloc[0]

        # Calculate how much slower this stint was than the fastest stint
        pace_difference = median_lap_time - fastest_stint_pace

        if pace_difference == 0:
            comparison = "fastest stint"
        else:
            comparison = f"+{pace_difference:.3f} seconds"

        print(
            f"Stint {int(stint_number)}: "
            f"{compound} | "
            f"Median: {median_lap_time:.3f} seconds | "
            f"{comparison}"
        )

# Run main() only when this file is executed directly
if __name__ == "__main__":
    main()