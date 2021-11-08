import os
import sys
import json
import time
import datetime
import traceback
import random
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
    st.title(':sunny:Streamlit is **_really_ cool**.:sunny:')
    charts=['Line','Bar','Area','Hist','Altair','Map','Distplot','Pdk','Graphviz']
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit=True
    else:
        st.session_state.first_visit=False
    # 初始化配置
    if st.session_state.first_visit:
        st.session_state.random_index=random.choice(range(len(charts)))
        st.session_state.random_num=random.randint(1,1000000)
        st.session_state.my_random=MyRandom(st.session_state.random_num)
        st.balloons()

    date_time=datetime.datetime.now() + datetime.timedelta(hours=8)
    d=st.sidebar.date_input('Date',date_time.date())
    t=st.sidebar.time_input('Time',date_time.time())
    t=f'{t}'.split('.')[0]
    st.sidebar.write(f'The current date time is {d} {t}')
    chart=st.sidebar.selectbox('Select Chart You Like',charts,index=st.session_state.random_index)
    st.markdown(f'### {chart} Chart')
    color = st.sidebar.color_picker('Pick A Color You Like', '#1535C9')
    st.sidebar.write('The current color is', color)

    if "celsius" not in st.session_state:
        # set the initial default value of the slider widget
        st.session_state.celsius = 50.0

    st.sidebar.slider("Temperature in Celsius",min_value=0.0,max_value=100.0,key="celsius")
    # This will get the value of the slider widget
    st.sidebar.write(st.session_state.celsius)
    # empty_ele=st.empty()
    df=get_chart_data(chart,st.session_state.my_random)
    mapping={
        'Line':['line_chart'],'Bar':['bar_chart'],'Area':['area_chart'],'Hist':['pyplot'],'Altair':['altair_chart'],
        'Map':['map'],'Distplot':['plotly_chart'],'Pdk':['pydeck_chart'],'Graphviz':['graphviz_chart']
    }
    eval(f'st.{mapping[chart][0]}(df{",use_container_width=True" if chart in ["Distplot","Altair"] else ""})')


    col1,col2,col3=st.columns(3)
    cat_img=get_one_picture('Cat',st.session_state.random_num)
    dog_img=get_one_picture('Dog',st.session_state.random_num)
    fox_img=get_one_picture('Fox',st.session_state.random_num)
    col1.image(cat_img, caption='A Cat Picture',use_column_width=True)
    col2.image(dog_img, caption='A Dog Picture',use_column_width=True)
    col3.image(fox_img, caption='A Fox Picture',use_column_width=True)

    with st.expander("View Code"):
        with open('my_streamlit.py','r') as f:
            code=f.read()
        st.code(code,language="python")

class MyRandom:
    def __init__(self,num):
        self.random_num=num

def my_hash_func(my_random):
    num = my_random.random_num
    return num

@st.cache(hash_funcs={st.delta_generator.DeltaGenerator: my_hash_func,MyRandom: my_hash_func},allow_output_mutation=True)
def get_chart_data(chart,my_random):
    data=np.random.randn(20,3)
    df=pd.DataFrame(data,columns=['a', 'b', 'c'])
    if chart in ['Line','Bar','Area']:
        return df
    # if chart == 'Line':
    #     st.line_chart(df)

    # elif chart == 'Bar':
    #     st.bar_chart(df)

    # elif chart == 'Area':
    #     st.area_chart(df)

    elif chart == 'Hist':
        arr = np.random.normal(1, 1, size=100)
        fig, ax = plt.subplots()
        ax.hist(arr, bins=20)
        return fig
        # st.pyplot(fig)

    elif chart == 'Altair':
        df = pd.DataFrame(np.random.randn(200, 3),columns=['a', 'b', 'c'])
        c = alt.Chart(df).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
        return c
        # st.altair_chart(c, use_container_width=True)

    elif chart == 'Map':
        df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        return df
        # st.map(df)

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
        return fig
        # st.plotly_chart(fig, use_container_width=True)

    elif chart == 'Pdk':
        df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        args=pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=37.76,longitude=-122.4,zoom=11,pitch=50,),
            layers=[pdk.Layer('HexagonLayer',data=df,get_position='[lon, lat]',radius=200,elevation_scale=4,elevation_range=[0, 1000],pickable=True,extruded=True),
            pdk.Layer('ScatterplotLayer',data=df,get_position='[lon, lat]',get_color='[200, 30, 0, 160]',get_radius=200)])
        # st.pydeck_chart(args)
        return args

    elif chart == 'Graphviz':
        viz='''
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
            }'''
        return viz
        # st.graphviz_chart(viz)

@st.cache
def get_one_picture(animal,random_num):
    if animal == 'Cat':
        url=requests.get('https://aws.random.cat/meow').json()['file']
    elif animal == 'Dog':
        url=requests.get('https://random.dog/woof.json').json()['url']
    elif animal == 'Fox':
        url=requests.get('https://randomfox.ca/floof/').json()['image']
    r=requests.get(url)
    img=Image.open(BytesIO(r.content))
    return img

@st.cache
def get_city_mapping():
    url='https://h5ctywhr.api.moji.com/weatherthird/cityList'
    r=requests.get(url)
    data=r.json()
    city_mapping=dict()
    for i in data.values():
        for each in i:
            city_mapping[each['cityId']]=each['name']

    return city_mapping




if __name__ == '__main__':
    main()