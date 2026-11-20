import streamlit as st

from config import DATA_SOURCE, PROJECT_DESCRIPTION, PROJECT_TITLE

st.title(PROJECT_TITLE)
st.write(PROJECT_DESCRIPTION)
st.caption("Frontend demo · Model integration pending")

st.divider()
explore, predict = st.columns(2, gap="medium")

with explore.container(border=True):
    st.subheader("Explore shopping sessions")
    st.write("Compare purchase rates by visitor type and day of the week using example sessions or a UCI CSV.")
    st.page_link("views/data_explorer.py", label="Open Data Explorer", icon=":material/bar_chart:")

with predict.container(border=True):
    st.subheader("Enter a session")
    st.write("Fill in browsing activity and review the details that will be sent to the prediction model.")
    st.page_link("views/prediction.py", label="Open Prediction", icon=":material/touch_app:")

st.link_button("View the UCI dataset", DATA_SOURCE)
