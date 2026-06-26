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
df['startup'] = df['startup'].replace({
    'Oyo' : 'OYO Rooms',
    'Oyorooms' : 'OYO Rooms',
    'OYO Rooms' : 'OYO Rooms',
    'Oyo Rooms' : 'OYO Rooms',
    'OyoRooms' : 'OYO Rooms',
    'Flipkart.com' : 'Flipkart'
    })

st.sidebar.title('🔍 Startup Funding Analysis')

def load_overall_analysis():
    st.set_page_config(
        page_title="Startup Funding Dashboard",
        page_icon="📊",
        layout="wide"
    )

    st.title("🚀 Startup Funding Insights Dashboard")
    st.caption("Analyzing startup funding trends, sectors, and investor behavior")
    st.title(" 🎯 Overall Analysis")
    st.caption("These metrics provide a quick overview of the scale and "
               "activity within the startup ecosystem.")

    total  = round(df['amount'].sum())
    #max funding infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #mean funding infused in a startup
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    #total funded startup
    num_startup = df['startup'].nunique()


    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total Funding', f'₹{total:,.0f} Cr')

    with col2:
        st.metric('Max Funding', f'₹{max_funding:,.0f} Cr')

    with col3:
        st.metric('Average Funding', f'₹{round(avg_funding):,.0f} Cr')

    with col4:
        st.metric('Total Startups', f'{num_startup:,}')

    st.header("📊 Month-On-Month Graph")
    st.caption(" Funding Trends Over Time ")
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()

    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['Month-Year'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3 = px.line(temp_df, x="Month-Year", y="amount")
    st.plotly_chart(fig3, use_container_width=True)

    col1, col2 ,col3  = st.columns(3)
    with col1:
        df['startup'] = df['startup'].str.replace('Flipkart.com', 'Flipkart')
        max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(5)

        fig_1 = px.bar(max_funding , title = "📊 Top 5 Invested Startups")
        # hide axis labels
        fig_1.update_layout(xaxis_title=None, yaxis_title=None)
        # show in streamlit
        st.plotly_chart(fig_1, use_container_width=True)
        st.markdown(
            "📌 **Insight:** Rapido Bike Taxi attracted the highest funding (~35k+ Cr).")

    with col2:
        vertical_amount = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)

        fig0 = px.bar(vertical_amount , title = "🏢 Top 5 Invested Sectors" )
        # hide axis labels
        fig0.update_layout(xaxis_title=None, yaxis_title=None)
        # show in streamlit
        st.plotly_chart(fig0, use_container_width=True)
        st.markdown(
            "📌 **Insight:** E-Commerce is the dominant sector, attracting the largest investment (~72k Cr).")

    with col3:
        city_invested = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(5)

        fig_b = px.pie(city_invested , names=city_invested.index, values='amount' ,title="🌍 Top 5 Invested Cities ")
        #show in streamlit
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown(
            "📌 **Insight:** Bengaluru dominates the startup funding landscape with 58.4% of total investments among "
            "all the cities.")

    col1, col2 = st.columns(2)

    with col1:
       stage_invested = df.groupby('round')['amount'].sum().sort_values(ascending=False).head(5)

       fig_s = px.pie(stage_invested ,
                      names=stage_invested.index ,
                      values='amount',
                      title="🤝 Funding By Stage ")
       #show in streamlit
       st.plotly_chart(fig_s, use_container_width=True)
       st.markdown(
           "📌 **Insight:** Private Equity dominates the funding landscape, accounting for 76.6% of total investments.")

    with col2:
        funding_trend = df.groupby('year')['amount'].sum().reset_index()

        fig = px.line(
            funding_trend,
            x='year',
            y='amount',
            title="📈 Year on Year",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "📌 **Insight:**  Startup funding peaked in 2017 and 2019, while 2020 witnessed a sharp decline.")

def load_investor_details(investor):
    st.title("Investors Details")
    st.subheader("💼 " + investor)
    #st.markdown("---")
    # load the recent 5 investment
    last5_df = df[df['investors'].str.contains(investor)].head()[
                            ['date', 'startup' , 'vertical' , 'city' , 'round' , 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        #biggest investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        fig = px.bar(big_series ,title="📊 Biggest Investment")
        st.plotly_chart(fig , use_container_width=True)

    with col2:
         fig = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
         fig_px = px.pie(fig, values='amount', names=fig.index , title = "🏢 Sector Invested in")
         st.plotly_chart(fig_px, use_container_width=True)

    col1, col2 , col3 = st.columns(3)

    with col1:
        fig2 = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        fig_px2 = px.pie(fig2, values='amount', names=fig2.index , title= "🤝 Investment by Round")
        st.plotly_chart(fig_px2, use_container_width=True)

    with col2:
        city_df = df[df['investors'].str.contains(investor, na=False)]
        # count city occurrences
        city_counts = city_df['city'].value_counts().reset_index()
        city_counts.columns = ['city', 'count']
        # create pie chart
        fig = px.pie(city_counts, names='city', values='count' ,title=' 🌍 Investment cities')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

        fig = px.line(
            year_series,
            x=year_series.index,
            y='amount',
            title="📈 Funding Trend Over Time",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "📌 **Insight:** Funding shows fluctuations over time, reflecting market cycles and investor confidence.")

option = st.sidebar.selectbox('Select One' , ['Overall Analysis' , 'Investor' , 'StartUp' ])
df['date'] = pd.to_datetime(df['date'])

def load_startup_details(startup):
    last5_df1 = df[df['startup'].str.contains(startup)].head()[
                        ['date', 'investors', 'vertical', 'city', 'round', 'amount']]
    st.title("🏢" + startup)
    st.subheader('Most Recent Investors')
    st.dataframe(last5_df1)

    col1 , col2 , col3 = st.columns(3)

    with col1:
        fig3 = df[df['startup'].str.contains(startup)].groupby('investors')['amount'].sum().sort_values(ascending=False)
        fig_px3 = px.pie(fig3, values='amount', names=fig3.index, title="📊 Investors Invested")
        if (fig3.values > 0 ).any():
            st.plotly_chart(fig_px3, use_container_width=True)
            st.markdown(
                "📌 **Insight:**  Investment participation is distributed among multiple investors, "
                "reflecting varying levels of investor interest and collaboration in funding the startup."
                )
        else:
            st.markdown("   ")

    with col2:
        fig3 = df[df['startup'].str.contains(startup)].groupby('round')['amount'].sum().sort_values(ascending=False)
        fig_px3 = px.pie(fig3, values='amount', names=fig3.index , title= "🤝 Invested Stage")

        if (fig3.values > 0).any():
            st.plotly_chart(fig_px3, use_container_width=True)
            st.markdown(
                "📌 **Insight:**  Funding activity is concentrated in specific investment stages, indicating the startup's "
                "position in its growth journey and the type of capital being attracted."
             )
        else:
            st.markdown("   ")


    with col3:
        fig3 = df[df['startup'].str.contains(startup)].groupby('city')['amount'].sum().sort_values(ascending=False)
        fig_px3 = px.pie(fig3, values='amount', names=fig3.index ,title = "🌍 Invested City")

        if (fig3.values > 0).any():
            st.plotly_chart(fig_px3, use_container_width=True)
            st.markdown(
                "📌 **Insight:**  Investments are associated with key startup ecosystems, emphasizing the "
                "importance of regional business environments and innovation hubs in attracting capital."
            )
        else:
            st.markdown("   ")

if option == 'Overall Analysis':
    load_overall_analysis()


elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select Startup' , sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())) )
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)