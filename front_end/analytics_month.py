import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def analytics_month_tab():
    response= requests.get(f"{API_URL}/analytics_by_month/")
    response=response.json()
    # st.write(response)
    data={
        "month":[i["month"] for i in response],
        "amount":[i["total"] for i in response]

    }
    df=pd.DataFrame(data)


    st.title("Expense Breakdown By Month")

    st.bar_chart(data=df.set_index("month")["amount"], width=0, height=0, use_container_width=True)

    df["amount"] = df["amount"].map("{:.2f}".format)
    with st.expander("Show Detailed Table", expanded=True):
        st.table(df)
    









