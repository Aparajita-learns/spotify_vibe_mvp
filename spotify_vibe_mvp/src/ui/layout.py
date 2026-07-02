"""
Spotify Vibe — Sidebar layout and navigation.
"""

import streamlit as st


def render_sidebar():
    """Renders the Spotify-inspired sidebar with logo and navigation."""
    with st.sidebar:
        # Logo
        st.markdown(
            """
            <div class="sidebar-logo">
                <span class="sidebar-logo-icon">🎧</span>
                <span class="sidebar-logo-text">Spotify Vibe</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation items
        nav_items = [
            ("🏠", "Home", True),
            ("🔍", "Search", False),
            ("✨", "Your Vibe", False),
        ]

        for icon, label, active in nav_items:
            active_cls = " active" if active else ""
            st.markdown(
                f"""
                <div class="nav-item{active_cls}">
                    <span>{icon}</span>
                    <span>{label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Library section
        st.markdown(
            """
            <div style="padding: 0 14px; margin-top: 8px;">
                <p style="font-size:0.75rem; font-weight:600; text-transform:uppercase;
                   letter-spacing:1.5px; color:#727272; margin-bottom:12px;">
                    Your Library
                </p>
                <div class="nav-item">
                    <span>💚</span>
                    <span>Liked Songs</span>
                </div>
                <div class="nav-item">
                    <span>📻</span>
                    <span>Your Episodes</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Footer
        st.markdown(
            """
            <div style="position:fixed; bottom:16px; padding:0 14px;">
                <p style="font-size:0.7rem; color:#555; font-weight:300;">
                    AI-Native Music Discovery MVP
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
