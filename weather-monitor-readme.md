# Weather Monitoring System

A Python-based weather monitoring system that collects real-time weather data for major Indian cities, stores it in a SQLite database, and provides data visualization capabilities.

## Features
- Real-time weather data collection for 6 major Indian cities (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad)
- Temperature monitoring and alert system
- Data storage in SQLite database
- Daily weather summaries
- Interactive data visualization including:
  - Daily temperature trends
  - Temperature ranges by city
  - Alert frequency visualization

## Prerequisites
- Python 3.8 or more
- Pip package manager
- OpenWeatherMap API key
- Active network connection
  
## Required Libraries
```bash
pip install -r requirements.txt
```

### Dependencies
- **requests**: For making API calls to OpenWeatherMap
- **pandas**: For data manipulation and analysis
- **matplotlib**: For creating visualizations
- **seaborn**: For enhanced visualizations
- **sqlite3**: For database operations (included in Python standard library)
- **time**: For handling intervals (included in Python standard library)
- **datetime**: For time-based operations (included in Python standard library)

## Project Structure
```
weather-monitoring-system/
├── weather_monitor.py    # Main monitoring script
├── visualization.py      # Data visualization script
├── weather_data.db      # SQLite database
└── README.md
```

## Database Structure

### Weather Data Table
```sql
> TABLE weather_data 
   >> id INTEGER PRIMARY KEY AUTOINCREMENT,
   >> city TEXT,
   >> main TEXT,
   >> temp REAL,
   >> feels_like REAL,
   >> timestamp INTEGER
```

### Daily Summaries Table
```sql
> TABLE daily_summaries 
   >> id INTEGER PRIMARY KEY AUTOINCREMENT,
   >> city TEXT,
   >> date TEXT,
   >> avg_temp REAL,
   >> max_temp REAL,
   >> min_temp REAL,
   >> dominant_condition TEXT
```

## Configuration
- API_KEY: OpenWeatherMap API key
- CITIES: List of monitored cities
- UPDATE_INTERVAL: Data collection interval (default: 300 seconds/5 minutes)
- Temperature threshold for alerts can be set during runtime

## Usage

### Weather Monitoring (weather_monitor.py)
Run the main monitoring script:
```bash
python weather_monitor.py
```

Menu options:
1. Start weather monitoring
2. Print weather data
3. Print daily summaries
4. Exit

### Data Visualization (visualization.py)
Run the visualization script:
```bash
python visualization.py
```

Menu options:
1. Plot Daily Temperature Trends
2. Plot Temperature Ranges by City
3. Plot Alert Frequency
4. Exit

## Features Details

### Weather Monitoring
- Collects real-time weather data from OpenWeatherMap API
- Stores data in SQLite database
- Generates daily summaries
- Alert system for high temperatures
- Converts temperature from Kelvin to Celsius

### Visualization
- Interactive plots using matplotlib
- Temperature trend analysis
- City-wise temperature comparison
- Alert frequency visualization with detailed annotations

## Error Handling
- API request error handling
- Database connection management
- Input validation for city selection
- Exception handling for visualization errors

## Setup Instructions

1. Clone the repository
2. Install required packages:
```bash
pip install requests pandas matplotlib seaborn
```

3. Set up your OpenWeatherMap API key in weather_monitor.py:
```python
API_KEY = "your_api_key_here"
```

4. Run the monitoring system:
```bash
python weather_monitor.py
```

5. For visualization, run:
```bash
python visualization.py
```

## Notes
- The system automatically creates the SQLite database if it doesn't exist
- Data is collected every 5 minutes by default
- Temperature alerts can be customized with user-defined thresholds
- Visualization options provide different perspectives on the collected data
