import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import  plotly.figure_factory as ff
df = pd.read_csv("athlete_events.csv")
region_df =  pd.read_csv(r"C:\Users\vivek gupta\Downloads\noc_regions.csv")

df = preprocessor.preprocess(df , region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://www.australiantimes.co.uk/wp-content/uploads/2021/07/Olympics-Image-by-Gerhard-G.-from-Pixabay--1200x858.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally' , 'Overall Analysis' , 'Country-wise Analysis' , 'Athlete wise Analysis')
)

if user_menu  == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years , country =  helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year" , years)
    selected_country = st.sidebar.selectbox("Select Country" , country)

    medal_tally = helper.fetch_medal_tally(df , selected_year , selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall'    and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall'    and selected_country != 'Overall':
        st.title(str(selected_country) + ' Overall Performance')
    if selected_year != 'Overall'    and selected_country != 'Overall':
        st.title(str(selected_country) + ' Performance in ' + str(selected_year) + ' Olympics')
    st.dataframe(medal_tally)




if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events  = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header("Total Olympics")
        st.title(editions)
    with col2:
        st.header("Hosted cities")
        st.title(cities)
    with col3:
        st.header("Total different Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Total Events")
        st.title(events)
    with col2:
        st.header("Total Nations Participated")
        st.title(nations)
    with col3:
        st.header("Total Athletes Participated")
        st.title(athletes)
    nations_over_time = helper.data_over_time(df , 'region')
    fig = px.line(nations_over_time, x='Edition', y = 'region')
    st.title("Participating Nation Over the Years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df , 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events Over the Years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title("Athelete Participating Over the Years")
    st.plotly_chart(fig)

    st.title("No.of Events over time(Every Sports")
    fig , ax =  plt.subplots(figsize = (20 , 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)


    st.title("Most Successful Athletes")
    sport_list  = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0 , 'Overall')
    selected_sport = st.selectbox('Select a Sport' , sport_list)
    if selected_sport == 'Overall':
        x = helper.most_successful(df)
    else :
        x = helper.most_successfuls(df, selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    Selected_country = st.sidebar.selectbox('Select a Country' , country_list)



    st.title(Selected_country + " Medal Tally Over the Years")
    temp_df = df.dropna(subset=['Medal'])
    medal_list = temp_df['Medal'].unique().tolist()
    medal_list.insert(0, 'Overall')
    selected_medal = st.selectbox('Select medal', medal_list)
    country_df = helper.year_wise_medal_tally(df , Selected_country , selected_medal)
    if selected_medal == 'Overall':
        fig = px.line(country_df, x='Year', y='Medal')
    else :
        fig = px.line(country_df, x='Year', y='count')


    st.plotly_chart(fig)

    st.title(Selected_country + " Excel in the Following Sports")
    pt = helper.country_event_heatmap(df , Selected_country)
    fig , ax =  plt.subplots(figsize = (20 , 20))
    ax = sns.heatmap(pt , annot = True)
    st.pyplot(fig)


    st.title('Male vs Female Participation in ' + Selected_country + ' Over the Year')
    final = helper.gender_participation(df , Selected_country)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


    st.title('Top 10 Athletes of ' + Selected_country)
    top10_df = helper.most_successful_countrywise(df , Selected_country)
    st.table(top10_df)



if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize = False , width = 1000 , height = 600)
    st.title('Distributions of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby',
                     'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distributions of Age wrt Sports(Gold Medalist')
    st.plotly_chart(fig)

    st.title('Height Vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_heght(df , selected_sport)
    fig , ax =  plt.subplots(figsize = (10 , 10))
    ax = sns.scatterplot(x = athlete_df['Weight'] , y = athlete_df['Height'] , hue = temp_df['Medal'] , style = temp_df['Sex'] , s= 60)
    st.pyplot(fig)


    st.title('Mens Vs Women Participation Over the Year')
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize = False , width = 1000 , height = 600)
    st.plotly_chart(fig)

