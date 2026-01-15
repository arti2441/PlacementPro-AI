import streamlit as st
from database import create_tables, add_user, get_users

create_tables()

st.title("SQLite Data Structure Demo")

name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Add User"):
    add_user(name, email)
    st.success("User added successfully!")

st.subheader("Stored Users")
users = get_users()
st.table(users)