import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    # Get city input
    list_of_cities = ', '.join(option.title() for option in list(CITY_DATA.keys()))
    city = input('Please enter the name of the city you would like to analyze. We have data for the following cities: {cities}\n'.format(cities = list_of_cities)).lower()
    while city not in CITY_DATA.keys():
        city = input('We don\'t have data on this city. Please try again\n').lower()
    
    # Confirm city selection
    print(city.title() + ' selected for analysis\n')
    
    
    # TO DO: get user input for month (all, january, february, ... , june)
    
    # Get month input
    month = input('Would you like to look at data from a specific month? We have data on the the following months: {options}\nIf not, please enter \'all\'\n'.format(options = ', '.join(month.capitalize() for month in months))).lower()
    while month != 'all' and month not in months:
        month = input('We don\'t have data on this month. Please try again').lower()
    
    # Confirm month selection
    if month == 'all':
        print('All months selected for analysis\n')
    else:
        print(month.capitalize() + ' selected for analysis\n')
    
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    # Get weekday input
    day = input('Would you like to filter data by weekday? We have data for the the following days: {options}\nIf not, please enter \'all\'\n'.format(options = ', '.join(day.capitalize() for day in weekdays))).lower()
    while day != 'all' and day not in weekdays:
        day = input('We don\'t have data for this day. Please try again').lower()
    # Confirm weekday selection
    if day == 'all':
        print('All weekdays selected for analysis\n')
    else:
        print(day.capitalize() + ' selected for analysis\n')
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month
    if month != 'all':
        df = df[df['month'] == months.index(month) + 1]
    # filter by day
    if day != 'all':
        df = df[df['weekday'] == day.capitalize()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month name
    print('Most common month:', months[df['month'].mode()[0] - 1].capitalize())

    # display the most common day of week
    print('Most common day of week:', df['weekday'].mode()[0])

    # display the most common start hour
    print('Most common start hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print('Most common combination:\n - Start: {start}\n - End: {end}'.format(start = popular_combination[0], end = popular_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    print('Total travel time:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print('Count per user type:\n{count}\n'.format(count = df['User Type'].value_counts()))

    # display counts of gender
    try:
        print('Count per gender:\n{count}\n'.format(count = df['Gender'].value_counts()))
    except KeyError:
        print('No data on Gender available\n')

    # display earliest, most recent, and most common year of birth
    try:
        print('Earliest year of birth:', df['Birth Year'].min().astype(int))
        print('Most recent year of birth:', df['Birth Year'].max().astype(int))
        print('Most common year of birth:', df['Birth Year'].value_counts().idxmax().astype(int))
    except KeyError:
        print('No data on years of birth available\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data = input('Would you like to see an excerpt from the table? Enter yes or no.\n').lower()
        if raw_data == 'yes':
            print(df.head(30))
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
