import db.db_handler as db
import streamlit as st
import streamlit_authenticator as stauth

@st.cache_data()
def get_credentials_from_db():
    credentials_dict = {'usernames': {}}
    # Populate credentials dict with users from DB
    for row in db.get_credentials():
        credentials_dict['usernames'][row['user_handle']] = {
            'email': row['user_email'],
            'name': row['user_name'],
            'password': row['pass_hash']
        }
    return credentials_dict

def get_auth():
    return stauth.Authenticate(
        get_credentials_from_db(),
        'CoEBe_cookie',
        'CoEBe_key',
        180,
    )

class Page:

    def run(self):
        authenticator = get_auth()
        _, authentication_status, username = authenticator.login('Login', 'main')
        if authentication_status:
            st.session_state['user_id'] = db.fetch_user_id(username)
        return (authentication_status, username)



