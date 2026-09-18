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

    player_bye = player_info.get('bye_week')
    if (player_bye is not None and player_bye == week):
        status = "BYE"

    unusable_statuses = ['Out', 'IR', 'Doubtful', 'PUP', 'SUS', 'BYE']
    unusable = status not in unusable_statuses
    
    projection_info = projections_by_id.get(player_id)
    if projection_info is not None and 'pts_ppr' in projection_info['stats'] and unusable:
        projected_points = projection_info['stats']['pts_ppr']
    else:
        projected_points = 0

    player = {
        "player_id" : player_id,
        "name" : name, 
        "position" : player_info['position'], 
        "team" : player_info['team'],
        "status" : status,
        "projected_points" : projected_points
    }
    return player

def best_points(start, bench, position):
    combined = []
    for player in start:
        if position == player['position']:
            combined.append(player)
    for player in bench:
        if position == player['position']:
            combined.append(player)

    if position == 'QB' or position == 'K' or position == 'DEF':
        n = 1
    else:
        n = 2

    best = []
    for i in range(n):
        highest = None
        for player in combined:
            if highest is None or player['projected_points'] > highest['projected_points']:
                highest = player
        if highest is not None:
            best.append(highest)
            combined.remove(highest)

    return best

def best_waiver_pickup(position):
    free_agents = []
    for player_id in all_players:
        player_info = all_players[player_id]
        if player_info['position'] == position and player_id not in all_rostered_ids and player_id not in temp_rostered:
            free_agents.append(player_stats(player_id))

    highest = None
    for player in free_agents:
        if player['projected_points'] > 0:
            if highest is None or player['projected_points'] > highest['projected_points']:
                highest = player
    return highest


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


# Find best players to start at every position, QB K DEF = 1, RB WR TE = 2
order = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
combined_players = starters + bench
combined_players.sort(key=lambda x: x['projected_points'], reverse=True)
best_players = []

for pos in order:
    best_starter = best_points(starters, bench, pos)
    for player in combined_players:
        if player in best_starter:
            best_players.append(player)
new_bench = []
for player in combined_players:
    if player not in best_players:
        new_bench.append(player)

flex_opt = ['RB', 'WR', 'TE']
flex = []

for _ in range(2):
    highest = None
    for player in new_bench:
        if highest is None or player['projected_points'] > highest['projected_points']:
            if player['position'] in flex_opt: 
                highest = player
    if highest is not None:
        flex.append(highest)
        new_bench.remove(highest)

all_rostered_ids = []
for roster in rosters:
    for player_id in roster['players']:
        all_rostered_ids.append(player_id)


potential_waiver = []
replacement_players = []
temp_rostered = []
for pos in order:
    pos_players = []
    for players in best_players + flex + new_bench:
        if players['position'] == pos:
            pos_players.append(players)
    pos_players_sorted = sorted(pos_players, key=lambda p: p['projected_points'])
    for _ in range(len(pos_players_sorted)):
        lowest = pos_players_sorted[0]
        new_player = best_waiver_pickup(pos)
        if new_player is not None:
                if lowest['projected_points'] < new_player['projected_points']:
                    potential_waiver.append(new_player)
                    replacement_players.append(lowest)
                    temp_rostered.append(new_player['player_id'])
                    pos_players_sorted.remove(lowest)
                else: 
                    break

# for all players to be replaced, print name and points compared to potential waiver pickups name and points
#for player, pickup in zip(replacement_players, potential_waiver):
#    print(f"Player to be replaced: {player['name']} [{player['status']}], Projected Points: {player['projected_points']}")
 #   print(f"Potential waiver pickup: {pickup['name']} [{pickup['status']}], Projected Points: {pickup['projected_points']}\n")