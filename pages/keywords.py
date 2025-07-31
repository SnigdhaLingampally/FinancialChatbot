import streamlit as st
from keybert import KeyBERT
import re
from style import apply_custom_style

def setup_ui():
    st.set_page_config(page_title="Keyword Extractor", layout="wide")
    apply_custom_style()
    st.markdown(
        "<h2 style='text-align:center; color:darkgreen;'>Extracted Keywords</h2>",
        unsafe_allow_html=True
    )

def clean_text(raw_text):
    text_wo_links = re.sub(r"http\S+", "", raw_text)
    cleaned = re.sub(r"\s+", " ", text_wo_links)
    return cleaned.strip()

@st.cache_resource
def load_keybert_model():
    return KeyBERT()

def show_keywords(keywords):
    if not keywords:
        st.info("No keywords could be extracted.")
        return
    
    st.success("Top Keywords:")
    for phrase, _ in keywords:
        st.markdown(f"- **{phrase}**")

def extract_keywords(text, model):
    return model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        top_n=10
    )

def main():
    setup_ui()

    if 'article_text' not in st.session_state:
        st.warning("No article text found. Please go back and input a link first.")
        return

    article_text = st.session_state['article_text']
    cleaned_text = clean_text(article_text)

    kw_model = load_keybert_model()

    try:
        keywords = extract_keywords(cleaned_text, kw_model)
        show_keywords(keywords)
    except Exception as e:
        st.error("Something went wrong during keyword extraction.")
        st.exception(e)

if __name__ == "__main__":
    main()
