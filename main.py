#Imports needed
import streamlit as st
import pandas as pd






#Main Code
def main(df, DP_Rows,n_df,Preview,Suffix,Prefix):
    #drops duplicates
    df = df.drop_duplicates()
    
    #drops columns
    if DP_Rows:
        df = df.drop(columns=DP_Rows)
    
    #removes empty rows
    if Empty_Remove:
        df = df.dropna()
        
    #formats DATE
    if Format_date:
        for col in Format_date:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    #replaces empty values
    if Replace_Empty:
        df = df.fillna(Replace_Empty)

    #New name for x column
    if Col_name and New_Name:
        df = df.rename(columns={Col_name: New_Name})

    #Capitalizes String
    if capital:
        for i in capital:
            df[i] = df[i].str.lower().str.capitalize()
    
    #Resets DataFrame To original
    if Reset:
        df = st.session_state.og
        st.session_state.df = df
    
    #Suffix/Prefix logic
    if Suffix and Prefix and n_df or Preview:
        try:
            if Suffix == 'Add':
                for i in Prefix:
                    if Preview:
                        df[i] = Preview + df[i].astype(str) 
                    if n_df:
                        df[i] = df[i].astype(str) + n_df
            elif Suffix == 'Remove':
                for i in Prefix:
                    if Preview:
                        df[i] = df[i].astype(str).str.removeprefix(Preview)
                    if n_df:
                        df[i] = df[i].astype(str).str.removeprefix(n_df)
        except:
            st.warning('If removing, make sure prefix/suffix exist, otherwise there has been a problem, try again')
    
    #download for new_df and etc..
    st.session_state.df=df
    Preview = st.write('preview data')
    n_df =st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    if st.download_button(label="Download Cleaned CSV",data=csv,file_name='cleaned_data.csv',mime='text/csv'):
        st.balloons()

#Title
st.markdown(
    """
    <h1 style='text-align: center;'>Amai 👌👌</h1>
    """,
    unsafe_allow_html=True
)


#Extra Space
st.write(" ")
st.write(" ")
file = st.file_uploader("Upload A Csv/Xlsx File 😁", type=['xlsx', 'csv'])

#Start Logic
if file:
    try:
        if '.xlsx' in file.name:
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)


        if "df" not in st.session_state:
            st.session_state.df = df
        if 'og' not in st.session_state:
            st.session_state.og = df

        df = st.session_state.df
        og = st.session_state.og
        expand = st.expander("Edit Data (Do It)", icon=":material/info:")
        with expand:
            #All customization widgets
            col1, col2, col3 = st.columns([3,2,2])
            column_names = df.columns.tolist()
            og = og.columns.to_list()
            Drop_Col = col1.multiselect("Drop Columns", column_names)
            Empty_Remove = col3.checkbox("Remove Rows with missing value")
            Format_date = col2.multiselect("Format Date of x column", column_names)
            Replace_Empty = col1.text_input('Fill Missing values with .....')
            column_rename = col2.expander('Rename Column')
            Col_name = column_rename.selectbox("Change Column x's name", column_names)
            New_Name = column_rename.text_input('With...')
            capital = col3.multiselect("Capitalize string of x columns", column_names)
            expan = st.expander('Add/Remove Suffix/Prefix')
            with expan:
                row1,row2=st.columns(2)
                Suf = row1.text_input('Enter Suffix')
                Pre = row2.text_input('Enter Prefix')
                re_ad = row1.pills('Action', ['Remove', 'Add'])
                col_select = row2.multiselect('Columns', column_names)
            Reset = st.button('Reset all')
        main(df, Drop_Col,Suf,Pre,re_ad,col_select)
    except:
        st.warning('Something went Wrong! Please Try Again')
else:
    #Gives warning if file Empty
    st.warning('upload a File')




