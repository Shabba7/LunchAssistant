import random
import string
import argparse
import streamlit_authenticator as stauth

def generate_password(user):
    characters = string.ascii_letters + string.digits
    seed = sum(ord(char) for char in user)
    random.seed(seed)
    password = ''.join(random.choice(characters) for _ in range(12))
    return password


def store_credential(username, password):
    # Hash password/passowords
    hashed_pass = stauth.Hasher([password]).generate()
    print(hashed_pass[0])
    #db_handler(username,hashed_pass)


def main():
    parser = argparse.ArgumentParser(description='Generate passwords based on input strings')
    parser.add_argument('input_strings', nargs='+', type=str, help='Input strings to generate passwords')

    args = parser.parse_args()

    for user in args.input_strings:
        password = generate_password(user)
        store_credential(user,password)
        print(f"\nUser: {user}\nPassword:{password}\n")


if __name__ == '__main__':
    main()