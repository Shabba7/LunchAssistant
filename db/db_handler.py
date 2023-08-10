import psycopg2
import streamlit as st
import psycopg2.extras
from pathlib import Path


@st.cache_resource
def init_connection():
    conn = psycopg2.connect(**st.secrets["postgres"])
    conn.autocommit = True
    return conn


# def _fetch_all(conn, query):
#     with conn.cursor() as cur:
#         cur.execute(
#             query,
#             params=dict(owner=k, pet=pet_owners[k])
#         )
#         cur.execute(query)
#         return cur.fetchall()


def _fetch_all_no_params(query):
    conn = init_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def _insert(query, params):
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query, params)


def register_user(username, name, hash):
    query = "INSERT INTO users (user_handle, user_name, pass_hash) VALUES(%s, %s, %s);"
    return _insert(query, (username, name, hash))


st.cache_data(ttl=60)
def fetch_restaurants_avg():
    # Average ratings of restaurants with at least one review
    query = """
        SELECT re.res_name, count(rv.*) review_count,
            ROUND(AVG(rv.food_rating),2) avg_food,
            ROUND(AVG(rv.service_rating),2) avg_service,
            ROUND(AVG(rv.price_rating),2) avg_price,
            ROUND(AVG(rv.price_paid),2) avg_paid
        FROM restaurants re
        LEFT JOIN reviews rv ON re.res_id = rv.res_id
        GROUP BY re.res_id
        HAVING COUNT(rv.*) > 0;
    """
    return _fetch_all_no_params(query)


def fetch_restaurants_location():
    return _fetch_all_no_params("SELECT * from restaurants;")

def get_credentials():
    return _fetch_all_no_params("SELECT user_handle, user_name, user_email, pass_hash FROM users;")


def reset_table():
    with open(Path('db','create.sql'),'r') as create_file:
        create = create_file.read()
    with open(Path('db','insert.sql'),'r') as insert_file:
        insert = insert_file.read()
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(create)
        cur.execute(insert)
        st.success('Now I Am Become Death, the Destroyer of Worlds')

# https://stackoverflow.com/questions/25577461/postgresql-earthdistance-earth-box-with-radius
