"""
Spotify Vibe — AI-Native Music Discovery MVP
=============================================

Main Streamlit application entry point.
Simulates a Spotify-like homepage with an AI-powered mood-to-music
recommendation experience.
"""

import streamlit as st
from pathlib import Path

# ── Page config (must be first Streamlit call) ──
st.set_page_config(
    page_title="Spotify Vibe — AI Music Discovery",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "Spotify Vibe — AI-Native Music Discovery MVP",
    },
)


def load_css():
    """Load the custom CSS stylesheet."""
    css_path = Path(__file__).parent / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS not found at assets/styles.css")


def main():
    """Application entry point."""
    # Load custom styles
    load_css()

    # Render sidebar
    from src.ui.layout import render_sidebar
    render_sidebar()

    # Render home page
    from src.ui.home_page import render_home_page
    render_home_page()


if __name__ == "__main__":
    main()
