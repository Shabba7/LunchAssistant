import db.db_handler as db
import streamlit as st

class Page:

    def run(self):
        st.title("DB Test")
     
        rows = db.fetch_restaurants_avg()
        st.write(rows)




