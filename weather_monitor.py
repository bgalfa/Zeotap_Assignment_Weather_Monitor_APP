import requests
import time
from datetime import datetime
import sqlite3


# Configuration
API_KEY = "8413fc0773dd3acf5e9c6648ec38f0da"
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
UPDATE_INTERVAL = 300  # 5 minutes in seconds

# Database setup
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        main TEXT,
        temp REAL,
        feels_like REAL,
        timestamp INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        avg_temp REAL,
        max_temp REAL,
        min_temp REAL,
        dominant_condition TEXT
    )
''')

conn.commit()

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': city,
            'main': data['weather'][0]['main'],
            'temp': kelvin_to_celsius(data['main']['temp']),
            'feels_like': kelvin_to_celsius(data['main']['feels_like']),
            'timestamp': data['dt']
        }
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None


def store_weather_data(data, cursor, conn):
    cursor.execute('''
        INSERT INTO weather_data (city, main, temp, feels_like, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['city'], data['main'], data['temp'], data['feels_like'], data['timestamp']))
    conn.commit()
    

def generate_daily_summary(cursor,conn):
    cursor.execute('''
        SELECT city, date(timestamp, 'unixepoch') as date,
               AVG(temp) as avg_temp,
               MAX(temp) as max_temp,
               MIN(temp) as min_temp,
               GROUP_CONCAT(main) as conditions
        FROM weather_data
        GROUP BY city, date
        ORDER BY date DESC
        LIMIT 6
    ''')
    summaries = cursor.fetchall()
    
    for summary in summaries:
        city, date, avg_temp, max_temp, min_temp, conditions = summary
        conditions_list = conditions.split(',')
        dominant_condition = max(set(conditions_list), key=conditions_list.count)
        cursor.execute('''
            INSERT OR REPLACE INTO daily_summaries
            (city, date, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (city, date, avg_temp, max_temp, min_temp, dominant_condition))
    
    conn.commit()

def check_alerts(data, threshold=35):
    if data['temp'] > threshold:
        print(f"ALERT: Temperature in {data['city']} is {data['temp']:.1f}°C, exceeding the threshold of {threshold}°C")


def weather_monitor(threshold=35):
    while True:
        for city in CITIES:
            data = fetch_weather_data(city)
            if data:
                store_weather_data(data,cursor,conn)
                check_alerts(data,threshold=threshold)
        
        generate_daily_summary(cursor,conn)
        print(f"Data updated at {datetime.now()}")
        time.sleep(UPDATE_INTERVAL)


def print_weather_data(cursor, conn):
    query = "SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50"
    print_data(cursor, conn, query)

def print_daily_summaries(cursor, conn):
    query = "SELECT * FROM daily_summaries ORDER BY date DESC LIMIT 50"
    print_data(cursor, conn, query)

def print_data(cursor, conn, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    
    if not rows:
        print("No data found in the table.")
        return

    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    # Print header
    print(" | ".join(column_names))
    print("-" * (len(" | ".join(column_names))))
    
    # Print rows
    for row in rows:
        formatted_row = []
        for item in row:
            if isinstance(item, float):
                formatted_row.append(f"{item:.2f}")
            else:
                formatted_row.append(str(item))
        print(f" | ".join(formatted_row))
    
    print(f"\nTotal rows: {len(rows)}")




def main():
    
    while True:
        print("\nMenu:")
        print("1. Start weather monitoring")
        print("2. Print weather data")
        print("3. Print daily summaries")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            threshold = int(input("Enter temperature threshold value to generate alerts: "))
            weather_monitor(threshold=threshold)
        elif choice == '2':
            print_weather_data(cursor, conn)
        elif choice == '3':
            print_daily_summaries(cursor, conn)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()