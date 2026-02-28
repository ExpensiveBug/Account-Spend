import streamlit as st 
import data_base as db

def app():
    if not st.session_state.get("logged_in",False):
        st.title("Login Required")
        st.warning("Please Login to continue !!")
        st.stop()

    st.title("Track Expenses")
    expense_type = st.selectbox("Select the expense type",
                        ["Food", "Entertainment","Travel","Health","Electrical or Mechanical", "Miscellaneous"], key = "exp_type")
    amt = st.number_input("Amount",min_value=0.0, step = 100.0, key = "bill")
    note = st.text_area("Note", placeholder = "Why you spend :( ", key = "bill_note")

    if st.button("Add Expense",width="stretch"):
        if amt <= 0:
            st.error("Amount must be greater than 0 !!")
        else :
            db.add_expense(st.session_state.user_id, expense_type, amt, note)
            st.balloons()
            st.success("Expense added Successfully")

    if st.button("Reset Expense",width="content",type="primary"):
        clean = db.delete_expense(st.session_state.user_id)
        if clean :
            st.info("Expense deleted")
            st.rerun()
        else :
            st.info("No data found")
