import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu
from webpages import (
    admin_page, login_page, main_page,
    picker_page, rankings_page, review_page,
    suggestion_page
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

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;font-size: 26px;} </style>', unsafe_allow_html=True)
st.markdown(
    """
<style>
.css-1y4p8pa {
    width: 100%;
    padding: 6rem 1rem 10rem;
    max-width: 66rem;
}
[data-testid="metric-container"] {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] > div {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] label {
    width: fit-content;
    margin: auto;
}
</style>
""",
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
    st.session_state["init_ran"] = True
    st.warning("Please enter your username and password")

else:
    st.error("Username/Password is incorrect")