import json
import time
import random
import datetime

import requests
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

import graphviz
import pydeck as pdk
import altair as alt
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

from PIL import Image
from io import BytesIO


def main():
    st.set_page_config(page_title="七里香还是稻香",page_icon=":rainbow:",layout="wide",initial_sidebar_state="expanded")
    st.title('七里香还是稻香:heart:')
    st.markdown('<br>',unsafe_allow_html=True)
    st.markdown('<br>',unsafe_allow_html=True)
    charts_mapping={
        'Line':'line_chart','Bar':'bar_chart','Area':'area_chart','Hist':'pyplot','Altair':'altair_chart',
        'Map':'map','Distplot':'plotly_chart','Pdk':'pydeck_chart','Graphviz':'graphviz_chart','PyEchart':''
    }
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit=True
    else:
        st.session_state.first_visit=False
    # 初始化全局配置
    if st.session_state.first_visit:
        st.session_state.date_time=datetime.datetime.now() + datetime.timedelta(hours=8)
        st.session_state.random_chart_index=random.choice(range(len(charts_mapping)))
        st.session_state.my_random=MyRandom(random.randint(1,1000000))
        st.session_state.city_mapping,st.session_state.random_city_index=get_city_mapping()
        # st.session_state.random_city_index=random.choice(range(len(st.session_state.city_mapping)))
        st.balloons()

    music=st.sidebar.radio('Select Music You Like',['七里香','稻香'],index=random.choice(range(2)))
    st.sidebar.write(f'正在播放 {music}-周杰伦 :musical_note:')
    audio_bytes=get_audio_bytes(music)
    st.sidebar.audio(audio_bytes, format='audio/mp3')

    d=st.sidebar.date_input('Date',st.session_state.date_time.date())
    t=st.sidebar.time_input('Time',st.session_state.date_time.time())
    t=f'{t}'.split('.')[0]
    st.sidebar.write(f'The current date time is {d} {t}')
    chart=st.sidebar.selectbox('Select Chart You Like',charts_mapping.keys(),index=st.session_state.random_chart_index)
    city=st.sidebar.selectbox('Select City You Like',st.session_state.city_mapping.keys(),index=st.session_state.random_city_index)
    color = st.sidebar.color_picker('Pick A Color You Like', '#1535C9')
    st.sidebar.write('The current color is', color)

    if "celsius" not in st.session_state:
        # set the initial default value of the slider widget
        st.session_state.celsius = 50.0

    st.sidebar.slider("Temperature in Celsius",min_value=0.0,max_value=100.0,key="celsius")
    # This will get the value of the slider widget
    st.sidebar.write(st.session_state.celsius)

    with st.container():
        st.markdown(f'### {city} Weather Forecast')
        forecastToday,df_forecastHours,df_forecastDays=get_city_weather(st.session_state.city_mapping[city])
        col1,col2,col3,col4,col5,col6=st.columns(6)
        col1.metric('Weather',forecastToday['weather'])
        col2.metric('Temperature',forecastToday['temp'])
        col3.metric('Body Temperature',forecastToday['realFeel'])
        col4.metric('Humidity',forecastToday['humidity'])
        col5.metric('Wind',forecastToday['wind'])
        col6.metric('UpdateTime',forecastToday['updateTime'])
        with st.expander("24 Hours Forecast"):
            st.table(df_forecastHours)
        with st.expander("7 Days Forecast",expanded=True):
            st.table(df_forecastDays)

    c = (
        Line()
        .add_xaxis(df_forecastHours.index.to_list())
        .add_yaxis('Temperature', [int(i.replace('°C','')) for i in df_forecastHours.Temperature.values.tolist()])
        .set_global_opts(title_opts=opts.TitleOpts(title="24 Hours Forecast"),toolbox_opts=opts.ToolboxOpts(),xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False))
        .set_series_opts(label_opts=opts.LabelOpts(formatter=JsCode("function(x){return x.data + '°C';}")))
        .render_embed() # generate a local HTML file
    )
    components.html(c, width=1200, height=800)

    st.markdown(f'### {chart} Chart')
    df=get_chart_data(chart,st.session_state.my_random)
    eval(f'st.{charts_mapping[chart]}(df{",use_container_width=True" if chart in ["Distplot","Altair"] else ""})' if chart != 'PyEchart' else f'st_echarts(options=df)')

    st.markdown('### Animal Pictures')
    col1,col2,col3=st.columns(3)
    cat_img,dog_img,fox_img=get_pictures(st.session_state.my_random)
    col1.image(cat_img, caption='A Cat Picture',use_column_width=True)
    col2.image(dog_img, caption='A Dog Picture',use_column_width=True)
    col3.image(fox_img, caption='A Fox Picture',use_column_width=True)

    st.markdown('### Some Ads Videos')
    col1,col2=st.columns(2)
    video1=get_video_bytes('开不了口')
    col1.video(video1)
    video2=get_video_bytes('最长的电影')
    col2.video(video2, format='video/mp4')

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

