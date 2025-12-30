

#imports 
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly_express as px
import io
import msoffcrypto
import duckdb as db


#Main Code/Scroll down to see start logic
def main():
    #file reading logic
    @st.cache_resource
    def read_file(file):
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
    #Checking Logic 
    def check(lit,index):
            lo = 0
            if all(lit) and st.session_state.widgets[index] != lit:
                st.session_state.widgets[index] = lit
                return True
            else:
                return False
    #updating values/rerunning
    def update(d):
        st.session_state.show = d
        st.rerun()
    def sidebar(df):
        #SideBar Full of customiziation

        with st.sidebar:

            #Column Modification
            #Will have Random Variable names for expanders

            #Sidebar Title
            st.title("Customize Your Data")
            #Data Column names and column/row info
            column_names = df.columns.tolist()


            #picking Value to Show
            a = st.expander("Pick Values To Show")
            
            with a:
                x = row
                st.title('You can only pick one to reset (1 one should be 0, and the second one should be 0,800)')
                Top_x = st.slider('Pick x Amount of Values To Use', 0, row)
                st.divider()
                x_x = st.slider('Pick X through X Values To Use',0,row,(0,row))
                st.divider()
                #Logic
                if Top_x > 0 and x_x == (0,row) and Top_x != st.session_state.widgets[0]:
                    st.session_state.widgets[0] = Top_x
                    df = df.head(Top_x)
                    update(df)

                    
                elif Top_x == 0 and x_x != (0,row) and x_x != st.session_state.widgets[1]:
                    st.session_state.widgets[1] = x_x
                    x = row
                    a,b = x_x[0], x_x[1]
                    df = df[a:b]
                    update(df)

            #Modifiying columns
            b = st.expander('Column Modification')
            with b:
                #Renaming Column
                c = st.expander('Rename Column')
                with c:
                    column = st.selectbox('Pick Your Column To Rename', column_names)
                    new_name = st.text_area('New Name For Column')

                    if check([column,new_name], 1):
                        df = df.rename(columns={column: new_name})
                        update(df)

                #New Column With Function
                New_Col = st.expander('Make new Column With Function')
                column_names = df.columns.tolist()
                with New_Col:
                    col1,col2,col3 = st.columns(3)
                    p = col1.selectbox('X Column', column_names)
                    times = col2.selectbox('X', ['x','+', '-', '/'])
                    p2 = col3.selectbox('X Column', column_names, key='s')
                    nam = st.text_input('Name Of New Column')
                    if check([p,times,p2,nam], 2):
                        match times:
                            case 'x':
                                df[nam] = df[p] * df[p2]
                            case '+':
                                df[nam] = df[p] + df[p2]
                            case '-':
                                df[nam] = df[p] - df[p2]
                            case '/':
                                df[nam] = df[p] / df[p2]
                        update(df)

                #Dropping columns
                op = st.expander("Drop Columns")
                with op:
                    column_names = df.columns.tolist()
                    Drop_Col = st.multiselect("Columns To Drop", column_names)

                    #checking if value changed
                    if check([Drop_Col], 3):
                        st.session_state.widgets[4] = Drop_Col
                        df = df.drop(columns=Drop_Col)
                        update(df)
                
                with st.expander('Add Suffix/Prefix'):
                    #adding suffix/prefix
                    column_names = df.columns.tolist()
                    columnss = st.multiselect('Pick Columns', column_names)
                    Suffix = st.text_input('Suffix')
                    Prefix = st.text_input('Prefix')
                    col4,col5 = st.columns(2)
                    remove = col4.button('Remove')
                    add = col5.button('Add')
                    
                    if add and remove:
                        st.toast('Please Pick One checkbox At A Time')
                    elif add or remove:
                        if Suffix or Prefix and columnss and [Suffix,Prefix,columnss,add,remove] != st.session_state.widgets[9]:
                            st.session_state.widgets[9] = [Suffix,Prefix,columnss,add,remove]
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
                            update(df)


            with st.expander('Values Modification'):
                #To modify missing values like replacing empty values

                with st.expander("Replace Empty Values In Columns"):
                    column_names = df.columns.tolist()
                    value = st.text_input('Value')
                    multi = st.multiselect('Columns', column_names)

                    if check([value,multi], 4):
                        for i in multi:
                            df[i].replace('', np.nan, inplace=True)
                            df[i].fillna(value, inplace=True)
                            update(df)
                
                with st.expander('Remove columns/rows with missing values'):
                    c1 = st.checkbox('Remove Rows With Missing Value')
                    c2 = st.checkbox('Remove Columns With Missing Value')
                    
                    if c2 and c1:
                        st.toast('You can only have one checkbox picked at once')
                    elif c1 or c2:
                        if [c1,c2] != st.session_state.widgets[7]:
                            st.session_state.widgets[7] = [c1,c2]
                            if c1:
                                df = df.dropna()
                                update(df)

                            if c2:
                                df = df.dropna(axis=1)
                                update(df)
                with st.expander('Replace string in column with x'):
                    #replacing string with another string 

                    column_names = df.columns.tolist()
                    select = st.multiselect('Pick column/columns', column_names)
                    replace = st.text_input('String To replace (Case Sensitive)')
                    wits = st.text_input('Replace the string with')

                    if check([select,replace,wits], 4):
                        for i in select:
                            df[i] = df[i].apply(lambda x: str(x))
                            df[i] = df[i].apply(lambda x: x.replace(replace, wits))
                        update(df)
            with st.expander('Sorting'):
                #sorting
                column_names = df.columns.tolist()
                lis = st.selectbox('Pick Column To Sort With', column_names)
                c3 = st.checkbox('Ascending')
                c4 = st.checkbox('Descending')
                if c3 and c4:
                    st.toast('Only pick one checkbox at once')
                elif (lis,c3,c4) != st.session_state.widgets[8]:
                    st.session_state.widgets[8] = (lis,c3,c4)
                    if c3:
                        df = df.sort_values(by=lis)
                        update(df)
                    if c4:
                        df = df.sort_values(by=lis, ascending=False)
                        update(df)




            with st.expander('Encryption For Sensetive Data'):
                #shuffling data
                with st.expander('Shuffle Data'):
                    pop = st.toggle('Shuffle Data')
                    if check([pop], 5):
                        st.session_state.widgets[13] = pop
                        for i in df.columns.tolist():
                            df[i] = df[i].sample(frac=1, random_state=5).reset_index(drop=True)
                        update(df)
            with st.expander('Extras'):
                #some extra functions
                with st.expander('Filter (Only With Numbers)'):
                    #filtering values
                    column_names = df.columns.tolist()
                    li = st.selectbox('Select Column To Filter With', column_names)
                    col6,col7 = st.columns(2)
                    j = col6.selectbox('Pick operartion', options=['>', '<', '=', 'not = to'])
                    k = col7.text_input('Write the comparison')
                    if check([li,j,k], 6):
                        match j:
                            case '>':
                                df = con.sql(f'''Select * From df WHERE {li}>{int(k)}''')           
                            case '<':
                                df = con.sql(f'''Select * From df WHERE {li}<{int(k)}''') 
                            case '=':
                                try:
                                    df = con.sql(f'''Select * From df WHERE {li}={int(k)}''') 
                                except:
                                    df = con.sql(f'''Select * From df WHERE {li}={str(k)}''') 
                            case 'not = to':
                                try:
                                    df = con.sql(f'''Select * From df WHERE {li}!={int(k)}''') 
                                except:
                                    df = con.sql(f'''Select * From df WHERE {li}!={str(k)}''') 
                            
                        update(df)
                with st.expander('Format Columns'):
                    #formating columns
                    column_names = df.columns.tolist()
                    sanji= st.selectbox('Pick what to do', ['Capitalize', 'Phone Format', 'Remove Extra Spaces'])
                    luffy = st.multiselect('Pick columns to format', column_names)
                    if check([luffy,sanji], 7):
                        for i in luffy:
                            match sanji:
                                case 'Capitalize':
                                    df[i] = df[i].str.lower().str.capitalize()
                                case 'Phone Format':
                                    df[i] = df[i].astype(str)
                                    df[i] = df[i].str.replace(r'\D', '', regex=True)
                                    df[i] = df[i].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
                                    df[i] = df[i].str.replace('nan--','')
                                    df[i] = df[i].str.replace('Na--','')
                                    df[i] = df[i].str.replace('NaN--','')
                                case 'Remove Extra Spaces':
                                    df[i].apply(lambda x: str(x))
                                    df[i] = df[i].str.strip()
                        update(df)
                col0,col11 = st.columns(2)
                summarize = col1.checkbox('')
                checks = col0.checkbox('Drop Duplicate Rows')
                if check([checks], 8):
                    #dropping duplicates
                    df = df.drop_duplicates()
                    update(df)



            #Making the Plot 
            with st.expander('Plot Your Data'):
                
                def plot(a,b,c):
                    with tab3:
                        
                        if plot_type == 'Map Plot':
                            df[a] = pd.to_numeric(df[a], errors='coerce')
                            df[b] = pd.to_numeric(df[b], errors='coerce')
                            df_map = df.dropna(subset=[a, b]).copy()
                            
                        if color != 'None':
                            match plot_type:
                                case 'line plot (2d)':
                                    fig = px.line(df,x=a,y=b,color = c)
                                case 'scatter plot (2d)':
                                    fig = px.scatter(df,x=a,y=b,color = c)
                                case 'bar chart (2d)':
                                    fig = px.bar(df,x=a,y=b,color = c)
                                case 'Horizontal Bar Chart (2d)':
                                    fig = px.bar(df,x=a,y=b,orientation='h',color = c)
                                case'Stacked Area Plot (2d)':
                                    fig = px.area(df,x=a,y=b,color = c)
                                case 'Histogram Plot (1d)':
                                    fig = px.histogram(df, x=a,color=c)
                                case 'Box Plot (1d)':
                                    fig = px.box(df, x=a,color=c)
                                case 'Map Plot':
                                    fig = px.scatter_map(df_map,lat=df_map[a],lon=df_map[b],zoom=1,color=c)

                        else:
                            match plot_type:
                                case 'line plot (2d)':
                                    fig = px.line(df,x=a,y=b)
                                case 'scatter plot (2d)':
                                    fig = px.scatter(df,x=a,y=b)
                                case 'bar chart (2d)':
                                    fig = px.bar(df,x=a,y=b)
                                case 'Horizantal Bar Chart (2d)':
                                    fig = px.bar(df,x=a,y=b,orientation='h')
                                case'Stacked Area Plot (2d)':
                                    fig = px.area(df,x=a,y=b)
                                case 'Histogram Plot (1d)':
                                    fig = px.histogram(df, x=a)
                                case 'Box Plot (1d)':
                                    fig = px.box(df, x=a)
                                case 'Map Plot':
                                    fig = px.scatter_map(df_map,lat=df_map[a],lon=df_map[b],zoom=1)
                        fig.update_layout(
                        title=f"{plot_type}",
                        xaxis_title=a,
                        yaxis_title=b,
                        legend_title= plot_type
                        )
                        st.plotly_chart(fig)
                        
                plot_type = st.selectbox('Selct The Type Of Chart You Want', ['line plot (2d)', 'scatter plot (2d)', 'bar chart (2d)', 'Horizantal Bar Chart (2d)', 'Stacked Area Plot (2d)', 'Histogram Plot (1d)', 'Box Plot (1d)', 'Map Plot'])
                column_names = df.columns.tolist()
                color = st.selectbox('Selct The Axis To be The Label/color', ['None'] + column_names)
                with st.expander('Plot Values'):
                    column_names = df.columns.tolist()
                    st.markdown('Pick None In Y For 1d Plots')
                    ap = st.selectbox('Pick x', column_names)
                    bp = st.selectbox('Pick y', column_names + ['None'])
                    if st.button('Submit '):
                        if plot_type == 'Map Plot':
                            st.toast('Please Use Map Section To plot on Map')
                        elif plot_type in ['Histogram Plot (1d)', 'Box Plot (1d)'] and bp != 'None':
                            st.toast('Please Pick None For Y if You are Doing a 1d plot')
                        elif plot_type not in ['Histogram Plot (1d)', 'Box Plot (1d)'] and bp == 'None':
                            st.toast('Please Pick X and Y for 2d Plot')
                        else:
                            plot(ap,bp,color)
                with st.expander('Plot On Map'):
                    ap = st.selectbox('Pick Latitude', column_names)
                    bp = st.selectbox('Pick Longtitude', column_names)
                    if st.button('Submit'):
                        if plot_type == 'Map Plot':
                            if not bp or not ap:
                                st.toast('Please Pick Latitude AND Longtitude')
                            else:
                                plot(ap,bp,color)
                        else:
                            st.toast('Please Pick Map Plot To Plot On Map')
                    
            st.link_button("Learn How To Use Amai", 'https://www.youtube.com/watch?v=9zrbpNRHqqA')  





    #Reading Correct Format Of File, and initialization
    df = read_file(file)
    con = db.connect()
    con.register("df", df)
    row,col = df.shape
    tab1,tab2,tab3    = st.tabs(['Data', 'Summurized Data','Plotted Data'])

    #initillazing session state
    if 'show' not in st.session_state:
        st.session_state.show = df
    if 'og' not in st.session_state:
        st.session_state.og = df
    if 'commit' not in st.session_state:
        st.session_state.commit = df
    if 'widgets' not in st.session_state:
        st.session_state.widgets = [None] * 15
    #buttons
    cola,colb,colc,cold = st.columns([1,2,1,2])
    if cola.button('Commit'):
        column_names = df.columns.tolist()
        st.session_state.commit = st.session_state.show
        df = st.session_state.commit
        st.rerun()
    
    if colb.button('Undo To last Commit'):
        st.session_state.show = st.session_state.commit
        df = st.session_state.commit
        st.rerun()

    if colc.button('Reset all'):
        st.session_state.commit = st.session_state.og
        st.session_state.show = st.session_state.og
        df = st.session_state.og
        st.rerun()
    csv = df.to_csv(index=False).encode('utf-8')
    if cold.download_button(label="Download Cleaned CSV",data=csv,file_name='cleaned_data.csv',mime='text/csv'):
         st.balloons()
    if st.button('Clear Cache(RECOMENDED TO USE RIGHT BEFORE EXITING)'):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    df = tab1.data_editor(st.session_state.show, num_rows="dynamic")
    tab2.data_editor(df.describe(include='all'))
    #Running everything
    sidebar(df)

