# import streamlit as st
# from datetime import datetime
# import requests
# import pandas as pd
#
#
# API_URL = "http://127.0.0.1:8000"
#
#
# def analytics_tab():
#     col1, col2 = st.columns(2)
#     with col1:
#         start_date = st.date_input("Start Date", datetime(2024, 8, 1))
#
#     with col2:
#         end_date = st.date_input("End Date", datetime(2024, 8, 5))
#
#     if st.button("Get Analytics"):
#         payload = {
#             "start_date": start_date.strftime("%Y-%m-%d"),
#             "end_date": end_date.strftime("%Y-%m-%d")
#         }
#
#         response = requests.post(f"{API_URL}/analytics/", json=payload)
#         response = response.json()
#
#         data = {
#             "Category": list(response.keys()),
#             "Total": [response[category]["total"] for category in response],
#             "Percentage": [response[category]["percentage"] for category in response]
#         }
#
#         df = pd.DataFrame(data)
#         df_sorted = df.sort_values(by="Percentage", ascending=False)
#
#         st.title("Expense Breakdown By Category")
#
#         st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], width=0, height=0, use_container_width=True)
#
#         df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
#         df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
#
#         st.table(df_sorted)
#

import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"


def analytics_tab():
    st.markdown("Expense Analytics")
    st.markdown("Select a date range to view the breakdown of your expenses by category.")

    with st.form(key="analytics_form"):
        cols = st.columns(2)
        with cols[0]:
            start_date = st.date_input("Start Date", datetime(2024, 8, 1))
        with cols[1]:
            end_date = st.date_input("End Date", datetime(2024, 8, 5))

        st.markdown("---")
        submit = st.form_submit_button("🔍 Get Analytics")

    if submit:
        # Prepare payload
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        # Fetch analytics
        with st.spinner("Fetching analytics..."):
            resp = requests.post(f"{API_URL}/analytics/", json=payload)
        if resp.status_code != 200:
            st.error(" Failed to retrieve analytics.")
            return
        analytics = resp.json()

        # Build DataFrame
        df = pd.DataFrame([
            {
                "Category": cat,
                "Total": analytics[cat]["total"],
                "Percentage": analytics[cat]["percentage"]
            }
            for cat in analytics
        ])
        df = pd.DataFrame(df)
        df_sorted = df.sort_values(by="Percentage", ascending=False)
        st.title("Expense Breakdown By Category")

        st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], width=0, height=0, use_container_width=True)

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

        with st.expander("Show Detailed Table", expanded=True):
            st.table(df_sorted)
