import pandas as pd
from src.recommender.mood_parser import MoodProfile
from src.recommender.candidate_generator import generate_candidates
from src.recommender.scorer import score_candidates
from src.recommender.ranker import rank_songs
from src.data.loader import load_songs_catalog
from src.data.preprocess import preprocess_songs_df

def test_ranking_pipeline():
    # Load and preprocess catalog
    raw_df = load_songs_catalog()
    df = preprocess_songs_df(raw_df)
    
    # Create a mock mood profile
    profile = MoodProfile(
        primary_mood="sad",
        secondary_mood="melancholic",
        energy_target=0.30,
        valence_target=0.20,
        tempo_range=(60, 95),
        context=["solo", "rainy evening"],
        exploration_mode="balanced"
    )
    
    # 1. Generate candidates
    candidates = generate_candidates(profile, df)
    assert len(candidates) >= 15  # Ensure fallback/broad criteria work
    
    # 2. Score candidates
    scored = score_candidates(candidates, profile)
    assert "final_score" in scored.columns
    assert "score_breakdown" in scored.columns
    assert scored["final_score"].between(0.0, 1.0).all()
    
    # 3. Rank candidates
    ranked = rank_songs(scored)
    assert len(ranked) <= 10
    if len(ranked) > 1:
        # Check sort order descending
        assert ranked["final_score"].iloc[0] >= ranked["final_score"].iloc[1]
    assert (ranked["rank"] == list(range(1, len(ranked) + 1))).all()
