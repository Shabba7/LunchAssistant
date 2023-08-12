import psycopg2
import streamlit as st
import psycopg2.extras
from pathlib import Path

#region DB Access
@st.cache_resource
def _init_connection():
    conn = psycopg2.connect(**st.secrets["postgres"])
    conn.autocommit = True
    return conn

def _fetch_one(query, params):
    conn = _init_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()[0]

def _fetch_all(query, params):
    conn = _init_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()

def _fetch_all_no_params(query):
    conn = _init_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()

def _insert(query, params):
    conn = _init_connection()
    with conn.cursor() as cur:
        cur.execute(query, params)

def rebuild():
    with open(Path("db", "create.sql"), "r") as create_file:
        create = create_file.read()
    with open(Path("db", "insert.sql"), "r") as insert_file:
        insert = insert_file.read()
    conn = _init_connection()
    with conn.cursor() as cur:
        cur.execute(create)
        cur.execute(insert)
#endregion


#region User
def fetch_user_id(username):
    query = "SELECT user_id FROM users WHERE user_handle = %s"
    return _fetch_one(query,(username,))

def get_credentials():
    return _fetch_all_no_params("SELECT user_handle, user_name, user_email, pass_hash FROM users;")

def register_user(username, name, hash):
    query = "INSERT INTO users (user_handle, user_name, pass_hash) VALUES(%s, %s, %s);"
    _insert(query, (username, name, hash))
#endregion


#region Restaurant
st.cache_data(ttl=60)
def fetch_restaurants_names():
    names = _fetch_all_no_params("SELECT res_name from restaurants;")
    return [name[0] for name in names]

def fetch_restaurants_locations():
    return _fetch_all_no_params("SELECT res_name, res_loc from restaurants;")

def register_restaurant(res_name, res_loc, res_user):
    query = "INSERT INTO restaurants (res_name, res_loc, res_user) VALUES(%s, %s, %s);"
    return _insert(query, (res_name, res_loc, res_user))

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
#endregion


#region Review
def submit_review(user_id, res_name, food_rating, service_rating, price_rating, price_paid, date):
    # Get the restaurant ID from its name and insert review into the review table
    query = """
        WITH restaurant_id AS (
            SELECT res_id
            FROM restaurants
            WHERE res_name = %s
        )
        INSERT INTO reviews (user_id, res_id, food_rating, service_rating, price_rating, price_paid, review_date)
        VALUES (%s, (SELECT res_id FROM restaurant_id), %s, %s, %s, %s, %s);
    """
    values = (res_name, user_id, food_rating, service_rating, price_rating, price_paid, date)
    _insert(query, values)
#endregion


# https://stackoverflow.com/questions/25577461/postgresql-earthdistance-earth-box-with-radius
