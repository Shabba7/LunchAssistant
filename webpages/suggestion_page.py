import db.db_handler as db
import googlemaps
import requests
import streamlit as st
from streamlit_searchbox import st_searchbox
from typing import List
import uuid


@st.cache_resource()
def init_gmaps():
    return googlemaps.Client(key=st.secrets["google"]["api_key"], queries_per_second=1)

@st.cache_data()
def strypes_geo_coords():
    return f'{st.secrets["strypes_geo"]["latitude"]},{st.secrets["strypes_geo"]["longitude"]}'

SESSION_TOKEN = "3bd8f04e-8637-4fda-a686-d42a83dd076f"

class Page:

    def run(self):
        self.page()

    def page(self):

        st.subheader("New restaurant?")

        restaurant = st_searchbox(self.restaurant_lookup, key="place_api_search")
        st.write(restaurant)

        # with st.form("restaurant_picker", clear_on_submit=True):
        #     restaurant = st.text_input(" ", placeholder="Type your restaurant suggestion here...",label_visibility="collapsed")
        #     if st.form_submit_button("Submit"):
        #         restaurants = [r.lower() for r in db.fetch_restaurants_names()]
        #         if restaurant and restaurant.strip() != "" and restaurant.strip().lower() not in restaurants:
        #             db.register_restaurant(restaurant, '-8.62, 41.15', st.session_state['user_id'])
        #             st.info("Restaurant added! Thanks for contributing!", icon='😍')
        #         elif restaurant and restaurant.strip() != "":
        #             st.info("Good pick! Someone already suggested it.", icon='😅')

        with st.form("suggestions", clear_on_submit=True):
            st.subheader("What can we improve?")
            suggestion = st.text_area(" ")
            if st.form_submit_button("Submit"):
                db.store_suggestion(st.session_state['user_id'][0],suggestion)
                st.success("Thank you for your suggestion!")

    @staticmethod
    def restaurant_lookup(searchterm: str) -> List[str]:
        #gmap = init_gmaps()
        predictions = gmap.places_autocomplete(
            input_text=searchterm, language="pt",
            location=strypes_geo_coords(), radius=5000, strict_bounds=True,     # Geo  restrictions
            components={"country":"PT"},                                        # Redundant?
            origin=strypes_geo_coords(),                                        # For straight line distance calculation
            types="food",                                                       # Type restrictions
            session_token=SESSION_TOKEN                                         # Billing safety
            # (Button to open session, generate token, close session with submit to db) # token per user? How streamlit does work?
        )
        return [f'{p["description"]} @ {p["distance_meters"]}m' for p in predictions]