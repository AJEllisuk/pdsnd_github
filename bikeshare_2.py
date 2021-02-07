# Import the libraries to provide the needed functionality:
# time
import time
# pandas - provides functions for data analysys
import pandas as pd
# numpy - a library for working with arrays
import numpy as np
from statistics import mode, StatisticsError

# This array contains information about the cities for which data is available
# and the filenames for the data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Create a list containg the 12 months. An extra entry 'all' is included to allow the user
# to work with data for all months in a data file for a given city. Each entry is in lower case 
# to simplify the process of checking the users entries to ensure they are valid.
month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
# Create a list containg the days of the week. An extra entry 'all' is included to allow the user
# to work with data for every day of the week in a data file for a given city. Each entry is in lower case 
# to simplify the process of checking the users entries to ensure they are valid.
day_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    The data entered by the user is converted to lower case with .lower()
    to simplify the process of checking the entry to ensure that it is valid.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    input_valid = 0

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please choose on of the following cities:\n')
    print('\nChicago, New York City, Washington\n')
    while True: # Loop until a break is issued
        city = input()
        # Check the city the user has entered. Convert the user entry to lower case
        # to make it easier to check the user's entry
        if city.lower() == 'chicago' or city.lower() == 'new york city' or city.lower() == 'washington':
            break
        else:
            print('Invalid entry. Please choose on of the following cities\n')
            print('\nchicago, new york city, washington\n')

    # get user input for month (all, january, february, ... , june)
    print('Please enter a month, or \'all\' for every month')
    while True:
        month = input()
        for i in range (13): # Loop through the month list, 13 is there becasue there is
                            # 'all' option to choose every month
            if month.lower() == month_list[i]: # check if the users entry matches the current entry in the list
                input_valid = 1 # if a match is found, set input valid to 1
                break # and break the loop

        if input_valid == 1: # if a valid input was entered...
            break #.. break out of the while loop

        else: # if the entry wasn't valid inform the user, and remind them of valid entries
            print('Invalid entry. Please enter a month, or \'all\' for every month')
            

    # get user input for day of week (all, monday, tuesday, ... sunday)
    input_valid = 0
    print('Please enter a day, or \'all\' for every day')
    while True: #Loop until a break is issued
        day = input() #Read the user input
        for i in range (8):
            if day.lower() == day_list[i]:
                input_valid = 1
                break

        if input_valid == 1: # if a valid input was entered...
            break #.. break out of the while loop

        else: # if the entry wasn't valid inform the user, and remind them of valid entries
            print('Invalid entry. Please enter a day, or \'all\' for every day')

    print('-'*40)
    return city, month, day

