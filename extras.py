import pandas as pd
import streamlit as st
import base64

# READ DATA
def read_data():
    part1 = pd.read_csv("datas/part1.csv", index_col=[0])
    part2 = pd.read_csv("datas/part2.csv", index_col=[0])
    part3 = pd.read_csv("datas/part3.csv", index_col=[0])
    part4 = pd.read_csv("datas/part4.csv", index_col=[0])
    part5 = pd.read_csv("datas/part5.csv", index_col=[0])
    part6 = pd.read_csv("datas/part6.csv", index_col=[0])
    part7 = pd.read_csv("datas/part7.csv", index_col=[0])
    df = pd.concat([part6, part7], ignore_index=True)
    return df



# BACKGROUD
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

