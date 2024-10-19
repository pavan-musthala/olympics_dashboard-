import numpy as np
import pandas as pd
import seaborn as sns
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset = ['Team','NOC','Year','City','Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    medal_tally['Total Medals'] = medal_tally["Gold"] + medal_tally["Silver"]+ medal_tally["Bronze"]
    return medal_tally


def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return year,country

    

def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset = ['Team','NOC','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    else:
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
        x['Total Medals'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    return x

def data_overtime(df, col):
    # Check if the specified column exists
    if col not in df.columns:
        raise ValueError(f"Column '{col}' does not exist in the DataFrame.")
    
    # Ensure columns are stripped of whitespace
    df.columns = df.columns.str.strip()

    # Print the DataFrame structure for debugging
    print("Columns in DataFrame:", df.columns)
    
    # Check for the relevant columns before proceeding
    print(df[['Year', col]].head())

    # Dropping duplicates and calculating value counts
    nations_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_overtime.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    nations_overtime.sort_values('Edition', ascending=True, inplace=True)  # Sort by Edition
    return nations_overtime



def most_succesfull(df, sport):
    temp_df = df.dropna(subset = ['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on = 'index', right_on = 'Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns = {'index':'Name', 'Name_x':"Medals"}, inplace = True)
    return x

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team', 'NOC', 'Year', 'City','Sport', 'Event', 'Medal'], inplace = True)

    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pt

def most_succesful_countrywise(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]
    
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on = 'index', right_on = 'Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns = {'index':'Name', 'Name_x':"Medals"}, inplace = True)
    return x

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset= ['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace = True)
    if sport != 'Overall':
         temp_df = athlete_df[athlete_df['Sport']== sport]
         return temp_df
    else:
        return athlete_df
    
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset= ['Name', 'region'])

    men = athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on= 'Year', how= 'left')
    final.rename(columns = {'Name_x': 'Male', 'Name_y': 'Female'}, inplace = True)

    final.fillna(0, inplace = True)

    return final