from multiprocessing.connection import answer_challenge
import time
import pandas as pd
import numpy as np
​
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
​
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
​
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter City you want to explore from chicago,new york city,washington: ').lower()
        if city not in CITY_DATA:
            print('\n Invalid Input,Please Enter Again')
                
        else: 
            break
    filter_type_list = {'month', 'day', 'both', 'none'}
    type = input_mod('\nWould you like to filter the data by month, day, both, or None? Type "None" for no time filter.\n',
                     '\nPlease input the right format like month, day, both, or None? Type "None" for no time filter.\n',
                     filter_type_list,
                     lambda x:str.lower(x))
​
    # get user input for month (all, january, february, ... , june)
    month = ''
    if (type == 'both' or type == 'month'):
        month_type_list = {'January', 'February', 'March', 'April', 'May', 'June', 'All'}
        month = input_mod('\nWhich month? January, February, March, April, May, or June? (Type All for every month)\n',
                          '\nPlease input the right format like January, February, March, April, May, or June? (Type All for every month)\n',
                          month_type_list,
                          lambda x: str.title(x))
​
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = -1
    if(type == 'both' or type == 'day'):
        day_type_list = {'1', '2', '3', '4', '5', '6', '7', '0'}
        day = input_mod('\nWhich day? Input an Interger like 1 (1 is Sunday, 0 is all) \n',
                        '\nPlease input the right format. Input an Interger like 1 (1 is Sunday, 0 is all) \n',
                        day_type_list,
                        lambda x:x)
​
    print('-' * 40)
    return city, month, day
​
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
​
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    day = int(day)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    # filter by month if applicable
    if month == '' and day == -1:
        return df
    # use the index of the months list to get the corresponding int
    if month != '' and month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != -1 and day != 0:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] + 1 == day]
    # print(df.head)
    return df
​
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
​
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
​
    # display the most common month
    print('The most common month is :')
    print(num_to_month(df['month'].value_counts().idxmax()))
    #print(num_to_month(df['month'].mode()[0]))
​
    # display the most common day of week
    print('\nThe most common day of week is :')
    print(num_to_weekday(df['day_of_week'].value_counts().idxmax() + 1))
    #print(num_to_weekday(df['day_of_week'].mode()[0] + 1))
​
    # display the most common start hour
    print('\nThe most common start hour is :')
    print(df['Start Time'].dt.hour.value_counts().idxmax())
    #print(df['Start Time'].dt.hour.mode()[0])
​
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
​
​
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
​
    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()
    print(df.columns)
    # display most commonly used start station
    print('\nThe most commonly used start station is :')
    print(df['Start Station'].value_counts().idxmax())
    #print(df['Start Station'].mode()[0])
​
    # display most commonly used end station
    print('\nThe most commonly used end station is :')
    print(df['End Station'].value_counts().idxmax())
    #print(df['End Station'].mode()[0])
​
    # display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of start station and end station trip is :')
    most_frequent_combination = df['Start Station'] + ' -  ' + df['End Station']
    print(most_frequent_combination.value_counts().idxmax())
    print('The time is :')
    print(most_frequent_combination.value_counts().max())
​
    #top = df.groupby(['Start Station', 'End Station']).size().idxmax()
    #print("The most frequent combination of start station and end station trip is {} to {}".format(top[0], top[1]))
​
    print("\nThis took %s seconChicagodds." % (time.time() - start_time))
    print('-'*40)
​
​
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
​
    print('\nCalculating Trip Duration...')
    start_time = time.time()
​
    # display total travel time
    print('\nThe total travel time is : ')
    total_time = df['Trip Duration'].sum()
    print(total_time, ' seconds, or ', total_time/3600, ' hours')
    
​
    # display mean travel time
    print('\nThe mean travel time is : ')
    avg_time = df['Trip Duration'].mean()
    print(avg_time, 'seconds, or', avg_time/3600, ' hours')
​
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
​
​
def user_stats(df):
    """Displays statistics on bikeshare users."""
​
    print('\nCalculating User Stats...\n')
    start_time = time.time()
​
    try:
        # Display counts of user types
        print('The counts of user types is : ')
        print(df['User Type'].value_counts())
​
        # Display counts of gender
        # Washington data set has no 'Gender' column. The if statements avoids errors during runtime.
        if 'Gender' in df:
            print('\nThe counts of gender is : ')
            print(df['Gender'].value_counts())
​
        # Display earliest, most recent, and most common year of birth
        # Washington data set has no 'Birth Year' column. The if statements avoids errors during runtime.
        if 'Birth Year' in df:
            print('The earliest year of birth is : ')
            print(df['Birth Year'].min())
            print('\nThe most recent year of birth is : ')
            print(df['Birth Year'].max())
            print('\nThe most common year of birth is : ')
            print(df['Birth Year'].value_counts().idxmax())
​
    except:
        print('error')
​
​
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
​
​
        
#User defined Function:
def input_mod(input_print, error_print, enterable_list, get_value):
    ret = get_value(input(input_print))
    while ret not in enterable_list:
        ret = get_value(input(error_print))
    return ret
​
def num_to_month(month):
    mon = ['January', 'February', 'March', 'April', 'May', 'June']
    return mon[month - 1]
​
def num_to_weekday(day):
    weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return weekday[day - 1]
​
​
#Function to display the data frame itself as per user request
​
def raw_data (df):
    """Displays the data due filteration.
    5 rows will added in each press"""
    
    #the next code to avoid infinite loop when the user still need more rows and we display all row 
    print('the shape of the selected data is : ',df.shape)
    last_row_index_number = df.iloc[-1].name      #to know the last index of selected data frame
    
    print('press anything except no to display the first 5 row data or press no to skip')
    x = 0
    while (input()!= 'no'):
        x = x+5    # here if u want to check the loop break if the user display all rows >> replace +5 by +500 to iterate faster 
        print(df.iloc[0 : x])
        if df.iloc[0 : x].iloc[-1].name >= last_row_index_number : # check if user display all rows 
            break
        else :
            print('press anything except no to display more 5 row data or  press no to skip')
    print('you display all row data')
​
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
​
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
​
        restart = input('\nWould you like to restart? Enter yes to restart or press anything to skip.\n')
        if restart.lower() != 'yes':
            break
​
if __name__ == "__main__":
    main()