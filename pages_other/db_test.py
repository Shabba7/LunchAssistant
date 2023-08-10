import db.db_handler as db
import streamlit as st
import utils.password_generator as pwgen
import streamlit_authenticator as stauth


class Page:
    def run(self):
        st.title("Register user")

        with st.form("my_form"):
            handle = st.text_input(
                "username",
                placeholder="jsmith",
                max_chars=32,
                label_visibility="hidden",
            )
            name = st.text_input(
                "name",
                placeholder="John Smith",
                max_chars=32,
                label_visibility="hidden",
            )
            password = st.text_input(
                "password",
                placeholder="password",
                type="password",
                max_chars=32,
                label_visibility="hidden",
            )

            submitted = st.form_submit_button("Register")
            if submitted:
                pw, hash = pwgen.generate_password(handle)
                
                ret = db.register_user(handle, name, hash)
                st.write(ret, pw)

        rows = db.fetch_restaurants_avg()
        st.write(rows)