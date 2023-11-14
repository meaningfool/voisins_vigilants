import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data from communes.csv into a dataframe
data = pd.read_csv('communes_final.csv', usecols=['code_postal', 'latitude', 'longitude', 'nom_commune_complet', 'commune_fleurie', 'commune_vigilante', 'communaute_vigilante'], dtype={'code_commune_INSEE': str, 'latitude': float, 'longitude': float, 'nom_commune_complet': str, 'commune_fleurie': int, 'commune_vigilante': int, 'communaute_vigilante': int})
data['code_postal'] = data['code_postal'].astype(str)
# Filter the data on cities within the metropolitan area
filtered_data = data[(data['latitude'] >= 40) & (data['latitude'] <= 52) & (data['longitude'] >= -6) & (data['longitude'] <= 10)]


# Display title intro
st.title("Voisins vigilants: a look at the data")   
st.info('This small project was born from cycling in France and noticing those creepy "Voisins vigilants" roadsigns. I also noticed some "Villes fleuries" roadsigns. I was curious if there was any correlation between the 2. And so I went on to scrape the data about both programs. Please note that the data is incomplete for Voisins Vigilants as I could not find a list and had to rely on cities that mention it on their website.', icon="ℹ️")


# Search for a city
st.header("Is your city member of Voisins Vigilants?")
with st.form("city_search"):
    search_text = str(st.text_input("Search a city", placeholder="Search by name or postal code"))
    submitted = st.form_submit_button("Submit")

    if(submitted):
        searched_data = filtered_data[(filtered_data['nom_commune_complet'].str.contains(search_text, case=False)) | (filtered_data['code_postal'].str.contains(search_text, case=False))][['nom_commune_complet', 'code_postal', 'commune_fleurie', 'commune_vigilante', 'communaute_vigilante']].rename(columns={'nom_commune_complet': 'City name', 'code_postal': 'Code postal', 'commune_fleurie': 'Is part of Voisins Vigilants?', 'commune_vigilante': 'Is part of Commune fleurie?', 'communaute_vigilante': 'Has at least one communauté vigilante?'})

        if(len(searched_data)>0):
            st.table(searched_data)
        else:
            st.write("No city matching your search")

# Display a map of France with the locations of cities that have both commune_vigilante and commune_fleurie equal to 1
st.header("Correlation between Communes vigilantes and Villes fleuries")
communes_vigilantes_or_fleuries = filtered_data[(filtered_data['commune_vigilante'] == 1) | (filtered_data['commune_fleurie'] == 1)]

# Create a confusion matrix
confusion_matrix = pd.crosstab(communes_vigilantes_or_fleuries['commune_fleurie'], communes_vigilantes_or_fleuries['commune_vigilante'])
confusion_matrix = confusion_matrix.reindex(index=[1,0], columns=[0,1])

# Display the confusion matrix
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='g')

col1, col2 = st.columns([3,2])
col1.pyplot(fig)
col2.write("There is almost no overlap between Ville fleurie and Commune vigilante.")


communes_vigilantes_and_fleuries = filtered_data[(filtered_data['commune_vigilante'] == 1) & (filtered_data['commune_fleurie'] == 1)]
col1, col2 = st.columns([3,2])
col2.table(communes_vigilantes_and_fleuries['nom_commune_complet'].reset_index(drop=True))
col1.map(communes_vigilantes_and_fleuries, size=10000, zoom=4)



st.divider()
st.header("Focus on cities part of Voisins Vigilants")
cities_vigilante = filtered_data[filtered_data['commune_vigilante'] == 1]
st.map(cities_vigilante)


st.divider()
st.header("Focus on cities part of Villes fleuries")
cities_fleurie = filtered_data[filtered_data['commune_fleurie'] == 1]
st.map(cities_fleurie)


st.divider()
st.header("Focus on cities part with at least 1 registered communauté vigilante")
st.info('The "communautés vigilantes" are referenced on the Voisins Vigilants website. There are commuautés in cities that are not part of the program.', icon="ℹ️")
cities_communaute_vigilante = filtered_data[filtered_data['communaute_vigilante'] == 1]
st.map(cities_communaute_vigilante, size=10)

