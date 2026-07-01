"""
Spotify Vibe — Reusable HTML components rendered via st.markdown().
All HTML strings must start at column 0 (no leading whitespace)
to prevent Streamlit's markdown renderer from treating them as code blocks.
"""

from textwrap import dedent


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


import urllib.parse

def vibe_chips(moods: dict[str, str]) -> str:
    """
    Returns HTML for quick-select mood chips.
    moods: dict of {label: emoji}
    """
    chips_html = ""
    for label, emoji in moods.items():
        encoded_label = urllib.parse.quote(label)
        chips_html += (
            f'<a href="?show_vibe=true&mood={encoded_label}" target="_self" style="text-decoration:none;">'
            f'<span class="vibe-chip">{emoji} {label}</span>'
            f'</a>\n'
        )
    return f'<div class="chip-container">{chips_html}</div>'


def top_pick_card(title: str, artist: str, score: float, reason: str) -> str:
    """Returns the highlighted top pick card HTML."""
    score_pct = int(score * 100)
    return dedent(f"""\
<div class="top-pick-card">
<div class="top-pick-label">✨ Best match right now</div>
<div class="top-pick-title">{title}</div>
<div class="top-pick-artist">{artist}</div>
<div class="top-pick-score">🎯 {score_pct}% match</div>
<div class="top-pick-reason">{reason}</div>
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
