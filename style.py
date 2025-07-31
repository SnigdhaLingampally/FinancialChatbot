import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
            body {
                background: honeydew;
                font-family: 'Segoe UI', sans-serif;
            }
            
            section[data-testid="stSidebar"] {
                background: lightgreen !important;
            }
            
            h1, h2, h3 {
                color: seagreen;
                text-align: center;
            }
            
            .keyword-block, 
            .summary-block, 
            .qa-block {
                background: palegreen;
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 10px;
                font-weight: 500;
                box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
            }
            
            .warning {
                color: firebrick;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)