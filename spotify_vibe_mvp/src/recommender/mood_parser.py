import json
import logging
from typing import List, Tuple
from pydantic import BaseModel, Field

from src.config import settings
from src.config.prompts import MOOD_PARSE_PROMPT

logger = logging.getLogger(__name__)

class MoodProfile(BaseModel):
    primary_mood: str
    secondary_mood: str
    energy_target: float = Field(..., ge=0.0, le=1.0)
    valence_target: float = Field(..., ge=0.0, le=1.0)
    tempo_range: Tuple[int, int]
    context: List[str]
    exploration_mode: str = Field("balanced", pattern="^(safe|balanced|adventurous)$")

_SAD_PROFILE = {
    "primary_mood": "sad",
    "secondary_mood": "melancholic",
    "energy_target": 0.30,
    "valence_target": 0.20,
    "tempo_range": (60, 95),
    "context": ["solo", "rainy evening"],
    "exploration_mode": "balanced",
}

# Maps non-catalog mood labels to catalog-aligned vocabulary
MOOD_ALIASES = {
    "grief": "sad",
    "grieving": "sad",
    "mourning": "sad",
    "loss": "sad",
    "bereavement": "sad",
    "sorrow": "sad",
    "depressed": "sad",
    "lonely": "sad",
    "sorrowful": "melancholic",
}

# Related tags/themes used when scoring sad-family moods
SAD_RELATED_TAGS = {"sad", "melancholic", "vulnerable", "heartbreak"}
SAD_RELATED_THEMES = {"heartbreak", "pain", "lonely"}

# Rule-based keyword mapping for deterministic fallback
KEYWORDS_MAPPING = {
    "chill": {
        "primary_mood": "chill",
        "secondary_mood": "calm",
        "energy_target": 0.30,
        "valence_target": 0.65,
        "tempo_range": (70, 95),
        "context": ["relaxing", "solo"],
        "exploration_mode": "safe"
    },
    "calm": {
        "primary_mood": "calm",
        "secondary_mood": "peaceful",
        "energy_target": 0.15,
        "valence_target": 0.60,
        "tempo_range": (60, 90),
        "context": ["relaxing", "sleep"],
        "exploration_mode": "safe"
    },
    "focus": {
        "primary_mood": "focused",
        "secondary_mood": "calm",
        "energy_target": 0.30,
        "valence_target": 0.50,
        "tempo_range": (80, 110),
        "context": ["focus", "study"],
        "exploration_mode": "safe"
    },
    "study": {
        "primary_mood": "focused",
        "secondary_mood": "calm",
        "energy_target": 0.30,
        "valence_target": 0.50,
        "tempo_range": (80, 110),
        "context": ["focus", "study"],
        "exploration_mode": "safe"
    },
    "workout": {
        "primary_mood": "energetic",
        "secondary_mood": "hype",
        "energy_target": 0.85,
        "valence_target": 0.70,
        "tempo_range": (120, 150),
        "context": ["workout", "active"],
        "exploration_mode": "balanced"
    },
    "gym": {
        "primary_mood": "energetic",
        "secondary_mood": "hype",
        "energy_target": 0.85,
        "valence_target": 0.70,
        "tempo_range": (120, 150),
        "context": ["workout", "active"],
        "exploration_mode": "balanced"
    },
    "hype": {
        "primary_mood": "hype",
        "secondary_mood": "energetic",
        "energy_target": 0.90,
        "valence_target": 0.75,
        "tempo_range": (125, 175),
        "context": ["workout", "party"],
        "exploration_mode": "balanced"
    },
    "sad": _SAD_PROFILE,
    "grief": _SAD_PROFILE,
    "grieving": _SAD_PROFILE,
    "mourning": _SAD_PROFILE,
    "bereavement": _SAD_PROFILE,
    "loss": _SAD_PROFILE,
    "sorrow": _SAD_PROFILE,
    "depressed": _SAD_PROFILE,
    "lonely": _SAD_PROFILE,
    "melancholic": {
        "primary_mood": "melancholic",
        "secondary_mood": "sad",
        "energy_target": 0.30,
        "valence_target": 0.20,
        "tempo_range": (60, 95),
        "context": ["solo", "rainy evening"],
        "exploration_mode": "balanced"
    },
    "heartbreak": {
        "primary_mood": "sad",
        "secondary_mood": "heartbreak",
        "energy_target": 0.35,
        "valence_target": 0.25,
        "tempo_range": (70, 110),
        "context": ["solo", "late night"],
        "exploration_mode": "balanced"
    },
    "rainy": {
        "primary_mood": "cozy",
        "secondary_mood": "chill",
        "energy_target": 0.35,
        "valence_target": 0.40,
        "tempo_range": (70, 100),
        "context": ["rainy evening", "solo"],
        "exploration_mode": "safe"
    },
    "night": {
        "primary_mood": "moody",
        "secondary_mood": "cool",
        "energy_target": 0.55,
        "valence_target": 0.45,
        "tempo_range": (90, 120),
        "context": ["driving", "late night drive", "night"],
        "exploration_mode": "balanced"
    },
    "drive": {
        "primary_mood": "cool",
        "secondary_mood": "moody",
        "energy_target": 0.60,
        "valence_target": 0.60,
        "tempo_range": (95, 125),
        "context": ["driving", "night"],
        "exploration_mode": "balanced"
    },
    "happy": {
        "primary_mood": "happy",
        "secondary_mood": "joyful",
        "energy_target": 0.80,
        "valence_target": 0.85,
        "tempo_range": (110, 135),
        "context": ["party", "dancing"],
        "exploration_mode": "adventurous"
    },
    "joyful": {
        "primary_mood": "joyful",
        "secondary_mood": "happy",
        "energy_target": 0.80,
        "valence_target": 0.85,
        "tempo_range": (110, 135),
        "context": ["party", "dancing"],
        "exploration_mode": "adventurous"
    },
    "chaos": {
        "primary_mood": "joyful",
        "secondary_mood": "hype",
        "energy_target": 0.85,
        "valence_target": 0.80,
        "tempo_range": (115, 140),
        "context": ["party", "dancing"],
        "exploration_mode": "adventurous"
    }
}

