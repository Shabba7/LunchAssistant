import streamlit as st
from pages_other import main_page, picker_page, rankings_page, login_page, review_page
import time
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh


st.markdown("<h1 style='text-align: center; color: #0F596E;'>Lunch Assistant</h1>", unsafe_allow_html=True)

auth_status, user = login_page.Page().run()

if auth_status:
    # Create tabs
    map_tabs_to_obj = {
        'Home':     main_page.Page(),
        'Rankings': rankings_page.Page(),
        'Picker':   picker_page.Page(user),
        'Review':   review_page.Page()
    }

    selected_menu = option_menu(None,
                            ["Home", "Rankings", "Picker", 'Review'],
                            icons=['house', 'arrow-down-up', "list-task", 'pencil-square'],
                            orientation="horizontal")
    if selected_menu == "Picker":
        st_autorefresh(interval=1000)
    else:
        st_autorefresh(interval=60000)
    map_tabs_to_obj[selected_menu].run()

elif auth_status is None:
    st.session_state["init_ran"] = True
    st.warning("Please enter your username and password")

else:
    st.error("Username/Password is incorrect")