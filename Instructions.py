import pandas as pd
import plotly.graph_objects as go
import calendar
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit as st




#! UHI df
df_max = pd.read_csv("UHI_summer Maximum T.csv")
df_mean = pd.read_csv("UHI_summer Mean T.csv")
df_min = pd.read_csv("UHI_summer Minimum T.csv")

#! Urban df
urban_summer_df_mean = pd.read_csv("Urban_summer Mean T.csv")
urban_summer_df_max = pd.read_csv("Urban_summer Maximum T.csv")
urban_summer_df_min = pd.read_csv("Urban_summer Minimum T.csv")

#! Rural df
rural_summer_df_mean = pd.read_csv("Rural_summer Mean T.csv")
rural_summer_df_max = pd.read_csv("Rural_summer Maximum T.csv")
rural_summer_df_min = pd.read_csv("Rural_summer Minimum T.csv")


def linear_fit_relation(df_y, df_x):

    model = LinearRegression()
    x = df_x.Mean.values.reshape(-1, 1)
    model.fit(x, df_y.Mean)

    x_range = np.linspace(x.min(), x.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    return x_range, y_range



x_mean_urban, y_urban_mean = linear_fit_relation(df_mean, urban_summer_df_mean)
x_min_urban, y_urban_min = linear_fit_relation(df_min, urban_summer_df_min)
x_max_urban, y_urban_max = linear_fit_relation(df_max, urban_summer_df_max)

# Linear fit for Rural region
x_mean_rural, y_rural_mean = linear_fit_relation(df_mean, rural_summer_df_mean)
x_min_rural, y_rural_min = linear_fit_relation(df_min, rural_summer_df_min)
x_max_rural, y_rural_max = linear_fit_relation(df_max, rural_summer_df_max)


fig = go.Figure()

# Section for Urban vs UHI Intensity
fig.add_trace(go.Scatter(y=df_min["Mean"], x=urban_summer_df_min["Mean"],
                    mode='markers',
                    name='Min Urban'))
fig.add_trace(go.Scatter(y= df_max["Mean"], x=urban_summer_df_max["Mean"],
                    mode='markers',
                    name='Max Urban'))
fig.add_trace(go.Scatter(y=df_mean["Mean"], x=urban_summer_df_mean["Mean"],
                    mode='markers',
                    name='Mean Urban'))

# Section for Rural vs UHI Intensity
fig.add_trace(go.Scatter(y=df_min["Mean"], x=rural_summer_df_min["Mean"],
                    mode='markers',
                    name='Min Rural'))
fig.add_trace(go.Scatter(y= df_max["Mean"], x=rural_summer_df_max["Mean"],
                    mode='markers',
                    name='Max Rural'))
fig.add_trace(go.Scatter(y=df_mean["Mean"], x=rural_summer_df_mean["Mean"],
                    mode='markers',
                    name='Mean Rural'))

fig.add_trace(go.Line(x=x_min_urban, y=y_urban_min,
                    mode='lines',
                    name='Min Linear Regression Fit'))
fig.add_trace(go.Line(x=x_max_urban, y=y_urban_max,
                    mode='lines',
                    name='Max Linear Regression Fit'))
fig.add_trace(go.Line(x=x_mean_urban, y=y_urban_mean,
                    mode='lines',
                    name='Mean Linear Regression Fit'))

fig.add_trace(go.Line(x=x_min_rural, y=y_rural_min,
                    mode='lines',
                    name='Min Linear Regression Fit'))
fig.add_trace(go.Line(x=x_max_rural, y=y_rural_max,
                    mode='lines',
                    name='Max Linear Regression Fit'))
fig.add_trace(go.Line(x=x_mean_rural, y=y_rural_mean,
                    mode='lines',
                    name='Mean Linear Regression Fit'))


fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="All",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True, False, False, False, False, False, False]},
                           {"title": "UHI Intensity vs Temperature Cº in Urban area",
                            "annotations": []}]),
                dict(label="Min Urban",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False, True, False, False, False, False, False]},
                           {"title": "UHI Intensity vs Temperature Cº for Minimum Values in Urban area",
                            "annotations": []}]),
                dict(label="Max Urban",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False, False, True, False, False, False, False]},
                           {"title": "UHI Intensity vs Temperature Cº for Maximum Values in Urban area",
                            "annotations": []}]),
                dict(label="Mean Urban",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False, False, False, True, False, False, False]},
                           {"title": "UHI Intensity vs Temperature Cº for Mean Values in Urban area",
                            "annotations": []}]),
                dict(label="Min Rural",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False, False, False, False, True, False, False]},
                           {"title": "UHI Intensity vs Temperature Cº for Minimum Values in Rural area",
                            "annotations": []}]),
                dict(label="Max Rural",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False, False, False, False, False, True, False]},
                           {"title": "UHI Intensity vs Temperature Cº for Maximum Values in Rural area",
                            "annotations": []}]),
                dict(label="Mean Rural",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True, False, False, False, False, False, True]},
                           {"title": "UHI Intensity vs Temperature Cº for Mean Values in Rural area",
                            "annotations": []}]),
            ]),
        )
    ])

fig.update_layout(title='UHI Intensity vs Temperature in Cº',
                   yaxis_title='UHI Intensity',
                   xaxis_title='Mean Temperature Cº',
                   template="simple_white")



st.set_page_config(
    page_title="Urban Climate",
)

st.write("# Welcome to my Urban Climate Homewrok! 👋")

st.sidebar.success("Select a part of the homework.")

st.markdown(
    """
    ## Instructions: 

    The two excel sheets named ‘save_BWI2’ and ‘save_DMH2’ provide measurements of daily mean, maximum, 
    and minimum air temperatures in unit of Fahrenheit at Baltimore-Washington International Airport (BWI) 
    and Maryland Science Center (DMH) from 2000 to 2016. Each column represents, from left to right, year, 
    month, day, daily mean temperature, daily maximum temperature, and daily minimum temperature. These data 
    are publically available at National Climate Data Center. Assume that the DMH site represents urban land, 
    and BWI site represents rural land.
"""
)


st.plotly_chart(fig, use_container_width=True)
