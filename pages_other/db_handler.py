import psycopg2
import streamlit as st

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

def run_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
def insert_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
    
def register_user(username, name, hash):
    return f"INSERT INTO users (username, name, hash) VALUES('{username}', '{name}', '{hash}');"