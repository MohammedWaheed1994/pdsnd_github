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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    is_input_data_valid : bool = False
    city: str = ""
    month: str = ""
    day: str = ""
    cities: list = ["chicago", "new york city", "washington"]
    while not is_input_data_valid:
        city = input("Please enter city name, kindly choose from (chicago, new york city, washington): ")
        city = city.lower()
        if city.lower() not in cities :
            print("Invlaid city name, please try again. ")
            is_input_data_valid = False
        else:
            is_input_data_valid = True
    
     # TO DO: get user input for month (all, january, february, ... , june)
    is_input_data_valid = False
    months = ["all", "january", "february", "march", "april", "may", "june"]
    
    while not is_input_data_valid:
        month = input("Please enter required month from (all, january, february, ... , june): ")
        month = month.lower()
        if month not in months and month.lower() != "all":
            print("Invlaid month, please try again. ")
            is_input_data_valid = False
        else:
            is_input_data_valid = True

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    is_input_data_valid = False
    week_days = ["Monday", "Tuesday", "Wednesday", "Thrusday", "Friday", "Saturday", "Sunday"]
    
    while not is_input_data_valid:
        day = input("Please enter week day or all for no specific day: ")
        day = day.lower()
        if day.title() not in week_days and day.lower() != "all":
            print("Invlaid day, please try again. ")
            is_input_data_valid = False
        else:
            is_input_data_valid = True
    
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
    
    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['staring hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month ]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df =  df[df['day_of_week'] == day.title() ]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month of using bycles is " ,df['month'].mode()[0])

    # TO DO: display the most common day of week
    print("The most common day of using bycles is " , df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    print("The most common starting hour of using bycles is " , df['staring hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common used start station: ",df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most common used end station: ",df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    
    start_end_series = df['Start Station'].combine(df['End Station'], lambda x,y : (x,y))
    print("The most frequent combination of start station and end station trip: ",start_end_series.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The longest trip duration is :" , df['Trip Duration'].max() , " seconds.")

    # TO DO: display mean travel time
    print("The average trip duration is :" , df['Trip Duration'].mean(), " seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of different user types: \n", df['User Type'].value_counts(), "\n")

    # TO DO: Display counts of gender
    #check if city is new york or chicago
    if 'Gender' in df.columns:
        print("Counts of different genders: \n", df['Gender'].value_counts(), "\n")


    # TO DO: Display earliest, most recent, and most common year of birth
    df["year"] = df['Start Time'].dt.year
    print("The earliest year is ", df['year'].min())
    print("The lastest year is ", df['year'].max())
    
    #check if city is new york or chicago
    if 'Gender' in df.columns:
        print("The common year of birth is ", df['Birth Year'].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """
    Display rows of Data based on user request
    """
    def _increment_index(index):
        """ Increment the index with 5 , and checks if it reaches the end"""
        if index < df.shape[0]-5:
            return index, index+5
        else:
            return index, df.shape[0]
            
    user_choice = input("Would you like to show the first 5 rows of Data, yes or no: ")
    if user_choice.lower() == "yes":
        print(df[:5])
        print('-'*40)
        
    show_next_flag = True
    start_index = 5
    end_index = 10
    while show_next_flag:
        user_choice = input("Would you like to show the next 5 rows of Data, yes or no: ")
        if user_choice.lower() == "yes":
            # check that we have showed all the rows
            if end_index == df.shape[0]:
                print("All raws are showed")
                break
            print(df[start_index: end_index])
            print('-'*40)
            start_index, end_index = _increment_index(end_index)
        else:
            break

def show_concrete_stats(df):
    """
    Display some generic stats like mean, count, 50%, ... etc
    """
    print(df.describe())
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_concrete_stats(df)
        show_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
    print("Terminating...")
    print('-'*40)

if __name__ == "__main__":
	main()
