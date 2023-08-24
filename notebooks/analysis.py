import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/country_notes.csv')


# DATA CLEANING

missing_values = df.isnull().sum() # Check for missing values
duplicate_rows = df.duplicated().sum() # Check for duplicate rows
data_types = df.dtypes # Check data types for each column
df = df[df['Country'] != 'Unknown'] # Filter out rows where 'Country' is "Unknown"
# print(missing_values, duplicate_rows, data_types)


# DATA EXPLORATION

# Remove countries with Perfume Count below median
df_perfumes = df['Perfume Count'].drop_duplicates(keep = 'first').sort_values(ascending = False)
perfumes_median = df_perfumes.median()
df = df[df['Perfume Count'] > perfumes_median]

# Get Top 10 notes from each Country
df_sorted = df.sort_values(['Country', 'Note Count'], ascending=[True, False])
df_top10 = df_sorted.groupby('Country').apply(lambda x: x.nlargest(10, 'Note Count')).reset_index(drop = True)

# Store top 10 notes in a dict for easy lookup
dict_top10 = {}
for country in df_top10['Country'].unique():
    dict_top10[country] = df_top10[df_top10['Country'] == country]

print(dict_top10['United Kingdom'])