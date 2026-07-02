import pandas as pd
import logging
from src.recommender.mood_parser import MoodProfile

logger = logging.getLogger(__name__)

def generate_candidates(mood_profile: MoodProfile, catalog_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a candidate pool of songs based on the user's mood profile.
    Applies broad numerical filters (energy, valence, tempo) and ensures
    a minimum candidate pool size (at least 30) for diversity.
    
    Args:
        mood_profile: The parsed MoodProfile model.
        catalog_df: The loaded song catalog DataFrame.
        
    Returns:
        pd.DataFrame: Candidate pool.
    """
    df = catalog_df.copy()
    
    # 1. Broad numeric filters (relaxed thresholds to ensure we keep a decent pool size)
    energy_min = max(0.0, mood_profile.energy_target - 0.3)
    energy_max = min(1.0, mood_profile.energy_target + 0.3)
    
    valence_min = max(0.0, mood_profile.valence_target - 0.3)
    valence_max = min(1.0, mood_profile.valence_target + 0.3)
    
    tempo_min = mood_profile.tempo_range[0] - 20
    tempo_max = mood_profile.tempo_range[1] + 20

    # Apply broad filters
    filtered_df = df[
        df["energy"].between(energy_min, energy_max) &
        df["valence"].between(valence_min, valence_max) &
        df["tempo"].between(tempo_min, tempo_max)
    ]
    
    logger.info(f"Broad numerical filtering kept {len(filtered_df)} candidates out of {len(df)}")
    
    # 2. Safety fallbacks if the candidate pool is too small
    if len(filtered_df) < 30:
        logger.info("Candidate pool size under 30. Relaxing numerical constraints.")
        # Relax to wider margins
        energy_min = max(0.0, mood_profile.energy_target - 0.4)
        energy_max = min(1.0, mood_profile.energy_target + 0.4)
        valence_min = max(0.0, mood_profile.valence_target - 0.4)
        valence_max = min(1.0, mood_profile.valence_target + 0.4)
        tempo_min = mood_profile.tempo_range[0] - 35
        tempo_max = mood_profile.tempo_range[1] + 35
        
        filtered_df = df[
            df["energy"].between(energy_min, energy_max) &
            df["valence"].between(valence_min, valence_max) &
            df["tempo"].between(tempo_min, tempo_max)
        ]
        logger.info(f"Relaxed numerical filtering kept {len(filtered_df)} candidates")

    # If it is still too small, just return the entire catalog to avoid recommending nothing
    if len(filtered_df) < 15:
        logger.warning("Candidate pool still too small. Falling back to the complete catalog.")
        return df

    return filtered_df
