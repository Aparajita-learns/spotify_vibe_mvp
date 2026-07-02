import pandas as pd

from src.recommender.explanation import generate_pick_reason
from src.recommender.mood_parser import MoodProfile


def _song(energy=0.15, valence=0.20, tempo=85):
    return pd.Series({
        "title": "Test Song",
        "artist": "Test Artist",
        "genre": "ambient",
        "energy": energy,
        "valence": valence,
        "tempo": tempo,
        "mood_tags": "calm|melancholic",
        "mood_tags_list": ["calm", "melancholic"],
        "context_tags": "solo",
        "context_tags_list": ["solo"],
        "lyrics_theme": "peaceful",
    })


def test_explanation_for_chill_mood():
    profile = MoodProfile(
        primary_mood="chill",
        secondary_mood="calm",
        energy_target=0.30,
        valence_target=0.65,
        tempo_range=(70, 95),
        context=["relaxing"],
        exploration_mode="safe",
    )
    reason = generate_pick_reason(profile, _song(energy=0.20, valence=0.60, tempo=80))
    assert "chill mood" in reason
    assert "0.3" not in reason
    assert "BPM" not in reason
    assert "slow" in reason.lower()


def test_explanation_for_sad_mood():
    profile = MoodProfile(
        primary_mood="sad",
        secondary_mood="melancholic",
        energy_target=0.30,
        valence_target=0.20,
        tempo_range=(60, 95),
        context=["solo"],
        exploration_mode="balanced",
    )
    reason = generate_pick_reason(profile, _song())
    assert "sad mood" in reason
    assert "emotional" in reason.lower() or "reflective" in reason.lower()
