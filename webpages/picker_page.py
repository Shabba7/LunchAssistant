# import datetime
# class CustomDatetime(datetime.datetime):
#     _hour = 9
#     @classmethod
#     def now(cls, tz=None):
#         return super().now(tz).replace(hour=cls._hour, minute=0, second=0, microsecond=0)
#     @classmethod
#     def set_hour(cls, hour):
#         cls._hour = hour
#
# datetime.datetime = CustomDatetime


######################################################################

import altair as alt
import asyncio
from datetime import datetime, timedelta
import db.db_handler as db
import pandas as pd
import random
import streamlit as st
import streamlit.components.v1 as stcomponents

my_html = """
<script>
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 * 5,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};
</script>

<body>
  <div>Registration closes in <span id="time">05:00</span> minutes!</div>
</body>
"""

async def periodic():
    while True:
        st.write("Hello world")
        r = await asyncio.sleep(1)
        st.write(f"asyncio sleep ? {r}")

class Page:

    VOTE_OPEN_HOUR = 8
    VOTE_CLOSE_HOUR = 12

    def run(self):
        # stcomponents.html(my_html)
        # asyncio.run(periodic())

        self.debug_menu()

        if not self.is_vote_window_open():
            self.off_voting_hours()
        else:
            self.on_voting_hours()

    def debug_menu(self):
        with st.sidebar:
            st.header("DEBUG MENU")
            Page.VOTE_OPEN_HOUR = st.number_input("OPEN HOUR", value=Page.VOTE_OPEN_HOUR, min_value=0, max_value=Page.VOTE_CLOSE_HOUR-1)
            Page.VOTE_CLOSE_HOUR = st.number_input("CLOSE HOUR", value=Page.VOTE_CLOSE_HOUR, min_value=Page.VOTE_OPEN_HOUR+1, max_value=23)
            if st.button("FORCE CLOSE VOTE"):
                db.end_restaurant_election()

    def off_voting_hours(self):
        st.markdown(
            f"<p style='text-align: center; background-color:#fffce6; color: #926C05;'>Poll is closed at the moment 🥸<br>Come back tomorrow between {Page.VOTE_OPEN_HOUR}am and {Page.VOTE_CLOSE_HOUR}am!</p>",
            unsafe_allow_html=True,
        )
        with st.expander("Latest poll", expanded = True):
            self.latest_election()
        self.add_restaurant()

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

    def on_voting_hours(self):
        id = db.is_restaurant_election_open()
        if not id:
            self.setup_vote()
        else:
            self.vote(id)



#region Voting
    def setup_vote(self):
        _,_,col,_,_ = st.columns(5)
        if col.button("Start new vote"):
            restaurant_ids = db.fetch_n_random_restaurants(2)
            db.start_restaurant_election(restaurant_ids)
            st.experimental_rerun()

    def vote(self, id):
        restaurants = db.fetch_restaurant_election_options(id)
        names = [r["res_name"] for r in restaurants]
        locs = [r["res_loc"] for r in restaurants]
        start_time = restaurants[0]["start_time"]
        time_left = self.calculate_times(start_time)

        st.write("### Select one:")
        lcol, rcol = st.columns(2)
        with lcol:
            choice = st.radio(" ", names, label_visibility="collapsed")
        with rcol:
            st.write("SHOW DATA HERE")
        _,ccol,_ = st.columns(3)
        with ccol:
            st.write(f'###### Poll will close in {str(time_left).split(".")[0]}')
            if st.button("Submit/Update vote"):
                restaurant_id = [r[1] for r in restaurants if r[2] == choice][0]
                db.add_restaurant_vote(st.session_state["user_id"], restaurant_id)
                st.toast('Vote submitted!', icon='😍')

    def calculate_times(self, start_time):
        end_time = self.get_time_n_hours_ahead(start_time, 4)
        time_left = end_time - datetime.now()
        return time_left

    @staticmethod
    def is_vote_window_open():
        return Page.VOTE_OPEN_HOUR <= datetime.now().time().hour <= Page.VOTE_CLOSE_HOUR

    def vote_in_progress(self):
        # Create a radio button for the restaurants
        st.write("### Select one:")
        #chosen_restaurant = st.radio(" ", st.session_state["random_restaurants"])
        time_left = self.get_time_until_next_midday()
        st.write(f'###### Polls will close in {str(time_left).split(".")[0]}')
        # progress_bar = st.progress(1)
        # progress_bar.progress(1- (time_left.total_seconds() / (60*60*24)))
        # if time_left.total_seconds() <= 0:
        #     self.set_vote_started(False)
        #     self.set_vote_finished(True)


    @staticmethod
    def get_time_n_hours_ahead(start, hours):
        future_time = start + timedelta(hours=hours)
        return future_time
#endregion

#region Add Restaurants
    def add_restaurant(self):
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
#endregion


###################################################################


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