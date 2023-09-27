import streamlit as st
import time
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Part 1")

st.markdown("# Part 1")
st.write(
    """Calculate the urban heat island intensity using daily mean, 
    maximum, and minimum temperatures for each day and then average 
    them to each month (no figure or value is needed). Then average 
    the monthly results from 2000 to 2016. For example, you should 
    average all the January results from 2000 to 2016 to obtain an 
    averaged January urban heat island effect. Plot the averaged urban 
    heat islands as a function of month (you can think of this as the 
    averaged seasonal cycle of urban heat island). Use different colors 
    or markers for daily mean, maximum, and minimum temperatures but 
    plot them on the same figure."""
)   
st.markdown("""In order to calculate Urban Heat Island Intensity we can use: 
            
$$ UHI_{Intensity} = \Delta T = T_{urban} - T_{rural}$$""")
            
st.sidebar.header("Part 1")


df_mean = pd.read_csv("UHI_intensityMean T.csv")
df_max = pd.read_csv("UHI_intensityMaximum T.csv")
df_min = pd.read_csv("UHI_intensityMinimum T.csv")

fig = go.Figure(data=[go.Table(
    header=dict(values=['Month', 'UHI Intensity 2000 - 2016 (Mean T)', 'UHI Intensity 2000 - 2016 (Max T)', 'UHI Intensity 2000 - 2016 (Min T)'],
                line_color='rgb(8, 81, 156)', fill_color='rgb(8, 81, 156)', font=dict(color='white'),
                align='left'),
    cells=dict(values=[df_mean.Month, df_mean.Mean, df_max.Mean, df_min.Mean],
               align='left'))
])

st.plotly_chart(fig, use_container_width=True)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")