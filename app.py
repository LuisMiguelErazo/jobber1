import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_wordcloud import st_wordcloud
import zipfile

with zipfile.ZipFile('map_skills.zip', 'r') as zipf:
    with zipf.open('map_skills.csv') as f:
        df = pd.read_csv(f)

st.title('Interactive Salary and Skills Dashboard')

categories = sorted(df['Category'].unique().tolist())
categories = ['All'] + categories

category = st.selectbox('Category', categories)
industries = df['Industry'].unique() if category == 'All' else df[df['Category'] == category]['Industry'].unique()
industries = ['All'] + sorted(industries.tolist())
industry = st.selectbox('Industry', industries)
experiences = df['Experience Level'].unique() if industry == 'All' else df[(df['Category'] == category) & (df['Industry'] == industry)]['Experience Level'].unique()
experiences = ['All'] + sorted(experiences.tolist())
experience = st.selectbox('Experience Level', experiences)

def update_map(category, industry, experience):
    filtered_df = df.copy()
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    if industry != 'All':
        filtered_df = filtered_df[filtered_df['Industry'] == industry]
    if experience != 'All':
        filtered_df = filtered_df[filtered_df['Experience Level'] == experience]

    state_salary = filtered_df.groupby('State').agg(
        Medium_Salary=('Medium Salary', 'mean'),
        Data_Count=('Medium Salary', 'size')
    ).reset_index()

    fig = px.choropleth(state_salary,
                        locations='State',
                        locationmode='USA-states',
                        color='Medium_Salary',
                        color_continuous_scale='Viridis',
                        scope='usa',
                        labels={'Medium_Salary': 'Medium Salary'},
                        hover_data={'State': True, 'Medium_Salary': True, 'Data_Count': True})
    fig.update_layout(title='Medium Salary by State', geo=dict(scope='usa'))
    st.plotly_chart(fig)

def plot_wordcloud(category):
    if category != 'All':
        filtered_df = df[df['Category'] == category]
        text = ' '.join(filtered_df['Soft Skill'].dropna().tolist())
        words = text.split()
        word_freq = pd.Series(words).value_counts().to_dict()
        
        st_wordcloud(word_freq, height=400, key='wordcloud')
    else:
        st.write('Select a Category to Display Word Cloud')

update_map(category, industry, experience)
plot_wordcloud(category)
