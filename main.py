import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

st.sidebar.title('Olympic Analysis')
df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal tally', 'Overall Analysis', 'Athlete Analysis', 'Country-wise analysis')
)

# st.dataframe(df)

if user_menu == 'Medal tally':
    st.sidebar.header("Medal Tally")

    st.title("Medal Tally")
    years, country = helper.country_year_list(df)
    Selected_year = st.sidebar.selectbox("Select Year", years)
    Selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, Selected_year, Selected_country)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Editions', y='region')
    st.title("Participating nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Editions', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Editions', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

if user_menu == "Country-wise analysis":
    st.sidebar.title("Country-Wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a country", country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(f"Medal tally of {selected_country} over the years")
    st.plotly_chart(fig)

    st.title(f"{selected_country}'s performance over the years")
    try:
        pt = helper.country_event_heatmap(df, selected_country)
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

    except:
        st.write("Nothing notable")

    st.title(f"Top Performing athletes of {selected_country}")
    top_10 = helper.most_successful_countrywise(df, selected_country)
    st.table(top_10)

if user_menu == 'Athlete Analysis':

    st.title("Distribution of age")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    selected_sport = st.sidebar.selectbox("Select a sport", sport_list)

    tmp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    try:
        ax = sns.scatterplot(tmp_df['Weight'], tmp_df['Height'], hue=tmp_df['Medal'], style=tmp_df['Sex'], s=100)
        st.pyplot(fig)
    except:
        st.write(" ")