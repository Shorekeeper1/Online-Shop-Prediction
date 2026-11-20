"""Streamlit entry point for the shopper purchase prediction frontend."""
import streamlit as st

from config import PROJECT_TITLE

st.set_page_config(page_title=PROJECT_TITLE, page_icon=":material/shopping_cart:", layout="wide")

pages = [
    st.Page("views/home.py", title="Overview", icon=":material/dashboard:", default=True),
    st.Page("views/data_explorer.py", title="Data Explorer", icon=":material/bar_chart:"),
    st.Page("views/prediction.py", title="Prediction", icon=":material/touch_app:"),
]
st.navigation(pages, position="top").run()
