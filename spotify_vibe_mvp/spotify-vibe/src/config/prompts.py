from textwrap import dedent

MOOD_PARSE_PROMPT = dedent("""\
    You are a music mood parser.
    Convert the user's mood/vibe input into structured JSON.

    Your response MUST be a single, valid JSON block. Do not include markdown formatting (like ```json ... ```) or explanation outside the JSON.

    Use ONLY mood labels that exist in the song catalog. Preferred primary/secondary moods include:
    sad, melancholic, vulnerable, heartbreak, chill, calm, peaceful, cozy, energetic, hype,
    happy, joyful, focused, moody, cool, hopeful, angsty, dreamy, nostalgic, bluesy

    Mapping rules for grief and loss:
    - grief, grieving, mourning, bereavement, loss, sorrow, depressed -> primary_mood: "sad", secondary_mood: "melancholic"
    - lonely -> primary_mood: "sad", secondary_mood: "melancholic"
    - Use low energy_target (~0.30) and valence_target (~0.20) for sad/grief moods
    - Use tempo_range around [60, 95] for sad/grief moods

    Expected fields:
    - primary_mood (string)
    - secondary_mood (string)
    - energy_target (float between 0.0 and 1.0)
    - valence_target (float between 0.0 and 1.0)
    - tempo_range (array of two integers: [min_bpm, max_bpm])
    - context (array of strings, e.g. ["night", "solo", "driving", "workout", "study", "relaxing"])
    - exploration_mode (string: "safe", "balanced", or "adventurous")

    User input:
    "{user_input}"
    """)

TOP_PICK_REASON_PROMPT = dedent("""\
    You are explaining a music recommendation inside an AI-powered music app.

    Given the user's mood profile, the top recommended song metadata, and up to two
    alternative songs, write a concise explanation (2-4 sentences) for why the top song
    is the best fit right now.

    Rules:
    - Mention mood fit and musical qualities (tempo feel, energy, mood tags, genre).
    - Sound personal but not overly emotional.
    - Use ONLY facts present in the metadata below. Do NOT invent lyrics, stories, or chart stats.
    - Do NOT mention scores, energy/valence numbers, or BPM values.
    - Return plain text only — no markdown, no bullet points.

    User mood profile:
    {mood_profile}

    Top song:
    {top_song}

    Other candidates:
    {other_candidates}
    """)
