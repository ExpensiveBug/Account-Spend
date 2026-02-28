import streamlit as st
import data_base as db
import pandas as pd
import matplotlib.pyplot as plt

def app():
    if not st.session_state.get("logged_in", False):
        st.title("Login Required !!")
        st.warning("Please Login to continue !")
        st.stop()

    total_earn = 0.0
    total_expense = 0.0
    income = pd.DataFrame()
    bill = pd.DataFrame()


    col1, col2 = st.columns(2)
    with col1 :
        st.title("Bill Report")
        bill_data = db.get_bill(st.session_state.user_id)

        if bill_data:
            bill = pd.DataFrame(bill_data, columns=["ID", "Category", "Amount", "Note"])
            st.dataframe(bill.drop(columns = ["ID"]),width= "content")

            total_expense = bill["Amount"].astype(float).sum()
            st.text(f"Total Expenses ₹{total_expense:,.2f}")

            fig, ax = plt.subplots(figsize = (8,4))
            bars = ax.bar(bill["Category"], bill["Amount"])
            ax.bar_label(bars, padding = 3)
            ax.set_title("Amount VS Expense")
            st.pyplot(fig)
            plt.close(fig)

        else :
            st.info("No Expense recorded yet.")

    with col2 :
        st.title("Income Report")
        income_data = db.get_income(st.session_state.user_id)
        if income_data:
            income = pd.DataFrame(income_data, columns=["ID", "Category", "Amount", "Note"])
            st.dataframe(income.drop(columns = ["ID"]),width= "content")

            total_earn= income["Amount"].astype(float).sum()
            st.text(f"Total Income ₹{total_earn:,.2f}")
            fig, ax = plt.subplots(figsize = (8,4))
            bars = ax.bar(income["Category"], income["Amount"])
            ax.bar_label(bars, padding = 3)
            ax.set_title("Source VS Income")
            st.pyplot(fig)
            plt.close(fig)

        else :
            st.info("No Income recorded yet.")

    net_balance = total_earn - total_expense
    st.subheader("Account Summary")
    if net_balance > 0 :
        st.success(f"Profit: ₹{net_balance:,.2f}")

    elif net_balance < 0:
        st.error(f"Loss: ₹{abs(net_balance):,.2f}")

    else :
        st.info("No Profit No loss ")

    expense_report = pd.DataFrame()
    income_report = pd.DataFrame()

    if not bill.empty:
        expense_report = bill.copy()
        expense_report["Type"] = "Expense"

    if not income.empty:
        income_report = income.copy()
        income_report["Type"] = "Income"

    report = pd.concat([expense_report, income_report], ignore_index=True)

    if report.empty:
        st.info("No Data available to Download !!")
    else :
        report = report[["Type","Category","Amount","Note"]]
        report_csv = report.to_csv(index=False)
        st.download_button(label="Download Report", data = report_csv, file_name="Report.csv",mime = "text/csv")
