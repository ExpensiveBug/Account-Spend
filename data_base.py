import streamlit as st
import firebase_admin
from firebase_admin import credentials, db , firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("personal-finance-tracker-429a7-e8eecd0703e4.json")
    firebase_admin.initialize_app(cred,{"databaseURL": st.secrets["firebase"]["database_url"]})

def get_bill(user_id):
    ref = db.reference(f"users/{user_id}/expenses")
    data = ref.get()
    if data:
        return [(key, value.get("category"), value.get("amount"), value.get("note")) for key, value in data.items()]
    else:
        return []
    
def add_expense(user_id,category, amount, note):
    ref = db.reference(f"users/{user_id}/expenses")
    ref.push({"category":category, "amount":amount, "note":note})

def delete_expense(user_id):
    ref = db.reference(f"users/{user_id}/expenses")
    if ref.get():
        ref.delete()
        return True
    else:
        return False

def get_income(user_id):
    ref = db.reference(f"users/{user_id}/income")
    data = ref.get()
    if data:
        return [(key, value.get("category"), value.get("amount"), value.get('note')) for key, value in data.items()]
    else :
        return []
    
def add_income(user_id, category, amount, note):
    ref = db.reference(f"users/{user_id}/income")
    ref.push({'category':category,'amount':amount,'note':note})

def delete_income(user_id):
    ref = db.reference(f"users/{user_id}/income")
    if ref.get():
        ref.delete()
        return True
    else:
        return False

