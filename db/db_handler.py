import psycopg2
import streamlit as st
import psycopg2.extras
from datetime import date, timedelta
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

def _fetch_one(query, params):
    conn = init_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()

def _fetch_one_no_params(query):
    conn = init_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        return cur.fetchone()

def _fetch_all_no_params(query):
    conn = init_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()

def _insert(query, params):
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query, params)

def fetch_user_id(username):
    query = "SELECT user_id FROM users WHERE user_handle = %s"
    return _fetch_one(query,(username,))[0]

def register_user(username, name, hash):
    query = "INSERT INTO users (user_handle, user_name, pass_hash) VALUES(%s, %s, %s);"
    _insert(query, (username, name, hash))

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

@st.cache_data(ttl=10)
def fetch_money_spent_this_month():
    # Query to calculate money spent in the current month
    current_month = date.today().strftime('%Y-%m')
    return _fetch_money_spent_month(current_month)

@st.cache_data(ttl=10)
def fetch_money_spent_previous_month():
    # Query to calculate money spent in the previous month
    previous_month = (date.today().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    return _fetch_money_spent_month(previous_month)

def _fetch_money_spent_month(month):
    # Query to calculate money spent

    query = f"""
        SELECT SUM(price_paid)
        FROM reviews
        WHERE EXTRACT(YEAR FROM review_date) = EXTRACT(YEAR FROM TIMESTAMP '{month}-01')
        AND EXTRACT(MONTH FROM review_date) = EXTRACT(MONTH FROM TIMESTAMP '{month}-01')
    """

    if not (money := _fetch_one_no_params(query)[0]):
        money=0

    return float(money)

@st.cache_data(ttl=10)
def fetch_restaurants_visited_this_month():
    # Query to calculate money spent
    current_month = date.today().strftime('%Y-%m')
    return _fetch_restaurants_visited_month(current_month)

@st.cache_data(ttl=10)
def fetch_restaurants_visited_previous_month():
    # Query to calculate money spent
    previous_month = date.today().strftime('%Y-%m')
    return _fetch_restaurants_visited_month(previous_month)

def _fetch_restaurants_visited_month(month):
    # Query to calculate money spent
    query = f"""
        SELECT COUNT(DISTINCT res_id)
        FROM reviews
        WHERE EXTRACT(YEAR FROM review_date) = EXTRACT(YEAR FROM TIMESTAMP '{month}-01')
        AND EXTRACT(MONTH FROM review_date) = EXTRACT(MONTH FROM TIMESTAMP '{month}-01')
    """

    if not (restaurants := _fetch_one_no_params(query)[0]):
        restaurants=0

    return restaurants

@st.cache_data(ttl=10)
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

@st.cache_data(ttl=10)
def fetch_total_money_spent():
    # Query to calculate total money spent
    query = "SELECT SUM(price_paid) FROM reviews"
    return float(_fetch_one_no_params(query)[0])

@st.cache_data(ttl=10)
def fetch_biggest_spender():
    # Query to find the user with the highest total spending and their user_name
    previous_month = (date.today().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    query = f"""
        SELECT u.user_name, SUM(r.price_paid) AS total_spending
        FROM users u
        JOIN reviews r ON u.user_id = r.user_id
        WHERE EXTRACT(YEAR FROM r.review_date) = EXTRACT(YEAR FROM TIMESTAMP '{previous_month}-01')
        AND EXTRACT(MONTH FROM r.review_date) = EXTRACT(MONTH FROM TIMESTAMP '{previous_month}-01')
        GROUP BY u.user_name
        ORDER BY total_spending DESC
        LIMIT 1
    """
    if not (bigest_spender := _fetch_one_no_params(query)):
        bigest_spender = ('---','---')

    return bigest_spender

@st.cache_data(ttl=10)
def fetch_reviews_done_this_month():
    # Query to count reviews done this month
    current_month = date.today().strftime('%Y-%m')
    return _fetch_reviews_done_month(current_month)

@st.cache_data(ttl=10)
def fetch_reviews_done_previous_month():
    # Query to count reviews done previous month
    previous_month = date.today().strftime('%Y-%m')
    return _fetch_reviews_done_month(previous_month)

def _fetch_reviews_done_month(month):
    # Query to count reviews done in month
    query = f"""
        SELECT COUNT(*)
        FROM reviews
        WHERE EXTRACT(YEAR FROM review_date) = EXTRACT(YEAR FROM TIMESTAMP '{month}-01')
        AND EXTRACT(MONTH FROM review_date) = EXTRACT(MONTH FROM TIMESTAMP '{month}-01')
    """

    if not (reviews := _fetch_one_no_params(query)[0]):
        reviews=0

    return reviews


def fetch_restaurants_locations():
    return _fetch_all_no_params("SELECT res_name, res_loc from restaurants;")

def fetch_restaurants_names():
    return _fetch_all_no_params("SELECT res_name from restaurants;")

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
