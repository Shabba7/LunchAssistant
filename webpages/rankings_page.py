import db.db_handler as db
import pandas as pd
import streamlit as st


class Page:

    def run(self):
        data = self.prepare_restaurants_df()

        if multi_search := self.multi_search():
            # Filtered restaurant list
            restaurant_list = self.get_restaurants_df(data, multi_search)
            st.dataframe(restaurant_list ,use_container_width=False, hide_index=True, width=1200)
            with st.expander(label="# Details", expanded=True):
                for selected_restaurant in multi_search:
                    result = db.fetch_single_restaurant_reviews(selected_restaurant)
                    st.markdown(f"##### {selected_restaurant}")
                    st.dataframe(pd.DataFrame(result,columns=['User','Food Rating', 'Service Rating', 'Price Rating', 'Price Paid', 'Overall Rating', 'Comment']),
                                use_container_width=True,
                                hide_index=True
                                )
        else:
            # All restaurants list
            restaurant_list = self.prepare_restaurants_df()
            st.dataframe(restaurant_list ,use_container_width=True, hide_index=True)

    def multi_search(self):
        restaurants = self.prepare_restaurants_df()['Restaurant']
        text_search = st.multiselect(label="Search restaurants:",options=restaurants)
        return text_search

    def get_restaurants_df(self, df, restaurant_names):
        # Create a new DataFrame containing only the rows corresponding to the specified restaurant names
        filtered_df = df[df['Restaurant'].isin(restaurant_names)]

        # Check if any restaurants from the input list are not found in the DataFrame
        not_found_restaurants = set(restaurant_names) - set(filtered_df['Restaurant'])
        if not_found_restaurants:
            st.warning(f"Restaurants not found: {', '.join(not_found_restaurants)}")

        return filtered_df

    def prepare_restaurants_df(self):
        data = pd.DataFrame(db.fetch_restaurants_avg(),
                            columns=['Restaurant','Reviews', 'Food Rating','Service Rating','Price Rating','Price Paid', 'Overall Rating'])
        data['Price Paid'] = data['Price Paid'].apply(lambda x: f"{x:.2f} €")
        return data