import streamlit as st
import pandas as pd
import ast
import re

url = 'https://github.com/bmbln/gender_sentiment/blob/main/gender_models.parquet?raw=true'

@st.cache_data
def load_data():
    df = pd.read_parquet(url)
    
    return df

#Add title to the app
st.title('Gender Sentiment App (beta)')

#read in data and convert into a dictionary
df = load_data()

pairs = st.radio('Choose a pair-set: ', options=df.pairs.unique())
metric = st.radio('Choose a metric: ', options=['simple', 'simple_avg', 'diff', 'diff_avg'], index=1)

gender_dict = df[df.pairs == pairs][['word', metric]].set_index('word').rename({metric: 'val'}, axis=1).to_dict(orient='index')
for k, v in gender_dict.items():
    gender_dict[k] = ast.literal_eval(v['val'])


txt = st.text_area('Insert a sample text')

new_text = []
# loop through words in the text and color them based on the color dictionary
for word in txt.split(' '):
    # check if the word is in the color dictionary
    clean_word = re.sub(r"[^a-zA-Z0-9'\s]", '', word)
    if clean_word in gender_dict:
        clean_word = clean_word
    else:
        clean_word = clean_word.lower()
    
    if clean_word in gender_dict:
        # get the color and shade values for the word from the dictionary
        color = gender_dict[clean_word]["colour"]
        shade = round(gender_dict[clean_word]["shade"] , 2)
        if color == 'red':
            rgba = f'rgba(255, 0, 0, {shade})'
        else:
            rgba = f'rgba(0, 0, 255, {shade})'
        
        text_color = 'black'
        if shade > 0.5:
            text_color = 'white'

        # create HTML code for the colored word
        colored_word = f'<u style="color:{text_color} ;background-color: {rgba};">{word}</u>'
        new_text.append(colored_word)
    else:
        new_text.append(word)

# print the final HTML text
st.write(' '.join(new_text) , unsafe_allow_html=True)


