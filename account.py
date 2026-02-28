import streamlit as st 
import firebase_admin
from firebase_admin import credentials, auth, db
import hashlib
import json

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "useremail" not in st.session_state:
    st.session_state.useremail = None

if not firebase_admin._apps:
    firebase_dict = json.loads(st.secrets["firebase"]["json"])
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred,{"databaseURL": st.secrets["firebase"]["database_url"]})          

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def app():
    st.title("Account")

    if not st.session_state.logged_in :
        choice = st.selectbox('Login/Signup',['Sign Up','Login'])
        if choice == 'Login':
            email = st.text_input('Enter Email',key = 'login_email')
            password = st.text_input('Enter Password', type='password',key='login_password')

            if st.button('Login'):
                if not email or not password:
                    st.warning("Fill the above details !!")
                    return

                ref = db.reference("users")
                query = ref.order_by_child("email").equal_to(email).get()

                if query :
                    uid , user_data = next(iter(query.items()))
                    if user_data.get("password") == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.username = user_data.get("username")
                        st.session_state.useremail = email
                        st.session_state.user_id = uid   
                        st.success("Account Logged in Successfully.")
                        st.rerun()
                        return
                    else:
                        st.error("Invalid Email or Password !!")
                        return
                st.error("Invalid Email or Password")
        else :
            email = st.text_input('Enter Email',key='signup_email')
            password = st.text_input('Enter Password', type='password',key='signup_password')
            user_name = st.text_input('Enter your unique username',key='signup_username')

            if st.button('Create my Account'):
                if not email or not password or not user_name:
                    st.warning("Fill above details first !!")
                    return
                
                try :
                    user = auth.create_user(email=email, password=password)
                    uid = user.uid

                    ref = db.reference(f"users/{user.uid}")
                    ref.set({
                        "username": user_name,
                        "email": email,
                        "password": hash_password(password)
                    })
                    st.success("Account Created Successfully !!")
                    st.info("Now login your account.")
                    st.balloons()

                except Exception as e:
                    st.error(f"Error:{e}")

    else :
        st.info(f"Logged in as: {st.session_state.username}")
        st.info(f"Email: {st.session_state.useremail}")
        if st.button("Sign Out",type="primary"):
            st.success("Signed Out Successfully")
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.useremail = None            
            st.rerun()




