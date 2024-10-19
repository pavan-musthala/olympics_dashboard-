import streamlit as st
import pandas as pd
import numpy as np
import preprocessor
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, df_region)

user_menu = st.sidebar.radio("Select an Option",
                              ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis'))

if user_menu == "Medal Tally":
    st.sidebar.header('Medal Tally')
    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', year)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != "Overall" and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    elif selected_year == "Overall" and selected_country != 'Overall': 
        st.title("Overall Performance of " + selected_country + " in Olympics")
    else:
        st.title("Performance of " + selected_country + " in " + str(selected_year) + " Olympics")
    
    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':
    edition = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Stats for the Olympics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(edition)

    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Athletes')
        st.title(athletes)

    with col3:
        st.header('Nations')
        st.title(nations)

    nations_overtime = helper.data_overtime(df, 'region')
    fig1 = px.line(nations_overtime, x='Edition', y='region')
    st.title("Number of Countries Participated in Olympics across the years")
    st.plotly_chart(fig1)

    events_overtime = helper.data_overtime(df, 'Event')
    fig2 = px.line(events_overtime, x='Edition', y='Event')
    st.title("Number of Events in Olympics across the years")
    st.plotly_chart(fig2)

    athletes_overtime = helper.data_overtime(df, 'Name')
    fig3 = px.line(athletes_overtime, x='Edition', y='Name')
    st.title("Number of Athletes in Olympics across the years")
    st.plotly_chart(fig3)

    st.title("Number of events in every sport in the Olympics over the years")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_succesfull(df, selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in the following Sports")
    pt = helper.country_event_heatmap(df, selected_country)

    if pt.empty:
        st.write(f"No data available for {selected_country}.")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True, fmt="d", cmap="Blues")
        st.pyplot(fig)

    st.title('Top 10 athletes of ' + selected_country)
    top10_df = helper.most_succesful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sport = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
                    'Gymnastics', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 
                    'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
                    'Archery', 'Volleyball', 'Table Tennis', 'Baseball', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon']
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df["Medal"] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)

    if selected_sport != 'Overall':
        temp_df = df[df['Sport'] == selected_sport]
    else:
        temp_df = df

    helper.weight_v_height(temp_df, selected_sport)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    ax.set_xlabel('Weight (kg)')
    ax.set_ylabel('Height (cm)')
    ax.set_title(f'Weight vs Height for {selected_sport}')

    st.pyplot(fig)

    st.title('Men VS Women Participation in Olympics')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', "Female"])
    st.plotly_chart(fig)
