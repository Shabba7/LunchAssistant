import logging
from pathlib import Path
import psycopg2
import psycopg2.extras
import streamlit as st

logging.basicConfig(filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")


# region DB Access
@st.cache_resource
def _init_connection():
    logging.warning("Connecting to database")
    conn = psycopg2.connect(**st.secrets["postgres"])
    conn.autocommit = True
    return conn

def _fetch_one(query, params):
    conn = _init_connection()
    logging.warning(f"Fetching @ {query} : {params}")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()[0]

def _fetch_one_no_params(query):
    conn = _init_connection()
    logging.warning(f"Fetching @ {query}")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        if row := cur.fetchone():
            return row[0]
        else:
            return None

def _fetch_all(query, params):
    conn = _init_connection()
    logging.warning(f"Fetching @ {query} : {params}")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()

def _fetch_all_no_params(query):
    conn = _init_connection()
    logging.warning(f"Fetching @ {query}")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()

def _batch_fetch_all_no_params(queries):
    conn = _init_connection()
    logging.warning(f"Fetching @ {queries}")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        results = []
        for q in queries:
            cur.execute(q)
            results.append(cur.fetchall())
        return results

def _insert(query, params):
    conn = _init_connection()
    logging.warning(f"Inserting @ {query} : {params}")
    with conn.cursor() as cur:
        cur.execute(query, params)

def _execute(query):
    conn = _init_connection()
    logging.warning(f"Executing @ {query}")
    with conn.cursor() as cur:
        cur.execute(query)

def rebuild():
    with open(Path("db", "create.sql"), "r") as create_file:
        create = create_file.read()
    with open(Path("db", "insert.sql"), "r") as insert_file:
        insert = insert_file.read()
    conn = _init_connection()
    with conn.cursor() as cur:
        cur.execute(create)
        cur.execute(insert)
# endregion


# region User
def fetch_user_id(username):
    query = "SELECT user_id FROM users WHERE user_handle = %s"
    return _fetch_one(query, (username,))

def get_credentials():
    return _fetch_all_no_params("SELECT user_handle, user_name, user_email, pass_hash FROM users;")

def register_user(username, name, hash):
    query = "INSERT INTO users (user_handle, user_name, pass_hash) VALUES(%s, %s, %s);"
    _insert(query, (username, name, hash))
# endregion


# region voting
def start_restaurant_election(restaurant_ids):
    _insert("SELECT start_election(%s);", (restaurant_ids,))
    return True

def is_restaurant_election_open():
    return _fetch_one_no_params("SELECT id FROM elections WHERE end_time IS NULL;")

def fetch_restaurant_election_options(election_id):
    query = (
        "SELECT e.start_time, r.res_id, r.res_name "
        "FROM elections e "
        "JOIN restaurants r ON r.res_id = ANY(e.restaurant_ids) "
        "WHERE e.id = %s; "
    )
    params = (election_id,)
    return _fetch_all(query, params)

def end_restaurant_election():
    _execute("UPDATE elections SET end_time = current_timestamp WHERE end_time IS NULL")

def add_restaurant_vote(voter_id, restaurant_id):
    try:
        _insert("SELECT vote(%s, %s);", (voter_id, restaurant_id))
        return True
    except psycopg2.errors.RaiseException as e:
        if e.pgerror == "No open election available for voting.":
            st.error(e.pgerror)
        else:
            print("Error:", e.pgerror)
    except psycopg2.Error as e:
        print("Error:", e)

def fetch_lastest_election_data():
    q_votes = (
        "SELECT u.user_name, r.res_name "
        "FROM users u "
        "JOIN votes v ON u.user_id = v.voter_id "
        "JOIN restaurants r ON v.restaurant_id = r.res_id "
        "JOIN elections el ON v.election_id = el.id "
        "WHERE el.id = (SELECT id FROM elections ORDER BY start_time DESC LIMIT 1) "
        "ORDER BY u.user_name; "
    )
    q_total = (
        "SELECT r.res_name, COALESCE(COUNT(v.restaurant_id), 0) AS total_votes "
        "FROM (SELECT * FROM elections ORDER BY start_time DESC LIMIT 1) e "
        "JOIN restaurants r ON r.res_id = ANY(e.restaurant_ids) "
        "LEFT JOIN votes v ON r.res_id = v.restaurant_id "
        "GROUP BY r.res_name, e.id "
        "ORDER BY total_votes DESC, r.res_name; "
    )
    results = _batch_fetch_all_no_params([q_votes, q_total])
    return results[0], results[1]
# endregion


# region Restaurant
def fetch_restaurants_names():
    names = _fetch_all_no_params("SELECT res_name from restaurants;")
    return [name[0] for name in names]

def fetch_restaurants_locations():
    return _fetch_all_no_params("SELECT res_name, res_loc from restaurants;")

def fetch_n_random_restaurants(nr):
    query = "SELECT res_id FROM restaurants ORDER BY RANDOM() LIMIT %s;"
    params = (nr,)
    return _fetch_all(query, params)

def fetch_n_unknown_random_restaurants(nr):
    query = (
        "SELECT res_id, re.res_name, re.res_loc "
        "FROM restaurants re "
        "LEFT JOIN reviews rv ON re.res_id = rv.res_id "
        "WHERE rv.res_id IS NULL "
        "ORDER BY RANDOM() "
        "LIMIT %s; "
    )
    params = (nr,)
    return _fetch_all(query, params)

def fetch_n_random_restaurants_with_rating(nr, rat):
    query = (
        "SELECT res_id, re.res_name, re.res_loc "
        "FROM restaurants re "
        "JOIN ( "
        "    SELECT res_id "
        "    FROM reviews "
        "    WHERE food_rating > %s "
        "    GROUP BY res_id "
        ") filtered_res ON re.res_id = filtered_res.res_id "
        "ORDER BY RANDOM() "
        "LIMIT %s; "
    )
    params = (rat, nr)
    return _fetch_all(query, params)

def fetch_n_random_restaurants_within_radius(nr, radius):
    query = (
        "SELECT res_id, re.res_name, re.res_loc "
        "FROM restaurants "
        "WHERE earth_box(ll_to_earth(41.1578156070871, -8.635795928658316), %s) @> ll_to_earth(res_loc[1], res_loc[0]) "
        "ORDER BY RANDOM() "
        "LIMIT %s; "
    )
    params = (radius, nr)
    return _fetch_all(query, params)

def register_restaurant(res_name, res_loc, res_user):
    query = "INSERT INTO restaurants (res_name, res_loc, res_user) VALUES(%s, %s, %s);"
    return _insert(query, (res_name, res_loc, res_user))

st.cache_data(ttl=60)
def fetch_restaurants_avg():
    # Average ratings of restaurants with at least one review
    query = (
        "SELECT re.res_name, count(rv.*) review_count, "
        "    ROUND(AVG(rv.food_rating),2) avg_food, "
        "    ROUND(AVG(rv.service_rating),2) avg_service, "
        "    ROUND(AVG(rv.price_rating),2) avg_price, "
        "    ROUND(AVG(rv.price_paid),2) avg_paid "
        "FROM restaurants re "
        "LEFT JOIN reviews rv ON re.res_id = rv.res_id "
        "GROUP BY re.res_id "
        "HAVING COUNT(rv.*) > 0; "
    )
    return _fetch_all_no_params(query)
# endregion


# region Review
def submit_review(user_id, res_name, food_rating, service_rating, price_rating, price_paid, date):
    # Get the restaurant ID from its name and insert review into the review table
    query = (
        "WITH restaurant_id AS ( "
        "    SELECT res_id "
        "    FROM restaurants "
        "    WHERE res_name = %s "
        ") "
        "INSERT INTO reviews (user_id, res_id, food_rating, service_rating, price_rating, price_paid, review_date) "
        "VALUES (%s, (SELECT res_id FROM restaurant_id), %s, %s, %s, %s, %s); "
    )
    values = (res_name, user_id, food_rating, service_rating, price_rating, price_paid, date)
    _insert(query, values)
# endregion


# https://stackoverflow.com/questions/25577461/postgresql-earthdistance-earth-box-with-radius
