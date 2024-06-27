import streamlit as st
import yaml
from yaml.loader import SafeLoader

import chat


with open("./config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)


st.title("I am Prometeus")

# import streamlit_authenticator as sauth
# from streamlit_authenticator.authenticate import Authenticate
# from streamlit_authenticator.utilities.hasher import Hasher


# hashed_passwords = Hasher(["abc", "def"]).generate()

# authenticator = Authenticate(
#     config["credentials"],
#     config["cookie"]["name"],
#     config["cookie"]["key"],
#     config["cookie"]["expiry_days"],
#     config["pre-authorized"],
# )

# name, authentication_status, username = authenticator.login(
#     "main", fields={"Form name": "custom_form_name"}
# )


# print(name, authentication_status, username)

# if st.session_state["authentication_status"]:
#     authenticator.logout()
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title("Some content")
# elif st.session_state["authentication_status"] is False:
#     st.error("Username/password is incorrect")
# elif st.session_state["authentication_status"] is None:
#     st.warning("Please enter your username and password")


import streamlit as st
import importlib

import auth_functions

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if "user_info" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(
        label="Do you have an account?", options=("Yes", "No", "I forgot my password")
    )
    auth_form = col2.form(key="Authentication form", clear_on_submit=False)
    email = auth_form.text_input(label="Email")
    password = (
        auth_form.text_input(label="Password", type="password")
        if do_you_have_an_account in {"Yes", "No"}
        else auth_form.empty()
    )
    auth_notification = col2.empty()

    # Sign In
    if do_you_have_an_account == "Yes" and auth_form.form_submit_button(
        label="Sign In", use_container_width=True, type="primary"
    ):
        with auth_notification, st.spinner("Signing in"):
            auth_functions.sign_in(email, password)

    # Create Account
    elif do_you_have_an_account == "No" and auth_form.form_submit_button(
        label="Create Account", use_container_width=True, type="primary"
    ):
        with auth_notification, st.spinner("Creating account"):
            auth_functions.create_account(email, password)

    # Password Reset
    elif (
        do_you_have_an_account == "I forgot my password"
        and auth_form.form_submit_button(
            label="Send Password Reset Email", use_container_width=True, type="primary"
        )
    ):
        with auth_notification, st.spinner("Sending password reset link"):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if "auth_success" in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif "auth_warning" in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # Sign out
    st.header("Sign out:")
    st.button(label="Sign Out", on_click=auth_functions.sign_out, type="primary")

    chat.chat()

    # # Show user information
    # st.header("User information:")
    # st.write(st.session_state.user_info)

    # # Delete Account
    # st.header("Delete account:")
    # password = st.text_input(label="Confirm your password", type="password")
    # st.button(
    #     label="Delete Account",
    #     on_click=auth_functions.delete_account,
    #     args=[password],
    #     type="primary",
    # )
