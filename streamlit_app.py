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

st.write("Dataset is limited to Fannie Mae Securities issued in July 2024. ")


def extract_data(query_string, columns, table, filters): 
    conn=duckdb.connect(':memory:')
    #st.text(query_string + column_string + table + filters)
    dfs = pd.read_sql(query_string + columns + table + filters, conn)
    
    return dfs

#def get_pyg_renderer() -> "StreamlitRenderer":
    # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
 #   return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw", kernel_computation=True)

select_string = "SELECT * "
column_string =  ""
#"\"" + "Loan Identifier" + "\""
from_string = " FROM read_parquet('data/secu_core.parquet')"
filter_string = " limit 100"

df = extract_data(select_string, column_string, from_string, filter_string)

print (df)

#st.text(select_string + column_string + from_string + filter_string)


# Three columns with different widths
col1, col2  = st.columns([1,2])
# col1 is wider

# Using 'with' notation:
with col1:
    txt_search = st.text_input("Search: CUSIP ID")
    if txt_search:
        filter_string =  " where " + "\"" + "cusip" + "\"" + "=" + "'" + txt_search +"'"
        df = extract_data(select_string, column_string, from_string, filter_string) 
   # df = pd.read_sql_query(query, conn)

with col2:
    with st.expander ("Selected Columns"):
        column_list = st.multiselect (label='Customize columns to display', options=df.columns, placeholder='Select columns')
        no_of_cols = (len(column_list))
        if column_list:
            select_string="Select "
        else:
            select_string = "Select * "
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
tab1, tab2, tab3 = st.tabs(["Dataset", "Collateral", "Details"])

#tab2.write("To create a visual, drag and drop attributes in to X or Y axis.")

# You can also use "with" notation:
with tab1:
    st.dataframe(df,  use_container_width=True, hide_index=True)
    #st.write("Test")
with tab2:
    #renderer = get_pyg_renderer()
    #renderer.explorer()
    if txt_search:
        select_string = "SELECT "
        column_string =  "*"
        from_string = " FROM read_parquet('data/ln_dsc.parquet')"
        df_loans = extract_data(select_string, column_string, from_string, filter_string)
        if df_loans.empty:
            st.write ("Collateral not found! You must have selected a Mega security. Still working on getting the collateral for Mega's!!")
        else:
            st.dataframe(df_loans, use_container_width=True,hide_index=True)
    else:
        st.write ("Submit a CUSIP in search above!")
            
with tab3:
    if txt_search:
        select_string = "SELECT "
        column_string =  "*"
        from_string = " FROM read_parquet('data/secu_core.parquet')"
        df_sec = extract_data(select_string, column_string, from_string, filter_string)
        df1=df_sec.T
        st.dataframe(df1, use_container_width=True)
    else:
        st.write ("Submit a CUSIP in search above!")