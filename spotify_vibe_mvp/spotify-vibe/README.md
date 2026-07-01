# 🎵 Spotify Vibe — AI-Native Music Discovery MVP

> **Tell us the vibe. We'll find the soundtrack.**

Spotify Vibe is an AI-native MVP that demonstrates mood-driven music discovery.
Instead of relying on opaque recommendation algorithms, it asks users what
mood/vibe they're in, produces transparent ranked recommendations, and explains
why each song was chosen.

## ✨ Features

- 🎧 **Spotify-inspired dark UI** with polished cards and layout
- 🌀 **Animated glowing Vibe icon** with Gemini-style rotating light
- 💬 **Free-text mood input** — describe your vibe in natural language
- ⚡ **Quick mood chips** — tap a preset like Chill, Focus, Workout
- 🏆 **Top Pick highlight** — green-bordered card with AI explanation
- 📊 **Ranked song list** — scored from best to least match

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone <repo-url>
cd spotify-vibe

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set up LLM API keys
cp .env.example .env
# Edit .env with your API keys

# 5. Run the app
streamlit run app.py
```

## 📁 Project Structure

```
spotify-vibe/
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .streamlit/config.toml  # Dark theme config
├── assets/styles.css       # Custom CSS
├── data/                   # Song catalogs (Phase 2)
├── src/
│   ├── config/             # Settings & prompts
│   ├── data/               # Loaders & preprocessors
│   ├── recommender/        # Mood parser, scorer, ranker, reasoner
│   ├── ui/                 # Layout, components, theme
│   └── utils/              # Logging & validators
└── tests/                  # Unit tests
```

## 🎨 Design

- Dark background: `#121212`
- Card background: `#181818`
- Accent green: `#1DB954`
- Typography: Inter (Google Fonts)

## 📋 Phases

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ | Project setup + UI skeleton |
| 2 | ⬜ | Song catalog + data loader |
| 3 | ⬜ | Mood input parsing |
| 4 | ✅ | Ranking engine |
| 5 | ✅ | LLM reasoning layer (free template default) |
| 6 | ⬜ | Polished recommendation UI |
| 7 | ⬜ | Deployment |

---

*Built as part of the Spotify Growth Team graduation project — Jun 2026*
