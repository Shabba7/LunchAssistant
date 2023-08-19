import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu
from webpages import (
    admin_page, login_page, main_page,
    picker_page, rankings_page, review_page,
    suggestion_page
)
from css import page_styling

st.set_page_config(
    page_title="Lunch Assistant",
    page_icon="🍴",
    layout="centered",
    initial_sidebar_state="expanded"
)

page_styling.setup_page()

auth_status, user = login_page.Page().run()

if auth_status:
    # Create tabs
    map_tabs_to_obj = {
        "Home": main_page.Page(),
        "Ranking": rankings_page.Page(),
        "Picker": picker_page.Page(),
        "Review": review_page.Page(),
        "Suggest": suggestion_page.Page(),
        "Admin": admin_page.Page(),
    }

    tabs = ["Home", "Ranking", "Picker", "Review", "Suggest"]
    icons = ["house", "arrow-down-up", "list-task", "pencil-square", "bookmark-plus-fill"]
    if user in [ "emoreira", "ngregori", "msilva"]:
        tabs.append("Admin")
        icons.append("person-badge-fill")

    selected_menu = option_menu(
        None,
        tabs,
        icons=icons,
        orientation="horizontal",
    )

    map_tabs_to_obj[selected_menu].run()

elif auth_status is None:
    st.warning("Please enter your username and password")

else:
    st.error("Username/Password is incorrect")