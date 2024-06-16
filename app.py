import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv('map_skills.csv')

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
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Top Soft Skills in {category} Category')
        st.pyplot(plt)
    else:
        st.write('Select a Category to Display Word Cloud')

update_map(category, industry, experience)
plot_wordcloud(category)
