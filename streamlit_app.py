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


#conn = sqlite3.connect('mydb.db')
#conn=duckdb.connect('mydatabase.db')
conn=duckdb.connect(':memory:')
query = "SELECT * FROM read_csv('data/illd.txt')"
df = pd.read_sql_query(query, conn)

def get_pyg_renderer() -> "StreamlitRenderer":
    # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
    return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")


# Three columns with different widths
col1, col2, col3 = st.columns([3,1,1])
# col1 is wider

# Using 'with' notation:
with col1:
    st.write('This is column 1')
with col2:
    st.write('Today')
with col3:
    st.write('Tomorrow')

# Insert containers separated into tabs:
tab1, tab2, tab3 = st.tabs(["Details", "Analyze", "Something Else"])

tab2.write("this is tab 2")

# You can also use "with" notation:
with tab1:
   st.dataframe(df,  use_container_width=True, hide_index=True)

with tab2:
    renderer = get_pyg_renderer()
    renderer.explorer()