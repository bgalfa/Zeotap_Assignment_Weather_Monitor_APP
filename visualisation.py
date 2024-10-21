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

def plot_alert_frequency():
    threshold = float(input("Enter the temperature threshold (°C): "))
    plot_alert_frequency_helper(daily_summaries, threshold)

def plot_alert_frequency_helper(df, threshold):
    df['alert'] = df['max_temp'] > threshold
    alert_data = df.groupby('date')['alert'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    plt.bar(alert_data['date'], alert_data['alert'])

    plt.title(f'Alert Frequency Over Time (Temperature > {threshold}°C)')
    plt.xlabel('Date')
    plt.ylabel('Number of Alerts')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

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