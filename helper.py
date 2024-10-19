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
    print("Columns in DataFrame:", df.columns.tolist())
    print("First few rows of DataFrame:")
    print(df.head())  # Print the first few rows of the DataFrame

    # Check if 'Year' column exists
    if 'Year' not in df.columns:
        raise ValueError("Column 'Year' does not exist in the DataFrame.")
    
    # Create a DataFrame with unique Year and specified column
    nations_overtime = df.drop_duplicates(['Year', col])
    
    # Ensure there are rows to work with
    if nations_overtime.empty:
        raise ValueError("No data available after dropping duplicates.")
    
    # Value counts for the specified column
    value_counts = nations_overtime['Year'].value_counts().reset_index()
    
    # Check the structure before renaming
    print("Value counts before renaming:", value_counts.head())
    
    # Rename columns appropriately
    value_counts.columns = ['Edition', col]  # Assign names directly to avoid KeyErrors
    
    # Check the structure after renaming
    print("Value counts after renaming:", value_counts.head())

    # Print the columns of value_counts for debugging
    print("Columns in value_counts:", value_counts.columns.tolist())
    
    # Ensure 'Edition' column exists before sorting
    if 'Edition' not in value_counts.columns:
        raise ValueError("Column 'Edition' does not exist after renaming.")
    
    # Sort by 'Edition'
    value_counts.sort_values('Edition', ascending=True, inplace=True)
    
    return value_counts




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
    # Check if necessary columns exist
    if 'Medal' not in df.columns or 'region' not in df.columns:
        raise ValueError("DataFrame must contain 'Medal' and 'region' columns.")

    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    # Get the top 10 countries by medal count
    medal_counts = temp_df['Name'].value_counts().reset_index().head(10)
    medal_counts.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge to get additional information
    x = medal_counts.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')
    
    return x[['Name', 'Medals', 'Sport', 'region']]


def weight_v_height(df, sport):
    # Check if necessary columns exist
    if 'Name' not in df.columns or 'region' not in df.columns or 'Sport' not in df.columns:
        raise ValueError("DataFrame must contain 'Name', 'region', and 'Sport' columns.")

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        if temp_df.empty:
            raise ValueError(f"No data available for sport: {sport}")
        return temp_df
    else:
        return athlete_df

    
def men_vs_women(df):
    # Check if necessary columns exist
    if 'Name' not in df.columns or 'Sex' not in df.columns or 'Year' not in df.columns:
        raise ValueError("DataFrame must contain 'Name', 'Sex', and 'Year' columns.")

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left', suffixes=('_Male', '_Female'))
    final.rename(columns={'Name_Male': 'Male', 'Name_Female': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final

