import db.db_handler as db
import googlemaps
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


class Page:

    def run(self):
        self.page()

    def page(self):

        if "tokens" not in st.session_state:
            st.session_state["tokens"] = {}
        if str(st.session_state["user_id"]) not in st.session_state["tokens"]:
            st.session_state["tokens"][str(st.session_state["user_id"])] = uuid.uuid4()

        st.subheader("New restaurant?")

        if st.secrets["dev"]["experimental_autocomplete"]:
            self.great_suggestion()
        else:
            self.weak_suggestion()

        with st.form("suggestions", clear_on_submit=True):
            st.subheader("What can we improve?")
            suggestion = st.text_area(" ")
            if st.form_submit_button("Submit"):
                db.store_suggestion(st.session_state['user_id'][0],suggestion)
                st.success("Thank you for your suggestion!")

    def great_suggestion(self):
        restaurant = st_searchbox(self.restaurant_lookup, key="place_api_search")
        if restaurant and restaurant != "" and st.button("Submit"):
            predictions = st.session_state[f"predictions{st.session_state['user_id']}"]
            place_id = [p["place_id"] for p in predictions if f'{p["description"]} @ {p["distance_meters"]}m' == restaurant]
            gmap = init_gmaps()
            token = st.session_state["tokens"][str(st.session_state["user_id"])]

            try:
                details = gmap.place(
                    place_id=place_id, language="pt",
                    fields=["name", "geometry/location"],                   # Place field data
                    session_token=token                                      # Billing safety
                )
                restaurant_name = details["result"]["name"]
                restaurant_loc = details["result"]["geometry"]["location"]
                if restaurant_name not in db.fetch_restaurants_names():
                    db.register_restaurant(restaurant_name, f'{restaurant_loc["lng"]},{restaurant_loc["lat"]}', st.session_state['user_id'][0])
                    st.info("Restaurant added! Thanks for contributing!", icon='😍')
                else:
                    st.info("Good pick! Someone already suggested it.", icon='😅')
            except Exception as e:
                st.error("Google f'ed up. Yes.")
                st.write(e)
            finally:
                st.session_state["tokens"][str(st.session_state["user_id"])] = uuid.uuid4()

    def weak_suggestion(self):
        with st.form("restaurant_picker", clear_on_submit=True):
            restaurant = st.text_input(" ", placeholder="Type your restaurant suggestion here...",label_visibility="collapsed")
            if st.form_submit_button("Submit"):
                restaurants = [r.lower() for r in db.fetch_restaurants_names()]
                if restaurant and restaurant.strip() != "" and restaurant.strip().lower() not in restaurants:
                    db.register_restaurant(restaurant, '-8.62, 41.15', st.session_state['user_id'])
                    st.info("Restaurant added! Thanks for contributing!", icon='😍')
                elif restaurant and restaurant.strip() != "":
                    st.info("Good pick! Someone already suggested it.", icon='😅')

    def restaurant_lookup(self, searchterm: str) -> List[str]:
        gmap = init_gmaps()
        token = st.session_state["tokens"][str(st.session_state["user_id"])]
        predictions = gmap.places_autocomplete(
            input_text=searchterm, language="pt",
            location=strypes_geo_coords(), radius=5000, strict_bounds=True,     # Geo  restrictions
            components={"country":"PT"},                                        # Redundant?
            origin=strypes_geo_coords(),                                        # For straight line distance calculation
            types="food",                                                       # Type restrictions
            session_token=token                                                 # Billing safety
        )
        st.session_state[f"predictions{st.session_state['user_id']}"] = predictions
        return [f'{p["description"]} @ {p["distance_meters"]}m' for p in predictions]