import altair as alt
from datetime import datetime, timedelta
import db.db_handler as db
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stcomponents


def build_timer(time):
    timer_html = """
<script>
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        hours = parseInt(timer / 3600, 10);
        minutes = parseInt((timer % 3600) / 60, 10);
        seconds = parseInt(timer % 60, 10);

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = hours + ":" + minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    display = document.querySelector('#time');
    startTimer("""+(str(time.total_seconds()))+""", display);
};
</script>

<html>
  <h4 style='font-family: "Source Sans Pro", sans-serif; font-weight: 600; color: rgb(49, 51, 63); line-height: 1.2; margin-bottom: 0px; margin-top: 0px;'>Poll will close in <span id="time">...</span></h4>
</html>
"""
    return timer_html
    # return timer_html

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
        width="600" height="450"\
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
        if st.secrets["dev"]["dev_on"]:
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

    @staticmethod
    def is_vote_window_open():
        return Page.VOTE_OPEN_HOUR <= datetime.now().time().hour <= Page.VOTE_CLOSE_HOUR

    def off_voting_hours(self):
        st.markdown(
            f"<p style='text-align: center; background-color:#fffce6; color: #926C05;'>Poll is closed at the moment 🥸<br>Come back tomorrow between {Page.VOTE_OPEN_HOUR}am and {Page.VOTE_CLOSE_HOUR}am!</p>",
            unsafe_allow_html=True,
        )
        with st.expander("Latest poll", expanded = True):
            self.latest_election()
        self.add_restaurant()

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
            db.start_restaurant_election(restaurant_ids)
            st.experimental_rerun()

    def vote(self, id):
        restaurants = db.fetch_restaurant_election_options(id)
        names = [r["res_name"] for r in restaurants]
        start_time = restaurants[0]["start_time"]
        time_left = self.calculate_times(start_time)

        st.write("### Select one:")
        choice = st.radio(" ", names, label_visibility="collapsed")
        if st.button("Submit/Update vote"):
            restaurant_id = [r[1] for r in restaurants if r[2] == choice][0]
            db.add_restaurant_vote(st.session_state["user_id"], restaurant_id)
            st.toast('Vote submitted!', icon='😍')
        stcomponents.html(build_timer(time_left), height=30)
        stcomponents.html(build_map(choice), height=450)

    def calculate_times(self, start_time):
        end_time = start_time + timedelta(hours=4)
        return end_time - datetime.now()

    @staticmethod
    def is_vote_window_open():
        return Page.VOTE_OPEN_HOUR <= datetime.now().time().hour <= Page.VOTE_CLOSE_HOUR
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
