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
import altair as alt
import matplotlib.pyplot as plt


def main():
    st.set_page_config(page_title="My Streamlit App",page_icon=":shark:",layout="wide")
    chart=st.sidebar.radio('选择图表',['Line','Bar','Area','Hist','Altair'])
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