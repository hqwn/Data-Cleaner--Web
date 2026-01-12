#imports 
import AI
import Clean_functions as cf
import streamlit as st
import plotly_express as px

#Main Code/Scroll down to see start logic
def main(file_widget):

    #Download dialog
    @st.dialog('Download Cleaned Data')
    def download_dialog():
        new_filename = st.text_input('Filename of your choice (without extension and press enter)', value='cleaned_data')
        with st.spinner('Preparing your download...'):
            csv = df.to_csv(index=False).encode('utf-8')
            if st.download_button(label="Download Cleaned CSV", data=csv, file_name=f'{new_filename}.csv', mime='text/csv'):
                st.balloons()

    #session state init
    if 'show' not in st.session_state or st.session_state.show is None:
        df_init = st.cache_data(show_spinner=False, func=cf.read_file)(file_widget,password)
        st.session_state.og = df_init.copy()      # For "Reset All"
        st.session_state.show = df_init.copy()    # Current working data
        st.session_state.commit = df_init.copy()  # For "Undo"
        st.session_state.widgets = [None] * 15

    #Tabs
    tab1,tab2,tab3,tab4 = st.tabs(['Data', 'Summurized Data','Plotted Data', 'Chat with Amai Ai(Beta)'])
    
    #Data frame
    DATA = tab1.data_editor(st.session_state.show, num_rows="dynamic", key="data_editor")
    st.session_state.show = DATA
    df = st.session_state.show
    row,col = df.shape
    
    #Tabs Init
    with tab2:
            
            summary_type = st.pills('Show correlation or Summary of data', ['Summary','Correlation'],default='Summary')
            tab2_data = st.empty()
            if summary_type == 'Summary':
                tab2_data.dataframe(df.describe(include='all'))
            elif summary_type == 'Correlation':
                corr_matrix = df.select_dtypes(include='int').corr()

                fig = px.imshow(
                    corr_matrix,
                    text_auto='.3f',
                    color_continuous_scale='greys',
                    height=500,
                    width=500
                )

                st.plotly_chart(fig)
            else:
                tab2_data.write('Pick an Option')
    with tab4:
        #title
        st.title('Chat with Amai Ai (Beta)')

        #explanation
        st.markdown('This is a beta feature that allows you to chat with an Groq Ai model or an Ollama Cloud model of your choice. This AI will reference the first 20 rows of your data and summary of your data')

        #Ai models up to use

        models = {
            'Groq GPT-OSS 120B (High Logic; Aka: Brain; Recommended)' : 'openai/gpt-oss-120b',
            'Groq QWEN 3 32B (Balance of Speed and Logic; Aka: Analyst)': 'qwen/qwen3-32b',
            'Groq KIMI-K2 INSTRUCT (Advanced Reasoning; Mainly for following instructions rather than data analysis)': 'moonshotai/kimi-k2-instruct-0905',
            'Ollama GPT-OSS 20b (Fast, logical, and follows instructions carefully; Aka: Specialist)': 'gpt-oss:20b-cloud'
        }
        with st.expander('AI settings/tweaks'):
            model_picked = st.selectbox(label='Pick Your Model', options=models.keys())
            temperature = st.slider('Creativity vs Factual; 0.1(Most Factual) 0.9(Most creative); 0.5 recommended', min_value=.1, max_value=.9,step=.1,value=.5)

        
        if 'chat_history' not in st.session_state or st.session_state.chat_history is None:
            message = '''"Hello! You are Amai AI, a world-class data analyst. Your goal is to welcome the user and provide a high-level executive summary of the data provided.
                    Instructions: Welcome: Start with a warm, professional greeting.

                    The 'Big Picture': Don't just list columns. Tell me what this dataset is (e.g., 'This looks like a Human Resources database covering 20 employees').

                    Statistical Highlights: Mention at least two interesting stats (e.g., the average of a numeric column, the most common category, or a weird outlier).

                    Data Health: Briefly mention if the data looks clean or if it needs work (e.g., 'I noticed some lowercase names that need capitalizing').'''
            
            response = ''
            for i in AI.AI_Response(message, df, [model_picked[0], models[model_picked]],temperature):
                if isinstance(i,str):
                    response += i
                elif isinstance(i, dict):
                    st.toast(f"📊 Tokens: {i['total']} (In: {i['prompt']} | Out: {i['completion']})")

            st.session_state.chat_history = [{"role": "ai", "content": response}]
        
        chat_placeholder = st.container(height=500)
        
        with chat_placeholder:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    
        if prompt := st.chat_input("Ask me anything about your data!"):
            # Write and Add user message to chat history
            with chat_placeholder:
                with st.chat_message('human',avatar='🧙‍♂️'):
                    st.write(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            # Write and Generate the AI response\
            with chat_placeholder:
                with st.chat_message("ai",avatar='🧠'):
                    with st.spinner('Amai AI is thinking...'):
                        response = st.write_stream(AI.AI_Response(prompt, df,[model_picked[0], models[model_picked]],temperature))
            st.session_state.chat_history.append({"role": "ai", "content": response})
    with tab3:
        data = st.empty()
        data.markdown('Plot Some data! (It will appear over here)')
    
    #Buttons
    column1,column2,column3,column4 = tab1.columns([1,2,1,2])
    #Commits Current Df
    if column1.button('Commit'):
        column_names = df.columns.tolist()
        st.session_state.commit = st.session_state.show.copy()
        st.session_state.show = st.session_state.commit
        df = st.session_state.show
        st.rerun()
    #Undo's to Last Commit
    if column2.button('Undo To last Commit'):
        st.session_state.show = st.session_state.commit
        df = st.session_state.commit
        st.rerun()
    #Resets back to original database
    if column3.button('Reset all'):
        st.session_state.commit = st.session_state.og
        st.session_state.show = st.session_state.og

        df = st.session_state.show
        st.rerun()
    #Button to Download file
    if column4.button('Download Cleaned Data as csv'):
        download_dialog()
    #Button to clear cache
    if tab1.button('Clear Cache(RECOMENDED TO USE RIGHT BEFORE EXITING)'):
        st.cache_data.clear()
        st.rerun()

    #updating values/rerunning
    def update(new_df):
        st.session_state.show = new_df
        df = st.session_state.show
        st.rerun()
    
    #Main Sidebar Function
    @st.fragment
    def sidebar():

        #SideBar Full of customiziation
        #Refrencing df
        df = st.session_state.show

        #Sidebar Title
        st.title("Customize Your Data")

        #Data Column names and column/row info
        column_names = df.columns.tolist()

        #picking Value to Show
        Shown_Values = st.expander("Pick Values To Show")
        with Shown_Values:
            #picking values
            st.title('You can only pick one to reset (1 one should be 0, and the second one should be 0,800)')
            First_x_values = st.slider('Pick x Amount of Values To Use', 0, row)
            st.divider()
            Blank_through_Blank = st.slider('Pick X through X Values To Use',0,row,(0,row))
            st.divider()

            #Logic
            if st.button("Value's Picked!"):

                try:
                    if First_x_values > 0 and Blank_through_Blank == (0,row):
                        st.session_state.widgets[0] = First_x_values
                        df = df.head(First_x_values)
                        update(df)

                        
                    elif First_x_values == 0 and Blank_through_Blank != (0,row):
                        st.session_state.widgets[1] = Blank_through_Blank
                        a,b = Blank_through_Blank[0], Blank_through_Blank[1]
                        df = df[a:b]
                        update(df)
                    
                    elif Blank_through_Blank != (0,row) and First_x_values > 0:
                        st.toast('Please only change one slider at a time')
                
                except Exception as e:
                    st.toast(f"Something Went wrong! Try resetting Sliders {e}")

        #Modifiying columns
        Column_Modification = st.expander('Column Modification')
        with Column_Modification:

            #Renaming Column
            Rename_Column = st.expander('Rename Column')
            with Rename_Column:
                column = st.selectbox('Pick Your Column To Rename', column_names)
                new_name = st.text_area('New Name For Column')

                if st.button('Rename The Column') and column and new_name :
                    try:
                        df = df.rename(columns={column: new_name})
                        update(df)
                    
                    except Exception as e:
                        st.toast(f"Something Went wrong! {e}")

            #New Column With Function
            New_Col = st.expander('Make new Column With Function')
            column_names = df.columns.tolist()
            with New_Col:
                col1,col2,col3 = st.columns(3)
                Selected_Columns = col1.selectbox('X Column', column_names)
                operation = col2.selectbox('X', ['x','+', '-', '/'])
                Selected_Columns2 = col3.selectbox('X Column', column_names, key='s')
                new_column_name = st.text_input('Name Of New Column')

                if st.button('Make Column') and Selected_Columns and operation and Selected_Columns2 and new_column_name:
                    result = cf.make_column(df,operation,new_column_name,Selected_Columns,Selected_Columns2)
                    if result is not False:
                        update(result)
                    
                    else:
                        st.toast('Something went Wrong!')
            
            #Dropping columns
            Drop_column = st.expander("Drop Columns")
            with Drop_column:
                column_names = df.columns.tolist()
                Drop_Col = st.multiselect("Columns To Drop", column_names)

                #checking if value changed
                if st.button('Drop Column/s') and Drop_Col:
                    try:
                        new_df = st.session_state.show.drop(columns=Drop_Col)
                        update(new_df)
                    
                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try reselecting columns')
            
            #Add/Remove Suffix/Prefix
            with st.expander('Add or Remove Suffix/Prefix'):
                #adding suffix/prefix
                column_names = df.columns.tolist()
                columnss = st.multiselect('Pick Columns', column_names)
                Suffix = st.text_input('Suffix')
                Prefix = st.text_input('Prefix')
                col4,col5 = st.columns(2)
                remove = col4.checkbox('Remove')
                add = col5.checkbox('Add')
                
                if add and remove:
                    st.toast('Please Pick One checkbox At A Time')
                elif st.button('Format!', key='FORMAT') and (add or remove):
                    try:
                        update(cf.suffix_prefix(Suffix, Prefix, columnss,df,add,remove))
                    
                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, try changing suffix/prefix')

        #Changes Dealing With Specific Values
        with st.expander('Values Modification'):
            #To modify missing values like replacing empty values

            #Replaces empty values in columns
            with st.expander("Replace Empty Values In Columns"):
                column_names = df.columns.tolist()
                value = st.text_input('Value')
                Columns_ = st.multiselect('Columns', column_names)

                if st.button('Replace Empty Values') and value and Columns_:
                    try:
                        update(cf.replace_empty_values(df, Columns_, value))
                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try reselecting columns or changing value')
                
            #Removes columns/rows with missing values
            with st.expander('Remove columns/rows with missing values'):
                c1 = st.checkbox('Remove Rows With Missing Value')
                c2 = st.checkbox('Remove Columns With Missing Value')
                
                submits = st.button('Format')
                try:
                    if c1 and c2 and submits:
                        st.toast('Please Pick One checkbox At A Time')
                    elif c1 and submits:
                        st.session_state.show = st.session_state.show.dropna()
                        st.rerun()
                    elif c2 and submits:
                        st.session_state.show = st.session_state.show.dropna(axis=1)
                        st.rerun()
                except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try deselecting than selecting a single checkbox')
            
            #Replaces all instances of str in column with another str
            with st.expander('Replace string in column with x'):
                #replacing string with another string 

                column_names = df.columns.tolist()
                selected_columns3 = st.multiselect('Pick column/columns', column_names)
                replace = st.text_input('String To replace (Case Sensitive)')
                replaced_with = st.text_input('Replace the string with')

                if st.button('Replace') and selected_columns3 and replace and replaced_with:
                    try:
                        update(cf.replace_str(df, replace, replaced_with, selected_columns3))

                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try reselecting columns')
        
        #Sorts Database using Column
        with st.expander('Sorting'):
            #sorting
            column_names = df.columns.tolist()
            lis = st.selectbox('Pick Column To Sort With', column_names)
            c3 = st.checkbox('Ascending')
            c4 = st.checkbox('Descending')

            if c3 and c4:
                st.toast('Only pick one checkbox at once')
            elif st.button('Sort') and (c3 or c4):
                try:
                    if c3:
                        df = df.sort_values(by=lis)
                        update(df)
                    if c4:
                        df = df.sort_values(by=lis, ascending=False)
                        update(df)

                except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try reselecting columns')

        #Shuffles data
        with st.expander('Shuffle data'):
            #shuffling data
            with st.expander('Shuffle Data'):

                pop = st.toggle('Shuffle Data')
                if st.button('shuffle') and pop:
                    try:
                        df = df.sample(frac=1).reset_index(drop=True)
                        update(df)
                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try toggling it back and forth')

        #Extra Functions
        with st.expander('Extras'):
            #some extra functions

            #Filtering with Value
            with st.expander('Filter (Only With Numbers)'):
                #filtering values
                column_names = df.columns.tolist()
                selected_columns4 = st.selectbox('Select Column To Filter With', column_names)
                col6,col7 = st.columns(2)
                operation2 = col6.selectbox('Pick operation', options=['>', '<', '=', 'not = to'])
                comparison = col7.text_input('Write the comparison')

                if st.button('Filter') and selected_columns4 and operation2 and comparison is not None:
                    try:
                        update(cf.filter(df, comparison,operation2,selected_columns4))
                    
                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try Changing Comparison')
            #formatting
            with st.expander('Format Columns'):
                #formating columns
                column_names = df.columns.tolist()
                format_to_do = st.selectbox('Pick what to do', ['Capitalize', 'Phone Format', 'Remove Extra Spaces'])
                Selected_Columns5 = st.multiselect('Pick columns to format', column_names)
                apply_format = st.button('Apply Formatting')

                if apply_format and Selected_Columns5:
                    try:
                        update(cf.Format(df, format_to_do,Selected_Columns5))
                    
                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try reselecting columns')

                elif apply_format and not Selected_Columns5:
                    st.toast('Please Pick At least One Column And One Format Type')

            #Dropping Duplicate Rows
            col0,col11 = st.columns(2)
            checks = col0.checkbox('Drop Duplicate Rows')
            if st.button('Drop_Duplicates') and checks:
                #dropping duplicates
                try:
                    df = df.drop_duplicates()
                    update(df)

                except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try unselecting then selecting the checkboxes again')

        #Plotting Data 
        with st.expander('Plot Your Data'):
            
            def plot(val_x,val_y,color):

                #Main plot logic (in Clean_functions.py)
                with tab3:
                    try:
                        data.plotly_chart(cf.plotting(val_x,val_y,color,plot_type,df))
                    
                    except Exception as e:
                        st.toast(f'Something went Wrong, {e}, Try reselecting values, and color if you had one')


            plot_type = st.selectbox('Selct The Type Of Chart You Want', ['line plot (2d)', 'scatter plot (2d)', 'bar chart (2d)', 'Horizantal Bar Chart (2d)', 'Stacked Area Plot (2d)', 'Histogram Plot (1d)', 'Box Plot (1d)', 'Map Plot'])
            column_names = df.columns.tolist()
            color = st.selectbox('Selct The Axis To be The Label/color', ['None'] + column_names)
            
            #picking values
            with st.expander('Plot Values'):
                column_names = df.columns.tolist()
                st.markdown('Pick None In Y For 1d Plots')
                x_val = st.selectbox('Pick x', column_names)
                y_val = st.selectbox('Pick y', column_names + ['None'])

                if st.button('Submit '):
                    if plot_type == 'Map Plot':
                        st.toast('Please Use Map Section To plot on Map')
                    elif plot_type in ['Histogram Plot (1d)', 'Box Plot (1d)'] and y_val != 'None':
                        st.toast('Please Pick None For Y if You are Doing a 1d plot')
                    elif plot_type not in ['Histogram Plot (1d)', 'Box Plot (1d)'] and y_val == 'None':
                        st.toast('Please Pick X and Y for 2d Plot')
                    else:
                        plot(x_val,y_val,color)

            #picking Map values
            with st.expander('Plot On Map'):
            
                lat = st.selectbox('Pick Latitude', column_names)
                lon = st.selectbox('Pick Longtitude', column_names)
                
                if st.button('Submit  Map'):
                    if plot_type == 'Map Plot':
                        if not lat or not lon:
                            st.toast('Please Pick Latitude AND Longtitude')
                        else:
                            plot(lat,lon,color)
                    else:
                        st.toast('Please Pick Map Plot To Plot On Map')
                
        st.link_button("Learn How To Use Amai", 'https://youtu.be/ZZrf9-v7QsA')  

    #Running everything
    with st.sidebar:
        sidebar()


#Streamlit Init
st.set_page_config(
    page_title="Amai AI | Professional Data Workspace", 
    page_icon="🥸",
    layout='centered',
    menu_items={
        'Get Help': 'https://youtu.be/ZZrf9-v7QsA',
        'Report a bug': "https://github.com/hqwn/Data-Cleaner--Web//issues",
        'About': "# Amai AI\nCreated for fast data cleaning and fun :D."
    },
)


#Title
st.markdown(
     """
     <h1 style='text-align: center;'>Amai 👌👌</h1>
     """,
     unsafe_allow_html=True,
 )
  
#Tabs
usage,about = st.tabs(['Use the app','About Amai'])

#About Tab
with about:
    st.markdown(
        """
        ## About Amai
        **Quick Tip, click the three dots to see multiple advanced options along with theme (Use Dark Theme In My Opinion)**
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
    #Youtube link
    st.link_button("Learn How To Use Amai", 'https://youtu.be/ZZrf9-v7QsA')  

#Usage Tab
with usage:
    #Start Logic

    #Uploading file
    file = st.file_uploader("Please Upload A Csv/Xlsx File", type=['xlsx', 'csv'])
    password = st.text_input('Please Write Your Password If Your File Has A password', type='password', key='password_input')
    if file:

        #Checking If New File Uploaded, If yes Resetting everything
        if st.session_state.get("file") != (file.name, file.size):
            st.session_state["file"] = (file.name, file.size)
            st.session_state.widgets = None  
            st.session_state.commit = None
            st.session_state.show = None
            st.session_state.og = None
            st.session_state.chat_history = None
            st.cache_data.clear()
        try:
            #Main Code
            main(file)
        except Exception as e:
            st.warning(f'Something Went Wrong! Please Try Again {e}')
    else:
        #Warning if 
        st.warning('Please Upload A csv/xlsx File Under 200 Mb')
        st.stop()


