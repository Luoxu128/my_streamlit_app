import os
import sys
import json
import time
import datetime
import traceback
from copy import deepcopy

import streamlit as st
import pandas as pd
import numpy as np
import requests

import graphviz
import pydeck as pdk
import altair as alt
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO


def main():
    st.set_page_config(page_title="My Streamlit App",page_icon=":shark:",layout="wide")
    chart=st.sidebar.radio('Select Chart You Like',['Line','Bar','Area','Hist','Altair','Map','Distplot','Pdk','Graphviz'])
    color = st.sidebar.color_picker('Pick A Color You Like', '#1535C9')
    st.sidebar.write('The current color is', color)

    if 'show_balloons' not in st.session_state:
        st.session_state.show_balloons=True
    else:
        st.session_state.show_balloons=False

    if st.session_state.show_balloons:
        st.balloons()

    if "celsius" not in st.session_state:
        # set the initial default value of the slider widget
        st.session_state.celsius = 50.0

    d=st.sidebar.date_input('Date')
    t=st.sidebar.time_input('Time')
    st.sidebar.write(f'The current date time is {d} {t}')
    st.sidebar.slider("Temperature in Celsius",min_value=0.0,max_value=100.0,key="celsius")
    # This will get the value of the slider widget
    st.sidebar.write(st.session_state.celsius)
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
        ax.hist(arr, bins=15)
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

    elif chart == 'Graphviz':
        empty_ele.graphviz_chart('''
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

    empty_ele1=st.empty()
    animal=st.sidebar.selectbox('Select Animal You Like',['Cat','Dog','Fox'])
    img=get_one_picture(animal)
    empty_ele1.image(img, caption=f'A {animal} Picture',use_column_width=False)

    with st.expander("View Code"):
        with open('my_streamlit.py','r') as f:
            code=f.read()
        st.code(code,language="python")

@st.cache
def get_one_picture(animal):
    if animal == 'Cat':
        url=requests.get('https://aws.random.cat/meow').json()['file']
    elif animal == 'Dog':
        url=requests.get('https://random.dog/woof.json').json()['url']
    elif animal == 'Fox':
        url=requests.get('https://randomfox.ca/floof/').json()['image']
    r=requests.get(url)
    img=Image.open(BytesIO(r.content))
    return img


if __name__ == '__main__':
    main()