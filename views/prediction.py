import streamlit as st

from config import VISITOR_TYPES

st.title("Purchase Prediction")
st.write("Enter browsing details for a single shopping session.")
st.caption("This form previews the inputs. Purchase probability will be available when the model is connected.")

inputs, output = st.columns([3, 2], gap="large")
with inputs:
    with st.form("purchase_session"):
        st.subheader("Session details")
        visitor_type = st.selectbox(
            "Visitor type",
            options=list(VISITOR_TYPES),
            format_func=VISITOR_TYPES.__getitem__,
        )
        pages = st.number_input("Product pages viewed", min_value=0, value=8, step=1)
        seconds = st.number_input("Time on product pages (seconds)", min_value=0, value=180, step=1)
        weekend = st.checkbox("Session took place on a weekend")
        submitted = st.form_submit_button("Preview session", type="primary")

    if submitted:
        if pages == 0 and seconds > 0:
            st.session_state.pop("purchase_session_preview", None)
            st.error("Set the time to zero when no product pages were viewed.")
        else:
            st.session_state["purchase_session_preview"] = {
                "VisitorType": visitor_type,
                "ProductRelated": pages,
                "ProductRelated_Duration": seconds,
                "Weekend": weekend,
            }

with output:
    with st.container(border=True):
        st.subheader("Session preview")
        session = st.session_state.get("purchase_session_preview")
        if session is None:
            st.write("Submit the form to review the session details here.")
        else:
            st.metric("Product pages viewed", session["ProductRelated"])
            st.metric("Time on product pages", f"{session['ProductRelated_Duration']} s")
            day = "Weekend" if session["Weekend"] else "Weekday"
            st.write(f"{VISITOR_TYPES[session['VisitorType']]} · {day}")
            with st.expander("View input fields"):
                st.json(session)
        st.caption("Purchase probability · Model pending")
