from pages_other import main_page, picker_page, rankings_page, login_page, review_page, db_test
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu
import psycopg2
import streamlit as st
import time

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# @st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

st.markdown("<h1 style='text-align: center; color: #0F596E;'>Lunch Assistant</h1>", unsafe_allow_html=True)

auth_status, user = login_page.Page().run()

if auth_status:
    # Create tabs
    map_tabs_to_obj = {
        'Home':     main_page.Page(),
        'Rankings': rankings_page.Page(),
        'Picker':   picker_page.Page(user),
        'Review':   review_page.Page(),
        'DBTest':   db_test.Page(run_query)
    }

    selected_menu = option_menu(None,
                            ["Home", "Rankings", "Picker", 'Review', 'DBTest'],
                            icons=['house', 'arrow-down-up', "list-task", 'pencil-square'],
                            orientation="horizontal")

    if selected_menu == "Picker" and picker_page.Page.get_time_until_next_midday().total_seconds() < 60:
        st_autorefresh(interval=1000)
    else:
        st_autorefresh(interval=60000)
    map_tabs_to_obj[selected_menu].run()

elif auth_status is None:
    st.session_state["init_ran"] = True
    st.warning("Please enter your username and password")

else:
    st.error("Username/Password is incorrect")