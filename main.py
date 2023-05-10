import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st

import helper, preprocessor

df = pd.read_csv(r'data/athlete_events.csv')
region = pd.read_csv(r'data/noc_regions.csv')
df = preprocessor.preprocess(df, region)
st.sidebar.title('Olympic Analysis')
st.sidebar.image(
    'https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athelete Wise Analysis')
)
if user_menu == 'Medal Tally':
    year,country=helper.list(df)
    st.sidebar.header('Medal Tally')
    Year=st.sidebar.selectbox('Select Year',year)
    Country=st.sidebar.selectbox('Select Country',country)
    medal=helper.get(df,Year,Country)
    if Year=='Overall' and Country=='Overall':
        st.title('Overall Tally')
    if Year=='Overall' and Country !='Overall':
        st.title('Performance of'+ Country+ 'in Year'+str(Year))
    if Year !='Overall' and Country=='Overall':
        st.title('Performance of All Countires in Year'+str(Year))
    if Year !='Overall' and Country !='Overall':
        st.title('Performance of {} in Year {}'.format(Country,Year))
    st.table(medal)
if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]
    cities=df.City.unique().shape[0]
    sports=df.Sport.unique().shape[0]
    events=df.Event.unique().shape[0]
    atheletes=df.Name.unique().shape[0]
    nations=df.region.unique().shape[0]
    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col4,col5,col6=st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)
    with col5:
        st.header('Atheletes')
        st.title(atheletes)
    with col6:
        st.header('Participating Nations')
        st.title(nations)

    pn=helper.PNA(df,'region')
    fig=px.line(pn,x='Year',y='region')
    st.title('Participating Nation in Each Year')
    st.plotly_chart(fig)
    pn=helper.PNA(df,'Event')
    fig=px.line(pn,x='Year',y='Event')
    st.title('Events In Each Year of Olympics')
    st.plotly_chart(fig)
    pn=helper.PNA(df,'Name')
    fig=px.line(pn,x='Year',y='Name')
    st.title('No of Atheletes in Each Year')
    st.plotly_chart(fig)
    st.title('No. of Events over time(Every Sport)')
    fig,ax=plt.subplots(figsize=(20,20))
    d=df.drop_duplicates(subset=['Year','Sport','Event']).pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0)
    ax=sns.heatmap(d,annot=True)
    st.pyplot(fig)
    st.title('Most Successful Atheletes')
    sport_list=df.Sport.unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    sport_selected=st.selectbox('Select a Sport',sport_list)
    top10=helper.Success(df,sport_selected)
    st.table(top10)
if user_menu == 'Country-Wise Analysis':
    year,country=helper.list(df)
    select_year=st.sidebar.selectbox('Select Year',year)
    select_country=st.sidebar.selectbox('Select Country',country)
    table=helper.country(df,select_year,select_country)
    if select_country=='Overall' and select_year=='Overall':
        st.title('Total Medals by each Country')
        fig=px.line(table,x='Year',y='Total',color='region')
        st.plotly_chart(fig)
    if select_country!='Overall' and select_year == 'Overall':
        st.title('Medal Won by'+select_country+'in Overall Years')
        fig=px.line(table,x='Year',y='Total')
        st.plotly_chart(fig)
    if select_country =='Overall' and select_year !='Overall':
        st.title('Medal won by each Country in Year'+str(select_year))
        fig=px.line(table,x='Year',y='Total')
        st.plotly_chart(fig)
    if select_year !='Overall' and select_country !='Overall':
        st.title('Total Medal Won by'+select_country+'in Year'+str(select_year))
        st.table(table)
    heat=helper.heatmap(df,select_country)
    st.title('Medal Progression of'+ select_country)
    fig=px.imshow(heat,text_auto=True)
    fig.update_layout(
        {'height':800,
         'width':1000})
    st.plotly_chart(fig)
    succ=helper.suc(df,select_country)
    st.title('Top 10 Atheletics of '+ select_country)
    st.table(succ)
    fig=px.bar(succ,x='Name',y='Total')
    st.plotly_chart(fig)
if user_menu == 'Athelete Wise Analysis':
    st.title('Distribution of Age')
    data=df.Age.dropna()
    data1=df[df['Medal']=='Gold']['Age'].dropna()
    data2 = df[df['Medal'] == 'Silver']['Age'].dropna()
    data3 = df[df['Medal'] == 'Bronze']['Age'].dropna()
    fig=ff.create_distplot([data,data1,data2,data3],['Age Distribution','Age Of Gold distribution','Age of Silver Medal distribution','Age of Bronze Medal distribution'],show_hist=False,show_rug=False)
    st.plotly_chart(fig)
    y,c=helper.list(df)
    select_c=st.selectbox('Select Country',c)
    ratio=helper.pie(df,select_c)
    st.title('Ratio of Male and Female')
    if select_c=='Overall':
        fig,ax=plt.subplots(figsize=(20,10))
        ax=ratio.plot(kind='pie',autopct='%.1f%%')
        st.pyplot(fig)
    else:
        fig=px.pie(ratio,values='count',names='Sex')
        st.plotly_chart(fig)
    men = df[df['Sex'] == 'M'].groupby('Year', as_index=False)['Sex'].value_counts()
    women = df[df['Sex'] == 'F'].groupby('Year', as_index=False)['Sex'].value_counts()
    data = men.merge(women, on='Year', how='left')
    data.fillna(0, inplace=True)
    data.rename(columns={'count_x': 'Male', 'count_y': 'Female'}, inplace=True)
    fig=px.line(data, x='Year', y=['Male', 'Female'])
    st.title('Participation Trend of Male and Female ')
    st.plotly_chart(fig)
















