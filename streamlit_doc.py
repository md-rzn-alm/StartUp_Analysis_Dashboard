import streamlit as st
import pandas as pd
import time

st.title("StartUp DashBoard")

st.header("I am learning Streamlit")
st.subheader("Indian startUp")

st.markdown("""
### My Favorites movies
- kbkhbhd
-hbfhv
-lnfehfeb
""")

st.code("""
def foo(input):
    return input**2
""")

st.latex('x^2 + y^2 + 2 = 0')       ## latex is used to express mathematically expression
st.latex('x^3 + x^2 + 2x + 15 = 0')

df = pd.DataFrame({
    'name' : ['Rizwan', 'MD' , 'Alam'],
    'gender' : ['Male', 'Male' , 'Male' ],
    'Branch' : ['CS' , 'ECE' , 'CSE' ]
})

st.dataframe(df)

st.metric("Revenue" , 'Rs 3L' ,'-3%')

st.json({
    'name' : ['Rizwan', 'MD' , 'Alam'],
    'gender' : ['Male', 'Male' , 'Male' ],
    'Branch' : ['CS' , 'ECE' , 'CSE' ]
})

st.image('AI .jpg')

## st.video()

st.sidebar.title("Side bar ka title")

st.title("Two columns")

col1 , col2 = st.columns(2)

with col1:
    st.image('AI .jpg')

with col2:
    st.image('AI .jpg')

st.error("Error name")
st.success("success msg")

bar = st.progress(0)
for i in range(1,101):
    time.sleep(0.1)
    bar.progress(i)

email = st.text_input("Enter email")
number = st.number_input("Enter number")
st.date_input("Enter date")

import streamlit as st

email = st.text_input("Enter Email")
password = st.text_input("Enter Password")

gender = st.selectbox("Select gender", ['male', 'female', 'Others'])

btn = st.button("Login Karo")

# if button clicked
if btn:
    if email == 'riz@gmail.com' and password == '123456':
        st.success("Login successfully")
        st.write(gender)
    else:
        st.error("Login Failed")

file = st.file_uploader('upload a csv file')

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())

