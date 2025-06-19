import streamlit as st

pages_path = "pages"
live_page = st.Page(
    f"{pages_path}/live.py", title="Live View", icon=":material/add_circle:"
)
historic_page = st.Page(
    f"{pages_path}/historic.py", title="Historic", icon=":material/history:"
)

import_page = st.Page(
    f"{pages_path}/import.py", title="Import Data", icon=":material/file_upload:"
)

# Initialize session state for data
if "data" not in st.session_state:
    st.session_state.data = None
if "loading_data" not in st.session_state:
    st.session_state.loading_data = False
if "data_start_date" not in st.session_state:
    st.session_state.data_start_date = None
if "data_end_date" not in st.session_state:
    st.session_state.data_end_date = None
pg = st.navigation([import_page, live_page, historic_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
# st.sidebar.header("Navigation")
pg.run()
