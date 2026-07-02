from src.recommender.mood_parser import (
    parse_mood_rule_based,
    parse_mood,
    MoodProfile,
    normalize_mood_profile,
)

def test_parse_mood_rule_based_chill():
    profile = parse_mood_rule_based("I want to chill and relax")
    assert profile.primary_mood == "chill"
    assert profile.energy_target == 0.30
    assert profile.valence_target == 0.65
    assert "relaxing" in profile.context

def test_parse_mood_rule_based_sad():
    profile = parse_mood_rule_based("feeling very sad and lonely today")
    assert profile.primary_mood == "sad"
    assert profile.valence_target == 0.20
    assert profile.exploration_mode == "balanced"

def test_parse_mood_rule_based_grief():
    profile = parse_mood_rule_based("grieving after a loss")
    assert profile.primary_mood == "sad"
    assert profile.secondary_mood == "melancholic"
    assert profile.valence_target == 0.20

def test_normalize_mood_profile_grief():
    raw = MoodProfile(
        primary_mood="grief",
        secondary_mood="loss",
        energy_target=0.30,
        valence_target=0.20,
        tempo_range=(60, 95),
        context=["solo"],
        exploration_mode="balanced",
    )
    profile = normalize_mood_profile(raw)
    assert profile.primary_mood == "sad"
    assert profile.secondary_mood == "melancholic"

def test_parse_mood_rule_based_workout():
    profile = parse_mood_rule_based("gym energy and workout hype")
    assert profile.primary_mood == "energetic"
    assert profile.energy_target == 0.85

def test_parse_mood_rule_based_default():
    profile = parse_mood_rule_based("completely random text that maps to nothing")
    assert profile.primary_mood == "balanced"
    assert profile.energy_target == 0.50

def test_parse_mood_empty_input():
    profile = parse_mood("")
    assert profile.primary_mood == "balanced"
