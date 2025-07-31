import streamlit as st
import re
from newspaper import Article
from style import apply_custom_style

def setup():
    st.set_page_config(page_title="Financial News Chatbot", layout="wide")
    apply_custom_style()
    st.markdown("<h1 style='text-align:center; color:seagreen;'>Financial News Chatbot</h1>", unsafe_allow_html=True)

def processtext(raw_text):
    cleaned = re.sub(r'\n+', ' ', raw_text)
    cleaned = re.sub(r'Read more.*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'Disclaimer:.*', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

def display_articleinfo(article):
    st.subheader("Details")
    st.write(f"**Title:** {article.title or 'Unknown'}")
    authors = ', '.join(article.authors) if article.authors else 'Unknown'
    st.write(f"**Authors:** {authors}")
    date = article.publish_date or 'Not available'
    st.write(f"**Published Date:** {date}")

def handle_article_processing(url):
    newsarticle = Article(url)
    newsarticle.download()
    newsarticle.parse()
    
    processedcontent = processtext(newsarticle.text)
    
    if len(processedcontent) < 200:
        raise ValueError("Article content too short")
    
    st.session_state.update({
        'url': url,
        'article_text': processedcontent,
        'title': newsarticle.title,
        'authors': newsarticle.authors,
        'publish_date': str(newsarticle.publish_date)
    })
    
    return newsarticle

setup()
article_link = st.text_input("Paste the article link here:")

if article_link:
    try:
        parsedarticle = handle_article_processing(article_link)
        st.success("Article loaded successfully!")
        display_articleinfo(parsedarticle)
    except ValueError as shorterror:
        st.error("Article too short. Try a different one.")
    except Exception as generalerror:
        st.error("Could not process the article.")