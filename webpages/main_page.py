import db.db_handler as db
import pandas as pd
import streamlit as st

STRYPES_LAT  = 41.1578156070871
STRYPES_LON = -8.635795928658316

class Page:
    restaurants = 27
    money = 1500
    reviews = 142
    def __init__(self) -> None:
        if not st.session_state["init_ran"]:
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center; } </style>', unsafe_allow_html=True)
            st.markdown(
                """
            <style>
            [role=radiogroup]{
            gap: 3rem;
            display: flex;
            justify-content: space-evenly;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

    def run(self):
        col1, col2, col3 = st.columns(3, gap="small")
        col1.metric(label="Money spent this month", value=self.money, delta=133)
        col2.metric(label="Reviews done this month", value=self.reviews, delta=7)
        col3.metric(label="Restaurants visited this month", value=self.restaurants, delta=3)

        col4, col5, col6 = st.columns(3, gap="small")
        col4.metric(label="Ratinho do lixo", value="Edgar Moreira")
        col5.metric(label="Next Stop", value="---")

        def prep_row(row):
            lon, lat = row['res_loc'][1:-1].split(',')
            return (float(lat), float(lon), 6, '#00ff00')
        rows = db.fetch_restaurants_location()
        rows = list(map(prep_row, rows))
        rows.append((STRYPES_LAT, STRYPES_LON, 20, '#ff0000'))

        data = pd.DataFrame(rows, columns=['lat', 'lon', 'size', 'color'])


        # Display the map using st.map()
        st.map(data=data, zoom=15, size='size', color='color')
