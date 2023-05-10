import pandas as pd
import numpy as np
def list(df):
    country=np.unique(df.region.dropna().values).tolist()
    country.insert(0,'Overall')
    year=df.Year.unique().tolist()
    year.sort()
    year.insert(0,'Overall')
    return year,country
def get(df,year,country):
    medal = df.dropna(subset='Medal').drop_duplicates(
        subset=['Team', 'NOC', 'region', 'Sport', 'Event', 'Year', 'Medal'])
    if year=='Overall' and country=='Overall':
        temp_df=medal.groupby('region')[['Gold','Silver','Bronze']].sum()
        temp_df['Total']=temp_df['Gold']+temp_df['Silver']+temp_df['Bronze']
        return temp_df
    elif year=='Overall' and country !='Overall':
        temp_df=medal[medal['region']==country].groupby(['region','Year'])[['Gold','Bronze','Silver']].sum()
        temp_df['Total']=temp_df['Gold']+temp_df['Silver']+temp_df['Bronze']
        return temp_df
    elif year!='Overall' and country=='Overall':
        temp_df=medal[medal['Year']==year].groupby(['region','Year'])[['Gold','Bronze','Silver']].sum()
        temp_df['Total']=temp_df['Gold']+temp_df['Silver']+temp_df['Bronze']
        return temp_df
    else:
        temp_df=medal[(medal['region']==country) & (medal['Year']==year)].groupby('Year')[['Gold','Silver','Bronze']].sum()
        temp_df['Total']=temp_df['Gold']+temp_df['Silver']+temp_df['Bronze']
        return temp_df

def PNA(df,col):
    pn=df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index()
    pn=pn.rename(columns={'index':'Year','Year':'No of participating Nations'})
    pn.columns=['Year',col]
    pn=pn.sort_values(by='Year')
    return pn
def Success(df,l):
    if l=='Overall':
        temp_df = df.dropna(subset=['Medal']).groupby(['Name', 'Sport'])[['Gold', 'Silver', 'Bronze']].sum()
        temp_df['Total'] = temp_df['Gold'] + temp_df['Bronze'] + temp_df['Silver']
        temp_df = temp_df.sort_values(by='Total').sort_values(by='Total', ascending=False).head(10)
        return temp_df
    else:
        temp_df = df.dropna(subset=['Medal'])
        temp_df = temp_df[temp_df['Sport'] == l].groupby(['Name', 'Sport'])[['Gold', 'Silver', 'Bronze']].sum()
        temp_df['Total'] = temp_df['Gold'] + temp_df['Bronze'] + temp_df['Silver']
        temp_df = temp_df.sort_values('Total', ascending=False).head(10)
        return temp_df
def country(df,year,region):
    medal = df.dropna(subset='Medal').drop_duplicates(subset=['Team', 'NOC', 'region', 'Sport', 'Event', 'Year', 'Medal'])
    if year=='Overall' and region=='Overall':
            x = medal.groupby(['Year', 'region'])[['Gold', 'Silver', 'Bronze']].sum().sum(axis=1).reset_index().rename(
                columns={0: 'Total'})
            return x
    if year=='Overall' and region !='Overall':
        x=medal[(medal['region']=="USA")].groupby('Year')[['Gold','Silver','Bronze']].sum().sum(axis=1).sort_index().reset_index().rename(columns={0:'Total'})
        return x
    if year !='Overall' and region=='Overall':
        x=medal[(medal['Year']==year)].groupby('region')[['Gold','Silver','Bronze']].sum().sum(axis=1).sort_values(ascending=False).reset_index().rename(columns={0:'Total'})
        return x
    if year !='Overall' and region !='Overall':
        x=medal[(medal['region']==region) &(medal['Year']==year)].groupby('Year')[['Gold','Silver','Bronze']].sum().sum(axis=1).sort_index().reset_index().rename(columns={0:'Total'})
        return x
def heatmap(df,region):
    medal = df.dropna(subset='Medal').drop_duplicates(
        subset=['Team', 'NOC', 'region', 'Sport', 'Event', 'Year', 'Medal'])
    x=medal[medal['region']==region].pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
    return x
def suc(df,region):
    x=df[df['region']==region].groupby('Name')[['Gold','Silver','Bronze']].sum().sum(axis=1).reset_index().rename(columns={0:'Total'}).sort_values(by='Total',ascending=False).head(10)
    return x
def pie(df,region):
    if region=='Overall':
        data=df.groupby('Sex')['Sex'].value_counts()
        return data
    else:
        data=df[df['region']==region].groupby('Sex',as_index=False)['Sex'].value_counts()
        return data







