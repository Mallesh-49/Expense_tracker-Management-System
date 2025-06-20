# import streamlit as st
# from datetime import datetime
# import requests
#
# API_URL = "http://127.0.0.1:8000"
#
#
# def add_update_tab():
#     selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
#     response = requests.get(f"{API_URL}/expenses/{selected_date}")
#     if response.status_code == 200:
#         existing_expenses = response.json()
#         # st.write(existing_expenses)
#     else:
#         st.error("Failed to retrieve expenses")
#         existing_expenses = []
#
#     categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]
#
#     with st.form(key="expense_form"):
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.text("Amount")
#         with col2:
#             st.text("Category")
#         with col3:
#             st.text("Notes")
#
#         expenses = []
#         for i in range(5):
#             if i < len(existing_expenses):
#                 amount = existing_expenses[i]['amount']
#                 category = existing_expenses[i]["category"]
#                 notes = existing_expenses[i]["notes"]
#             else:
#                 amount = 0.0
#                 category = "Shopping"
#                 notes = ""
#
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
#                                                label_visibility="collapsed")
#             with col2:
#                 category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
#                                               key=f"category_{i}", label_visibility="collapsed")
#             with col3:
#                 notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")
#
#             expenses.append({
#                 'amount': amount_input,
#                 'category': category_input,
#                 'notes': notes_input
#             })
#
#         submit_button = st.form_submit_button()
#         if submit_button:
#             filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
#
#             response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
#             if response.status_code == 200:
#                 st.success("Expenses updated successfully!")
#             else:
#                 st.error("Failed to update expenses.")

import streamlit as st
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000"


def add_update_tab():
    st.markdown("Select a Date to View or Update Expenses")
    selected_date = st.date_input("Choose Date", datetime(2024, 8, 1))

    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses from server.")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    st.markdown("---")
    st.markdown("Enter or Edit Your Expenses")

    with st.form(key="expense_form"):
        st.markdown("#### Fill up to 5 expense entries")

        expenses = []
        for i in range(5):
            st.markdown(f"**Expense #{i + 1}**")
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}")
            with col2:
                category_input = st.selectbox("Category", options=categories, index=categories.index(category),
                                              key=f"category_{i}")
            with col3:
                notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

            st.markdown("---")

        submit_button = st.form_submit_button("💾 Save Expenses")
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")
