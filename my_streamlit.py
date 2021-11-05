import os
import sys
import json
import time
import datetime
import traceback
from copy import deepcopy

import requests
import pandas as pd
import numpy as np
import streamlit as st


st.set_page_config(page_title="My Streamlit App",page_icon=":shark:",layout="wide")
st.slider.radio('选择图表',['Line','Bar'])
st.title(':sunny:')
st.markdown('Streamlit is **_really_ cool**.')
st.caption('This is a string that explains something above.')
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')
st.text('This is some text.')
st.latex(r'''a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =\sum_{k=0}^{n-1} ar^k =a \left(\frac{1-r^{n}}{1-r}\right)''')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")


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