@st.cache(hash_funcs={MyRandom: my_hash_func},allow_output_mutation=True)
def get_chart_data(chart,my_random):
    data=np.random.randn(20,3)
    df=pd.DataFrame(data,columns=['a', 'b', 'c'])
    if chart in ['Line','Bar','Area']:
        return df

    elif chart == 'Hist':
        arr = np.random.normal(1, 1, size=100)
        fig, ax = plt.subplots()
        ax.hist(arr, bins=20)
        return fig

    elif chart == 'Altair':
        df = pd.DataFrame(np.random.randn(200, 3),columns=['a', 'b', 'c'])
        c = alt.Chart(df).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
        return c

    elif chart == 'Map':
        df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        return df

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

    elif chart == 'Pdk':
        df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        args=pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=37.76,longitude=-122.4,zoom=11,pitch=50,),
            layers=[pdk.Layer('HexagonLayer',data=df,get_position='[lon, lat]',radius=200,elevation_scale=4,elevation_range=[0, 1000],pickable=True,extruded=True),
            pdk.Layer('ScatterplotLayer',data=df,get_position='[lon, lat]',get_color='[200, 30, 0, 160]',get_radius=200)])
        return args

    elif chart == 'Graphviz':
        graph = graphviz.Digraph()
        graph.edge('grandfather', 'father')
        graph.edge('grandmother', 'father')
        graph.edge('maternal grandfather', 'mother')
        graph.edge('maternal grandmother', 'mother')
        graph.edge('father', 'brother')
        graph.edge('mother', 'brother')
        graph.edge('father', 'me')
        graph.edge('mother', 'me')
        graph.edge('brother', 'nephew')
        graph.edge('Sister-in-law', 'nephew')
        graph.edge('brother', 'niece')
        graph.edge('Sister-in-law', 'niece')
        graph.edge('me', 'son')
        graph.edge('me', 'daughter')
        graph.edge('where my wife?', 'son')
        graph.edge('where my wife?', 'daughter')
        return graph

    elif chart == 'PyEchart':
        options = {
            "xAxis": {
                "type": "category",
                "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            },
            "yAxis": {"type": "value"},
            "series": [
                {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
            ],
        }
        return options

@st.cache(hash_funcs={MyRandom: my_hash_func})
def get_pictures(my_random):
    try:
        cat_img=Image.open(BytesIO(requests.get(requests.get('https://aws.random.cat/meow').json()['file']).content))
        dog_img=Image.open(BytesIO(requests.get(requests.get('https://random.dog/woof.json').json()['url']).content))
        fox_img=Image.open(BytesIO(requests.get(requests.get('https://randomfox.ca/floof/').json()['image']).content))
    except Exception as e:
        if 'cannot identify image file' in str(e):
            return get_pictures(my_random)
        else:
            st.error(str(e))
    return cat_img,dog_img,fox_img

@st.cache
def get_city_mapping():
    url='https://h5ctywhr.api.moji.com/weatherthird/cityList'
    r=requests.get(url)
    data=r.json()
    city_mapping=dict()
    guangzhou=0
    flag=True
    for i in data.values():
        for each in i:
            city_mapping[each['name']]=each['cityId']
            if each['name'] != '广州市' and flag:
                guangzhou+=1
            else:
                flag=False

    return city_mapping,guangzhou

@st.cache
def get_city_weather(cityId):
    url='https://h5ctywhr.api.moji.com/weatherDetail'
    headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data={"cityId":cityId,"cityType":0}
    r=requests.post(url,headers=headers,json=data)
    result=r.json()

    # today forecast
    forecastToday=dict(
        humidity=f"{result['condition']['humidity']}%",
        temp=f"{result['condition']['temp']}°C",
        realFeel=f"{result['condition']['realFeel']}°C",
        weather=result['condition']['weather'],
        wind=f"{result['condition']['windDir']}{result['condition']['windLevel']}级",
        updateTime=(datetime.datetime.fromtimestamp(result['condition']['updateTime'])+datetime.timedelta(hours=8)).strftime('%H:%M:%S')
    )

    # 24 hours forecast
    forecastHours=[]
    for i in result['forecastHours']['forecastHour']:
        tmp={}
        tmp['PredictTime']=(datetime.datetime.fromtimestamp(i['predictTime'])+datetime.timedelta(hours=8)).strftime('%H:%M')
        tmp['Temperature']=f"{i['temp']}°C"
        tmp['Body Temperature']=f"{i['realFeel']}°C"
        tmp['Humidity']=f"{i['humidity']}%"
        tmp['Weather']=i['weather']
        tmp['Wind']=f"{i['windDesc']}{i['windLevel']}级"
        forecastHours.append(tmp)
    df_forecastHours=pd.DataFrame(forecastHours).set_index('PredictTime')

    # 7 days forecast
    forecastDays=[]
    day_format={1:'昨天',0:'今天',-1:'明天',-2:'后天'}
    for i in result['forecastDays']['forecastDay']:
        tmp={}
        now=datetime.datetime.fromtimestamp(i['predictDate'])+datetime.timedelta(hours=8)
        diff=(st.session_state.date_time-now).days
        festival=i['festival']
        tmp['PredictDate']=(day_format[diff] if diff in day_format else now.strftime('%m/%d')) + (f' {festival}' if festival != '' else '')
        tmp['Temperature']=f"{i['tempLow']}~{i['tempHigh']}°C"
        tmp['Humidity']=f"{i['humidity']}%"
        tmp['WeatherDay']=i['weatherDay']
        tmp['WeatherNight']=i['weatherNight']
        tmp['WindDay']=f"{i['windDirDay']}{i['windLevelDay']}级"
        tmp['WindNight']=f"{i['windDirNight']}{i['windLevelNight']}级"
        forecastDays.append(tmp)
    df_forecastDays=pd.DataFrame(forecastDays).set_index('PredictDate')
    return forecastToday,df_forecastHours,df_forecastDays

@st.cache
def get_audio_bytes(music):
    audio_file = open(f'music/{music}-周杰伦.mp3', 'rb')
    audio_bytes = audio_file.read()
    audio_file.close()
    return audio_bytes

@st.cache
def get_video_bytes(video):
    video_file = open(f'video/{video}-广告曲.mp4', 'rb')
    video_bytes = video_file.read()
    video_file.close()
    return video_bytes

if __name__ == '__main__':
    main()