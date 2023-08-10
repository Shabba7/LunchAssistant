import db.db_handler as db
import pandas as pd
import streamlit as st


class Page:
    restaurants = None
    df = None
    def __init__(self) -> None:
        self.df = self.prepare_restaurants_df()
        self.restaurants = self.df['Restaurant']

    def run(self):
        if search:=self.search():
            st.dataframe(self.get_restaurants_df(self.df, search),use_container_width=True, hide_index=True)
        else:
            st.dataframe(self.df,use_container_width=True, hide_index=True)

    def search(self):
        text_search = st.multiselect(label="Search restaurants:",options=self.restaurants)
        return text_search

    def _create_table(values):
        pass

    def get_restaurants_df(self, df, restaurant_names):
        # Create a new DataFrame containing only the rows corresponding to the specified restaurant names
        filtered_df = df[df['Restaurant'].isin(restaurant_names)]

        # Check if any restaurants from the input list are not found in the DataFrame
        not_found_restaurants = set(restaurant_names) - set(filtered_df['Restaurant'])
        if not_found_restaurants:
            st.warning(f"Restaurants not found: {', '.join(not_found_restaurants)}")

        return filtered_df
    
    def prepare_restaurants_df(self):
        rows = db.fetch_restaurants_avg()
        return pd.DataFrame(rows, columns=['Restaurant','Nº Reviews', 'Food Rating','Service Rating','Price Rating','Price Paid'])