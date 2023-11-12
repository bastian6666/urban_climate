import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
sns.set_palette("Set2")


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
df_crop.to_csv('data_clean/diurnal_crop_converted.csv', index=False)
df_grass.to_csv('data_clean/diurnal_grass_converted.csv', index=False)
df_urban.to_csv('data_clean/diurnal_urban_converted.csv', index=False)


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
    plt.savefig(f'a)_{variable}.pdf', format='pdf')
    plt.show()

# Plot diurnal cycles for each variable
plot_diurnal_cycles(df_crop, df_grass, df_urban, 'q')
plot_diurnal_cycles(df_crop, df_grass, df_urban, 'e_star')
plot_diurnal_cycles(df_crop, df_grass, df_urban, 'RH')



def compare_RH(df1, site1, df2, site2, df3, site3):
    fig, axs = plt.subplots(1, 3, figsize=(12, 8))

    # Subplot 1: Compare RH for site1
    axs[0].scatter(df1[f'Rh_{site1}'], df1[f'RH_{site1}'])
    limits = [min(axs[0].get_xlim()[0], axs[0].get_ylim()[0]), max(axs[0].get_xlim()[1], axs[0].get_ylim()[1])]
    axs[0].plot(limits, limits, color='red')
    axs[0].set_title(f'Comparison of Given and Computed RH at {site1}', fontsize=14)
    axs[0].set_xlabel('Given RH (%)', fontsize=12)
    axs[0].set_ylabel('Computed RH (%)', fontsize=12)

    # Subplot 2: Compare RH for site2
    axs[1].scatter(df2[f'Rh_{site2}'], df2[f'RH_{site2}'])
    limits = [min(axs[1].get_xlim()[0], axs[1].get_ylim()[0]), max(axs[1].get_xlim()[1], axs[1].get_ylim()[1])]
    axs[1].plot(limits, limits, color='red')
    axs[1].set_title(f'Comparison of Given and Computed RH at {site2}', fontsize=14)
    axs[1].set_xlabel('Given RH (%)', fontsize=12)
    axs[1].set_ylabel('Computed RH (%)', fontsize=12)

    # Subplot 3: Compare RH for site3
    axs[2].scatter(df3[f'Rh_{site3}'], df3[f'RH_{site3}'])
    limits = [min(axs[2].get_xlim()[0], axs[2].get_ylim()[0]), max(axs[2].get_xlim()[1], axs[2].get_ylim()[1])]
    axs[2].plot(limits, limits, color='red')
    axs[2].set_title(f'Comparison of Given and Computed RH at {site3}', fontsize=14)
    axs[2].set_xlabel('Given RH (%)', fontsize=12)
    axs[2].set_ylabel('Computed RH (%)', fontsize=12)

    plt.tight_layout(pad=3.0)
    plt.show()

# Compare RH for each dataframe
compare_RH(df_crop, 'crop', df_grass, 'grass', df_urban, '26_5m')

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
    plt.savefig(f'b)_{site}.pdf', format='pdf')
    plt.show()

# Plot diurnal cycles for each dataframe
plot_diurnal_cycles(df_crop, 'crop')
plot_diurnal_cycles(df_grass, 'grass')
plot_diurnal_cycles(df_urban, '26_5m')


def calculate_heat_index(df, site):
    T = (df[f'Ta_{site}'] - 273.15) * 9/5 + 32
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
    sns.lineplot(data=df_crop['heat_index_crop'], label='Heat Index (crop)', linewidth=2)
    sns.lineplot(data=df_grass['heat_index_grass'], label='Heat Index (grass)', linewidth=2)
    sns.lineplot(data=df_urban['heat_index_26_5m'], label='Heat Index (urban)', linewidth=2)

    plt.legend(fontsize=12)
    plt.title('Average Diurnal Cycles of Heat Index', fontsize=16)
    plt.xlabel('Hour of the day', fontsize=14)
    plt.ylabel('Heat Index (°F)', fontsize=14)

    # Add gridlines
    plt.grid(True)
    plt.savefig(f'd)_heat_index.pdf', format='pdf')
    plt.show()

# Plot diurnal cycles for all dataframes
plot_diurnal_cycles_heat_index(df_crop, df_grass, df_urban)


def calculate_partial_derivatives(df, site):
    # Calculate d1, d2, and d3
    df[f'd1_{site}'] = -df[f'e_{site}'] / (df[f'e_star_{site}']**2)
    print(df[f'd1_{site}'])
    df[f'd2_{site}'] = (2.50398e6*np.exp((17.27*df[f'Ta_{site}']-4717.3)/(df[f'Ta_{site}']-35.85)))/(df[f'Ta_{site}']-35.85)**2
    print(df[f'd2_{site}'])
    df[f'd3_{site}'] = 1/(df[f'e_star_{site}'])

    return df

# Calculate function value for each dataframe
df_crop = calculate_partial_derivatives(df_crop, 'crop')
df_grass = calculate_partial_derivatives(df_grass, 'grass')
df_urban = calculate_partial_derivatives(df_urban, '26_5m')

df_crop.to_csv('data_clean/diurnal_crop_converted.csv', index=False)
df_grass.to_csv('data_clean/diurnal_grass_converted.csv', index=False)
df_urban.to_csv('data_clean/diurnal_urban_converted.csv', index=False)

def calculate_terms(df_crop, df_urban, site):
    df_crop[f'term1_{site}'] = 100*(df_crop[f'd1_{site}'] * df_crop[f'd2_{site}'] * (-df_crop[f'Ta_{site}'] + df_urban['Ta_26_5m']))
    df_crop[f'term2_{site}'] = 100*(df_crop[f'd3_{site}'] * (-df_crop[f'e_{site}'] + df_urban['e_26_5m']))

    df_crop[f'DeltaRH_terms_{site}'] = df_crop[f'term1_{site}'] + df_crop[f'term2_{site}']

                                          
    return df_crop