# Based on code in practice solution 3
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
    # load the city data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        param1 (df): The data frame for the previously selected CSV file
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # use the mode function to find the most common month
    # if the is no mode, a StatisticsError exception is thrown
    try:
        most_popular_month = df['month'].mode()[0]   
        print(f"The most popular month is: {month_list[most_popular_month]}")
    
    except StatisticsError:
        print('Bike usage is the same each month')
          
        

    # display the most common day of week
    # if the is no mode, a StatisticsError exception is thrown
    try:
        most_popular_day = df['day_of_week'].mode()[0]   
        print(f"The most popular day is: {most_popular_day}")
    
    except StatisticsError:
        print('Bike usage is the same each day')
        most_popular_day = df['day_of_week'].mode()[0]   

    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    # if the is no mode, a StatisticsError exception is thrown
    try:
        popular_hour = df['hour'].mode()[0]
        print(f"The most popular hour is: {popular_hour}")
    
    except StatisticsError:
        print('Bike usage is the same each hour')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        param1 (df): The data frame for the previously selected CSV file
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station    
    # if the is no mode, a StatisticsError exception is thrown
    try:
        most_common_start_station = df['Start Station'].mode()[0]
        print(f"The most frequently used start station: {most_common_start_station}")
    
    except StatisticsError:
        print('All stations have equal starting usage')

    # display most commonly used end station
    # if the is no mode, a StatisticsError exception is thrown
    try:
        most_common_end_station = df['End Station'].mode()[0]
        print(f"The most frequently used end station: {most_common_end_station}")

    
    except StatisticsError:
        print('All stations have equal finishing usage')
    
    # display most frequent combination of start station and end station trip
    # join the start station string with the end station string to find the most common
    # combination of start and stop stations
    # str.cat is used to combine the strings
    # if the is no mode, a StatisticsError exception is thrown
    try:
        df['Start to End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
        most_common_combo = df['Start to End'].mode()[0]
        print(f"The most frequently combination of start & end stations: {most_common_combo}")
    except StatisticsError:
        print('All stations have equal finishing usage')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        param1 (df): The data frame for the previously selected CSV file
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration = df['Trip Duration'].sum()
    minutes, seconds = divmod(trip_duration, 60)
    hours, minutes = divmod(minutes, 60)
    #if minutes is greater than 60
    if minutes > 60:
        # convert the trip to hours, mins, secs
        hours, minutes = divmod(minutes, 60)
        print(f"\nThe trip duration is {hours} hours, {minutes} minutes and {seconds} seconds.")
    else:
        print(f"\nThe trip duration is {minutes} minutes and {seconds} seconds.")

    
    # display mean travel time
    average_trip_duration = round(df['Trip Duration'].mean())
    #Finds the average duration in minutes and seconds format
    minutes, seconds = divmod(average_trip_duration, 60)

    #if minutes is greater than 60
    if minutes > 60:
        # convert the average trip to hours, mins, secs
        hours, minutes = divmod(minutes, 60)
        print(f"\nThe average trip duration is {hours} hours, {minutes} minutes and {seconds} seconds.")
    else:
        print(f"\nThe average trip duration is {minutes} minutes and {seconds} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        param1 (df): The data frame for the previously selected CSV file
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display the number user types
    user_type = df['User Type'].value_counts()
    print(f"\nThe number of each user type:\n{user_type}")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(f"The number of each gender for all user types is:\n{gender}")
    else:
        print("There is no gender information in this file")

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        earliest_year_of_birth = int(df['Birth Year'].min())
        recent_year_of_birth = int(df['Birth Year'].max())
        common_year_of_birth = int(df['Birth Year'].mode()[0])
        print(f"The earliest year of birth: {earliest_year_of_birth}")
        print(f"The most recent year of birth: {recent_year_of_birth}")
        print(f"The most common year of birth: {common_year_of_birth}")
    else:
        print('There is no year of birth in this file')    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays statistics on bikeshare users.
    Args:
        param1 (df): The data frame for the previously selected CSV file
    Returns:
        None.
    """
    
    start_time = time.time()

    # This variable is used to keep track of the current count in
    # the CSV file
    line_count = 0

    # This variable is used to store and check the user response
    # It is cleared here to ensure the is no spurious data in it
    response = ''

    while 1:
        print("Would you like to view the raw data from the CSV file?")
        print("\n(Yes or No)")
        response = input().lower()
        if response == "yes":
            # Read the first 5 lines from the CSV file
            # Note: df.head() defaults to reading the first 5 lines
            print(df.head())
            break; # move on to the next stage
        elif response == "no":
            break;
        
        else:
            print("\nInvalid entry\n")
            print("Please enter \'Yes\' or \'No\'\n")

        
    while 1:
        print ("Would you like to view more data?")
        print ("\n(Yes or No)\n")
        response = input().lower()
        if response == "yes":
            # increment the line count by 5 lines
            line_count += 5
            # display 5 lines
            # line_count gives the starting point in the CSV file,
            # the value to the right of the colon ':' gives the finish point
            # ie read and display from line_count up to line_count + 5
            print(df[line_count:line_count+5])
        elif response == "no":
            break;
        
        else:
            print("\nInvalid entry\n")
            print("Please enter \'Yes\' or \'No\'\n")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
