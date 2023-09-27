import pandas as pd
import plotly.graph_objects as go
import calendar
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit as st


st.set_page_config(page_title="Part 3")

st.markdown("# Part 3")
st.write(
    """Identify and list the heat wave days in the period of 2000-2016. For simplicity, let’s define a day as a heat wave day if the daily mean temperature at BWI is higher than 30 oC. Define the other days in the summer season as non-heat wave days. Make sure when you add heat wave days and non-heat wave days, you get 1564 days in total.

* Calculate the urban heat island intensity using daily mean, maximum, and minimum temperatures averaged over all heat wave days.

* Calculate the urban heat island intensity using daily mean, maximum, and minimum temperatures averaged over all non-heat wave but summer days.
    """
)   

def linear_fit_relation(df_y, df_x):

    model = LinearRegression()
    x = df_x.Mean.values.reshape(-1, 1)
    model.fit(x, df_y.Mean)

    x_range = np.linspace(x.min(), x.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    return x_range, y_range

def plot_heat_waves(UHI_df, T_df, name):

    df = pd.read_csv(UHI_df)
    df['Mean'] = df['UHI Heat Wave']
    df = df.dropna()
    heat_wave_df = pd.read_csv(T_df)
    heat_wave_df = heat_wave_df.dropna(subset=['Mean'])
    


    fig = go.Figure()

    # Section for Urban vs UHI Intensity
    fig.add_trace(go.Scatter(y=df['UHI Heat Wave'], x=heat_wave_df["Mean"],
                        mode='markers',
                        name='Mean Urban'))

    x, y = linear_fit_relation(df, heat_wave_df)

    fig.add_trace(go.Line(x=x, y=y,
                        mode='lines',
                        name='Mean Linear Regression Fit'))

    fig.update_layout(title='UHI Intensity During Heat Waves (Or Not) vs Temperature in Cº',
                    yaxis_title='UHI Intensity',
                    xaxis_title='Mean Temperature Cº',
                    template="simple_white")
    
    st.plotly_chart(fig, use_container_width=True)

plot_heat_waves(UHI_df = "UHI_mean_heat_wave.csv", T_df = "Urbanmean_heat_wave.csv", name = "Mean_heat_wave")
plot_heat_waves(UHI_df = "UHI_mean_Non_heat_wave.csv", T_df = "Urbanmean_Non_heat_wave.csv", name = "Mean_Non_heat_wave")
            

st.markdown("""Compare the results in 1.8, 1.9 and 1.3. Discuss your findings in terms of whether the urban heat island intensity is enhanced during heat wave days or not.
            
            Discussion: 
            """)

st.sidebar.header("Part 3")

