import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set API key
API_key = '8f0d8e18eace091d3523bd922a52b137'

# Cities to find  data for
cities = ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Pune']

# Find and store weather data
weather_data = []
for city in cities:
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data.append({
            'City': data['name'],
            'Temperature in celcius': data['main']['temp'],
            'Feels Like (°C)': data['main']['feels_like'],
            'Humidity (%)': data['main']['humidity'],
            'Pressure (hPa)': data['main']['pressure'],
            'Wind Speed (m/s)': data['wind']['speed'],
            'Condition': data['weather'][0]['description']
        })
    else:
        print(f"Failed to fetch weather data for {city}")

# Convert to DataFrame
df = pd.DataFrame(weather_data)

# Prepare data for pie chart
condition_to_cities = df.groupby('Condition')['City'].apply(lambda x: ', '.join(x)).to_dict()
condition_counts = df['Condition'].value_counts()
labels = [f"{condition} ({condition_to_cities[condition]})" for condition in condition_counts.index]

# 2x2 grid for subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Weather Dashboard for Major IT Hubs in India', fontsize=18)

# 1. Bar chart – Temperature
sns.barplot(ax=axs[0, 0], x='City', y='Temperature in celcius', data=df)
axs[0, 0].set_title('Temperature (°C)')
axs[0, 0].set_ylim(20, 50)

# 2. Line plot – Actual vs Feels Like
sns.lineplot(ax=axs[0, 1], x='City', y='Temperature in celcius', label='Actual', data=df, marker='o')
sns.lineplot(ax=axs[0, 1], x='City', y='Feels Like (°C)', label='Feels Like', data=df, marker='o')
axs[0, 1].set_title('Actual vs Feels Like Temp')
axs[0, 1].set_ylim(20, 50)
axs[0, 1].grid(True)
axs[0, 1].legend()

# 3. Bar chart – Humidity
sns.barplot(ax=axs[1, 0], x='City', y='Humidity (%)', data=df)
axs[1, 0].set_title('Humidity (%)')
axs[1, 0].set_ylim(0, 100)
axs[1, 0].grid(axis='y')

# 4. Pie chart – Weather Conditions
axs[1, 1].pie(condition_counts, labels=labels, autopct='%1.1f%%', startangle=140)
axs[1, 1].set_title('Weather Conditions')

# Adjust layout
plt.tight_layout(rect=(0, 0, 1, 0.95))
plt.show()
