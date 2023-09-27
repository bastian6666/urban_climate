import pandas as pd
import plotly.graph_objects as go
import calendar
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit as st


st.set_page_config(page_title="Part 2")

st.markdown("# Part 2")
st.write(
    """Calculate the urban heat island intensity using daily mean, 
    maximum, and minimum temperatures for each day (no figure or value 
    is needed). Average the daily urban heat island intensities over 
    the summer season (including June, July, August) in the period of 
    2000-2016 and report the values. Report the values for daily mean, 
    maximum, and minimum temperature separately. Here you should not take 
    the simple average of June, July, and August results you obtain in 1 
    because June/July/August have different numbers of days, but you also 
    show not report values for June, July, August separately. All I want 
    is the values for the summer season, not for individual months in the summer season.
"""
)   
            
st.sidebar.header("Part 2")


df_mean = pd.read_csv("UHI_summer Mean T.csv")
df_max = pd.read_csv("UHI_summer Maximum T.csv")
df_min = pd.read_csv("UHI_summer Minimum T.csv")

fig = go.Figure(data=[go.Table(
    header=dict(values=['Index day', 'UHI Intensity Mean T 2000 - 2016', 'UHI Intensity Max T 2000 - 2016', 'UHI Intensity Min T 2000 - 2016'],
                line_color='rgb(8, 81, 156)', fill_color='rgb(8, 81, 156)', font=dict(color='white'),
                align='left'),
    cells=dict(values=[df_mean.index, df_mean.Mean, df_max.Mean, df_min.Mean],
               align='left'))
])


st.plotly_chart(fig, use_container_width=True)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.

"""
Focus on daily results in the summer (June, July, August) seasons in the period of 2000-2016 (you should have 17 years x 92 summer days per year = 1564 summer days). Plot the daily urban heat island intensity (use different subplots or subfigures for daily mean, maximum, and minimum temperatures) as a function of the daily mean temperature of the rural site and fit a linear relation between the two. How does the urban heat island intensity change with the mean temperature of the rural site?

    * Discussion:

Focus on daily results in the summer (June, July, August) seasons in the period of 2000-2016 (you should have 17 years x 92 summer days per year = 1564 summer days). Plot the daily urban heat island intensity (use different subplots or subfigures for daily mean, maximum, and minimum temperatures) as a function of the daily mean temperature of the urban site and fit a
linear relation between the two. How does the urban heat island intensity change with the mean temperature of the urban site?

    * Discussion:
"""


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

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Discussion: 

One of the questions researchers have been trying to figure out is whether the UHI intensity increases or decreases as the climate system warms up (i.e., in a warming climate). Your results in 1.4 and 1.5 probably give you different answers to this question. Which one do you think is correct or more correct? Discuss your results.

    * Answer: 
            """)

st.button("Re-run")