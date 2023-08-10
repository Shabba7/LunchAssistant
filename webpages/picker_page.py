import streamlit as st
import pandas as pd
import random
import altair as alt
from datetime import datetime

class Page:

    user = None
    random_restaurants = None

    def __init__(self, user) -> None:
        if not st.session_state["init_ran"]:
            self.user = user

    def run(self):
        self.vote()
        self.add_restaurant()
        self.list_restaurants()

    def vote(self):
        # Create a button to start the vote if within allowed timeslot
        if not self.is_vote_started() and 8 <= datetime.now().time().hour <= 12:
            # Little trick to center Start vote button
            _,_,col,_,_ = st.columns(5)
            if col.button("Start Vote"):
                # Pick 3 random restaurants from the list for voting

                self.pick_3_restaurants()

        else:
            if self.is_vote_started():
                self.vote_in_progress()

        if self.is_vote_finished():
            # Create a DataFrame from the vote_counts dictionary

            # # Create an Altair chart
            # chart = alt.Chart(df).mark_bar().encode(
            #     y=alt.Y('Votes:Q', axis=alt.Axis(title='Votes')),
            #     x=alt.X('Restaurant:N', axis=alt.Axis(title='Restaurant', labelAngle=0)),
            #     tooltip=['Restaurant', 'Votes']
            # )

            # # Hide the legend
            # chart = chart.configure_legend(orient='none')

            # # Display the chart
            # st.altair_chart(chart, use_container_width=True)
            pass

    def vote_in_progress(self):

        # Create a radio button for the restaurants
        st.write("### Select one:")
        #chosen_restaurant = st.radio(" ", st.session_state["random_restaurants"])
        time_left = self.get_time_until_next_midday()
        st.write(f'###### Polls will close in {str(time_left).split(".")[0]}')
        progress_bar = st.progress(1)
        progress_bar.progress(time_left.total_seconds() / (60*60*24))
        if time_left.total_seconds() <= 0:
            self.set_vote_started(False)
            self.set_vote_finished(True)

    def add_restaurant(self):

        with st.form("my_form", clear_on_submit=True):
            restaurant = st.text_input('Add restaurant')
            if st.form_submit_button("Submit"):
                if restaurant.strip() != "" and restaurant not in self.restaurants:
                    self.add_restaurant_to_db(restaurant, self.user)
                    st.toast("Restaurant added! Thanks for contributing!", icon='😍')

    def list_restaurants(self):
        # Display the list of restaurants
        st.write("### List of Restaurants")

        # Displaying the table
        #st.dataframe(self.df,use_container_width=True, hide_index=True)

    def add_restaurant_to_db(restaurant, user):
        # TODO: Should add this to the DB list of restaurants
        pass

    def add_vote_to_restaurant(self):
        # Check if user already voted in one restaurant and if he already did remove and add to the new one
        # TODO: create DB call for this
        pass

    def get_restaurants_list(self):
        # TODO: Return restaurant list from DB
        pass

    def pick_3_restaurants(self):
        # TODO: This list has to be stored in the DB so that it does not change
        self.random_restaurants = random.sample(self.get_restaurants_list(), 3).sort()
        self.set_vote_started(True)
        st.experimental_rerun()

    def is_vote_started(self):
            # TODO: create DB to store this
            return True

    def is_vote_finished(self):
        # TODO: create DB to store this
        st.session_state

    def set_vote_started(self, status):
        # TODO: create DB to store this
        pass

    def set_vote_finished(self, status):
        # TODO: create DB to store this
        pass

    @staticmethod
    def get_time_until_next_midday():
        now = datetime.now()
        midday = now.replace(hour=12, minute=0, second=0, microsecond=0)

        if now > midday:
            midday = midday.replace(day=midday.day + 1)

        return (midday - now)