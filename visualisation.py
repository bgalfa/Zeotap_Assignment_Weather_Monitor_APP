import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

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

# 1. Time Series Graph: Daily temperature trends
def plot_daily_temperature_trends(df, city):
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

# 2. Bar Chart: Daily temperature ranges
def plot_temperature_ranges(df, date):
    date_data = df[df['date'] == date]
    
    plt.figure(figsize=(12, 6))
    
    x = range(len(date_data['city']))
    plt.bar(x, date_data['max_temp'] - date_data['min_temp'], bottom=date_data['min_temp'], label='Range')
    plt.plot(x, date_data['avg_temp'], 'ro', label='Average')
    
    plt.title(f'Temperature Ranges by City on {date}')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(x, date_data['city'], rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 3. Heat Map: Temperature variations across cities and time
def plot_temperature_heatmap(df):
    pivot_df = df.pivot(index='date', columns='city', values='avg_temp')
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df, cmap='YlOrRd', annot=True, fmt='.1f', cbar_kws={'label': 'Temperature (°C)'})
    
    plt.title('Temperature Variations Across Cities and Time')
    plt.xlabel('City')
    plt.ylabel('Date')
    plt.tight_layout()
    plt.show()

# 12. Alert Frequency Graph (using temperature threshold as a proxy for alerts)
def plot_alert_frequency(df, threshold=35):
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

# Example usage:
plot_daily_temperature_trends(daily_summaries, 'Delhi')
#plot_temperature_ranges(daily_summaries, daily_summaries['date'].min())
plot_alert_frequency(daily_summaries, threshold=35)

# Close the database connection
conn.close()