DEFAULT_PROFILE = {
    "primary_mood": "balanced",
    "secondary_mood": "neutral",
    "energy_target": 0.50,
    "valence_target": 0.50,
    "tempo_range": (90, 120),
    "context": ["listening"],
    "exploration_mode": "balanced"
}


def normalize_mood_label(mood: str) -> str:
    """Map a mood label to catalog-aligned vocabulary."""
    return MOOD_ALIASES.get(mood.lower().strip(), mood.lower().strip())


def normalize_mood_profile(profile: MoodProfile) -> MoodProfile:
    """Normalize primary/secondary moods to catalog-aligned labels."""
    primary = normalize_mood_label(profile.primary_mood)
    secondary = normalize_mood_label(profile.secondary_mood)
    if primary == secondary:
        secondary = "melancholic" if primary == "sad" else profile.secondary_mood.lower()
    return profile.model_copy(update={"primary_mood": primary, "secondary_mood": secondary})


def expand_moods_for_matching(primary_mood: str, secondary_mood: str) -> set[str]:
    """Expand profile moods to related catalog tags for scoring overlap."""
    moods = {normalize_mood_label(primary_mood), normalize_mood_label(secondary_mood)}
    if moods & ({"sad", "melancholic", "heartbreak"} | set(MOOD_ALIASES.keys())):
        moods.update(SAD_RELATED_TAGS)
    return moods


def expand_themes_for_matching(primary_mood: str, secondary_mood: str) -> set[str]:
    """Expand profile moods to related lyrics themes for scoring."""
    moods = expand_moods_for_matching(primary_mood, secondary_mood)
    themes = set(moods)
    if moods & SAD_RELATED_TAGS:
        themes.update(SAD_RELATED_THEMES)
    return themes


def parse_mood_rule_based(user_input: str) -> MoodProfile:
    """
    Parses free-text input deterministically using keyword mapping.
    """
    normalized = user_input.lower().strip()
    
    # Try to find a matching keyword in our map
    for keyword, profile_dict in KEYWORDS_MAPPING.items():
        if keyword in normalized:
            logger.info(f"Rule-based parser matched keyword: '{keyword}'")
            return MoodProfile(**profile_dict)
            
    # Default fallback
    logger.info("Rule-based parser fallback to default profile")
    return MoodProfile(**DEFAULT_PROFILE)

def parse_mood_llm(user_input: str) -> MoodProfile:
    """
    Parses free-text input into a MoodProfile using an LLM.
    """
    prompt = MOOD_PARSE_PROMPT.format(user_input=user_input)

    if settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        content = response.choices[0].message.content
        logger.info(f"OpenAI mood parse response: {content}")
        parsed_json = json.loads(content)
        return MoodProfile(**parsed_json)

    elif settings.LLM_PROVIDER == "anthropic" and settings.ANTHROPIC_API_KEY:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        content = response.content[0].text
        logger.info(f"Anthropic mood parse response: {content}")
        parsed_json = json.loads(content)
        return MoodProfile(**parsed_json)

    raise ValueError("No valid LLM credentials / configuration found.")

def parse_mood(user_input: str) -> MoodProfile:
    """
    Main entrypoint to parse mood. Attempts LLM parsing first,
    falling back to rule-based parser on failure or if credentials aren't set.
    """
    if not user_input.strip():
        return MoodProfile(**DEFAULT_PROFILE)

    profile = None
    try:
        has_openai = settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY
        has_anthropic = settings.LLM_PROVIDER == "anthropic" and settings.ANTHROPIC_API_KEY

        if has_openai or has_anthropic:
            profile = parse_mood_llm(user_input)
        else:
            logger.info("LLM credentials not available. Using rule-based fallback.")
    except Exception as e:
        logger.warning(f"LLM parsing failed: {e}. Falling back to rule-based parser.")

    if profile is None:
        profile = parse_mood_rule_based(user_input)

    return normalize_mood_profile(profile)
