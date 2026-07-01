import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "song_id",
    "title",
    "artist",
    "genre",
    "energy",
    "valence",
    "danceability",
    "tempo",
    "mood_tags",
    "context_tags",
    "lyrics_theme",
    "popularity"
]

def load_songs_catalog(file_path: str = None) -> pd.DataFrame:
    """
    Loads and validates the songs catalog CSV.
    
    Args:
        file_path: Optional custom path to the catalog CSV. If None, defaults to the project's data directory.
        
    Returns:
        pd.DataFrame: Loaded and validated song catalog DataFrame.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If validation fails (missing columns or out of bounds values).
    """
    if file_path is None:
        file_path = Path(__file__).parent.parent.parent / "data" / "songs_catalog.csv"
    else:
        file_path = Path(file_path)

    if not file_path.exists():
        logger.error(f"Catalog file not found: {file_path}")
        raise FileNotFoundError(f"Songs catalog file not found at {file_path}")

    logger.info(f"Loading songs catalog from {file_path}")
    df = pd.read_csv(file_path)

    # Clean whitespace from column headers
    df.columns = df.columns.str.strip()

    # Validate columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns in catalog: {missing_cols}")
        raise ValueError(f"Missing required columns in catalog: {missing_cols}")

    # Strip whitespace from text columns
    text_cols = ["title", "artist", "genre", "mood_tags", "context_tags", "lyrics_theme"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # Validate ranges
    for col in ["energy", "valence", "danceability"]:
        if not df[col].between(0.0, 1.0).all():
            out_of_bounds = df[~df[col].between(0.0, 1.0)]
            logger.error(f"Out of bounds values in '{col}':\n{out_of_bounds[['song_id', 'title', col]]}")
            raise ValueError(f"Value in column '{col}' is outside the valid range [0.0, 1.0]")

    if not df["popularity"].between(0, 100).all():
        out_of_bounds = df[~df["popularity"].between(0, 100)]
        logger.error(f"Out of bounds values in 'popularity':\n{out_of_bounds[['song_id', 'title', 'popularity']]}")
        raise ValueError("Value in column 'popularity' is outside the valid range [0, 100]")

    if not (df["tempo"] > 0).all():
        invalid_tempo = df[df["tempo"] <= 0]
        logger.error(f"Invalid tempo values:\n{invalid_tempo[['song_id', 'title', 'tempo']]}")
        raise ValueError("Value in column 'tempo' must be positive")

    return df
