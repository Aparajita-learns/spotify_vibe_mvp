import json
import logging
from typing import Optional

import pandas as pd

from src.config import settings
from src.config.prompts import TOP_PICK_REASON_PROMPT
from src.data.preprocess import split_and_normalize_tags
from src.recommender.explanation import _character_phrase, _mood_label, _rhythm_phrase
from src.recommender.mood_parser import MoodProfile

logger = logging.getLogger(__name__)


def _song_tags(song: pd.Series, field: str, list_field: str) -> list[str]:
    tags = song.get(list_field)
    if isinstance(tags, list):
        return tags
    return split_and_normalize_tags(song.get(field, ""))


def _format_song_metadata(song: pd.Series) -> str:
    mood_tags = ", ".join(_song_tags(song, "mood_tags", "mood_tags_list")) or "unknown"
    context_tags = ", ".join(_song_tags(song, "context_tags", "context_tags_list")) or "unknown"
    genre = str(song.get("genre", "")).replace("-", " ")
    theme = str(song.get("lyrics_theme", "")).strip() or "unknown"
    return (
        f"{song['title']} by {song['artist']} | genre: {genre} | "
        f"mood tags: {mood_tags} | context: {context_tags} | "
        f"lyrics theme: {theme} | tempo feel: {_rhythm_phrase(float(song['tempo']))}"
    )


def generate_template_reason(
    profile: MoodProfile,
    top_song: pd.Series,
    alternatives: Optional[pd.DataFrame] = None,
) -> str:
    """Deterministic 2-4 sentence explanation using only known song metadata."""
    title = top_song["title"]
    artist = top_song["artist"]
    mood_label = _mood_label(profile)
    energy = float(top_song["energy"])
    valence = float(top_song["valence"])
    tempo = float(top_song["tempo"])

    character = _character_phrase(profile, energy, valence)
    rhythm = _rhythm_phrase(tempo)
    mood_tags = _song_tags(top_song, "mood_tags", "mood_tags_list")
    tag_phrase = " and ".join(mood_tags[:2]) if mood_tags else profile.primary_mood
    genre = str(top_song.get("genre", "")).replace("-", " ")
    theme = str(top_song.get("lyrics_theme", "")).strip()

    sentences = [
        f"{title} by {artist} is our top pick for your {mood_label}.",
        f"It's {character} with {rhythm}, bringing {tag_phrase} energy in a {genre} style.",
    ]

    if theme:
        sentences.append(f"The {theme} lyrical tone fits what you're looking for right now.")

    if alternatives is not None and not alternatives.empty:
        alt_title = alternatives.iloc[0]["title"]
        sentences.append(f"It stood out ahead of {alt_title} for overall mood match.")

    return " ".join(sentences[:4])


def explain_top_pick_llm(
    profile: MoodProfile,
    top_song: pd.Series,
    alternatives: Optional[pd.DataFrame] = None,
) -> str:
    """Generate an explanation via LLM using only provided metadata."""
    alt_lines = "None"
    if alternatives is not None and not alternatives.empty:
        alt_lines = "\n".join(_format_song_metadata(row) for _, row in alternatives.head(2).iterrows())

    prompt = TOP_PICK_REASON_PROMPT.format(
        mood_profile=json.dumps(profile.model_dump(), indent=2),
        top_song=_format_song_metadata(top_song),
        other_candidates=alt_lines,
    )

    if settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        content = response.choices[0].message.content.strip()
        logger.info("OpenAI top-pick reason generated")
        return content

    if settings.LLM_PROVIDER == "anthropic" and settings.ANTHROPIC_API_KEY:
        import anthropic

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.content[0].text.strip()
        logger.info("Anthropic top-pick reason generated")
        return content

    raise ValueError("No valid LLM credentials / configuration found.")


def explain_top_pick(
    profile: MoodProfile,
    top_song: pd.Series,
    alternatives: Optional[pd.DataFrame] = None,
) -> str:
    """
    Main entrypoint for top-pick reasoning.
    Uses free template reasoning by default; LLM only when explicitly enabled.
    """
    if settings.ENABLE_LLM_REASONING:
        try:
            has_openai = settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY
            has_anthropic = settings.LLM_PROVIDER == "anthropic" and settings.ANTHROPIC_API_KEY
            if has_openai or has_anthropic:
                return explain_top_pick_llm(profile, top_song, alternatives)
        except Exception as exc:
            logger.warning("LLM reasoning failed: %s. Using template fallback.", exc)

    return generate_template_reason(profile, top_song, alternatives)
