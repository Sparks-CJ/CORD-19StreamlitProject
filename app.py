# ========================================
# CORD-19 Data Analysis and Streamlit App
# ========================================

# Part 1: Load and Explore Dataset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import streamlit as st

# Load CSV
try:
    df = pd.read_csv('metadata.csv')
    st.write("Dataset loaded successfully.")
except FileNotFoundError:
    st.error("metadata.csv file not found. Please place it in the working directory.")

# Display basic info
st.write("Shape of dataset:", df.shape)
st.write(df.head())
st.write(df.info())
st.write("Missing values per column:\n", df.isnull().sum())

# Part 2: Data Cleaning
# Handle missing publish_time
df = df.dropna(subset=['publish_time'])

# Convert publish_time to datetime and extract year
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df = df.dropna(subset=['publish_time'])
df['year'] = df['publish_time'].dt.year

# Optional: Create abstract word count
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(str(x).split()))

# Part 3: Data Analysis & Visualization

# 1. Publications by Year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
sns.barplot(x=year_counts.index, y=year_counts.values, palette="viridis")
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Publications")
st.pyplot(plt.gcf())

# 2. Top Journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="magma")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
st.pyplot(plt.gcf())

# 3. Word Cloud of Paper Titles
text = " ".join(title for title in df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(15,7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
st.pyplot(plt.gcf())

# 4. Publications by Source
source_counts = df['source_x'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=source_counts.index, y=source_counts.values, palette="cool")
plt.title("Top Sources of Papers")
plt.xlabel("Source")
plt.ylabel("Number of Papers")
st.pyplot(plt.gcf())

# Part 4: Streamlit App Interactive Widgets
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers interactively.")

# Filter by Year Range
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.slider("Select Year Range", min_year, max_year, (2020, 2021))
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"Showing papers from {year_range[0]} to {year_range[1]}")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'year']].head(20))

# Optional: Select top journals interactively
selected_journal = st.selectbox("Select Journal to Explore", df['journal'].dropna().unique())
st.write(filtered_df[filtered_df['journal'] == selected_journal][['title', 'year', 'authors']].head(10))

st.write("Interactive visualizations and exploration complete.")
