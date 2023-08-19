import streamlit as st

def setup_page():
    # Set page title
    st.markdown("<h1 style='text-align: center; color: #0F596E;'>Lunch Assistant</h1>",
                unsafe_allow_html=True
                )

    #Center radio buttons
    st.markdown("<style> div.row-widget.stRadio > div{flex-direction:row;justify-content: center;font-size: 26px; </style>",
                unsafe_allow_html=True
                )

    #Center Metrics
    st.markdown("""
    <style>
    [data-testid="metric-container"] {
        width: fit-content;
        margin: auto;
    }

    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }

    [data-testid="metric-container"] label {
        width: fit-content;
        margin: auto;
    }
    </style>""",
    unsafe_allow_html=True)

    #Make page larger
    st.markdown("""
    <style>
    .css-1y4p8pa {
        width: 100%;
        padding: 6rem 1rem 10rem;
        max-width: 66rem;
    }
    </style>""",
    unsafe_allow_html=True)
