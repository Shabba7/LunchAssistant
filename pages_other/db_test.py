import streamlit as st

class Page:
    cursor = None
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        pass

    def run(self):
        st.title("DB Test")
     
        rows = self.cursor("SELECT * from test;")

        # Print results.
        for row in rows:
            st.write(f"{row[0]} : {row[1]}")



