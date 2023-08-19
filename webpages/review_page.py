import streamlit as st
import pandas as pd
import os
import db.db_handler as db
from psycopg2.errors import UniqueViolation
import datetime
import pytz

class Page:
    review_saved = None

    def run(self):
        self.page()

    def page(self):
        st.title("Review Submission")

        # Input fields for user review
        col1, col2 = st.columns(2)
        options = db.fetch_restaurants_names()

        with col1:
            restaurant_name = st.selectbox("Restaurant Name",options=options)
            if review:=db.fetch_user_restaurant_review(restaurant_name,st.session_state['user_id']):
                food_rating_slider    = review[0]['food_rating']
                service_rating_slider = review[0]['service_rating']
                price_rating_slider   = review[0]['price_rating']
                price_paid_value      = float(review[0]['price_paid'])
                comment               = review[0]['comment']
            else:
                food_rating_slider    = 5
                service_rating_slider = 5
                price_rating_slider   = 5
                price_paid_value      = 0.0
                comment               = ''

        with col2:
            price_paid = st.number_input("Price Paid", min_value=0.0,value=price_paid_value)

        food_rating    = st.slider("Food Rating", 0, 10, food_rating_slider)
        service_rating = st.slider("Service Rating", 0, 10, service_rating_slider)
        price_rating   = st.slider("Price Rating", 0, 10, price_rating_slider  , help="0 - too expensive | 10 - awesomely cheap")
        review_comment = st.text_area(label="Tell us your experience!",value=comment)
        button_label = "Update Review" if review else "Submit Review"
        if st.button(label=button_label,use_container_width=True):
            # Process the submitted review
            if price_paid < 300:
                if review:
                    db.update_review(st.session_state['user_id'],
                                    restaurant_name,
                                    food_rating,
                                    service_rating,
                                    price_rating,
                                    price_paid,
                                    datetime.datetime.now(pytz.timezone("Europe/London")),
                                    review_comment
                                    )
                    st.success("Review updated successfully!")
                else:
                    db.submit_review(st.session_state['user_id'],
                                    restaurant_name,
                                    food_rating,
                                    service_rating,
                                    price_rating,
                                    price_paid,
                                    datetime.datetime.now(pytz.timezone("Europe/London")),
                                    review_comment
                                    )
                    st.success("Review submitted successfully!")
            else:
                st.error('That is too expensive!💰')



