#This is a python file for all of the data cleaning functions
#imports
import pandas as pd
import io
import msoffcrypto
import numpy as np
import streamlit as st
import plotly_express as px


#Reads File
def read_file(file,password):
    if password and file:
            office_file = msoffcrypto.OfficeFile(file)
            office_file.load_key(password=password)
            decrypted_data = io.BytesIO()
            office_file.decrypt(decrypted_data)
            decrypted_data.seek(0) # Reset stream position to the beginning
            return pd.read_excel(decrypted_data)
    elif '.xlsx' in file.name:
        return pd.read_excel(file)
    else:
        return pd.read_csv(file)

#makes new column
def make_column(df,operation,new_name,column1,column2):
    try:
        match operation:
            case 'x':
                df[new_name] = df[column1] * df[column2]
            case '+':
                df[new_name] = df[column1] + df[column2]
            case '-':
                df[new_name] = df[column1] - df[column2]
            case '/':
                df[new_name] = df[column1] / df[column2]
        return df
    except Exception as e:
        return False

#add or remove a prefix/suffix
def suffix_prefix(Suffix, Prefix, columnss,df,add,remove):   
    if Suffix or Prefix and columnss:
        if add:
            for i in columnss:
                    if Prefix:
                        df[i] = Prefix + df[i].astype(str) 
                    if Suffix:
                        df[i] = df[i].astype(str) + Suffix
        if remove:
            for i in columnss:
                if Prefix:
                    df[i] = df[i].astype(str).str.removeprefix(Prefix)
                if Suffix:
                    df[i] = df[i].astype(str).str.removesuffix(Suffix)
    return df

#Replace Empty Values
def replace_empty_values(df, Columns_, value):
    for i in Columns_:
        df[i].replace('', np.nan, inplace=True)
        df[i].fillna(value, inplace=True)
    return df

#Replace str with different str
def replace_str(df, replace, replaced_with, selected_columns3):
    for i in selected_columns3:
        df[i] = df[i].apply(lambda x: str(x))
        df[i] = df[i].apply(lambda x: x.replace(replace, replaced_with))
    return df

#Filter
def filter(df, comparison,operation2,selected_columns4):
    try:
        val = float(comparison)
        numeric = True
    except ValueError:
        val = comparison  
        numeric = False

    if numeric:
        if operation2 == '>':
            df = df[pd.to_numeric(df[selected_columns4], errors='coerce') > val]
        elif operation2 == '<':
            df = df[pd.to_numeric(df[selected_columns4], errors='coerce') < val]
        elif operation2 == '=':
            df = df[pd.to_numeric(df[selected_columns4], errors='coerce') == val]
        elif operation2 == 'not = to':
            df = df[pd.to_numeric(df[selected_columns4], errors='coerce') != val]
    else:
        if operation2 == '=':
            df = df[df[selected_columns4] == val]
        elif operation2 == 'not = to':
            df = df[df[selected_columns4] != val]
        else:
            st.toast("Cannot use '<' or '>' with text")
    return df

#Formatting
def Format(df, format_to_do,Selected_Columns5):
    for i in Selected_Columns5:
        df[i] = df[i].astype(str)
        
        match format_to_do:
            case 'Capitalize':
                df[i] = df[i].str.lower().str.capitalize()
            case 'Phone Format':
                df[i] = df[i].astype(str)
                df[i] = df[i].str.replace(r'\D', '', regex=True)
                df[i] = df[i].apply(lambda x: f'{x[0:3]}-{x[3:6]}-{x[6:10]}' if len(x) >= 10 else x)
            case 'Remove Extra Spaces':
                df[i].apply(lambda x: str(x))
                df[i] = df[i].str.strip()
    return df

#Plotting
def plotting(val_x,val_y,color,plot_type,df):
    kwargs = { 'x': val_x, 'y': val_y}
    if color != 'None':
        kwargs['color'] = color

    match plot_type:
        case 'line plot (2d)':
            fig = px.line(df,**kwargs)
        case 'scatter plot (2d)':
            fig = px.scatter(df,**kwargs)
        case 'bar chart (2d)':
            fig = px.bar(df,**kwargs)
        case 'Horizantal Bar Chart (2d)':
            fig = px.bar(df,orientation='h',**kwargs)
        case'Stacked Area Plot (2d)':
            fig = px.area(df,**kwargs)
        case 'Histogram Plot (1d)':
            if color:
                fig = px.histogram(df, x=val_x, color=color)
            else:
                fig = px.histogram(df, x=val_x)
        case 'Box Plot (1d)':
            if color:
                fig = px.box(df, x=val_x, color=color)
        case 'Map Plot':
            df[val_x] = df[val_x].apply(lambda x: float(x))
            df[val_y] = df[val_y].apply(lambda x: float(x))
            if color:
                fig = px.scatter_map(df,lat=val_x,lon=val_y,zoom=1, color=color)
            else:
                fig = px.scatter_map(df,lat=val_x,lon=val_y,zoom=1)
    return fig
