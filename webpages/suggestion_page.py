import streamlit as st
import db.db_handler as db

class Page:

    def run(self):
        self.page()

    def page(self):

        with st.form("restaurant_picker", clear_on_submit=True):
            st.subheader("New restaurant?")
            restaurant = st.text_input(" ", placeholder="Type your restaurant suggestion here...",label_visibility="collapsed")
            if st.form_submit_button("Submit"):
                restaurants = [r.lower() for r in db.fetch_restaurants_names()]
                if restaurant and restaurant.strip() != "" and restaurant.strip().lower() not in restaurants:
                    db.register_restaurant(restaurant, '-8.62, 41.15', st.session_state['user_id'])
                    st.info("Restaurant added! Thanks for contributing!", icon='😍')
                elif restaurant and restaurant.strip() != "":
                    st.info("Good pick! Someone already suggested one.", icon='😅')

        with st.form("suggestions", clear_on_submit=True):
            st.subheader("What can we improve?")
            suggestion = st.text_area(" ")
            if st.form_submit_button("Submit"):
                db.store_suggestion(st.session_state['user_id'],suggestion)
                st.success("Thank you for your suggestion!")