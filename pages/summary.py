import streamlit as st
from transformers import pipeline
from style import apply_custom_style

def setup_ui():
    st.set_page_config(page_title="Summary", layout="wide")
    apply_custom_style()
    st.markdown("<h2 style='text-align:center; color:darkgreen;'>Article Summary</h2>", unsafe_allow_html=True)

@st.cache_resource
def get_summary_model():
    return pipeline("summarization", model="Falconsai/text_summarization")

def splittext(text, chunk_size=600): 
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_summ(text_chunks, model):
    summaries = []
    for chunk in text_chunks:
        if len(chunk.split()) < 30:
            continue
        summary = model(chunk, max_length=60, min_length=20, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return " ".join(summaries) if summaries else None

setup_ui()

if 'article_text' not in st.session_state:
    st.warning("Please process an article first")
else:
    summarizer = get_summary_model()
    articlecontent = st.session_state['article_text']
    
    with st.spinner("Creating summary"):
        textchunks = splittext(articlecontent)
        final_summ = generate_summ(textchunks, summarizer)
        
        if final_summ:
            st.write(final_summ)
        else:
            st.info("Not enough content to summarize")
