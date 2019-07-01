import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city=''
    month=''
    day=''
    while city not in ['chicago','new york city','washington']:
        city= input('\ncan you please in write the name of the city that you want to see the data for (please choose either chicago, new york city or washington)\n').lower()

    # get user input for month (all, january, february, ... , june)
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month= input('\ncan you please select which month you want to see the data for (choose from (all, january, february, ... , june) )\n').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ['all','saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday','friday']:
        day= input('\ncan you please select which day of the week you want to see the data for (choose from (all, monday, tuesday, ... sunday) )\n').lower()


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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    beginning_time = time.time()
    df['Start Time'] =pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month =  df['month'].mode()[0]
    print('Most Frequent month:', popular_month)



    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week =  df['day_of_week'].mode()[0]
    print('\nMost Frequent day of the week:', popular_day_of_week)



    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour =  df['hour'].mode()[0]
    print('\nMost Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - beginning_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    beginning_time = time.time()

    # display most commonly used start station
    print('\nmost commonly used start station',df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nmost commonly used end station',df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['comp']= df['End Station']+df['Start Station']
    print('\nmost frequent combination of start station and end station trip',df['comp'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - beginning_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    beginning_time = time.time()

    # display total travel time
    df['End Time']=pd.to_datetime(df['End Time'])
    df['travel time']=df['End Time']-df['Start Time']
    total_travel_time=df['travel time'].sum()
    print('\ntotal travel time is equal to ',total_travel_time)

    # display mean travel time
    mean_travel_time=df['travel time'].mean()
    print('\nMean travel time is equal to ',mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - beginning_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    beginning_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\ncounts per user type\n',user_types,'\n')
    # Display counts of gender


    if city != 'washington':
        gender = df['Gender'].value_counts()
        print('\ncounts per gender\n',gender,'\n')
        # Display earliest, most recent, and most common year of birth
        earliest_DOB=int(min(df['Birth Year']))#.dropna().min()[0]
        print('\noldest user was born on ', earliest_DOB)
        most_recent_DOB=int(max(df['Birth Year']))
        print('\nthe youngest user was born on ', most_recent_DOB)
        common_DOB=df['Birth Year'].mode()[0]
        print('\nthe most common Year of birth is ', most_recent_DOB)

    raw_data=input('\nDo you want to see raw data?\n').lower()
    data_start=0
    data_end=5
    if raw_data == 'yes':
        while raw_data =='yes':
            print(df.iloc[data_start:data_end])
            data_start+=5
            data_end+=5
            raw_data=input('\nDo you want to see more 5 lines of raw data?\n')
            if raw_data == 'no':
                break

    print("\nThis took %s seconds." % (time.time() - beginning_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
