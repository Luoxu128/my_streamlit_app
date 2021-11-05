import os
import sys
import json
import time
import datetime
import traceback
from copy import deepcopy

import requests
import graphviz
import pydeck as pdk
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from bokeh.plotting import figure,show
import plotly.figure_factory as ff
import matplotlib.pyplot as plt


def main():
    st.set_page_config(page_title="My Streamlit App",page_icon=":shark:",layout="wide")
    chart=st.sidebar.radio('选择图表',['Line','Bar','Area','Hist','Altair','Map','Distplot','Pdk','Bokeh','Graphviz'])
    st.title(':sunny:Streamlit is **_really_ cool**.:sunny:')
    empty_ele=st.empty()
    data=np.random.randn(20,3)
    df=pd.DataFrame(data,columns=['a', 'b', 'c'])
    if chart == 'Line':
        empty_ele.line_chart(df)

    elif chart == 'Bar':
        empty_ele.area_chart(df)

    elif chart == 'Area':
        empty_ele.bar_chart(df)

    elif chart == 'Hist':
        arr = np.random.normal(1, 1, size=100)
        fig, ax = plt.subplots()
        ax.hist(arr, bins=20)
        empty_ele.pyplot(fig)

    elif chart == 'Altair':
        df = pd.DataFrame(np.random.randn(200, 3),columns=['a', 'b', 'c'])
        c = alt.Chart(df).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
        empty_ele.altair_chart(c, use_container_width=True)

    elif chart == 'Map':
        df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        empty_ele.map(df)

    elif chart == 'Distplot':
        x1 = np.random.randn(200) - 2
        x2 = np.random.randn(200)
        x3 = np.random.randn(200) + 2
        # Group data together
        hist_data = [x1, x2, x3]
        group_labels = ['Group 1', 'Group 2', 'Group 3']
        # Create distplot with custom bin_size
        fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5])
        # Plot!
        empty_ele.plotly_chart(fig, use_container_width=True)

    elif chart == 'Pdk':
        df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        empty_ele.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=37.76,longitude=-122.4,zoom=11,pitch=50,),
            layers=[pdk.Layer('HexagonLayer',data=df,get_position='[lon, lat]',radius=200,elevation_scale=4,elevation_range=[0, 1000],pickable=True,extruded=True),
            pdk.Layer('ScatterplotLayer',data=df,get_position='[lon, lat]',get_color='[200, 30, 0, 160]',get_radius=200)]))

    elif chart == 'Bokeh':
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]
        p = figure(title='simple line example',x_axis_label='x',y_axis_label='y')
        p.line(x, y, legend_label='Trend', line_width=2)
        show(p)

    elif chart == 'Graphviz':
        st.graphviz_chart('''
            digraph {
                run -> intr
                intr -> runbl
                runbl -> run
                run -> kernel
                kernel -> zombie
                kernel -> sleep
                kernel -> runmem
                sleep -> swap
                swap -> runswap
                runswap -> new
                runswap -> runmem
                new -> runmem
                sleep -> runmem
            }''')

    if "celsius" not in st.session_state:
        # set the initial default value of the slider widget
        st.session_state.celsius = 50.0

    st.slider(
        "Temperature in Celsius",
        min_value=-100.0,
        max_value=100.0,
        key="celsius"
    )

    # This will get the value of the slider widget
    st.write(st.session_state.celsius)

if __name__ == '__main__':
    main()