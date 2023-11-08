import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# make global scope variables to be used in any function i want:
# For Cities:
Cities = ['chicago', 'new york city', 'washington']
# For Months:
Months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
# For Weekdays:
Days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter the name of the city you want to know more.\n'
                     'You can chose between Chicago, New York City and Washington: \n> ')
        city = city.lower()
        if city in Cities:
            break
        else:
            print("Sorry, there isn\'t data for that city. Please enter another city.\n")
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Is there any particular month you are interested?\n'
                      'You can chose any month between January to June or type ALL to analyse all months: \n> ')
        month = month.lower()
        if month in Months:
            break
        else:
            print("Sorry, there isn\'t data for that month. Please enter another month.\n")

        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day do you want to analyse?\n'
                    'You can type any day or type all to analyse ALL days.\n> ')
        day = day.lower()
        if day in Days:
            break
        else:
            print("Sorry, that isn\'t a day. Please enter a day.\n")

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['week_day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = Months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['week_day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Based on my calculations, the most common month was:', common_month)
    # display the most common day of week
    common_day_week = df['week_day'].mode()[0]
    print('And the most common day of the week was:', common_day_week)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('You may also want to know that the most \n'
          'common start hour was:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('I can also tell you that the most commonly used\n'
          'start station was {}'.format(most_common_start_station))
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('And the most commonly used\n'
          'end station was {}'.format(most_common_end_station))
    # display most frequent combination of start station and end station trip
    commonly_start_to_end_stat = df[['Start Station', 'End Station']].mode().loc[0]
    print('Finally, the most frequent combination of \n'
          'start station and end station trip was: \n'
          '*{}* as starting station and \n'
          '*{}* as end station.'
          .format(commonly_start_to_end_stat[0], commonly_start_to_end_stat[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration_total = df['Trip Duration'].sum() / 3600
    print('The total travel time in hours was {}.'.format(duration_total))
    # display mean travel time
    travel_mean = df['Trip Duration'].mean() / 3600
    print('And the total travel mean in hours was {}.'.format(travel_mean))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print('There are some interesting stats from our users. \n'
          'the gender count was:')
    # Display counts of gender
    while True:
        if 'Gender' in df.columns or 'Birth Year' in df.columns:
            gender_types = df['Gender'].value_counts()
            print(gender_types)
            # Display earliest, most recent, and most common year of birth:
            birth_yob = df['Birth Year']
            # the most earliest birth year
            earliest_yob = birth_yob.min()
            print("The earliest year of birth was: ", earliest_yob)
            # the most recent birth year
            most_recent_yob = birth_yob.max()
            print("The most resent year of birth was: ", most_recent_yob)
            # the most common birth year
            common_yob = birth_yob.mode()[0]
            print("And the most common year of birth was: ", common_yob)
            break
        else:
            print('Gender Stats can\'t be determined')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    print('\nCalculating Raw Data Stats...\n')
    start_time = time.time()
    x = 0
    while True:
        raw = input('Would you like to see explore the data?\n'
                    'If so type YES or type NO to skip.\n>')
        raw = raw.lower()
        if raw != 'yes':
            print('Thank you for Exploring US BikeShare')
            break
        else:
            x = x + 10
            print(df.iloc[x: x + 10])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()