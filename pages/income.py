import streamlit as st
import data_base as db

def app():
    if not st.session_state.get("logged_in",False):
        st.title("Login Required !!")
        st.warning("Please Login to continue!")
        st.stop()

    st.title("Income Source")
    
    source = st.selectbox("Select income type",["Job", "Passive Income","Investment", "Business","other"], key="in_type")
    amt = st.number_input("Amount",min_value=0.0, step = 1000.0, key="amount")
    note = st.text_area("Note ", placeholder="Write something about your income...", key="note")

    if st.button("Add Income",width="stretch"):         
        if amt <= 0 :
            st.error("Amount must be greater that 0 !!")
        else :
            db.add_income(st.session_state.user_id, source ,amt,note)
            st.balloons()
            st.success("Income added Successfully")

    if st.button("Reset Income", width="content",type="primary"):
        clean = db.delete_income(st.session_state.user_id)
        if clean : 
            st.info("Income Deleted")
            st.rerun()
        else :
            st.info("No data found")

