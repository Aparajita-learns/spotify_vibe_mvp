import pandas as pd
from unittest.mock import patch

from src.recommender.mood_parser import MoodProfile
from src.recommender.reasoner import explain_top_pick, generate_template_reason


def _profile(primary="chill", secondary="calm"):
    return MoodProfile(
        primary_mood=primary,
        secondary_mood=secondary,
        energy_target=0.30,
        valence_target=0.65,
        tempo_range=(70, 95),
        context=["relaxing", "solo"],
        exploration_mode="safe",
    )


def _top_song():
    return pd.Series({
        "title": "Weightless",
        "artist": "Marconi Union",
        "genre": "ambient",
        "energy": 0.15,
        "valence": 0.20,
        "tempo": 60,
        "mood_tags": "calm|peaceful|melancholic",
        "mood_tags_list": ["calm", "peaceful", "melancholic"],
        "context_tags": "sleep|solo",
        "context_tags_list": ["sleep", "solo"],
        "lyrics_theme": "peaceful",
    })


def _alternatives():
    return pd.DataFrame([
        {"title": "Gymnopedie No. 1", "artist": "Erik Satie"},
    ])


def test_template_reason_is_natural_language():
    reason = generate_template_reason(_profile(), _top_song())
    assert "Weightless" in reason
    assert "Marconi Union" in reason
    assert "chill mood" in reason
    assert "0.15" not in reason
    assert "BPM" not in reason


def test_template_reason_mentions_alternative():
    reason = generate_template_reason(_profile(), _top_song(), _alternatives())
    assert "Gymnopedie No. 1" in reason


def test_template_reason_uses_song_metadata():
    reason = generate_template_reason(_profile(), _top_song())
    assert "ambient" in reason
    assert "peaceful" in reason


def test_explain_top_pick_uses_template_by_default():
    with patch("src.recommender.reasoner.settings.ENABLE_LLM_REASONING", False):
        reason = explain_top_pick(_profile(), _top_song(), _alternatives())
    assert "Weightless" in reason
    assert len(reason.split(".")) >= 2


def test_explain_top_pick_sad_mood():
    profile = _profile(primary="sad", secondary="melancholic")
    song = _top_song()
    reason = generate_template_reason(profile, song)
    assert "sad mood" in reason
    assert "emotional" in reason.lower() or "reflective" in reason.lower() or "gentle" in reason.lower()
