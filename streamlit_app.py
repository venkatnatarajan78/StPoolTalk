import streamlit as st
import pandas as pd
import duckdb
from pygwalker.api.streamlit import StreamlitRenderer
 

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="MyPooltalk",
    layout="wide"
    
)
st.header ("My Pool Talk!!")
st.write(
    "Loans securitized this month!"
)

conn=duckdb.connect(':memory:')
query = "SELECT * FROM read_csv('data/illd.txt') limit 1000"
df = pd.read_sql_query(query, conn)

def get_pyg_renderer() -> "StreamlitRenderer":
    # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
    return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw", kernel_computation=True)


# Three columns with different widths
col1, col2, col3 = st.columns([3,1,1])
# col1 is wider

# Using 'with' notation:
with col1:
    ln_search = st.text_input("Search: Loan Identifier")
    if ln_search:
        query = "select * from read_csv('data/illd.txt') where " + "\"" + "Loan Identifier" + "\"" + "=" + "'" + ln_search +"'"
        
    df = pd.read_sql_query(query, conn)

with col2:
    column_list = st.multiselect (label='Customize columns to display', options=df.columns)
    st.write(column_list)
    no_of_cols = (len(column_list))
    st.write(no_of_cols)    
    query_string = "Select "
    i=0
    while i < no_of_cols:
        if i == (no_of_cols-1):
            query_string += "\"" + column_list[i] + "\" from read_csv('data/illd.txt')"
        else: 
            query_string += "\"" + column_list[i] + "\", "
        i+=1
    if column_list:
        df = pd.read_sql_query(query_string, conn)

# Insert containers separated into tabs:
tab1, tab2, tab3 = st.tabs(["Dataset", "Analyze", "Details"])

tab2.write("To create a visual, drag and drop attributes in to X or Y axis.")

# You can also use "with" notation:
with tab1:
   st.dataframe(df,  use_container_width=True, hide_index=True)

with tab2:
    renderer = get_pyg_renderer()
    renderer.explorer()

with tab3:
    if ln_search:
        df1=df.T
        st.dataframe(df1, use_container_width=True)