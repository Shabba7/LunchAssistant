import random
import streamlit_authenticator as stauth
import string
import streamlit as st

def generate_password(user):
    characters = string.ascii_letters + string.digits
    random.seed(f'{st.secrets["auth"]["seed"]}{user}')
    password = ''.join(random.choice(characters) for _ in range(12))

    hashed = stauth.Hasher([password]).generate()[0]

    return password, hashed
