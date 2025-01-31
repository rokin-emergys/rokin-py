import os
import hashlib
import streamlit as st

# Constants
USER_DIR = "user_data"

# Utility Functions
def create_directory_structure():
    """
    Creates the directory structure for storing user data.
    """
    roles = ['employee', 'admin', 'manager']
    if not os.path.exists(USER_DIR):
        os.mkdir(USER_DIR)
    
    for role in roles:
        role_path = os.path.join(USER_DIR, role)
        if not os.path.exists(role_path):
            os.mkdir(role_path)

def hash_password(password):
    """
    Hashes the password using SHA256.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_exists(role, username):
    """
    Checks if a user exists in the specified role directory.
    """
    file_path = os.path.join(USER_DIR, role, f"{username}.txt")
    return os.path.exists(file_path)

def write_user_data(role, username, password_hash, email_or_phone):
    """
    Writes new user data to the text file in the respective role folder.
    """
    file_path = os.path.join(USER_DIR, role, f"{username}.txt")
    with open(file_path, 'w') as file:
        file.write(f"{username},{password_hash},{email_or_phone}")

def read_user_data(role, username):
    """
    Reads user data from the text file.
    """
    file_path = os.path.join(USER_DIR, role, f"{username}.txt")
    with open(file_path, 'r') as file:
        data = file.read().strip().split(',')
        return data

def authenticate_user(role, username, password):
    """
    Authenticates a user based on the role, username, and password.
    """
    if check_user_exists(role, username):
        stored_data = read_user_data(role, username)
        stored_password_hash = stored_data[1]
        return stored_password_hash == hash_password(password)
    return False

def change_password(role, username, new_password):
    """
    Changes the password for the specified user.
    """
    if check_user_exists(role, username):
        new_password_hash = hash_password(new_password)
        stored_data = read_user_data(role, username)
        email_or_phone = stored_data[2]
        write_user_data(role, username, new_password_hash, email_or_phone)
        return True
    return False

# Streamlit UI
def user_interface():
    create_directory_structure()

    st.title("User Management system")
    
    # Sidebar for navigation
    option = st.sidebar.selectbox("Select Option", ['Register New Account', 'Login', 'Password Reset'])

    # Register Section
    if option == 'Register New Account':
        st.header("Register New Account")
        username_reg = st.text_input("Username")
        password_reg = st.text_input("Password", type="password")
        email_or_phone_reg = st.text_input("Email or Phone")
        role = st.selectbox("Role", ['employee', 'admin', 'manager'])
        
        if st.button("Register"):
            if not check_user_exists(role, username_reg):
                password_hash = hash_password(password_reg)
                write_user_data(role, username_reg, password_hash, email_or_phone_reg)
                st.success("Registration successful!")
            else:
                st.error("Username already exists!")

    # Login Section
    elif option == 'Login':
        st.header("Login")
        username_login = st.text_input("Username", key="username_login")
        password_login = st.text_input("Password", type="password", key="password_login")
        role_login = st.selectbox("Role", ['employee', 'admin', 'manager'], key="role_login")  # Added role input for login
        
        if st.button("Login"):
            if authenticate_user(role_login, username_login, password_login):
                st.success("Login successful!")
            else:
                st.error("Invalid credentials!")

    # Password Reset Section
    elif option == 'Password Reset':
        st.header("Password Reset")
        username_reset = st.text_input("Username (for password reset)", key="reset_username")
        new_password = st.text_input("New Password", type="password", key="reset_password")
        role_reset = st.selectbox("Role", ['employee', 'admin', 'manager'], key="role_reset")  
        
        if st.button("Reset Password"):
            if change_password(role_reset, username_reset, new_password):  
                st.success("Password reset successful!")
            else:
                st.error("Username not found!")

if __name__ == "__main__":
    user_interface()