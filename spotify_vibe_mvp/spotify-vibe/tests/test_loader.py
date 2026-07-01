import pytest
import pandas as pd
import tempfile
from pathlib import Path
from src.data.loader import load_songs_catalog
from src.data.preprocess import preprocess_songs_df, split_and_normalize_tags

def test_split_and_normalize_tags():
    assert split_and_normalize_tags("chill|warm|sunset") == ["chill", "warm", "sunset"]
    assert split_and_normalize_tags("  Chill | Warm  |") == ["chill", "warm"]
    assert split_and_normalize_tags("") == []
    assert split_and_normalize_tags(None) == []

def test_load_songs_catalog_success():
    # Load the actual catalog to ensure it is valid
    df = load_songs_catalog()
    assert len(df) >= 100
    assert "song_id" in df.columns
    assert df["energy"].between(0.0, 1.0).all()

def test_load_songs_catalog_missing_cols():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
        f.write("song_id,title,artist\n1,Test Song,Test Artist\n")
        temp_path = f.name
    try:
        with pytest.raises(ValueError, match="Missing required columns"):
            load_songs_catalog(temp_path)
    finally:
        Path(temp_path).unlink()

def test_load_songs_catalog_invalid_range():
    # Out of bounds energy
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
        f.write("song_id,title,artist,genre,energy,valence,danceability,tempo,mood_tags,context_tags,lyrics_theme,popularity\n"
                "1,Test Song,Test Artist,pop,1.5,0.5,0.5,120,chill,study,hopeful,80\n")
        temp_path = f.name
    try:
        with pytest.raises(ValueError, match="is outside the valid range"):
            load_songs_catalog(temp_path)
    finally:
        Path(temp_path).unlink()

def test_preprocess_songs_df():
    df = load_songs_catalog()
    processed_df = preprocess_songs_df(df)
    
    assert "mood_tags_list" in processed_df.columns
    assert "context_tags_list" in processed_df.columns
    assert isinstance(processed_df["mood_tags_list"].iloc[0], list)
