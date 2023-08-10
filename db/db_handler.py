import psycopg2
import streamlit as st


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
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def _insert(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)


def register_user(username, name, hash):
    return f"INSERT INTO users (username, name, hash) VALUES('{username}', '{name}', '{hash}');"


st.cache_data(ttl=60)
def fetch_restaurants_avg():
    query = """
        SELECT re.res_name, count(rv.*) review_count,
            AVG(rv.food_rating) avg_food, AVG(rv.service_rating) avg_service, AVG(rv.price_rating) avg_price, AVG(rv.price_paid) avg_paid
        FROM restaurants re
        LEFT JOIN reviews rv ON re.res_id = rv.res_id
        GROUP BY re.res_id
        HAVING COUNT(rv.*) > 0;
    """
    st.write("Average ratings of restaurants with at least one review")
    return _fetch_all_no_params(query)


def fetch_restaurants_location():
    return _fetch_all_no_params("SELECT * from restaurants;")


# https://stackoverflow.com/questions/25577461/postgresql-earthdistance-earth-box-with-radius
