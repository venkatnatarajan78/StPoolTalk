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

def extract_data(query_string, column_string, table, filters): 
    conn=duckdb.connect(':memory:')
    df = pd.read_sql_query(query_string + column_string + table + filters, conn)
    st.text(query_string + column_string + table + filters)
    return df

#def get_pyg_renderer() -> "StreamlitRenderer":
    # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
 #   return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw", kernel_computation=True)

select_string = "SELECT "
column_string =  "\"" + "Loan Identifier" + "\""
from_string = " FROM read_csv('data/illd.txt')"
filter_string = " limit 100"

df = extract_data(select_string, column_string, from_string, filter_string)

#st.text(select_string + column_string + from_string + filter_string)


# Three columns with different widths
col1, col2, col3 = st.columns([3,1,1])
# col1 is wider

# Using 'with' notation:
with col1:
    ln_search = st.text_input("Search: Loan Identifier")
    if ln_search:
        filter_string =  " where " + "\"" + "Loan Identifier" + "\"" + "=" + "'" + ln_search +"'"
        df = extract_data(select_string, column_string, from_string, filter_string) 
   # df = pd.read_sql_query(query, conn)

with col2:
    column_list = st.multiselect (label='Customize columns to display', options=df.columns, placeholder='Select columns')
    no_of_cols = (len(column_list))
    column_string = ""
    i=0
    while i < no_of_cols:
        if i == (no_of_cols-1):
            column_string += "\"" + column_list[i] + "\""
        else: 
            column_string += "\"" + column_list[i] + "\", "
        i+=1
    #if column_list:
    df = extract_data(select_string, column_string, from_string, filter_string)

# Insert containers separated into tabs:
tab1, tab2, tab3 = st.tabs(["Dataset", "Analyze", "Details"])

#tab2.write("To create a visual, drag and drop attributes in to X or Y axis.")

# You can also use "with" notation:
with tab1:
   st.dataframe(df,  use_container_width=True, hide_index=True)

with tab2:
    #renderer = get_pyg_renderer()
    #renderer.explorer()
    st.write ("Under construction")
with tab3:
    if ln_search:
        df1=df.T
        st.dataframe(df1, use_container_width=True)