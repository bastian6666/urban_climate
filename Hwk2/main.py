import pandas as pd
import matplotlib.pyplot as plt


def diurnal_cycles(site_data1, site_data2, site_data3):
    """
    Plots the diurnal cycles for each variable for a given site.

    Parameters
    ----------
    df1 : pandas.DataFrame
        The data for a given urban site.
    df2 : pandas.DataFrame
        The data for a given rural site.
    df3 : pandas.DataFrame
        The data for a given rural site.

    Returns
    -------
    None
    """
    # Convert the date column to datetime format
    site_data1["T_Local"] = pd.to_datetime(site_data1["T_Local"])
    site_data2["T_Local"] = pd.to_datetime(site_data2["T_Local"])
    site_data3["T_Local"] = pd.to_datetime(site_data3["T_Local"])

    # Extract the day and hour from the date column
    #site_data["day"] = site_data["T_Local"].dt.day
    site_data1["hour"] = site_data1["T_Local"].dt.hour
    site_data2["hour"] = site_data2["T_Local"].dt.hour
    site_data3["hour"] = site_data3["T_Local"].dt.hour

    # Compute the average values per hour in multiple days
    mean_values1 = site_data1.groupby(["hour"]).mean()
    mean_values2 = site_data2.groupby(["hour"]).mean()
    mean_values3 = site_data3.groupby(["hour"]).mean()
    
    variables1 = mean_values1.columns
    print(variables1)
    variables2 = mean_values2.columns
    variables3 = mean_values3.columns

    # Plot the average diurnal cycles for each variable for each site
    ii = 0
    for var in range(len(variables1)):
        plt.figure()
        plt.plot(mean_values1[variables1[ii]], label="Urban")
        plt.plot(mean_values2[variables2[ii]], label="Grass")
        plt.plot(mean_values3[variables3[ii]], label="Crop")
        variable_name = variables1[ii].replace('_26_5m', '')
        plt.title(variable_name)
        plt.xlabel("Hour")
        plt.ylabel(variable_name)
        plt.legend()
        #plt.show()
        plt.savefig("figures/figures9_16/" + str(variables1[ii]) + ".pdf")

        ii += 1

    return mean_values1, mean_values2, mean_values3


def Air_UHI_Intensity(df1, df2, df3):
    """
    Computes the UHI intensity for a given site.

    Parameters
    ----------
    df1 : pandas.DataFrame
        The data for a given urban site.
    df2 : pandas.DataFrame
        The data for a given rural site.
    df3 : pandas.DataFrame
        The data for a given rural site.

    Returns
    -------
    None
    """
    var = ['Ta_26_5m', 'Ta_grass', 'Ta_crop']

    UHI_I_Grass = df1[var[0]] - df2[var[1]]
    UHI_I_Crop = df1[var[0]] - df3[var[2]]
    print(UHI_I_Grass)
    print(UHI_I_Crop)

    # plt.figure()
    # plt.plot(df1['hour'], UHI_I_Grass, label="UHI intensity (Grass)")
    # plt.title("UHI intensity (Grass)")
    # plt.xlabel("Hour")
    # plt.ylabel("UHI intensity")
    # plt.legend()
    # # plt.show()
    # plt.savefig("figures/UHI_figures/Grass_UHI_intensity_air.pdf")
    

    plt.plot(df1['hour'], UHI_I_Crop, label="UHI intensity (Crop)")
    plt.title("UHI intensity (Air)")
    plt.xlabel("Hour")
    plt.ylabel("UHI intensity")
    plt.legend()
    # plt.show()
    plt.savefig("figures/UHI_figures/Crop_UHI_intensity_air.pdf")

def Surface_UHI_Intensity(df1, df2, df3, var, emissivity1, emissivity2, emissivity3):
    """
    Computes the UHI intensity for a given site.
    
    Parameters
    ----------
    df1 : pandas.DataFrame
        The data for a given urban site.
        df2 : pandas.DataFrame
        The data for a given rural site.
        df3 : pandas.DataFrame
        The data for a given rural site.
        var : list
        The list of variables to plot.
        emissivity1 : float
        The emissivity of the urban site.
        emissivity2 : float
        The emissivity of the grass site.
        emissivity3 : float
        The emissivity of the crop site.
        
        Returns
        -------
        None
    """

    sigma = 5.67e-8
    Ts_urban = ((df1[var[1]] - (1-emissivity1)*df1[var[0]])/(sigma*emissivity1))**(1/4)
    Ts_grass = ((df2[var[3]] - (1-emissivity2)*df2[var[2]])/(sigma*emissivity2))**(1/4)
    Ts_crop = ((df3[var[5]] - (1-emissivity3)*df3[var[4]])/(sigma*emissivity3))**(1/4)

    Ts_urban = kelvin_to_celsius(Ts_urban)
    Ts_grass = kelvin_to_celsius(Ts_grass)
    Ts_crop = kelvin_to_celsius(Ts_crop)

    Ts_urban.to_csv("data_clean/Ts_urban.csv")
    Ts_grass.to_csv("data_clean/Ts_grass.csv")
    Ts_crop.to_csv("data_clean/Ts_crop.csv")

    UHI_I_Grass = Ts_urban - Ts_grass
    UHI_I_Crop = Ts_urban - Ts_crop

    plt.figure()
    plt.plot(df1['hour'], UHI_I_Grass, label="UHI intensity (Grass)")
    plt.title("UHI intensity (Grass)")
    plt.xlabel("Hour")
    plt.ylabel("UHI intensity")
    plt.legend()
    # plt.show()
    plt.savefig("figures/UHI_figures/Grass_UHI_intensity_surface.pdf")
    plt.figure()
    plt.plot(df1['hour'], UHI_I_Crop, label="UHI intensity (Crop)")
    plt.title("UHI intensity (Surface)")
    plt.xlabel("Hour")
    plt.ylabel("UHI intensity")
    plt.legend()
    # plt.show()
    plt.savefig("figures/UHI_figures/Crop_UHI_intensity_surface.pdf")

def heat_fluxes(df1, df2, df3, var):
    """
    Computes the heat fluxes for a given site.

    Parameters
    ----------
    df1 : pandas.DataFrame
        The data for a given urban site.
    df2 : pandas.DataFrame
        The data for a given rural site.
    df3 : pandas.DataFrame
        The data for a given rural site.
    var : list
        The list of variables to plot.
        
    Returns
    -------
    None
    """

    Urban_Hf = df1[var[0]] - df1[var[1]] - df1[var[2]]
    Grass_Hf = df2[var[3]] - df2[var[4]] - df2[var[5]]
    Crop_Hf = df3[var[6]] - df3[var[7]] - df3[var[8]]

    plt.figure()
    plt.plot(df1['hour'], Urban_Hf, label="Urban")
    plt.plot(df1['hour'], Grass_Hf, label="Grass")
    plt.plot(df1['hour'], Crop_Hf, label="Crop")
    plt.title("Heat fluxes")
    plt.xlabel("Hour")
    plt.ylabel("Heat fluxes" + r"$(W/m^2)$")
    plt.legend()
    # plt.show()
    plt.savefig("figures/figures9_16/Heat_fluxes.pdf")

def kelvin_to_celsius(temp_k):
    """
    Convert temperature from Kelvin to Celsius.

    Parameters
    ----------
    temp_k : float
        Temperature in Kelvin.

    Returns
    -------
    float
        Temperature in Celsius.
    """
    return temp_k - 273.15