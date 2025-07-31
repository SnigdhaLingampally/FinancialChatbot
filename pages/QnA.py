import streamlit as st
import google.generativeai as genai
from style import apply_custom_style

def setup_app_ui():
    st.set_page_config(
        page_title="Financial News Assistant",
        layout="centered"
    )
    apply_custom_style()
    st.title("Ask About the Article")
    st.markdown("""
        <style>
            .title-text {
                color: darkgreen;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
                margin-bottom: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

def generate_gemini_response(question, context):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        prompt = f"""
        You're a financial news assistant. Answer the question based on the provided article.
        Keep responses concise (1-2 sentences) and factual.

        Article:
        {context}

        Question: {question}

        Answer:
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error("Failed to get response from Gemini")
        st.write(f"Technical details: {str(e)}")
        return None

def display_answer(answer):
    if not answer:
        return
    answer_container = st.container()
    with answer_container:
        st.markdown("### Answer")
        st.info(answer)

def main():
    genai.configure("Your api key")
    setup_app_ui()
    if 'article_text' not in st.session_state:
        st.warning("Please analyze an article on the homepage first.")
        st.stop()
    user_question = st.text_input(
        "What would you like to know about the article?",
        placeholder="Type your question here",
        key="user_query"
    )
    if user_question:
        with st.spinner("Analyzing article and preparing response "):
            article_text = st.session_state['article_text'][:5000]
            response = generate_gemini_response(user_question, article_text)
            if response:
                display_answer(response)
            else:
                st.warning("Couldn't generate a response. Please try a different question.")

if __name__ == "__main__":
    main()