#Title
st.markdown(
     """
     <h1 style='text-align: center;'>Amai 👌👌</h1>
     """,
     unsafe_allow_html=True
 )

usage,about = st.tabs(['Use the app','About Amai'])

with about:
    st.markdown(
        """
        ## About Amai
        Amai is a data cleaning web application built using Streamlit and Pandas. It allows users to upload CSV or Excel files, perform various data cleaning operations, and visualize the cleaned data through different types of plots.

        ### Features:
        - Upload CSV or Excel files (with optional password protection)
        - Rename columns
        - Create new columns using mathematical operations
        - Drop unnecessary columns
        - Handle missing values (replace, remove)
        - Sort data
        - Shuffle data for anonymization
        - Filter data based on conditions
        - Format columns (capitalize, phone format, remove extra spaces)
        - Plot data using various chart types (line, scatter, bar, histogram, box plot, map)
        - Download cleaned data as CSV

        Amai aims to simplify the data cleaning process and make it accessible to users without extensive programming knowledge.
        """
    )
    st.link_button("Learn How To Use Amai", 'https://www.youtube.com/watch?v=9zrbpNRHqqA')  

with usage:
    #Start Logic
    file = st.file_uploader("Please Upload A Csv/Xlsx File", type=['xlsx', 'csv'])
    password = st.text_input('Please Write Your Password If Your File Has A password', type='password', key='password_input')
    if file:
        try:
            main()
        except Exception as e:
            st.warning(f'Something Went Wrong! Please Try Again {e}')
    else:
        st.warning('Please Upload A csv/xlsx File Under 200 Mb')
        st.stop()
    




