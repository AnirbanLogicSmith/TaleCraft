# TaleCraft 📖✨

> AI-powered interactive fiction — every choice shapes your story.

TaleCraft is a web application that lets you collaboratively write branching narratives with an AI co-author. Pick a genre, set the scene, and watch GEMINI craft a rich story where **your choices** determine what happens next.

![TaleCraft UI](https://img.shields.io/badge/stack-FastAPI%20%2B%20Gemini-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- **8 genres** — Fantasy, Sci-Fi, Horror, Mystery, Romance, Thriller, Historical, Fairy Tale
- **AI-generated story segments** — rich, 3–5 paragraph prose at every turn
- **2–3 meaningful choices** per step, generated dynamically by the AI
- **Full story history** — see every choice you made and how the narrative evolved
- **Natural story endings** — after 6–7 turns, the AI concludes with a satisfying finale
- **Clean, minimal UI** — distraction-free reading experience

---

## 🚀 Quickstart

### Prerequisites
- Python 3.11+
- An [Gemini API key](https://aistudio.google.com/api-keys)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/AnirbanLogicSmith/TaleCraft.git
cd TaleCraft

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your GEMINI API key
export GEMINI_API_KEY="AIza..."   # Windows: set GEMINI_API_KEY=AIza...

# 5. Run the app
python main.py
```

Open your browser at **http://localhost:8000** 🎉

---

## 🏗️ Architecture

```
TaleCraft/
├── main.py           # FastAPI backend — story generation endpoints
├── requirements.txt  # Python dependencies
├── static/
│   └── index.html    # Single-file frontend (HTML + CSS + JS)
└── README.md
```

### API Endpoints

| Method | Endpoint        | Description                        |
|--------|-----------------|------------------------------------|
| GET    | `/`             | Serves the frontend                |
| POST   | `/api/start`    | Start a new story (genre + premise)|
| POST   | `/api/continue` | Continue with a player choice      |

### How it works

1. **User** selects a genre and writes an opening premise
2. **`/api/start`** sends the premise to GEMINI with a structured system prompt, returning a story segment + 2–3 choices as JSON
3. **User** picks a choice; **`/api/continue`** replays the full conversation history plus the new choice back to GEMINI
4. After 6–7 turns, GEMINI naturally concludes the story (`is_ending: true`)

---

## 🤖 Built with GitHub Copilot

This project was built for the [Microsoft Agents League Hackathon](https://github.com/microsoft/agentsleague) — Creative Apps track. GitHub Copilot was used throughout development for:

- Scaffolding the FastAPI project structure
- Writing the GEMINI prompt engineering logic
- Generating the CSS layout and animations
- Debugging JSON response handling

---

## 📝 Example Prompts

| Genre     | Premise |
|-----------|---------|
| Fantasy   | A disgraced knight discovers an ancient map hidden in a monastery wall |
| Sci-Fi    | The last archivist on a dying space station receives a transmission from Earth — which has been silent for 200 years |
| Mystery   | A forensic linguist is called to analyze the suicide note of a man who was illiterate |
| Horror    | You inherit your grandmother's house and find her journal — the final entry was written yesterday |

---

## 📄 License


MIT — see [LICENSE](LICENSE)
