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
    df = pd.concat([part1, part2, part3, part4, part5, part6, part7], ignore_index=True)
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

def outlier_thresholds(dataframe, col_name, q1=0.05, q3=0.95):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

def threshold(dataframe, num_cols):
    for col in num_cols:
        replace_with_thresholds(dataframe, col)