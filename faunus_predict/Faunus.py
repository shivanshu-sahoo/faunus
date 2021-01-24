import streamlit as st
st.set_page_config(page_icon="favicon.ico" )
import joblib
import pandas as pd
import numpy as np
import webbrowser
import base64
from load_css import local_css
from bokeh.models.widgets import Div

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background: url("data:image/png;base64,%s");
    background-size: cover;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('image.png')




local_css("styles.css")
# st.markdown("<div class='fullscreen-image'><h1 class='landing-h1'>Lorem Ipsum</h1><p class='landing-p'>Lorem ipsum dolor sit.</p></div>", unsafe_allow_html=True)
st.markdown("<div class='heading blue'><h1>FAUNUS</h1> </div>", unsafe_allow_html=True)

st.markdown("<div><h1 class='highlight blue'>Predict if your Forest is in Danger</h1> </div>", unsafe_allow_html=True)
st.title("")

st.markdown("<div class='text blue'><h3><p>Enter Rain in mm/m2:</p></h3></div>", unsafe_allow_html=True)
rain= st.number_input("",key='a')
st.markdown("<div class='text blue'><h3><p>Enter Wind Speed in km/h:</p></h3></div>", unsafe_allow_html=True)
wind=st.number_input("",key='b')
st.markdown("<div class='text blue'><h3><p>Enter Relative Humidity in %:</p> </h3></div>", unsafe_allow_html=True)
rh=st.number_input("",key='c')
st.markdown("<div class='text blue'><h3><p>Enter Temperature in Celsius degrees:</p></h3> </div>", unsafe_allow_html=True)
temp=st.number_input("",key='d')
st.markdown("<div class='text blue'><h3><p>Enter ISI index from the FWI system:</p></h3> </div>", unsafe_allow_html=True)
isi=st.number_input("",key='e')
st.markdown("<div class='text blue'><h3><p>Enter DC index from the FWI system:</p></h3> </div>", unsafe_allow_html=True)
dc=st.number_input("",key='f')
st.markdown("<div class='text blue'><h3><p>Enter DMC index from the FWI system:</p> </h3></div>", unsafe_allow_html=True)
dmc=st.number_input("",key='g')
st.markdown("<div class='text blue'><h3><p>Enter FFMC index from the FWI system:</p></h3> </div>", unsafe_allow_html=True)
ffmc=st.number_input("",key='h')

model= joblib.load('model.pkl') 
button=st.button('Check')
if(button):
    preds=pd.DataFrame({'FFMC':ffmc,"DMC":dmc,"DC":dc,"ISI":isi,'Temp':temp,'RH':rh,'wind':wind,'rain':rain},index=[0])
    area= model.predict(preds)
    if(area>0): 
        st.markdown("<div class='text blue'><h2>The Forest is in Danger!!! <a href='https://shivanshu-sahoo.github.io/'>See Here</a> what you can do!</h2></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='text blue'><h2>The Forest is  <a href='https://shivanshu-sahoo.github.io/'>Safe!!!</a></h2></div>", unsafe_allow_html=True)
    #js = "window.open('https://shivanshu-sahoo.github.io/#about')"  # New tab or window
    #js = "window.location.href = 'https://shivanshu-sahoo.github.io/#about'"  # Current tab
    #html = '<img src onerror="{}">'.format(js)
    #div = Div(text=html)
    #st.bokeh_chart(div)