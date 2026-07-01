import pandas as pd
from typing import List

def split_and_normalize_tags(tags_str: str) -> List[str]:
    """
    Splits pipe-delimited tag strings and normalizes casing (lowercased and stripped).
    
    Args:
        tags_str: Pipe-delimited string of tags, e.g. "chill|warm|sunset"
        
    Returns:
        List[str]: List of normalized tags.
    """
    if pd.isna(tags_str) or not isinstance(tags_str, str):
        return []
    return [tag.strip().lower() for tag in tags_str.split("|") if tag.strip()]

def preprocess_songs_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the song catalog DataFrame by splitting pipe-delimited tags
    and normalizing casing/spaces for genre, lyrics_theme, and titles/artists.
    
    Args:
        df: Input raw/validated DataFrame of songs.
        
    Returns:
        pd.DataFrame: A new DataFrame with preprocessed fields.
    """
    df = df.copy()
    
    # Normalize main text fields
    df["genre"] = df["genre"].str.strip().str.lower()
    df["lyrics_theme"] = df["lyrics_theme"].str.strip().str.lower()
    
    # Split pipe-delimited tags into lists
    df["mood_tags_list"] = df["mood_tags"].apply(split_and_normalize_tags)
    df["context_tags_list"] = df["context_tags"].apply(split_and_normalize_tags)
    
    return df