# Calculate product for each dataframe
df_crop = calculate_terms(df_crop, df_urban, 'crop')
df_crop.to_csv('data_clean/diurnal_crop_converted.csv', index=False)



def calculate_delta_RH(df1, df2, site1, site2):
    df1[f'delta_RH_{site1}_{site2}'] =  df2[f'RH_{site2}'] - df1[f'RH_{site1}']
    return df1

# Calculate ∆RH for crop and urban
df_crop = calculate_delta_RH(df_crop, df_urban, 'crop', '26_5m')

# Calculate ∆RH for grass and urban
df_grass = calculate_delta_RH(df_grass, df_urban, 'grass', '26_5m')

# Save the dataframes
df_crop.to_csv('data_clean/diurnal_crop_converted.csv', index=False)
df_grass.to_csv('data_clean/diurnal_grass_converted.csv', index=False)


def plot_subfigures(df, site1, site2):
    fig, axs = plt.subplots(1, 2, figsize=(24, 8))

    # Subplot 1: Term1, Term2 and their Sum
    axs[0].plot(df[f'term1_{site1}'], label=f'term1_{site1}', linewidth=2)
    axs[0].plot(df[f'term2_{site1}'], label=f'term2_{site1}', linewidth=2)
    axs[0].plot(df[f'term1_{site1}'] + df[f'term2_{site1}'], label='sum', linestyle='--', linewidth=2)
    axs[0].set_xlabel('Hour', fontsize=14)
    axs[0].set_ylabel('RH_urban-RH_crop (%)', fontsize=14)
    axs[0].set_title(f'Term1, Term2 and their Sum for {site1}', fontsize=16)
    axs[0].legend(fontsize=12)

    # Subplot 2: Comparison of DeltaRH_terms and delta_RH
    axs[1].plot(df[f'DeltaRH_terms_{site1}'], label=f'DeltaRH_terms_{site1}', linewidth=2)
    axs[1].plot(df[f'delta_RH_{site1}_{site2}'], label=f'delta_RH_{site1}_{site2}', linewidth=2)
    axs[1].set_xlabel('Hour', fontsize=14)
    axs[1].set_ylabel('RH_urban-RH_crop (%)', fontsize=14)
    axs[1].set_title(f'Comparison of DeltaRH_terms_{site1} and delta_RH_{site1}_{site2}', fontsize=16)
    axs[1].legend(fontsize=12)

    plt.subplots_adjust(wspace=0.3)
    plt.savefig('e.4_e.5.pdf', format='pdf')
    plt.show()

# Plot subfigures for crop and urban
plot_subfigures(df_crop, 'crop', '26_5m')


def compute_densities(df, site):
    R_dry_air = 287.058  # specific gas constant for dry air in J/(kg·K)
    R_water_vapor = 461.5  # specific gas constant for water vapor in J/(kg·K)


    # Compute air density
    df[f'air_density_{site}'] = df[f'P_mean_{site}'] / (R_dry_air * df[f'Ta_{site}'])

    # Compute water vapor density
    df[f'water_vapor_density_{site}'] = df[f'P_mean_{site}'] / (R_water_vapor * df[f'Ta_{site}'])

    return df

def plot_diurnal_cycles_densities(df_crop, df_grass, df_urban, site1, site2, site3):
    fig, axs = plt.subplots(1, 2, figsize=(12, 8))

    # Plot air density for all three sites
    sns.lineplot(data=df_crop[f'air_density_{site1}'], label=f'Air Density ({site1})', linewidth=2, ax=axs[0])
    sns.lineplot(data=df_grass[f'air_density_{site2}'], label=f'Air Density ({site2})', linewidth=2, ax=axs[0])
    sns.lineplot(data=df_urban[f'air_density_{site3}'], label=f'Air Density ({site3})', linewidth=2, ax=axs[0])

    axs[0].legend(fontsize=12)
    axs[0].set_title('Average Diurnal Cycles of Air Densities', fontsize=16)
    axs[0].set_xlabel('Hour of the day', fontsize=14)
    axs[0].set_ylabel('Air Density (kg/m³)', fontsize=14)
    axs[0].grid(True)

    # Plot water vapor density for all three sites
    sns.lineplot(data=df_crop[f'water_vapor_density_{site1}'], label=f'Water Vapor Density ({site1})', linewidth=2, ax=axs[1])
    sns.lineplot(data=df_grass[f'water_vapor_density_{site2}'], label=f'Water Vapor Density ({site2})', linewidth=2, ax=axs[1])
    sns.lineplot(data=df_urban[f'water_vapor_density_{site3}'], label=f'Water Vapor Density ({site3})', linewidth=2, ax=axs[1])

    axs[1].legend(fontsize=12)
    axs[1].set_title('Average Diurnal Cycles of Water Vapor Densities', fontsize=16)
    axs[1].set_xlabel('Hour of the day', fontsize=14)
    axs[1].set_ylabel('Water Vapor Density (kg/m³)', fontsize=14)
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig('f)_bonus.pdf', format='pdf')
    plt.show()

df_crop = compute_densities(df_crop, 'crop')
df_grass = compute_densities(df_grass, 'grass')
df_urban = compute_densities(df_urban, '26_5m')

plot_diurnal_cycles_densities(df_crop, df_grass, df_urban, 'crop', 'grass', '26_5m')