"""
Spotify Vibe — Home page & Vibe feature toggle.
"""

import streamlit as st

from src.ui.components import (
    hero_section,
    vibe_chips,
    vibe_chips_buttons,
    section_header,
    content_card,
    top_pick_card,
    song_card,
)
from src.ui.theme import MOOD_ICONS, ALBUM_GRADIENTS


def render_spotify_home():
    """Renders a mock Spotify mobile home screen."""

    st.markdown(
        '<div style="font-size:1.5rem; font-weight:700; margin-bottom:4px;">Good evening</div>'
        '<div style="display:flex; gap:16px; font-size:1.2rem; color:#b3b3b3; margin-bottom:24px;">'
        '<span>🔔</span><span>🕒</span><span>⚙️</span></div>',
        unsafe_allow_html=True,
    )

    # ── Clickable animated Spotify Vibe icon (Native st.button styled via CSS) ──
    st.markdown('<div style="text-align:center; margin:24px 0 8px 0;">', unsafe_allow_html=True)
    
    # We render the button using type="primary". The CSS will style all primary buttons
    # on this page to have the rotating border and pulsing glow.
    if st.button("🎵", key="vibe_launcher", type="primary"):
        st.session_state.show_vibe = True
        if not st.query_params.get("mood"):
            st.session_state.mood_input_val = ""
            st.session_state.prev_query_mood = ""
        st.rerun()

    st.markdown(
        '<div style="margin-top:12px;font-size:0.85rem;font-weight:600;color:#1DB954;letter-spacing:1px;text-transform:uppercase;">'
        'Spotify Vibe</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Dummy mixes grid
    cols = st.columns(2)
    mixes = [
        ("Liked Songs", ALBUM_GRADIENTS[0]),
        ("Chill Mix", ALBUM_GRADIENTS[1]),
        ("Discover Weekly", ALBUM_GRADIENTS[2]),
        ("Daily Mix 1", ALBUM_GRADIENTS[3]),
        ("Your Top Songs 2025", ALBUM_GRADIENTS[4]),
        ("Release Radar", ALBUM_GRADIENTS[5]),
    ]

    for i, (title, grad) in enumerate(mixes):
        with cols[i % 2]:
            st.markdown(
                f'<div style="background:#242424; border-radius:4px; display:flex; '
                f'align-items:center; margin-bottom:8px; overflow:hidden;">'
                f'<div style="width:56px; height:56px; background:{grad}; flex-shrink:0;"></div>'
                f'<div style="padding:0 8px; font-size:0.85rem; font-weight:600;">{title}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Trending section ──
    st.markdown(
        section_header("Trending Vibes", "Popular moods across listeners"),
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    trending = [
        ("Chill Evening", "Wind down with mellow beats", ALBUM_GRADIENTS[0]),
        ("Focus Mode", "Deep work, zero distractions", ALBUM_GRADIENTS[1]),
    ]

    for col, (title, desc, grad) in zip(cols, trending):
        with col:
            st.markdown(
                content_card(title, desc, grad),
                unsafe_allow_html=True,
            )


def render_vibe_feature():
    """Renders the actual AI Vibe MVP experience."""
    
    # Back button to return to home
    if st.button("← Back to Home", type="secondary"):
        st.session_state.show_vibe = False
        st.query_params.clear()
        if "mood_input_val" in st.session_state:
            st.session_state.mood_input_val = ""
        if "prev_query_mood" in st.session_state:
            st.session_state.prev_query_mood = ""
        st.rerun()

    # ── Hero section with animated glowing icon ──
    st.markdown(hero_section(), unsafe_allow_html=True)

    # ── Mood input area ──
    st.markdown(
        '<div class="mood-input-section">',
        unsafe_allow_html=True,
    )

    if "mood_input_val" not in st.session_state:
        st.session_state.mood_input_val = ""

    query_mood = st.query_params.get("mood", "")
    if query_mood and st.session_state.get("prev_query_mood") != query_mood:
        st.session_state.mood_input_val = query_mood
        st.session_state.prev_query_mood = query_mood

    mood_input = st.text_input(
        "What's your vibe right now?",
        key="mood_input_val",
        placeholder="e.g. chill evening, gym energy, rainy day nostalgia...",
        label_visibility="collapsed",
    )

    selected_chip = vibe_chips_buttons(MOOD_ICONS)
    if selected_chip and selected_chip != st.session_state.get("prev_query_mood"):
        st.session_state.mood_input_val = selected_chip
        st.session_state.prev_query_mood = selected_chip
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CTA Button ──
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        find_clicked = st.button("🎵 Find My Vibe", type="secondary", use_container_width=True)

    # Load and preprocess song catalog
    from src.data.loader import load_songs_catalog
    from src.data.preprocess import preprocess_songs_df
    try:
        catalog_df = preprocess_songs_df(load_songs_catalog())
    except Exception as e:
        st.error(f"Failed to load song catalog: {e}")
        return

    # ── Parse and display mood profile ──
    if mood_input:
        from src.recommender.mood_parser import parse_mood
        from src.recommender.candidate_generator import generate_candidates
        from src.recommender.scorer import score_candidates
        from src.recommender.ranker import rank_songs
        
        profile = parse_mood(mood_input)
        candidates = generate_candidates(profile, catalog_df)
        scored = score_candidates(candidates, profile)
        ranked = rank_songs(scored)

        if ranked.empty:
            st.warning("No matching songs found for this vibe.")
        else:
            st.markdown(
                section_header(
                    "Your Vibe Mix",
                    "AI-curated picks based on your mood"
                ),
                unsafe_allow_html=True,
            )

            # Top Pick (Rank 1)
            top_song = ranked.iloc[0]
            alternatives = ranked.iloc[1:3]
            from src.recommender.reasoner import explain_top_pick

            pick_reason = explain_top_pick(profile, top_song, alternatives)

            st.markdown(
                top_pick_card(
                    title=top_song["title"],
                    artist=top_song["artist"],
                    score=float(top_song["final_score"]),
                    reason=pick_reason
                ),
                unsafe_allow_html=True,
            )

            # Secondary ranked list
            st.markdown(
                section_header("More For You"),
                unsafe_allow_html=True,
            )

            for idx in range(1, len(ranked)):
                song = ranked.iloc[idx]
                gradient = ALBUM_GRADIENTS[(idx - 1) % len(ALBUM_GRADIENTS)]
                tag = f"{song['genre']} | {song['lyrics_theme']}"
                st.markdown(
                    song_card(
                        rank=int(song["rank"]),
                        title=song["title"],
                        artist=song["artist"],
                        score=float(song["final_score"]),
                        tag=tag,
                        gradient=gradient
                    ),
                    unsafe_allow_html=True,
                )


def render_home_page():
    """Main router between Spotify Home Mock and Vibe Feature."""
    # Check query parameters for state trigger
    if st.query_params.get("show_vibe") == "true":
        st.session_state.show_vibe = True

    if "show_vibe" not in st.session_state:
        st.session_state.show_vibe = False

    if not st.session_state.show_vibe:
        render_spotify_home()
    else:
        render_vibe_feature()
