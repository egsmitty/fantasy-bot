# Fantasy Bot

Fantasy Bot is a lightweight Python automation for fantasy football decision support. It connects to Sleeper, evaluates your roster and projected points, and recommends lineup and waiver moves.

## What it does

- Pulls your Sleeper user and league data
- Loads player metadata and weekly projections
- Compares starters against bench players
- Recommends optimized starts by position
- Identifies waiver pickups that improve your roster
- Sends the summary to Telegram

## Repo layout

- `fetch_user.py` — main analysis and recommendation logic
- `tele_text.py` — Telegram message helper
- `requirements.txt` — Python dependencies
- `README.md` — project documentation

## Requirements

- Python 3.9+
- A Sleeper account and league access
- A Telegram bot token and chat ID

## Setup

1. Clone the repo:

```bash
git clone https://github.com/egsmitty/fantasy-bot.git
cd fantasy-bot
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

5. Update the hardcoded Sleeper values in `fetch_user.py` to match your account and league.

6. Run the bot:

```bash
python fetch_user.py
```

## Notes

- This project is designed for a single user and a single league.
- It caches Sleeper player data locally in `players.json`.
- It is intended for personal automation and can be scheduled with cron, GitHub Actions, or a hosted service.
