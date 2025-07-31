import streamlit as st
from transformers import pipeline
from style import apply_custom_style

def setup():
    st.set_page_config(page_title="Sentiment", layout="wide")
    apply_custom_style()
    st.markdown("<h2 style='text-align:center; color:darkgreen;'>Article Sentiment</h2>", unsafe_allow_html=True)

@st.cache_resource
def get_sentiment_model():
    return pipeline("sentiment-analysis")

def analyze_senti(text_chunk, sentiment_pipeline):
    result = sentiment_pipeline(text_chunk)[0]
    return {
        'label': result['label'],
        'confidence': round(result['score'] * 100)
    }

setup()

if 'article_text' not in st.session_state:
    st.warning("Please load an article first.")
else:
    article_snippet = st.session_state['article_text'][:512]
    sentiment_pipeline = get_sentiment_model()
    
    try:
        with st.spinner("Analyzing sentiment"):
            analysis = analyze_senti(article_snippet, sentiment_pipeline)
            st.write(f"**Sentiment:** {analysis['label']} ({analysis['confidence']}%)")
    except Exception:
        st.error("Could not analyze sentiment.")
