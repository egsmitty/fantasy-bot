# Fantasy Bot

Fantasy Bot is a lightweight Python automation for fantasy football decision support. It connects to the Sleeper API, evaluates your roster and projected points, identifies the strongest lineup adjustments, and sends a concise Telegram update with suggested lineup changes and waiver pickups.

This project is built for a single user's league workflow and is designed to be easy to customize for your own roster, league settings, and Telegram channel.

## What it does

- Pulls your Sleeper user and league data
- Loads player metadata and current NFL week state
- Calculates projected points for your starters and bench players
- Recommends the best lineup optimizations by position
- Identifies waiver-wire additions that could outperform current rostered players
- Sends the results via Telegram

## Current repo structure

- `fetch_user.py` – main fantasy analysis logic and recommendation engine
- `tele_text.py` – helper to send a Telegram message
- `requirements.txt` – Python dependencies
- `README.md` – project documentation

## Features

### Lineup optimization
The bot compares your current starters to your bench and evaluates which players should be started at each position based on projected points. It accounts for:

- QB, RB, WR, TE, K, and DEF slots
- currently rostered starters versus bench players
- bye weeks and injury/availability status
- flex considerations for RB/WR/TE

### Waiver suggestions
The bot checks free agents from the same positions and recommends pickups when the projected value exceeds the weakest player currently on your roster.

### Telegram notifications
The project sends a formatted message through the Telegram Bot API. This makes it easy to receive lineup updates in a group chat or personal DM.

## Requirements

- Python 3.9+
- A Sleeper account and access to your fantasy league
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

- `username = "theman2006"` → your Sleeper username
- `league_response = requests.get(...)` and `roster_response = requests.get(...)` → your league and roster configuration

6. Run the bot:

```bash
python fetch_user.py
```

## How it works

`fetch_user.py` does the following:

1. Fetches the Sleeper user profile using the configured username
2. Finds the relevant league and roster data
3. Loads all NFL players from Sleeper
4. Pulls current-week fantasy projections
5. Builds player metadata for starters and bench players
6. Compares projected points to find optimal starts
7. Checks free agents for waiver recommendations
8. Sends the final summary to Telegram using `tele_text.py`

## Example output

```text
Suggested lineup changes:
- Start Ja'Marr Chase (WR, 17.4 pts)
- Start Josh Jacobs (RB, 15.1 pts)

Waiver suggestions:
- Pick up Tank Dell (15.8 pts) over Mike Williams (9.7 pts)
```

## Notes

- The project currently uses hardcoded Sleeper values for the user and league. You should update those values to match your own league setup before using it.
- The script writes a local `players.json` file so it can cache the Sleeper player data during runtime.
- The bot is intended for personal automation and can be extended to schedule recurring checks using cron, GitHub Actions, or a hosted scheduler.

## Future improvements

Potential improvements include:

- moving league and user configuration to environment variables
- adding command-line arguments for username, season, and league ID
- handling multiple leagues or multiple users
- adding error handling for API failures and rate limiting
- logging results to a file or database
- adding tests for the lineup optimization logic

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, consider adding an open-source license such as MIT.

## Contributing

If you want to expand or improve the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with a clear summary of improvements

