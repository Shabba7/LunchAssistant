import bcrypt
import random
import streamlit_authenticator as stauth
import string

def generate_password(user):
    characters = string.ascii_letters + string.digits
    seed = sum(ord(char) for char in user)
    random.seed(seed)
    password = ''.join(random.choice(characters) for _ in range(12))

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return password, hashed