import pandas as pd
import plotly.graph_objects as go
import calendar
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit as st




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



