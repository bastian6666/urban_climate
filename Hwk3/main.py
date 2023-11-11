import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convert_units(df, site):
    df[f'Ta_{site}'] = df[f'Ta_{site}'] + 273.15
    df[f'P_mean_{site}'] = df[f'P_mean_{site}'] * 1000
    df[f'e_{site}'] = df[f'e_{site}'] * 1000
    return df

# Read the CSV files
df_crop = pd.read_csv('data_clean/diurnal_crop.csv')
df_grass = pd.read_csv('data_clean/diurnal_grass.csv')
df_urban = pd.read_csv('data_clean/diurnal_urban.csv')

# Convert the units for each dataframe
df_crop = convert_units(df_crop, 'crop')
df_grass = convert_units(df_grass, 'grass')
df_urban = convert_units(df_urban, '26_5m')

# Save the dataframes
# df_crop.to_csv('data_clean/diurnal_crop_converted.csv', index=False)
# df_grass.to_csv('data_clean/diurnal_grass_converted.csv', index=False)
# df_urban.to_csv('data_clean/diurnal_urban_converted.csv', index=False)


def calculate_humidity(df, site):
    # Calculate e*
    df[f'e_star_{site}'] = 611 * np.exp((17.27 * (df[f'Ta_{site}'] - 273.15)) / ((df[f'Ta_{site}'] - 273.15) + 237.3))

    # Calculate q
    df[f'q_{site}'] = 0.622 * (df[f'e_{site}'] / (df[f'P_mean_{site}'] - df[f'e_{site}']))

    # Calculate RH
    df[f'RH_{site}'] = (df[f'e_{site}'] / df[f'e_star_{site}']) * 100

    return df

# Calculate humidity for each dataframe
df_crop = calculate_humidity(df_crop, 'crop')
df_grass = calculate_humidity(df_grass, 'grass')
df_urban = calculate_humidity(df_urban, '26_5m')

# Save the dataframes
df_crop.to_csv('data_clean/diurnal_crop_converted.csv', index=False)
df_grass.to_csv('data_clean/diurnal_grass_converted.csv', index=False)
df_urban.to_csv('data_clean/diurnal_urban_converted.csv', index=False)



def plot_diurnal_cycles(df_crop, df_grass, df_urban, variable):
    units = {
        'q': 'g/kg',
        'e_star': 'Pa',
        'RH': '%',
    }

    plt.figure(figsize=(10, 6))

    # Plot variable for all three sites
    plt.plot(df_crop[f'{variable}_crop'], label=f'{variable} (crop)', linewidth=2)
    plt.plot(df_grass[f'{variable}_grass'], label=f'{variable} (grass)', linewidth=2)
    plt.plot(df_urban[f'{variable}_26_5m'], label=f'{variable} (urban)', linewidth=2)

    plt.legend(fontsize=12)
    plt.title(f'Average Diurnal Cycles of {variable}', fontsize=16)
    plt.xlabel('Hour of the day', fontsize=14)
    plt.ylabel(f'{variable} ({units[variable]})', fontsize=14)

    # Add gridlines
    plt.grid(True)

    plt.show()

# Plot diurnal cycles for each variable
plot_diurnal_cycles(df_crop, df_grass, df_urban, 'q')
plot_diurnal_cycles(df_crop, df_grass, df_urban, 'e_star')
plot_diurnal_cycles(df_crop, df_grass, df_urban, 'RH')


def compare_RH(df, site):
    plt.figure(figsize=(6, 6))

    # Assuming 'RH_given' is the column name for the given relative humidity
    plt.scatter(df[f'Rh_{site}'], df[f'RH_{site}'])

    # Draw the line y = x
    limits = [min(plt.xlim()[0], plt.ylim()[0]), max(plt.xlim()[1], plt.ylim()[1])]
    plt.plot(limits, limits, color='red')

    plt.title(f'Comparison of Given and Computed RH at {site}')
    plt.xlabel('Given RH (%)')
    plt.ylabel('Computed RH (%)')
    plt.show()

# Compare RH for each dataframe
compare_RH(df_crop, 'crop')
compare_RH(df_grass, 'grass')
compare_RH(df_urban, '26_5m')

def plot_diurnal_cycles(df, site):
    # Assuming there's a 'hour' column in your dataframes
    df_grouped = df.groupby('hour').mean()

    plt.figure(figsize=(10, 6))

    # Plot both given and calculated RH with enhanced line width and style
    plt.plot(df_grouped[f'Rh_{site}'], label='Given RH (%)', linewidth=2, linestyle='--')
    plt.plot(df_grouped[f'RH_{site}'], label='Calculated RH (%)', linewidth=2, linestyle='-')

    plt.legend(fontsize=12)
    plt.title(f'Average Diurnal Cycles of Given and Calculated RH at {site}', fontsize=16)
    plt.xlabel('Hour of the day', fontsize=14)
    plt.ylabel('RH (%)', fontsize=14)

    # Add gridlines
    plt.grid(True)

    plt.show()

# Plot diurnal cycles for each dataframe
plot_diurnal_cycles(df_crop, 'crop')
plot_diurnal_cycles(df_grass, 'grass')
plot_diurnal_cycles(df_urban, '26_5m')


def calculate_heat_index(df, site):
    T = df[f'Ta_{site}']
    R = df[f'Rh_{site}']

    # Compute the heat index
    df[f'heat_index_{site}'] = -42.379 + 2.04901523*T + 10.14333127*R - 0.22475541*T*R - 6.83783*10**-3*T**2 - 5.481717*10**-2*R**2 + 1.22874*10**-3*T**2*R + 8.5282*10**-4*T*R**2 - 1.99*10**-6*T**2*R**2

    return df

# Calculate heat index for each dataframe
df_crop = calculate_heat_index(df_crop, 'crop')
df_grass = calculate_heat_index(df_grass, 'grass')
df_urban = calculate_heat_index(df_urban, '26_5m')

# Save the dataframes
df_crop.to_csv('data_clean/diurnal_crop_converted.csv', index=False)
df_grass.to_csv('data_clean/diurnal_grass_converted.csv', index=False)
df_urban.to_csv('data_clean/diurnal_urban_converted.csv', index=False)


def plot_diurnal_cycles_heat_index(df_crop, df_grass, df_urban):

    plt.figure(figsize=(10, 6))

    # Plot heat index for all three sites
    plt.plot(df_crop['heat_index_crop'], label='Heat Index (crop)', linewidth=2)
    plt.plot(df_grass['heat_index_grass'], label='Heat Index (grass)', linewidth=2)
    plt.plot(df_urban['heat_index_26_5m'], label='Heat Index (urban)', linewidth=2)

    plt.legend(fontsize=12)
    plt.title('Average Diurnal Cycles of Heat Index', fontsize=16)
    plt.xlabel('Hour of the day', fontsize=14)
    plt.ylabel('Heat Index (°C)', fontsize=14)

    # Add gridlines
    plt.grid(True)

    plt.show()

# Plot diurnal cycles for all dataframes
plot_diurnal_cycles_heat_index(df_crop, df_grass, df_urban)