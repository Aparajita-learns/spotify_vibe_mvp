import pandas as pd
from src.recommender.mood_parser import MoodProfile, normalize_mood_profile
from src.recommender.scorer import calculate_score, score_candidates
from src.data.loader import load_songs_catalog
from src.data.preprocess import preprocess_songs_df


def test_grief_profile_scores_sad_songs_higher():
    catalog_df = preprocess_songs_df(load_songs_catalog())

    grief_profile = normalize_mood_profile(MoodProfile(
        primary_mood="grief",
        secondary_mood="loss",
        energy_target=0.30,
        valence_target=0.20,
        tempo_range=(60, 95),
        context=["solo", "rainy evening"],
        exploration_mode="balanced",
    ))

    sad_row = catalog_df[catalog_df["title"] == "Fix You"].iloc[0]
    happy_row = catalog_df[catalog_df["title"] == "Dynamite"].iloc[0]

    sad_score, _ = calculate_score(sad_row, grief_profile)
    happy_score, _ = calculate_score(happy_row, grief_profile)

    assert sad_score > happy_score


def test_grief_ranking_pipeline_prefers_sad_tracks():
    from src.recommender.candidate_generator import generate_candidates
    from src.recommender.ranker import rank_songs

    catalog_df = preprocess_songs_df(load_songs_catalog())
    profile = normalize_mood_profile(MoodProfile(
        primary_mood="grief",
        secondary_mood="melancholic",
        energy_target=0.30,
        valence_target=0.20,
        tempo_range=(60, 95),
        context=["solo", "rainy evening"],
        exploration_mode="balanced",
    ))

    candidates = generate_candidates(profile, catalog_df)
    scored = score_candidates(candidates, profile)
    ranked = rank_songs(scored)

    top_titles = set(ranked.head(3)["title"])
    assert top_titles & {"Fix You", "Ocean Eyes", "Someone You Loved", "Breathe Me"}
