import streamlit as st
import pandas as pd
import os
class Page:
    review_saved = None
    def __init__(self) -> None:
        pass

    def run(self):
        self.page()

    def page(self):
        st.title("Restaurant Review Submission")

        # Input fields for user review
        col1, col2 = st.columns(2)

        with col1:
            restaurant_name = st.text_input("Restaurant Name")
        with col2:
            price_paid = st.number_input("Price Paid", min_value=0.0)

        food_rating = st.slider("Food Rating", 0, 10, 5, help="Tell us how good was the food")
        service_rating = st.slider("Service Rating", 0, 10, 5, help="Classify not only the service but the place as well")
        price_rating = st.slider("Price Rating", 0, 10, 5,  help="How fair is the price?",)

        _, _, center,_,_ = st.columns(5)
        with center:
            if st.button("Submit Review"):
                # Process the submitted review
                review_data = {
                    "Restaurant": restaurant_name,
                    "FoodRating": food_rating,
                    "ServiceRating": service_rating,
                    "PriceRating": price_rating,
                    "PricePaid": price_paid
                }
                if self._check_input(review_data):
                    self.save_review_data(review_data)
                else:
                    st.toast("Oops! Looks like your review is invalid")

                # Confirmation message
        if self.review_saved:
            st.success("Review submitted successfully!")
            self.review_saved = False

    def _check_input(self, data):
        return True if data['PricePaid'] > 4 else False

    # Function to save the review data (You can customize this based on your storage preferences)
    def save_review_data(self, review_data):
        # For demonstration purposes, let's just append the data to a CSV file
        df = pd.DataFrame([review_data])
        df.to_csv("restaurant_reviews.csv", mode="a", header=not os.path.exists("restaurant_reviews.csv"), index=False)
        self.review_saved = True

