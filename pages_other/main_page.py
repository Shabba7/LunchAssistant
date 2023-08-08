import streamlit as st
import pandas as pd
import numpy as np

class Page:
    restaurants = 27
    money = 1500
    reviews = 142
    def __init__(self) -> None:
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

        # df = pd.DataFrame({
        #     "col1": np.random.randn(10) / 150 + 41.1578156070871,
        #     "col2": np.random.randn(10) / 150 + -8.635795928658316,
        # })

        # st.map(df,
        #     latitude='col1',
        #     longitude='col2',
        #     size='2',
        #     color='#ff00005f')
        # st.map(data=None, latitude='41.1578156070871', longitude='-8.635795928658316', color=None, size=None, zoom=19, use_container_width=True)
        latitude = 41.1578156070871
        longitude = -8.635795928658316
        data = pd.DataFrame({
            "lat": [latitude,41.16],
            "lon": [longitude,longitude],
            "size": [20, 6],
            "color": ['#ff0000', '#00ff00']
        })


        # Display the map using st.map()
        st.map(data=data, zoom=15, size='size', color='color')
