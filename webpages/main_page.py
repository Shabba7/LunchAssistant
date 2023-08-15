import db.db_handler as db
import pandas as pd
import streamlit as st
import pydeck as pdk
import colorsys

class Page:
    restaurants = 27
    money = 1500
    reviews = 142
    def __init__(self) -> None:
        if "init_ran" not in st.session_state:
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center; } </style>', unsafe_allow_html=True)

    def run(self):

        col1, col2, col3 = st.columns(3, gap="small")

        # Metrics
        col1.metric(label="Money spent this month",
                    value=f'{db.fetch_money_spent_this_month()}€',
                    delta=f'{round(db.fetch_money_spent_this_month() - db.fetch_money_spent_previous_month(),2)}€')


        col2.metric(label="Next stop", value=self._get_next_stop())

        col3.metric(label="Restaurants visited this month",
                    value=db.fetch_restaurants_visited_this_month(),
                    delta=db.fetch_restaurants_visited_this_month() - db.fetch_restaurants_visited_previous_month())

        col4, col5, col6 = st.columns(3, gap="small")

        col4.metric(label='Total money spent', value=db.fetch_total_money_spent())

        bs_name, bs_money = db.fetch_biggest_spender()
        col5.metric(label="Ratinho do lixo 🐁", value=bs_name,delta=f'{bs_money}€',help="This will show last month's biggest spender.\nHe will have a free lunch paid by the rest")


        col6.metric(label="Reviews done this month",
                    value=db.fetch_reviews_done_this_month(),
                    delta=db.fetch_reviews_done_this_month()-db.fetch_reviews_done_previous_month())

        # Map
        self.generate_map()

    @staticmethod
    def _get_next_stop():
        return st.session_state['next_stop'] if 'next_stop' in st.session_state else "---"

    @staticmethod
    def generate_map():
        STRYPES_LAT = st.secrets["strypes_geo"]["latitude"]
        STRYPES_LON = st.secrets["strypes_geo"]["longitude"]
        view_state = pdk.ViewState(latitude=STRYPES_LAT,
                            longitude=STRYPES_LON,
                            zoom=15,
                            pitch=0)

        rows = db.fetch_restaurant_to_map()
        rows = list(map(prep_row, rows))
        rows.append(('Strypes HQ', STRYPES_LAT, STRYPES_LON, 15, [16,89,110]))
        data = pd.DataFrame(rows, columns=['name', 'lat', 'lon', 'size', 'color'])

        tooltip = {"text": "{name}"}

        slayer = pdk.Layer(
            type='ScatterplotLayer',
            data=data,
            get_position=["lon", "lat"],
            get_color="color",
            get_line_color=[0, 0, 0],
            get_radius="size",
            pickable=True,
            onClick=True,
            filled=True,
            line_width_min_pixels=10,
            opacity=2,
        )

        pp = pdk.Deck(
            initial_view_state=view_state,
            map_provider='mapbox',
            map_style=pdk.map_styles.MAPBOX_LIGHT,
            layers=[
                slayer,
            ],
            tooltip=tooltip
        )

        st.pydeck_chart(pp)


def prep_row(row):
    lon, lat = row['res_loc'][1:-1].split(',')
    color = _prep_row_color(row['overall_rating'])

    return (f"{row['res_name']}\nRating: {row['overall_rating']}", float(lat), float(lon), 10, color)

def _prep_row_color(rating):
    # Normalize the value to the range [0, 1]
    normalized_value = float(rating) / 10.0

    # Map normalized value to hue in HSV
    hue = normalized_value * 120  # Red (0) to Green (120) in HSV

    # Set saturation and value to 100% (maximum)
    saturation = 1.0
    value = 1.0

    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue / 360.0, saturation, value)

    # Scale RGB values to [0, 255]
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return [r,g,b]
