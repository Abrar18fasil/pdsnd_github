import pandas as pd
import time

CITY_DATA = {
    'chicago': 'chicago_cleaned.csv',
    'new york city': 'new_york_city_cleaned.csv',
    'washington': 'washington_cleaned.csv'
}


def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable."""
    df = pd.read_csv(CITY_DATA[city.lower()])

    # Convert the Start Time and End Time columns to datetime
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    # Extract month, day of week, and hour from the start time
    df['month'] = df['start_time'].dt.month
    df['day_of_week'] = df['start_time'].dt.day_name()
    df['hour'] = df['start_time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df


def display_data(df):
    """Displays 5 rows of data at a time upon user request."""
    start_loc = 0
    while True:
        # Ask the user if they want to see data
        show_data = input("\nDo you want to see 5 rows of raw data? Enter 'yes' or 'no': ").strip().lower()
        if show_data != 'yes':
            break

        # Display the next 5 rows of data
        end_loc = start_loc + 5
        print(df.iloc[start_loc:end_loc])
        start_loc = end_loc


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()

    # Most common month
    most_common_month = df['month'].mode()[0]

    # Most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]

    # Most common start hour
    most_common_start_hour = df['hour'].mode()[0]

    print(f"\nMost Common Month: {most_common_month}")
    print(f"Most Common Day of Week: {most_common_day_of_week}")
    print(f"Most Common Start Hour: {most_common_start_hour:02d}:00")

    print(f"\nThis took {time.time() - start_time} seconds.")


def station_stats(df):
    """
    Displays statistics on the most popular stations and trips.
    
    Args:
        df (DataFrame): The dataset containing station and trip data.
    """
    start_time = time.time()

    # Calculate statistics
    most_common_start_station = df['start_station'].mode()[0]
    most_common_end_station = df['end_station'].mode()[0]
    most_common_trip = df.groupby(['start_station', 'end_station']).size().idxmax()

    # Output results
    print("\nStation and Trip Statistics:")
    print(f"Most Common Start Station: {most_common_start_station}")
    print(f"Most Common End Station: {most_common_end_station}")
    print(f"Most Common Trip: {most_common_trip[0]} -> {most_common_trip[1]}")
    print(f"Calculation Time: {time.time() - start_time:.2f} seconds")
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    start_time = time.time()

    # Total travel time
    total_travel_time = df['tripduration'].sum()

    # Average travel time
    average_travel_time = df['tripduration'].mean()

    print(f"\nTotal Travel Time: {total_travel_time} seconds")
    print(f"Average Travel Time: {average_travel_time} seconds")

    print(f"\nThis took {time.time() - start_time} seconds.")


def user_stats(df):
    """Displays statistics on bikeshare users."""
    start_time = time.time()

    # User types
    user_types = df['user_type'].value_counts()

    print(f"\nUser Types:\n{user_types}")

    print(f"\nThis took {time.time() - start_time} seconds.")


def main():
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city, month, and day
    city = input("Enter the city (Chicago, New York City, Washington): ").strip().lower()
    month = input("Enter the month (January to June or 'all' for no filter): ").strip().lower()
    day = input("Enter the day of the week (e.g., Monday) or 'all' for no filter: ").strip().lower()

    try:
        df = load_data(city, month, day)

        # Display raw data upon request
        display_data(df)

        # Calculate and display stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

    except KeyError:
        print(f"Error: The city '{city}' is not recognized. Please check the city name and try again.")

    # Ask if the user wants to restart
    restart = input("\nWould you like to restart? Enter 'yes' or 'no': ").strip().lower()
    if restart == 'yes':
        main()


if __name__ == "__main__":
    main()
