import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from weather_monitor import CITIES

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Function to load data from the database
def load_data_from_db(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, conn)

# Load data from both tables
weather_data = load_data_from_db('weather_data')
daily_summaries = load_data_from_db('daily_summaries')

# Convert timestamp to datetime for weather_data
weather_data['datetime'] = pd.to_datetime(weather_data['timestamp'], unit='s')
weather_data['date'] = weather_data['datetime'].dt.date

# Convert date to datetime for daily_summaries
daily_summaries['date'] = pd.to_datetime(daily_summaries['date'])

def main_menu():
    print("Welcome to the Weather Data Visualization Program!")
    print("Please select an option:")
    print("1. Plot Daily Temperature Trends")
    print("2. Plot Temperature Ranges by City")
    print("3. Plot Alert Frequency")
    print("4. Exit")

    choice = input("Enter your choice (1-5): ")
    return choice

def plot_daily_temperature_trends():
    print("Available data for the following cities: ")
    print(",".join(CITIES))
    city = input("Enter the city name: ")
    if city not in CITIES:
        print("Data for the requested city is not available.")
        return

    plot_daily_temperature_trends_helper(daily_summaries, city)

def plot_daily_temperature_trends_helper(df, city):
    city_data = df[df['city'] == city].sort_values('date')

    plt.figure(figsize=(12, 6))
    plt.plot(city_data['date'], city_data['avg_temp'], label='Average')
    plt.plot(city_data['date'], city_data['max_temp'], label='Max')
    plt.plot(city_data['date'], city_data['min_temp'], label='Min')

    plt.title(f'Daily Temperature Trends for {city}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_alert_frequency_helper(df, threshold):

    # Create figure with larger size for better label visibility
    plt.figure(figsize=(14, 7))
    
    # Group data by date and city, finding max temps for each
    daily_city_temps = df.groupby(['date', 'city'])['max_temp'].max().reset_index()
    
    # Create alert mask and get cities exceeding threshold
    daily_city_temps['alert'] = daily_city_temps['max_temp'] > threshold
    
    # Group by date to get alert counts
    alert_data = daily_city_temps.groupby('date')['alert'].sum().reset_index()
    
    # Create the bar plot
    bars = plt.bar(alert_data['date'], alert_data['alert'], color='coral', alpha=0.7)
    
    # For each date, find cities that exceeded threshold
    for date in alert_data['date'].unique():
        cities_exceeding = daily_city_temps[
            (daily_city_temps['date'] == date) & 
            (daily_city_temps['max_temp'] > threshold)
        ]
        
        if not cities_exceeding.empty:
            # Get the corresponding bar height
            bar_height = alert_data[alert_data['date'] == date]['alert'].iloc[0]
            
            # Format date string
            date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
            
            # Create formatted text with date and cities
            text_lines = [f"Date: {date_str}"]
            text_lines.extend([
                f"{row['city']}: {row['max_temp']:.1f}°C"
                for _, row in cities_exceeding.iterrows()
            ])
            label_text = '\n'.join(text_lines)
            
            # Add text above bar
            plt.text(
                date,                          # x position
                bar_height,                    # y position
                label_text,                    # text
                ha='center',                   # horizontal alignment
                va='bottom',                   # vertical alignment
                fontsize=8,                    # smaller font size for better fit
                rotation=0,                    # no rotation
                bbox=dict(                     # add a background box
                    facecolor='white',
                    alpha=0.9,                 # increased opacity for better readability
                    edgecolor='lightgray',     # light border
                    pad=1.5,                   # increased padding
                    boxstyle='round,pad=0.5'   # rounded corners
                )
            )
    
    # Customize the plot
    plt.title(f'Alert Frequency Over Time (Temperature > {threshold}°C)', pad=40)
    plt.xlabel('Date')
    plt.ylabel('Number of Cities Exceeding Threshold')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Adjust layout to prevent label clipping
    plt.tight_layout()
    
    # Add extra padding at the top for labels
    plt.margins(y=0.2)
    
    return plt.gcf()

def plot_alert_frequency():
    threshold = float(input("Enter the temperature threshold (°C): "))
    
    try:
        # Load data from database
        conn = sqlite3.connect('weather_data.db')
        daily_summaries = pd.read_sql_query(
            "SELECT date, city, max_temp FROM daily_summaries",
            conn
        )
        
        # Convert date strings to datetime objects
        daily_summaries['date'] = pd.to_datetime(daily_summaries['date'])
        
        # Create and show the plot
        fig = plot_alert_frequency_helper(daily_summaries, threshold)
        plt.show()
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


def plot_temperature_ranges_by_city():
    plt.figure(figsize=(12, 6))

    cities = daily_summaries['city'].unique()
    x = range(len(cities))
    min_temps = []
    max_temps = []

    for city in cities:
        city_data = daily_summaries[daily_summaries['city'] == city]
        min_temps.append(city_data['min_temp'].mean())
        max_temps.append(city_data['max_temp'].mean())

    width = 0.2
    plt.bar(x, min_temps, width=width, label='Minimum Temperature',color="green")
    plt.bar([i + width for i in x], max_temps, width=width, label='Maximum Temperature',color="red")

    plt.title('Temperature Ranges by City')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks([i + width/2 for i in x], cities, rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    while True:
        choice = main_menu()

        if choice == "1":
            plot_daily_temperature_trends()
        elif choice == "2":
            plot_temperature_ranges_by_city()
        elif choice == "3":
            plot_alert_frequency()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()