import pandas as pd
import streamlit as st
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(layout='wide' , page_title='StartUp Analysis')

df = pd.read_csv('startUp_cleaned (1).csv')
df['date'] = pd.to_datetime(df['date'] , format='mixed')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# st.dataframe(df)
st.sidebar.title('Startup Funding Analysis')

def load_overall_analysis():
    st.title("Overall Analysis")

    total  = round(df['amount'].sum())
    #max funding infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #mean funding infused in a startup
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    #total funded startup
    num_startup = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total', str(total) + '  Cr')
    with col2:
        st.metric('Max', str(max_funding) + '  Cr')
    with col3:
        st.metric('Average' , str(round(avg_funding)) + '  Cr')
    with col4:
        st.metric("Total Startup" , str(num_startup) + '  Cr')

    st.header("Month-On-Month Graph")
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['month', 'year'])['amount'].sum().reset_index()

    else:
        temp_df = df.groupby(['month', 'year'])['amount'].count().reset_index()
    #temp_df = df.groupby(['month', 'year'])['amount'].sum().reset_index()
    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    #temp_df[['amount', 'x-axis']]

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x-axis'], temp_df['amount'])

    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment
    last5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup' , 'vertical' , 'city' , 'round' , 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1, col2 =st.columns(2)
    with col1:
        #biggest investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)
        # st.subheader("Amounts in crores")
        # st.dataframe(big_series)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader("Sector Invested in")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index , autopct="%0.01f")

        st.pyplot(fig1)

    #print(df.info())
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader("Year-On-Year Investment")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)

option = st.sidebar.selectbox('Select One' , ['Overall Analysis' , 'StartUp' , 'Investor'])
df['date'] = pd.to_datetime(df['date'])

if option == 'Overall Analysis':
    #btn0 = st.sidebar.button("Shoe overall analysis")
    #if btn0:
    load_overall_analysis()
elif option == 'StartUp':
    st.sidebar.selectbox('Select Startup' , sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())) )
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)