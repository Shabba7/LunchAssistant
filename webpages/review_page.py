import streamlit as st
import pandas as pd
import os
import db.db_handler as db
from psycopg2.errors import UniqueViolation
import datetime

class Page:
    review_saved = None

    def run(self):
        self.page()

    def page(self):
        st.title("Review Submission")
        with st.form("review"):
            # Input fields for user review
            col1, col2 = st.columns(2)
            options = db.fetch_restaurants_names()

            with col1:
                restaurant_name = st.selectbox("Restaurant Name",options=[rest[0] for rest in options])
            with col2:
                price_paid = st.number_input("Price Paid", min_value=0.0)

            food_rating    = st.slider("Food Rating", 0, 10, 5)
            service_rating = st.slider("Service Rating", 0, 10, 5)
            price_rating   = st.slider("Price Rating", 0, 10, 5)
            if st.form_submit_button("Submit Review",use_container_width=True):
                # Process the submitted review
                if price_paid >= 4:
                    try:
                        db.submit_review(st.session_state['user_id'],
                                        restaurant_name,
                                        food_rating,
                                        service_rating,
                                        price_rating,
                                        price_paid,
                                        datetime.datetime.now()
                                        )
                        st.success("Review submitted successfully!")
                    except UniqueViolation:
                        st.error("You already reviewed this restaurant 😔")
                else:
                    st.toast("Oops! Looks like your review is invalid")

