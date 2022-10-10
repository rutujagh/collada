import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Collada", page_icon=":bar_chart:", layout="wide")

# --- USER AUTHENTICATION ---
names = ["Damini", "Kirti"]
usernames = ["damini", "kirti"]
passwords = ["damini@123", "kirti@123"]

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "data_visualization", "abcdef",
                                    cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    # configuration
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # title of the app
    st.title(":bar_chart: Bug Report Visualization")

    # Add a sidebar
    authenticator.logout("Logout", "sidebar")
    st.sidebar.subheader("Visualization Settings")

    # Setup file upload
    uploaded_file = st.sidebar.file_uploader(
        label="Upload CSV or Excel file. (200MB max)",
        type=['csv', 'xlsx'])

    global df
    if uploaded_file is not None:
        print(uploaded_file)

        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            print(e)
            df = pd.read_excel(uploaded_file)

    global numeric_columns
    global non_numeric_columns
    try:
        st.write(df)
        numeric_columns = list(df.select_dtypes(['float', 'int', 'object', 'double', 'datetime']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
    except Exception as e:
        print(e)
        st.write("Please upload file to the application.")

    # add a select widget to the side bar
    chart_select = st.sidebar.selectbox(
        label="Select the chart type",
        options=['Scatterplots', 'Lineplots', 'Histogram']
    )

    if chart_select == 'Scatterplots':
        st.sidebar.subheader("Scatterplot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
            plot = px.scatter(data_frame=df, x=x_values, y=y_values, template="xgridoff")
            # display the chart
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Lineplots':
        st.sidebar.subheader("Line Plot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
            plot = px.line(data_frame=df, x=x_values, y=y_values, template="xgridoff")
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Histogram':
        st.sidebar.subheader("Histogram Settings")
        try:
            x = st.sidebar.selectbox('Feature', options=numeric_columns)
            plot = px.histogram(x=x, data_frame=df, template="xgridoff")
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
