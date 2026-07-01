"""
Spotify Vibe — Reusable HTML components rendered via st.markdown().
All HTML strings must start at column 0 (no leading whitespace)
to prevent Streamlit's markdown renderer from treating them as code blocks.
"""

import streamlit as st


def vibe_chips(moods: dict[str, str]) -> str:
    return ""


def vibe_chips_buttons(moods: dict[str, str]):
    st.markdown('<div class="chip-grid">', unsafe_allow_html=True)
    cols = st.columns(len(moods))
    selected = None
    for col, (label, emoji) in zip(cols, moods.items()):
        with col:
            if st.button(f"{emoji} {label}", key=f"chip_{label}"):
                selected = label
    st.markdown('</div>', unsafe_allow_html=True)
    return selected
from textwrap import dedent
import urllib.parse


def animated_vibe_icon() -> str:
    """
    Returns the HTML for the Gemini-style animated glowing Spotify Vibe icon.
    A rotating conic gradient border orbits the music icon with a pulsing glow.
    """
    return dedent("""\
<div style="display:flex; justify-content:center; margin-bottom:8px;">
<div class="vibe-icon-container">
<div class="vibe-icon-glow"></div>
<div class="vibe-icon">🎵</div>
</div>
</div>""")


def hero_section() -> str:
    """Returns the HTML for the hero banner with animated icon."""
    icon = animated_vibe_icon()
    return dedent(f"""\
<div class="hero-section">
{icon}
<div class="hero-title">Spotify Vibe</div>
<div class="hero-subtitle">Tell us the vibe. We'll find the soundtrack.</div>
</div>""")


def song_card(rank: int, title: str, artist: str, score: float,
              tag: str, gradient: str) -> str:
    """Returns a single ranked song card HTML."""
    score_pct = int(score * 100)
    return dedent(f"""\
<div class="song-card">
<div class="album-art" style="background:{gradient};">🎶</div>
<div class="song-rank">{rank}</div>
<div class="song-info">
<div class="song-title">{title}</div>
<div class="song-artist">{artist}</div>
<div class="song-tag">{tag}</div>
</div>
<div class="song-score-pill">{score_pct}%</div>
</div>""")


def section_header(title: str, subtitle: str = "") -> str:
    """Returns a section header with optional subtitle."""
    sub = f'<div class="section-subheader">{subtitle}</div>' if subtitle else ""
    return f'<div class="section-header">{title}</div>{sub}'


def content_card(title: str, description: str, gradient: str) -> str:
    """Returns a generic content card (used for placeholders)."""
    return dedent(f"""\
<div class="content-card">
<div class="album-art" style="background:{gradient}; width:100%; height:120px; border-radius:8px; margin-bottom:12px;">
</div>
<div class="content-card-title">{title}</div>
<div class="content-card-desc">{description}</div>
</div>""")
