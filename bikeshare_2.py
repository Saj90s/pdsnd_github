import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'jun', 'all']

DAY_DATA = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city_name = ''
    while city_name.lower() not in CITY_DATA:
        city_name = input("\nWhich city would you like to explore, washington, chicago, new york?\n")
        if city_name in CITY_DATA:

            city = CITY_DATA[city_name]
        else:
            print("Oops, sorry we only have data for Washington, chicago, or New York.")

    # get user input for month (all, january, february, ... , june)
    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input("\n On which month you would like to explore? january, february, march, april, may, jun or type 'all'\n")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
        else:
            print("Sorry, we only  have a specific months. Try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_name = ''
    while day_name.lower() not in DAY_DATA:
        day_name = input("\nChoose which day you are looking for? if  you do not a specific type 'all' to see all the days of the week.\n")
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
        else:
           print("Oops, you might have spelled the day wrong! Try again please.")


    print('-'*50)
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

    df = pd.read_csv(city)


    df['Start Time'] = pd.to_datetime(df['Start Time'])


    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':

        month = MONTH_DATA.index(month) + 1


        df = df.loc[df['month'] == month]

    if day != 'all':

        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df["month"].mode()[0]
    print("The most common month is:" + MONTH_DATA[common_month].title())


    # display the most common day of week

    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day is:' + str(common_day_of_week))
    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common hour is :' + str(common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is:' + common_start_station)


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station:' + common_end_station)

    # display most frequent combination of start station and end station trip


    frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print("\nThe most frequent combination of start staion and end station trip is : " + str(frequent_combination.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_time_travel = df['Trip Duration'].sum()
    print("The time for total travel is :" + str(total_time_travel))

    # display mean travel time
    mean_time_travel = df['Trip Duration'].mean()
    print("The mean time for travil is:" + str(mean_time_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The count of user types: \n" + str(user_types))

    if city == 'chicago.csv' or city == 'new_york_city.csv':

    # Display counts of gender
        gender = df['Gender'].value_counts()
        print("The count of user gender is: \n" + str(gender))

    # Display earliest, most recent, and most common year of birth
        earlist_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()
        print('Earlist birth is: {}\n'.format(earlist_birth))
        print('The most recent birth is: {}\n'.format(most_recent_birth))
        print('The most common birth is: {}\n'.format(most_common_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def display_raw_data(df):

    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nDo you want to view next five row of raw data? Enter yes or no. \n')
        if view_raw_data.lower() != 'yes':
           return
        next = next + 5
        print(df.iloc[next:next+5])



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while  True:
            view_raw_data = input('\nDo you want to view first row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
