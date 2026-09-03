"""Streamlit app entry point for cloud deployment."""
import os
import sys

# Add the project directory to the path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

try:
    # Try to run the full app
    from app import main
    main()
except Exception as e:
    # Fallback to basic error handling
    import streamlit as st
    st.error(f"Error loading app: {str(e)}")
    st.info("Please ensure ANTHROPIC_API_KEY is set in Streamlit secrets.")
