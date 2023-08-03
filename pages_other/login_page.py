import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

class Page:
    authenticator = None
    def __init__(self) -> None:
        with open('credentials.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        self.authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        )
    def run(self):

        name, authentication_status, username = self.authenticator.login('Login', 'main')
        return (authentication_status, username)



