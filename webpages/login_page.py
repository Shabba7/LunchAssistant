import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import db.db_handler as db

class Page:
    authenticator = None
    def __init__(self) -> None:
        self.authenticator = stauth.Authenticate(
            self._get_credentials_from_db(),
            'CoEBe_cookie',
            'CoEBe_key',
            180,
            )

    def run(self):
        _, authentication_status, username = self.authenticator.login('Login', 'main')
        if authentication_status:
            st.session_state['user_id'] = db.fetch_user_id(username)
        return (authentication_status, username)

    @st.cache_data()
    def _get_credentials_from_db(_self):
        credentials_dict = {'usernames': {}}
        # Populate credentials dict with users from DB
        for row in db.get_credentials():
            credentials_dict['usernames'][row['user_handle']] = {
                'email': row['user_email'],
                'name': row['user_name'],
                'password': row['pass_hash']
            }
        return credentials_dict



