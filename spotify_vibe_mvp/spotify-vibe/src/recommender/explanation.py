import pandas as pd

from src.recommender.mood_parser import MoodProfile


def _mood_label(profile: MoodProfile) -> str:
    labels = {
        "chill": "chill mood",
        "calm": "calm vibe",
        "cozy": "cozy vibe",
        "peaceful": "peaceful vibe",
        "sad": "sad mood",
        "melancholic": "melancholic mood",
        "focused": "focus session",
        "energetic": "workout energy",
        "hype": "hype vibe",
        "happy": "happy mood",
        "joyful": "joyful vibe",
        "moody": "late-night mood",
        "cool": "cool vibe",
        "balanced": "vibe",
    }
    return labels.get(profile.primary_mood.lower(), f"{profile.primary_mood} mood")


def _rhythm_phrase(tempo: float) -> str:
    if tempo < 90:
        return "slow, unhurried beats"
    if tempo < 115:
        return "a steady, easy groove"
    return "an upbeat, driving rhythm"


def _character_phrase(profile: MoodProfile, energy: float, valence: float) -> str:
    mood = profile.primary_mood.lower()
    secondary = profile.secondary_mood.lower()

    if mood in {"chill", "calm", "cozy", "peaceful"}:
        return "mellow and relaxed"
    if mood in {"sad", "melancholic"} or secondary in {"heartbreak", "sad", "melancholic"}:
        return "tender and emotional" if valence < 0.45 else "reflective and soothing"
    if mood in {"energetic", "hype"} or energy > 0.7:
        return "punchy and motivating"
    if mood in {"happy", "joyful"} or valence > 0.75:
        return "bright and feel-good"
    if mood == "focused":
        return "steady and unobtrusive"
    if energy < 0.35:
        return "soft and gentle"
    if valence < 0.4:
        return "emotional and introspective"
    return "a great sonic match"


def generate_pick_reason(profile: MoodProfile, song: pd.Series) -> str:
    """Build a short, human-readable reason why a song fits the user's mood."""
    from src.recommender.reasoner import generate_template_reason

    return generate_template_reason(profile, song)
