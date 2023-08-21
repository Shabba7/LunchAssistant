import db.db_handler as db
import streamlit as st
import utils.password_generator as pwgen
import streamlit_authenticator as stauth
from psycopg2.errors import UniqueViolation

class Page:
    def run(self):


        register_col, recover_col = st.columns(2)

        with register_col.form("register"):
            st.markdown("### Register User")
            handle = st.text_input(
                "Username",
                placeholder="jsmith",
                max_chars=32,
            )

            name = st.text_input(
                "Name",
                placeholder="John Smith",
                max_chars=32,
            )

            if st.form_submit_button("Register"):
                pw, hash = pwgen.generate_password(handle)

                try:
                    db.register_user(handle, name, hash)
                    st.success(f"Password: {pw}")
                except UniqueViolation:
                    st.error("User already exists")
                except Exception as e:
                    st.write(e)
                st.cache_data.clear()


        with recover_col.form("recover_pass"):
            st.markdown("### Recover Password")
            handle = st.text_input(
                "Username",
                placeholder="jsmith",
                max_chars=32,
            )
            if st.form_submit_button("Recover password"):
                pw, _ = pwgen.generate_password(handle)
                st.success(f"Password: {pw}")



        # if st.secrets["dev"]["dev_on"]:
        #     _,_,col,_,_ = st.columns(5)
        #     if col.button("NUKE"):
        #         db.rebuild()
        #         st.success("Now I Am Become Death, the Destroyer of Worlds")
