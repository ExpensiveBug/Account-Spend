import streamlit as st
from streamlit_option_menu import option_menu
import account, expense, income, report

st.set_page_config(page_title= "Account Spend")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
def run():
    with st.sidebar:
        selected =  option_menu(menu_title=None, 
                            options=["Account", "Expense", "Income", "Report"], 
                            icons = ["person-circle","cash-stack","wallet2","bar-chart"], default_index=0,  
                            styles = {
                                "container":{"padding" : "5!important", "background-color":"black"},  
                                "icon" : {"color":"white", "font-size":"23px"},
                                "nav-link":{"color":"white","font-size":"20px", "text-align":"left","margin":"0px"},
                                "nav-link-selected":{"background-color":"#02ab21"},  })
    
    if selected == "Account":
        account.app()
    elif selected == "Expense":
        expense.app()
    elif selected == "Income":
        income.app()
    elif selected == "Report":
        report.app()
run()
