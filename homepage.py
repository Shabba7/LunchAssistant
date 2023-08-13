import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu
from webpages import (
    admin_page, login_page, main_page,
    picker_page, rankings_page, review_page,
)

st.set_page_config(
    page_title="Lunch Assistant",
    page_icon="🍴",
    layout="centered",
    initial_sidebar_state="expanded"
)

# count = st_autorefresh(interval=1000, key="strefreshcounter")

st.markdown(
    "<h1 style='text-align: center; color: #0F596E;'>Lunch Assistant</h1>",
    unsafe_allow_html=True,
)

auth_status, user = login_page.Page().run()

if auth_status:
    # Create tabs
    map_tabs_to_obj = {
        "Home": main_page.Page(),
        "Ranking": rankings_page.Page(),
        "Picker": picker_page.Page(),
        "Review": review_page.Page(),
        "Admin": admin_page.Page(),
    }

    tabs = ["Home", "Ranking", "Picker", "Review"]
    icons = ["house", "arrow-down-up", "list-task", "pencil-square"]
    if user in ["emoreira", "ngregori"]:
        tabs =  ["Home", "Ranking", "Picker", "Review", "Admin"]
        icons=["house", "arrow-down-up", "list-task", "pencil-square", "person-badge-fill"]

    selected_menu = option_menu(
        None,
        tabs,
        icons=icons,
        orientation="horizontal",
    )

    # if (
    #     selected_menu == "Picker"
    #     and picker_page.Page.get_time_until_next_midday().total_seconds() < 60
    # ):
    #     st_autorefresh(interval=100)
    # else:
    #     st_autorefresh(interval=100)
    map_tabs_to_obj[selected_menu].run()

elif auth_status is None:
    st.session_state["init_ran"] = True
    st.warning("Please enter your username and password")

else:
    st.error("Username/Password is incorrect")
