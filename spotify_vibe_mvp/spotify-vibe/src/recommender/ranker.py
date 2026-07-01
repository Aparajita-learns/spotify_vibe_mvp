import pandas as pd

def rank_songs(scored_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ranks the scored candidates by score descending and returns the top 10 songs.
    Adds a 'rank' column (1-indexed).
    
    Args:
        scored_df: DataFrame with 'final_score' column.
        
    Returns:
        pd.DataFrame: Top 10 ranked songs.
    """
    if scored_df.empty:
        return scored_df
        
    ranked_df = scored_df.sort_values(by="final_score", ascending=False).reset_index(drop=True)
    ranked_df["rank"] = ranked_df.index + 1
    return ranked_df.head(10)
