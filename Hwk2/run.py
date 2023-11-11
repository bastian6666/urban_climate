import pandas as pd
from main import diurnal_cycles, Air_UHI_Intensity, Surface_UHI_Intensity, heat_fluxes


def cycles():
    # Read the data from the files for all three sites
    site1_data = pd.read_csv("data_clean/urban_warm_2013.csv")
    site2_data = pd.read_csv("data_clean/grass_warm_2013.csv")
    site3_data = pd.read_csv("data_clean/crop_warm_2013.csv")

    diurnal_urban, diurnal_grass, diurnal_crop = diurnal_cycles(site1_data, site2_data, site3_data)

    print(diurnal_urban)
    print(diurnal_grass)
    print(diurnal_crop)

    diurnal_urban.to_csv("data_clean/diurnal_urban.csv")
    diurnal_grass.to_csv("data_clean/diurnal_grass.csv")
    diurnal_crop.to_csv("data_clean/diurnal_crop.csv")

def UHI_plots():
    
    site1_data = pd.read_csv("data_clean/diurnal_urban.csv")
    site2_data = pd.read_csv("data_clean/diurnal_grass.csv")
    site3_data = pd.read_csv("data_clean/diurnal_crop.csv")

    Air_UHI_Intensity(site1_data, site2_data, site3_data)

    var = ['DLR_26_5m', 'ULR_26_5m', 'DLR_grass', 'ULR_grass', 'DLR_crop', 'ULR_crop']

    # emmisivity = 0.95
    # emmisivity_grass = 0.93
    # emmisivity_crop = 0.93
    # Surface_UHI_Intensity(site1_data, site2_data, site3_data, var, emmisivity, emmisivity_grass, emmisivity_crop)

def Heat():

    site1_data = pd.read_csv("data_clean/diurnal_urban.csv")
    site2_data = pd.read_csv("data_clean/diurnal_grass.csv")
    site3_data = pd.read_csv("data_clean/diurnal_crop.csv")

    var = ['Rn_26_5m', 'Hs_26_5m', 'Le_26_5m', 'Rn_grass', 'Hs_grass', 'Le_grass', 'Rn_crop', 'Hs_crop', 'Le_crop']

    heat_fluxes(site1_data, site2_data, site3_data, var)



# Call the functions

# cycles()
UHI_plots()
# Heat()




