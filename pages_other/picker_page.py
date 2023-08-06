import streamlit as st
import pandas as pd
import random
import altair as alt
import os

class Page:
    user = None
    restaurants = []
    df = None
    def __init__(self, user) -> None:
        self.user = user
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center; } </style>', unsafe_allow_html=True)
        st.markdown(
            """
        <style>
        [role=radiogroup]{
        gap: 3rem;
        display: flex;
        justify-content: space-evenly;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        self.update()

    def run(self):
        self.vote()
        self.submit()
        self.list_rest()

    def vote(self):
        restaurants = list(self.df['Restaurant'])
        user = self.user
        self.user_votes = {}

        # Initialize session_state if not already present
        if "votes" not in st.session_state:
            st.session_state.votes = {restaurant: 0 for restaurant in restaurants}


        # Create a button to start the vote
        if "vote_started" not in st.session_state:
            _,_,col,_,_ = st.columns(5)
            with col:
                if st.button("Start Vote"):
                    # Pick 3 random restaurants from the list for voting
                    random_restaurants = random.sample(restaurants, 3)
                    random_restaurants.sort()
                    st.session_state["random_restaurants"] = random_restaurants
                    st.session_state["vote_started"] = True
                    st.experimental_rerun()

        # Display the vote bars if the vote has started
        if "vote_started" in st.session_state:
            if st.session_state["vote_started"]:
                # Create a radio button for the restaurants

                chosen_restaurant = st.radio("", st.session_state["random_restaurants"])

                # Update the user's vote in session_state
                self.user_votes[user] = chosen_restaurant

                # Update the vote count based on user votes
                vote_counts = {restaurant: list(self.user_votes.values()).count(restaurant)
                            for restaurant in st.session_state["random_restaurants"]}

                # Create a DataFrame from the vote_counts dictionary
                df = pd.DataFrame(list(vote_counts.items()), columns=["Restaurant", "Votes"])

                # Create an Altair chart
                chart = alt.Chart(df).mark_bar().encode(
                    y=alt.Y('Votes:Q', axis=alt.Axis(title='Votes')),
                    x=alt.X('Restaurant:N', axis=alt.Axis(title='Restaurant', labelAngle=0)),
                    tooltip=['Restaurant', 'Votes']
                )

                # Hide the legend
                chart = chart.configure_legend(orient='none')

                # Display the chart
                st.altair_chart(chart, use_container_width=True)

    def submit(self):

        if 'text' not in st.session_state:
            st.session_state.text = ''

        def submit():
            st.session_state.text = st.session_state.widget
            st.session_state.widget = ''

        st.text_input('Add restaurant', key='widget', on_change=submit)
        if st.session_state.text.strip() != "" and st.session_state.text not in self.restaurants:
            self.save_data({'Restaurant': st.session_state.text, 'User': self.user})
            st.toast("Restaurant added! Thanks for contributing!", icon='😍')
            self.update()

    def list_rest(self):
        # Display the list of restaurants
        st.header("List of Restaurants")

            # Displaying the table
        st.dataframe(self.df,use_container_width=True, hide_index=True)

    def save_data(self, data):
        # For demonstration purposes, let's just append the data to a CSV file
        df = pd.DataFrame([data])
        df.to_csv("list_of_restaurants.csv", mode="a", header=not os.path.exists("list_of_restaurants.csv"), index=False)

    def update(self):
        self.df = pd.read_csv("list_of_restaurants.csv")
        self.restaurants = self.df['Restaurant']

