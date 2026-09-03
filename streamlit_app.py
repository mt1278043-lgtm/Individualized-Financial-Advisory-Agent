"""Streamlit app entry point for cloud deployment."""
import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from app import main

if __name__ == "__main__":
    main()
