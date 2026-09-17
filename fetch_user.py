import requests
import json

# Create and return the requested player's info dictionary

def player_stats(player_id):
    player_info = all_players[player_id]
    if 'full_name' in player_info:
        name = player_info['full_name']
    else:
        name = player_info['first_name'] + " " + player_info['last_name']
    if player_info.get('injury_status') is not None:
        status = player_info['injury_status']
    else:
        status = "Active"

    projection_info = projections_by_id.get(player_id)
    if projection_info is not None and 'pts_ppr' in projection_info['stats']:
        projected_points = projection_info['stats']['pts_ppr']
    else:
        projected_points = 0

    player = {
        "name" : name, 
        "position" : player_info['position'], 
        "team" : player_info['team'],
        "status" : status,
        "projected_points" : projected_points
    }
    return player

# Access the user's leagues, and get the rosters associated with them

username = "theman2006"
response = requests.get(f"https://api.sleeper.app/v1/user/{username}")
data = response.json()

league_response = requests.get(f"https://api.sleeper.app/v1/user/{data['user_id']}/leagues/nfl/2026")
leagues = league_response.json()

roster_response = requests.get(f"https://api.sleeper.app/v1/league/1403537722152378368/rosters")
rosters = roster_response.json()

# Extract only the rosters of the user

my_roster = None
for roster in rosters:
    if roster['owner_id'] == data['user_id']:
        my_roster = roster

# Get player's overall details

players_response = requests.get("https://api.sleeper.app/v1/players/nfl")
all_players = players_response.json()

# Get the current week in order to assign current projections

state_response = requests.get("https://api.sleeper.app/v1/state/nfl")
state = state_response.json()
week = state['week']

projection_response = requests.get(
    f"https://api.sleeper.app/projections/nfl/2026/{week}?season_type=regular&position[]=QB&position[]=RB&position[]=WR&position[]=TE&position[]=K&position[]=DEF"
)
projections = projection_response.json()

# Assign projections to player's id to be extracted

projections_by_id = {}
for entry in projections:
    projections_by_id[entry['player_id']] = entry

# write all players and then read from them

with open("players.json", "w") as f:
    json.dump(all_players, f)

with open("players.json", "r") as f:
    all_players = json.load(f)


# Generate info for starters and bench players

starters = []
bench = []
for player_id in my_roster['players']:
    if player_id in my_roster['starters']:
        starters.append(player_stats(player_id))
for player_id in my_roster['players']:
    if player_id not in my_roster['starters']:
        bench.append(player_stats(player_id))    

# Get all projected points per position for comparison as to who to sub in or out

starter_points = {}
for player in starters:
    position = player['position']
    points = player['projected_points']
    if position not in starter_points:
        starter_points[position] = []
    starter_points[position].append(points)

bench_points = {}
for player in bench:
    position = player['position']
    points = player['projected_points']
    if position not in bench_points:
        bench_points[position] = []
    bench_points[position].append(points)





