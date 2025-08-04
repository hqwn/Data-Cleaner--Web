import random
import streamlit as st
import pandas as pd
import numpy as np

def kinda_main():
    #file reading logic
    @st.cache_data
    def read_file(file):
        if '.xlsx' in file.name:
            return pd.read_excel(file)
        else:
            return pd.read_csv(file)




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
                    st.session_state.show = df
                    st.rerun()

                    
                elif Top_x == 0 and x_x != (0,row) and x_x != st.session_state.widgets[1]:
                    st.session_state.widgets[1] = x_x
                    x = row
                    a,b = x_x[0], x_x[1]
                    df = df[a:b]
                    st.session_state.show = df
                    st.rerun()

            #Modifiying columns
            b = st.expander('Column Modification')
            with b:
                #Renaming Column
                c = st.expander('Rename Column')
                with c:
                    column = st.selectbox('Pick Your Column To Rename', column_names)
                    new_name = st.text_area('New Name For Column')

                    if column and new_name and column != st.session_state.widgets[2] and new_name != st.session_state.widgets[3]:
                        st.session_state.widgets[2] = column
                        st.session_state.widgets[3] = row
                        df = df.rename(columns={column: new_name})
                        st.session_state.show = df.copy()
                        st.rerun()

                #New Column With Function
                New_Col = st.expander('Make new Column With Function')
                column_names = df.columns.tolist()
                with New_Col:
                    col1,col2,col3 = st.columns(3)
                    p = col1.selectbox('X Column', column_names)
                    times = col2.selectbox('X', ['x','+', '-', '/'])
                    p2 = col3.selectbox('X Column', column_names, key='s')
                    nam = st.text_input('Name Of New Column')
                    if p and times and p2 and nam and [p,times,p2, nam] != st.session_state.widgets[5]:
                        st.session_state.widgets[5] = [p,times,p2,nam]
                        match times:
                            case 'x':
                                df[nam] = df[p] * df[p2]
                            case '+':
                                df[nam] = df[p] + df[p2]
                            case '-':
                                df[nam] = df[p] - df[p2]
                            case '/':
                                df[nam] = df[p] / df[p2]
                        st.session_state.show = df.copy()
                        st.rerun()

                #Dropping columns
                op = st.expander("Drop Columns")
                with op:
                    column_names = df.columns.tolist()
                    Drop_Col = st.multiselect("Columns To Drop", column_names)

                    if Drop_Col and Drop_Col != st.session_state.widgets[4]:
                        st.session_state.widgets[4] = Drop_Col
                        df = df.drop(columns=Drop_Col)
                        st.session_state.show = df
                        st.rerun()
                
                with st.expander('Add Suffix/Prefix'):
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
                            st.session_state.show = df.copy()
                            st.rerun()


                    

            with st.expander('Values Modification'):
                #To modify missing values like replacing empty values

                with st.expander("Replace Empty Values In Columns"):
                    column_names = df.columns.tolist()
                    value = st.text_input('Value')
                    multi = st.multiselect('Columns', column_names)

                    if value and multi and [value, multi] != st.session_state.widgets[6]:
                        st.session_state.widgets[6] = [value, multi]
                        for i in multi:
                            df[i].replace('', np.nan, inplace=True)
                            df[i].fillna(value, inplace=True)
                            st.session_state.show = df
                            st.rerun()
                
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
                                st.session_state.show = df.copy()
                                st.rerun()

                            if c2:
                                df = df.dropna(axis=1)
                                st.session_state.show = df.copy()
                                st.rerun()
                with st.expander('Replace string in column with x'):
                    column_names = df.columns.tolist()
                    select = st.multiselect('Pick column/columns', column_names)
                    replace = st.text_input('String To replace (Case Sensitive)')
                    wits = st.text_input('Replace the string with')

                    if select and replace and wits and [select,replace,wits] != st.session_state.widgets[14]:
                        st.session_state.widgets[14] = [select,replace,wits]
                        for i in select:
                            df[i] = df[i].apply(lambda x: str(x))
                            df[i] = df[i].apply(lambda x: x.replace(replace, wits))
                        st.session_state.show = df
                        st.rerun()
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
                        st.session_state.show = df.copy()
                        st.rerun()
                    if c4:
                        df = df.sort_values(by=lis, ascending=False)
                        st.session_state.show = df.copy()
                        st.rerun()




            with st.expander('Encryption For Sensetive Data'):
                with st.expander('Shuffle Data'):
                    pop = st.toggle('Shuffle Data')
                    if pop and pop != st.session_state.widgets[13]:
                        st.session_state.widgets[13] = pop
                        for i in df.columns.tolist():
                            df[i] = df[i].sample(frac=1, random_state=5).reset_index(drop=True)
                        st.session_state.show = df
                        st.rerun()
            with st.expander('Extras'):
                with st.expander('Filter (Only With Numbers)'):
                    column_names = df.columns.tolist()
                    li = st.selectbox('Select Column To Filter With', column_names)
                    col6,col7 = st.columns(2)
                    j = col6.selectbox('Pick operartion', options=['>', '<', '=', 'not = to'])
                    k = col7.text_input('Write the comparison')
                    if li and j and k and [li,j,k] != st.session_state.widgets[10]:
                        st.session_state.widgets[10] = [li,j,k]
                        match j:
                            case '>':
                                k = int(k)
                                df = df[df[li] > k]
                            case '<':
                                k = int(k)
                                df = df[df[li] < k]
                            case '=':
                                try:
                                    k = int(k)
                                    df = df[df[li] == k]
                                except:
                                    k = str(k)
                                    df = df[df[li] == k]
                            case 'not = to':
                                try:
                                    k = int(k)
                                    df = df[df[li] != k]
                                except:
                                    k = str(k)
                                    df = df[df[li] != k]
                            
                        st.session_state.show = df.copy()
                        st.rerun()
                with st.expander('Format Columns'):
                    column_names = df.columns.tolist()
                    sanji= st.selectbox('Pick what to do', ['Capitalize', 'Phone Format', 'Remove Extra Spaces'])
                    luffy = st.multiselect('Pick columns to format', column_names)
                    if luffy and sanji and [luffy, sanji] != st.session_state.widgets[12]:
                        st.session_state.widgets[12] = [luffy,sanji]
                        print(sanji)
                        for i in luffy:
                            match sanji:
                                case 'Capitalize':
                                    df[i] = df[i].str.lower().str.capitalize()
                                case 'Phone Format':
                                    df[i] = df[i].apply(lambda x: str(x))
                                    df[i] = df[i].str.replace('[a-zA-Z0-9]', '')
                                    df[i] = df[i].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
                                    df[i] = df[i].str.replace('nan--','')
                                    df[i] = df[i].str.replace('Na--','')
                                    df[i] = df[i].str.replace('NaN--','')
                                case 'Remove Extra Spaces':
                                    df[i].apply(lambda x: str(x))
                                    df[i] = df[i].str.strip()
                        st.session_state.show = df
                        st.rerun()
                col0,col11 = st.columns(2)
                summarize = col1.checkbox('')
                check = col0.checkbox('Drop Duplicate Rows')
                if check and st.session_state.widgets[11] != check:
                    st.session_state.widgets[11] = check
                    df = df.drop_duplicates()
                    st.session_state.show = df
                    st.rerun()
            st.link_button("Learn How To Use Amai", 'https://www.youtube.com/watch?v=9zrbpNRHqqA')
                



    #Reading Correct Format Of File, and initialization
    df = read_file(file)
    row,col = df.shape
    tab1,tab2 = st.tabs(['Data', 'Summurized Data'])
    #initillazing session state
    if 'show' not in st.session_state:
        st.session_state.show = df
    if 'og' not in st.session_state:
        st.session_state.og = df
    if 'commit' not in st.session_state:
        st.session_state.commit = df
    if 'widgets' not in st.session_state:
        st.session_state.widgets = [0, [0, row], '', '', [],[],[],[],[],[],[],'', '', '', '']

    #buttons
    cola,colb,colc,cold = st.columns([1,2,1,2])
    if cola.button('Commit'):
        column_names = df.columns.tolist()
        st.session_state.commit = st.session_state.show.copy()
        df = st.session_state.commit.copy()
        st.rerun()
    
    if colb.button('Undo To last Commit'):
        st.session_state.show = st.session_state.commit.copy()
        df = st.session_state.commit.copy()
        st.rerun()

    if colc.button('Reset all'):
        st.session_state.commit = st.session_state.og.copy()
        st.session_state.show = st.session_state.og.copy()
        df = st.session_state.og.copy()
        st.rerun()
    csv = df.to_csv(index=False).encode('utf-8')
    if cold.download_button(label="Download Cleaned CSV",data=csv,file_name='cleaned_data.csv',mime='text/csv'):
         st.balloons()
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

#File
file = st.file_uploader("Please Upload A Csv/Xlsx File", type=['xlsx', 'csv'])

#Start Logic
if file:
    kinda_main()
else:
    st.warning('Please Upload A File Under 200 Mb')


