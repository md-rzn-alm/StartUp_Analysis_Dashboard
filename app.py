import pandas as pd
import streamlit as st
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import time
import plotly.express as px
from pandas.core.methods.describe import select_describe_func

st.set_page_config(layout='wide' , page_title='StartUp Analysis')

df = pd.read_csv('StartUp_Cleaned.csv')
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
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()

    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        #temp_df = df.groupby(['month', 'year'])['amount'].sum().reset_index()

    temp_df['Month-Year'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        #temp_df[['amount', 'x-axis']]

    # fig3, ax3 = plt.subplots()
    # ax3.plot(temp_df['x-axis'], temp_df['amount'])
    #
    # st.pyplot(fig3)
    fig3 = px.line(temp_df, x="Month-Year", y="amount")

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("              ")

    col1, col2 = st.columns(2)
    with col1:
        df['startup'] = df['startup'].str.replace('Flipkart.com', 'Flipkart')
        max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(5)
        st.subheader("Top 5 Invested Startups (in cr) ")
        fig_1 = px.bar(max_funding)
        # show in streamlit
        st.plotly_chart(fig_1, use_container_width=True)

    with col2:
        # Top 5 investment sector
        df['vertical'] = df['vertical'].str.replace('ECommerce', 'E-Commerce')
        df['vertical'] = df['vertical'].str.replace('eCommerce', 'E-Commerce')

        st.subheader("Top 5 Invested Sectors  (in cr) ")
        vertical_amount = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
        # fig0, ax0 = plt.subplots()
        # ax0.bar(vertical_amount.index, vertical_amount.values)
        # st.pyplot(fig0)
        fig0 = px.bar(vertical_amount)

        # show in streamlit
        st.plotly_chart(fig0, use_container_width=True)


    # # Top 5 investment sector
    # df['vertical'] = df['vertical'].str.replace('ECommerce', 'E-Commerce')
    # df['vertical'] = df['vertical'].str.replace('eCommerce', 'E-Commerce')
    #
    # st.subheader("Top 5 Investment Sector")
    # vertical_amount = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
    # # fig0, ax0 = plt.subplots()
    # # ax0.bar(vertical_amount.index, vertical_amount.values)
    # # st.pyplot(fig0)
    # fig0 = px.bar(vertical_amount,title='Amounts are in crores')
    #
    # # show in streamlit
    # st.plotly_chart(fig0, use_container_width=True)


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment
    last5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup' , 'vertical' , 'city' , 'round' , 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1, col2  =st.columns(2)
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
         #vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

         st.subheader("Sector Invested in")
         #fig1, ax1 = plt.subplots()
         #ax1.pie(vertical_series, labels=vertical_series.index , autopct="%0.01f")

         #st.pyplot(fig1)

         fig = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
         fig_px = px.pie(fig, values='amount', names=fig.index)
         st.plotly_chart(fig_px, use_container_width=True)

    st.subheader("                ")
    col1, col2 = st.columns(2)
    #print(df.info())
    with col1:
        st.subheader("Amount Invested")
        fig2 = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        fig_px2 = px.pie(fig2, values='amount', names=fig2.index)
        st.plotly_chart(fig_px2, use_container_width=True)

    with col2:
        st.subheader("Investment cities")
        # filter dataframe
        city_df = df[df['investors'].str.contains(investor, na=False)]
        # count city occurrences
        city_counts = city_df['city'].value_counts().reset_index()
        city_counts.columns = ['city', 'count']
        # create pie chart
        fig = px.pie(city_counts, names='city', values='count')
        st.plotly_chart(fig, use_container_width=True)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader("Year-On-Year Investment")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)

    st.pyplot(fig2)

option = st.sidebar.selectbox('Select One' , ['Overall Analysis' , 'StartUp' , 'Investor'])
df['date'] = pd.to_datetime(df['date'])

def load_startup_details(startup):
    last5_df1 = df[df['startup'].str.contains(startup)].head()[
        ['date', 'investors', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investors')
    st.dataframe(last5_df1)

    col1 , col2 = st.columns(2)
    with col1:
        st.subheader("Investors")
        fig3 = df[df['startup'].str.contains(startup)].groupby('investors')['amount'].sum().sort_values(ascending=False)
        fig_px3 = px.pie(fig3, values='amount', names=fig3.index)
        st.plotly_chart(fig_px3, use_container_width=True)

    with col2:
        st.subheader("Stage")
        fig3 = df[df['startup'].str.contains(startup)].groupby('round')['amount'].sum().sort_values(ascending=False)
        fig_px3 = px.pie(fig3, values='amount', names=fig3.index)
        st.plotly_chart(fig_px3, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("City")
        fig3 = df[df['startup'].str.contains(startup)].groupby('city')['amount'].sum().sort_values(ascending=False)
        fig_px3 = px.pie(fig3, values='amount', names=fig3.index)
        st.plotly_chart(fig_px3, use_container_width=True)

if option == 'Overall Analysis':
    #btn0 = st.sidebar.button("Shoe overall analysis")
    #if btn0:
    load_overall_analysis()
elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select Startup' , sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())) )
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)