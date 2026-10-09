# Fantasy Bot

Fantasy Bot is a lightweight Python automation for fantasy football decision support. It connects to Sleeper, evaluates your roster and projected points, identifies the best lineup changes, and flags waiver-wire pickups that may outperform your current players. Results are sent via Telegram.

This project is designed for a single user's league workflow and is easy to customize for your own roster, league settings, and Telegram channel.

## What it does

- Pulls your Sleeper user and league data
- Loads current player metadata and weekly NFL state
- Compares starter projections against bench players
- Recommends optimized starts by position
- Identifies waiver additions that could improve your roster
- Sends the final summary to Telegram

## Repo structure

- `fetch_user.py` – main analysis and recommendation logic
- `tele_text.py` – Telegram message helper
- `requirements.txt` – Python dependencies
- `README.md` – project documentation

## Features

### Lineup optimization
The bot compares your starters to your bench and evaluates which players should be started at each position based on projected points. It accounts for:

- QB, RB, WR, TE, K, and DEF slots
- current starters versus bench players
- bye weeks and availability status
- flex considerations for RB/WR/TE

### Waiver suggestions
The bot checks free agents in relevant positions and recommends pickups when their projected value exceeds the weakest player currently on your roster.

### Telegram notifications
The project sends a formatted message through the Telegram Bot API, which makes it easy to receive lineup updates in a group chat or direct message.

## Requirements

- Python 3.9+
- A Sleeper account and access to your league
- A Telegram bot token and chat ID

## Setup

1. Clone the repository:

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

5. Update the hardcoded values in `fetch_user.py` to match your Sleeper account and league:

- `username = "___"` → your Sleeper username
- `league_response = requests.get(...)` and `roster_response = requests.get(...)` → your league and roster configuration

6. Run the bot:

```bash
python fetch_user.py
```

## How it works

`fetch_user.py` does the following:

1. Fetches your Sleeper user profile
2. Finds the relevant league and roster data
3. Loads player metadata from Sleeper
4. Pulls current-week fantasy projections
5. Compares projected points to find the best lineup
6. Checks free agents for waiver recommendations
7. Sends the results to Telegram

## Example output

```text
Suggested lineup changes:
- Start Ja'Marr Chase (WR, 17.4 pts)
- Start Josh Jacobs (RB, 15.1 pts)

Waiver suggestions:
- Pick up Tank Dell (15.8 pts) over Mike Williams (9.7 pts)
```

## Notes

- The project currently supports a single user and hardcoded Sleeper values for that user and league.
- The script writes a local `players.json` file to cache Sleeper player data during runtime.
- This is intended for personal automation and can be extended to run on a schedule with cron, GitHub Actions, or a hosted service.
