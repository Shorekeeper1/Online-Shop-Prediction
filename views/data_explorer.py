import pandas as pd
import streamlit as st

from config import DATA_SOURCE, VISITOR_TYPES

REQUIRED_COLUMNS = {"VisitorType", "Weekend", "Revenue"}

EXAMPLE_SESSIONS = [
    ("New_Visitor", False, False),
    ("Returning_Visitor", False, False),
    ("Returning_Visitor", True, True),
    ("New_Visitor", True, False),
    ("Returning_Visitor", False, True),
    ("Returning_Visitor", False, False),
    ("New_Visitor", False, True),
    ("Returning_Visitor", True, False),
    ("Returning_Visitor", True, False),
    ("New_Visitor", False, False),
    ("Other", False, False),
    ("Returning_Visitor", False, False),
]


def read_sessions(upload) -> pd.DataFrame:
    if upload is None:
        return pd.DataFrame(EXAMPLE_SESSIONS, columns=["VisitorType", "Weekend", "Revenue"])

    sessions = pd.read_csv(upload)
    missing = REQUIRED_COLUMNS.difference(sessions.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}.")
    if sessions.empty:
        raise ValueError("The CSV has no shopping sessions.")
    if not sessions["VisitorType"].isin(VISITOR_TYPES).all():
        raise ValueError("VisitorType must contain New_Visitor, Returning_Visitor, or Other.")
    for column in ("Weekend", "Revenue"):
        flags = sessions[column].astype("string").str.strip().str.lower().map({
            "true": True, "false": False, "1": True, "0": False,
        })
        if flags.isna().any():
            raise ValueError(f"{column} must contain True/False or 1/0.")
        sessions[column] = flags.astype(bool)
    return sessions


st.title("Data Explorer")
st.write("Compare how often shopping sessions end in a purchase.")
upload = st.file_uploader("Upload the UCI shopping sessions CSV", type=["csv"])
if upload is None:
    st.info("Showing 12 fictional example sessions. Upload the UCI CSV to explore the actual dataset.")
    st.link_button("Get the UCI dataset", DATA_SOURCE)

try:
    sessions = read_sessions(upload)
except (ValueError, UnicodeError) as error:
    st.error(f"Could not read the CSV. {error}")
    st.stop()

visitors = st.multiselect(
    "Visitor types",
    options=list(VISITOR_TYPES),
    default=list(VISITOR_TYPES),
    format_func=VISITOR_TYPES.__getitem__,
)
days = st.segmented_control("Day type", ["All days", "Weekday", "Weekend"], default="All days")
filtered = sessions[sessions["VisitorType"].isin(visitors)]
if days in ("Weekday", "Weekend"):
    filtered = filtered[filtered["Weekend"] == (days == "Weekend")]
if filtered.empty:
    st.warning("No sessions match these filters.")
    st.stop()

purchases = int(filtered["Revenue"].sum())
count, converted, rate = st.columns(3)
count.metric("Sessions", f"{len(filtered):,}", border=True)
converted.metric("Purchases", f"{purchases:,}", border=True)
rate.metric("Purchase rate", f"{purchases / len(filtered):.1%}", border=True)

left, right = st.columns(2, gap="medium")
with left:
    st.subheader("Purchase outcomes")
    outcomes = pd.Series({"Purchase": purchases, "No purchase": len(filtered) - purchases}, name="Sessions")
    st.bar_chart(outcomes, horizontal=True, x_label="Sessions")
with right:
    st.subheader("Purchase rate by visitor type")
    rates = filtered.groupby("VisitorType")["Revenue"].mean().mul(100)
    rates = rates.rename(index=VISITOR_TYPES).rename("Purchase rate (%)")
    st.bar_chart(rates, horizontal=True, x_label="Purchase rate (%)")

st.subheader("Session records")
st.dataframe(
    filtered.rename(columns={"VisitorType": "Visitor type", "Revenue": "Purchased"})
    .assign(**{"Visitor type": filtered["VisitorType"].map(VISITOR_TYPES)}),
    hide_index=True,
    width="stretch",
)
