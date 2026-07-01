import pandas as pd
from src.recommender.mood_parser import MoodProfile, expand_moods_for_matching, expand_themes_for_matching
from src.data.preprocess import split_and_normalize_tags

def calculate_score(row: pd.Series, mood_profile: MoodProfile) -> tuple[float, dict]:
    """
    Calculates the detailed recommendation score and component breakdown for a single song.
    """
    # Parse tag lists if they are not already lists (e.g. if loaded but not preprocessed)
    song_mood_tags = row.get("mood_tags_list")
    if not isinstance(song_mood_tags, list):
        song_mood_tags = split_and_normalize_tags(row.get("mood_tags", ""))
        
    song_context_tags = row.get("context_tags_list")
    if not isinstance(song_context_tags, list):
        song_context_tags = split_and_normalize_tags(row.get("context_tags", ""))

    # 1. mood_tag_overlap (0.30)
    profile_moods = expand_moods_for_matching(
        mood_profile.primary_mood, mood_profile.secondary_mood
    )
    mood_overlap_count = sum(1 for m in profile_moods if m in song_mood_tags)
    mood_tag_overlap = mood_overlap_count / max(1, len(profile_moods))

    # 2. energy_similarity (0.20)
    energy_similarity = 1.0 - abs(row["energy"] - mood_profile.energy_target)

    # 3. valence_similarity (0.15)
    valence_similarity = 1.0 - abs(row["valence"] - mood_profile.valence_target)

    # 4. tempo_similarity (0.10)
    min_bpm, max_bpm = mood_profile.tempo_range
    song_tempo = row["tempo"]
    if min_bpm <= song_tempo <= max_bpm:
        tempo_similarity = 1.0
    else:
        # Scale decay up to 50 BPM difference
        distance = min(abs(song_tempo - min_bpm), abs(song_tempo - max_bpm))
        tempo_similarity = max(0.0, 1.0 - (distance / 50.0))

    # 5. context_overlap (0.10)
    profile_context = {c.lower() for c in mood_profile.context}
    context_overlap_count = sum(1 for c in profile_context if c in song_context_tags)
    context_overlap = context_overlap_count / max(1, len(profile_context))

    # 6. lyrics_theme_match (0.10)
    song_theme = str(row.get("lyrics_theme", "")).strip().lower()
    profile_themes = expand_themes_for_matching(
        mood_profile.primary_mood, mood_profile.secondary_mood
    )
    lyrics_theme_match = 1.0 if song_theme in profile_themes else 0.0

    # 7. popularity_balance (0.05)
    popularity = row["popularity"]
    if mood_profile.exploration_mode == "safe":
        # Prefer higher popularity
        popularity_balance = popularity / 100.0
    elif mood_profile.exploration_mode == "adventurous":
        # Prefer obscure/lower popularity
        popularity_balance = 1.0 - (popularity / 100.0)
    else:  # balanced
        # Prefer mid-range popularity
        popularity_balance = 1.0 - (abs(popularity - 50.0) / 50.0)

    # Final weighted score
    final_score = (
        0.30 * mood_tag_overlap +
        0.20 * energy_similarity +
        0.15 * valence_similarity +
        0.10 * tempo_similarity +
        0.10 * context_overlap +
        0.10 * lyrics_theme_match +
        0.05 * popularity_balance
    )

    breakdown = {
        "mood_tag_overlap": round(mood_tag_overlap, 3),
        "energy_similarity": round(energy_similarity, 3),
        "valence_similarity": round(valence_similarity, 3),
        "tempo_similarity": round(tempo_similarity, 3),
        "context_overlap": round(context_overlap, 3),
        "lyrics_theme_match": round(lyrics_theme_match, 3),
        "popularity_balance": round(popularity_balance, 3)
    }

    return round(final_score, 4), breakdown

def score_candidates(candidates_df: pd.DataFrame, mood_profile: MoodProfile) -> pd.DataFrame:
    """
    Applies the weighted scoring formula to all candidates in the DataFrame.
    
    Args:
        candidates_df: The candidate songs DataFrame.
        mood_profile: The target MoodProfile model.
        
    Returns:
        pd.DataFrame: DataFrame with added 'final_score' and 'score_breakdown' columns.
    """
    df = candidates_df.copy()
    
    scores = []
    breakdowns = []
    
    for _, row in df.iterrows():
        score, breakdown = calculate_score(row, mood_profile)
        scores.append(score)
        breakdowns.append(breakdown)
        
    df["final_score"] = scores
    df["score_breakdown"] = breakdowns
    
    return df
