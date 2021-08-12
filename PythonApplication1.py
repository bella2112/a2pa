
#from typing import Callable
#from altair.vegalite.v4.schema.core import Data
#import numpy as np
import altair as alt
#from streamlit import caching
import streamlit as st
import pandas as pd
#import subprocess
from glob import glob
import configparser
import plotly.express as px
#import matplotlib.pyplot as plt
import os

user_name = os.environ.get('USERNAME')

#st.image("intel_logo.png", width=700)
#st.text("")
#st.text("")

st.subheader("Please fill in the FACR information")
st.text("")
@st.cache(allow_output_mutation=True)
def get_data():
    return []

test_step = st.text_input ("Test Step", "")
opn = st.text_input ("OPN", "")
facr_no = st.text_input ("FACR ID", "")
altera_lot_number = st.text_input ("Lot Number (Altera/PSG)", "")
lotop_vendor_lot = st.text_input ("Lot Number (Intel/VPO)", "")
range = st.text_input ("Number of adjacent lot", "")
wafer = st.text_input("Wafer Number", "")
x_axis = st.text_input ("x axis", "")
y_axis = st.text_input ("y axis", "")

if st.button("Submit"):
    get_data().append({"test_step": test_step, "opn": opn, "facr_no": facr_no,"altera_lot_number": altera_lot_number, "lotop_vendor_lot": lotop_vendor_lot, "range": range, "wafer": wafer, "x_axis": x_axis, "y_axis": y_axis})

st.write(pd.DataFrame(get_data()))
pd.DataFrame(get_data()).to_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/InputFile.csv", index=False)
'''
if st.button("Refresh"):
    caching.clear_cache()

if st.button("Run SQL"):
    subprocess.call(["C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/run.bat"])

st.title('Outlier Screening (Unit Level)')
if st.button("Plot"):

    #pat_query = "C:/Users/alianabi/OneDrive - Intel Corporation/Desktop/DEBUG/query"

    df = pd.read_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/UnitsDB.csv")
    df2 = pd.read_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/InputFile.csv")
    #st.write(df)

    df_ff = df[(df['final_test_flag'] > 0) & (df['soft_bin_name'] == 'PASSING') | (df['soft_bin_name'] == 'Passing')]
    df_ff_pass = df_ff.to_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/Passing_Unit.csv", index = False)
    df_ff_pass = pd.read_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/Passing_Unit.csv")
    df_ff_pass = df_ff_pass.astype({"wafer_number": int, "die_x_pos": int, "die_y_pos": int})
    df_ff_pass["w_x_y"] = df_ff_pass['wafer_number'].astype(str) + '_' + df_ff_pass['die_x_pos'].astype(str) + '_' + df_ff_pass['die_y_pos'].astype(str)
    df_ff_pass.to_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/Passing_Unit_Concat.csv", index = False)
    st.write(df_ff_pass)

    df2 = df2.astype({"wafer": int, "x_axis": int, "y_axis": int})
    df2["w_x_y"] = df2['wafer'].astype(str) + '_' + df2['x_axis'].astype(str) + '_' + df2['y_axis'].astype(str)
    df2.to_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/InputFile.csv", index = False)
    st.write(df2)
    #device = df2.iloc[0]['device']
    opn = df2.iloc[0]['opn']
    altera_lot = df2.iloc[0]['altera_lot_number']
    row = df2.iloc[0]['range']
    facr = df2.iloc[0]['facr_no']

    input_config = glob ("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/FT_PAT.ini")[0]
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(input_config)
    col_param1 = dict(config.items(opn))

    #df_param = df_ff_pass.loc[: , "altera_lot_name"]
    #df_inputfile = df2.loc[: , "altera_lot_number"]

    df_param = df_ff_pass.loc[: , "w_x_y"]
    df_inputfile = df2.loc[: , "w_x_y"]

    df3 = pd.DataFrame(df_ff_pass,columns=['w_x_y'])
    df3.loc[df3['w_x_y'] == df_inputfile[0], 'label'] = 'FACR'  
    df3.loc[df3['w_x_y'] != df_inputfile[0], 'label'] = 'REF'  
    df_label = pd.DataFrame(df3,columns=['label'])
    frames = [df_ff_pass, df_label]
    df_result = pd.concat(frames, axis = 1)
    df_result.to_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/unitlabel.csv", index = False)

    frame_prod = pd.DataFrame.from_dict(col_param1, orient='index').reset_index().rename(columns = {0: "current_limit", "index":"parameter"})
    frame_prod.to_csv ("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/currentprodlimit.csv", index=False)

    parameters = pd.read_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/currentprodlimit.csv")
    distribution = pd.read_csv("C:/Users/" + user_name + "/OneDrive - Intel Corporation/Desktop/DEBUG/query/unitlabel.csv")

    #param = st.selectbox('Select Paramater to Display', parameters['parameter'])

    def plot_Distribution(parameter):
    
        if parameter == "ioleakagel__min" or parameter  == 'IOLEAKAGEL__MIN':
            u0 = parameters[parameters["parameter"] == parameter].loc[:, ["current_limit"]].squeeze()
        else : 
            u0 = parameters[parameters["parameter"] == parameter].loc[:, ["current_limit"]].squeeze()
        
        fig = px.histogram(distribution, x=parameter, color = 'label', color_discrete_map = {'FACR' : 'red', 'REF' : 'grey'}, marginal = "box", hover_data = distribution.columns)
        fig.update_yaxes(visible=False)
        fig.update_xaxes(visible=False)
        fig.update_layout(title=parameter, title_x = 0.5)
        fig.update_layout(barmode = 'stack')
        #fig.add_vline(x=u0, line_width=1, line_dash="dash", line_color="grey", annotation_text = 'Current Limit')
    
        st.plotly_chart(fig)

        #c = alt.Chart(distribution).mark_bar().encode(alt.X(parameter, bin = True))
        #st.write(c)

    for unit in parameters["parameter"].tolist() :
         plot_Distribution(unit)
'''
