# We need to import several libraries to handle data loading, cleaning, analysis, and visualization
# Import necessary modules/libraries
import csv  # loads CSV data
import pandas as pd  # Creates and manipulates DataFrames (DF)
import numpy as np  # numerical operations
import matplotlib.pyplot as plt  # plotting library

# Simple script to load our data using pandas
# Load the data from CSV
data_file = 'data.csv'  # path to the data file
df = pd.read_csv(data_file)  # read the CSV into a DF

# Display the DataFrame to explore its structure
# we can print information to our console!
print("Loaded data shape:", df.shape)
# this is good for debugging and knowing what line our code is on
print("\nFirst 5 rows:")
print(df.head())  # print the rows of the DF

# Print column names to inspect the data structure
print("\nColumn names:")
print(df.columns.tolist())

# This particualar dataset uses -99.9 and -99.99 to indicate missing values
# We need to clean these values before analysis
# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()
# Replace sentinel missing values with NaN
df = df.replace([-99.9, -99.99], np.nan)
# Drop rows with NaN in temperature columns
df_clean = df.dropna(subset=['MAX TEMP', 'MIN TEMP'])

# \n is just newline here
print(f"\nCleaned data shape (after removing missing temps): {df_clean.shape}")

# Compute and print temperature statistics
# max() finds the maximum value in a column
highest_max_temp = df_clean['MAX TEMP'].max()
# min() finds the minimum value in a column
lowest_max_temp = df_clean['MAX TEMP'].min()
highest_min_temp = df_clean['MIN TEMP'].max()
lowest_min_temp = df_clean['MIN TEMP'].min()

print(f"\nTemperature Statistics:")
# f-strings are great for formatting output
print(f"Highest Max Temp: {highest_max_temp}°F")
print(f"Lowest Max Temp: {lowest_max_temp}°F")
print(f"Highest Min Temp: {highest_min_temp}°F")
print(f"Lowest Min Temp: {lowest_min_temp}°F")

# We sometimes need to format our datetime data for time-series analysis
# (it's not always intuitive)
# Create a 'DATE' column from YEAR, MONTH, DAY with error handling
df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']], errors='coerce')
df_clean = df.dropna(subset=['DATE'])  # Drop rows with invalid dates (NaT)

# Set 'DATE' as the index
# inplace=True modifies the DF directly
df_clean.set_index('DATE', inplace=True)

# We need to further clean our data let's drop NaN in key columns (temperatures and precipitation)
df_clean = df_clean.dropna(subset=['MAX TEMP', 'MIN TEMP', 'PRECIPITATION'])

# Print the shape of the cleaned data (rows, columns)
print(f"\nFinal cleaned data shape: {df_clean.shape}")

# Let's verifiy our data!
# Verify the cleaned data by printing the head
print("\nFirst 5 rows of final cleaned data:")
print(df_clean.head())

# Now we can visualize our data using Matplotlib
# Set a style for the plots
# PLOT 1: Max and Min Temperatures Over Time using Matplotlib
plt.figure(figsize=(12, 8))  # set figure size
plt.plot(df_clean.index, df_clean['MAX TEMP'], label='Max Temperature',
         color='#FF6B6B', linewidth=1.5)  # red line for max temp
plt.plot(df_clean.index, df_clean['MIN TEMP'], label='Min Temperature',
         color='#4D96FF', linewidth=1.5)  # blue line for min temp
plt.fill_between(df_clean.index, df_clean['MIN TEMP'], df_clean['MAX TEMP'],
                 alpha=0.3, color='lightblue')  # shaded area between temps

plt.title('Max and Min Temperatures Over Time',
          fontsize=16, fontweight='bold')  # title
plt.xlabel('Date', fontsize=12)  # x-axis label
plt.ylabel('Temperature (°F)', fontsize=12)  # y-axis label
plt.legend(loc='upper left', fontsize=11)  # legend
plt.grid(True, alpha=0.3)  # add subtle grid
plt.xticks(rotation=45)  # rotate x-ticks for readability
plt.tight_layout()  # adjust layout to fit elements

# Save the temperature plot
plt.savefig("temperatures_over_time.png", dpi=300, bbox_inches='tight')
print("\nTemperature plot saved as 'temperatures_over_time.png'")

# PLOT 2: Precipitation Over Time using Matplotlib
plt.figure(figsize=(12, 6))  # Set figure size
plt.plot(df_clean.index, df_clean['PRECIPITATION'],
         label='Precipitation', color='#45B7D1', linestyle='--', linewidth=1.5)

plt.title('Precipitation Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Precipitation (inches)', fontsize=12)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, alpha=0.3)  # add subtle grid
plt.xticks(rotation=45)  # rotate x-ticks for readability
plt.tight_layout()  # adjust layout to fit elements

# Save the precipitation plot
plt.savefig("precipitation_over_time.png", dpi=300, bbox_inches='tight')
print("Precipitation plot saved as 'precipitation_over_time.png'")

# PLOT 3: BONUS - Mean Temperature Over Time
plt.figure(figsize=(12, 6))
plt.plot(df_clean.index, df_clean['MEAN TEMP'],
         label='Mean Temperature', color='#10B981', linewidth=2)

plt.title('Mean Temperature Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Temperature (°F)', fontsize=12)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the mean temperature plot
plt.savefig("mean_temperature_over_time.png", dpi=300, bbox_inches='tight')
print("Mean temperature plot saved as 'mean_temperature_over_time.png'")

# We can also save our cleaned data to a new CSV for future use
df_clean.to_csv('cleaned_weather_data.csv', index=True)

# Or we can print summary statistics
print(f"\n{'='*50}")
print("DATA PROCESSING COMPLETE")
print(f"{'='*50}")
print(f"Total records processed: {len(df_clean):,}")
print(
    f"Date range: {df_clean.index.min().strftime('%Y-%m-%d')} to {df_clean.index.max().strftime('%Y-%m-%d')}")
print(f"Plots saved:")
print(f"  1. temperatures_over_time.png")
print(f"  2. precipitation_over_time.png")
print(f"  3. mean_temperature_over_time.png")
print(f"{'='*50}")

# Close all figures to free memory
plt.close('all')
print("All plots closed and memory freed.")
