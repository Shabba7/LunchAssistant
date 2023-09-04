import altair as alt
from datetime import datetime, timedelta
import db.db_handler as db
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stcomponents
import css.progress_bar as pb
import pytz

def build_map(choice):
    name = choice.replace(" ", "+")
    map_url = f'https://www.google.com/maps/embed/v1/directions\
?key={st.secrets["google"]["api_key"]}\
&origin=Rua+Monsenhor+Fonseca+Soares+44\
&destination={name}+Porto\
&mode=walking\
&language=pt\
&region=pt'

    gmap = f'\
        <iframe\
        resize: both;\
        overflow: auto;\
        width="100%" height="450"\
        frameborder="0" style="border:0"\
        referrerpolicy="no-referrer-when-downgrade"\
        src="{map_url}"\
        allowfullscreen>\
        </iframe>\
    '
    return gmap

class Page:

    VOTE_OPEN_HOUR = 8
    VOTE_CLOSE_HOUR = 12

    def run(self):

        # if st.secrets["dev"]["dev_on"]:
        #     self.debug_menu()

        if not self.is_vote_window_open():
            self.off_voting_hours()
        else:
            self.on_voting_hours()

    def debug_menu(self):
        with st.sidebar:
            st.header("DEBUG MENU")
            Page.VOTE_OPEN_HOUR = st.number_input("OPEN HOUR", value=Page.VOTE_OPEN_HOUR, min_value=0, max_value=Page.VOTE_CLOSE_HOUR-1)
            Page.VOTE_CLOSE_HOUR = st.number_input("CLOSE HOUR", value=Page.VOTE_CLOSE_HOUR, min_value=Page.VOTE_OPEN_HOUR+1, max_value=24)
            if st.button("FORCE CLOSE VOTE"):
                db.end_restaurant_election()

    @staticmethod
    def is_vote_window_open():
        return Page.VOTE_OPEN_HOUR <= datetime.now(pytz.timezone("Europe/London")).time().hour < Page.VOTE_CLOSE_HOUR

    def off_voting_hours(self):

        #HACK
        if db.is_restaurant_election_open() != None:
            db.end_restaurant_election()

        st.markdown(
            f"<p style='text-align: center; background-color:#fffce6; color: #926C05;'>Poll is closed at the moment 🥸<br>Come back tomorrow between {Page.VOTE_OPEN_HOUR}am and {Page.VOTE_CLOSE_HOUR}am!</p>",
            unsafe_allow_html=True,
        )
        with st.expander("Latest poll", expanded = True):
            self.latest_election()

    def on_voting_hours(self):
        id = db.is_restaurant_election_open()
        if not id:
            self.setup_vote()
        else:
            self.vote(id)

#region Voting
    def latest_election(self):
        votes, totals = db.fetch_lastest_election_data()
        df_votes = pd.DataFrame(votes, columns=['Who','Where'])
        df_totals = pd.DataFrame(totals, columns=['Restaurant','Votes'])

        chart = alt.Chart(df_totals).mark_bar().encode(
            y=alt.Y('Votes:Q', axis=alt.Axis(title='Votes')),
            x=alt.X('Restaurant:N', axis=alt.Axis(title='Restaurant', labelAngle=0)),
            tooltip=['Restaurant', 'Votes']
        )

        # Hide the legend
        chart = chart.configure_legend(orient='none')

        # Display the chart
        st.altair_chart(chart, use_container_width=True)

        # Display votes list
        st.dataframe(df_votes, use_container_width=True, hide_index=True)

    def setup_vote(self):
        _,_,col,_,_ = st.columns(5)
        if col.button("Start new vote"):
            restaurant_ids = db.fetch_n_random_restaurants(3)
            # TODO: Check if this is needed
            db.start_restaurant_election(restaurant_ids)
            st.experimental_rerun()

    def vote(self, id):
        restaurants = db.fetch_restaurant_election_options(id)
        names = [r["res_name"] for r in restaurants]
        time_left = self.calculate_times()

        st.write("### Select one:")
        choice = st.radio(" ", names, label_visibility="collapsed")
        stcomponents.html(pb.build_timer(time_left), height=50)
        _, center, _ = st.columns([0.24, 0.3, 0.1])

        if center.button("Submit/Update vote"):
            restaurant_id = [r[1] for r in restaurants if r[2] == choice][0]
            db.add_restaurant_vote(st.session_state["user_id"], restaurant_id)
            st.toast('Vote submitted!', icon='😍')
        stcomponents.html(build_map(choice), height=450)

    def calculate_times(self):
        end_time = datetime.now(pytz.timezone("Europe/London")).replace(hour=Page.VOTE_CLOSE_HOUR,minute=0,second=0)
        return end_time - datetime.now(pytz.timezone("Europe/London"))

#endregion
