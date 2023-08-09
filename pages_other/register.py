import random
import string
import argparse
import streamlit as st
import streamlit_authenticator as stauth
import db_handler

def generate_password(user):
    characters = string.ascii_letters + string.digits
    seed = sum(ord(char) for char in user)
    random.seed(seed)
    password = ''.join(random.choice(characters) for _ in range(12))
    return password


def store_credential(username, name, password):
    # Hash password/passwords
    hashed_pass = stauth.Hasher([password]).generate()

    conn = db_handler.init_connection()
    conn.autocommit = True
    query = db_handler.register_user(username, name, hashed_pass[0])
    db_handler.insert_query(conn, query)

def main():
    parser = argparse.ArgumentParser(description='Generate passwords based on input strings')
    parser.add_argument('input_strings', nargs='+', type=str, help='Input strings to generate passwords')

    args = parser.parse_args()

    for user in args.input_strings:

        try:
            user, username = user.split(':')
        except ValueError:
            raise("Input users in the format: 'user1:username1 user2:username2'")

        password = generate_password(user)
        store_credential(user, username, password)
        print(f"\nUser: {user}\nPassword:{password}\n")


if __name__ == '__main__':
    main()