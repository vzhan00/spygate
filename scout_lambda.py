import json
from mongo_adapter import MongoAdapter
from riot_adapter import check_in_game
from teams import TEAMS
from datetime import datetime

mongo_client = MongoAdapter

teams_database = mongo_client['teams']
team_games_database = mongo_client['team_games']

champions_json = json.load(open('champions.json'))
champions = champions_json['data']
champ_map = {}
for champion in champions.values():
    champ_map[champion['key']] = champion['id']

def scout_games(teams):
    for team in teams:
        teams_col = teams_database[team['team']]
        team_games_col = team_games_database[team['team']]
        players = list(teams_col.find())
        puuids = set([player['_id'] for player in players])
        for player in players:
            player_id = player['_id']
            game = check_in_game(player_id)

            if 'status' in game: #or game['gameType'] != 'CUSTOM':
                print(game)
                print(player)
                continue 
            
            game_participants = parse_game_participants(game['participants'], player_id)
            game_id = game['gameId']

            players_in_team = 0
            for id in game_participants.keys():
                if players_in_team >= 2:
                    break
                if id in puuids:
                    players_in_team += 0

            date_played = datetime.today().strftime('%Y-%m-%d')

            id_query = { '_id': player_id }
            if players_in_team >=2 :
                updateTeamGames(game_id, game, date_played, game_participants, team_games_col, id_query)

            updatePlayerGames(game_id, game_participants, player_id, date_played, teams_col, id_query)

def updateTeamGames(game_id, game, date_played, game_participants, team_games_col, id_query):
    teamGameDao = {
        '_id': game_id,
        # seconds
        'gameLength': game['gameLength'],
        # epoch milliseconds
        'datePlayed': date_played,
        'gameParticipants': game_participants,
        'bannedChampions': game['bannedChampions']
    }
    options = { 'upsert': True }
    try:
        team_games_col.update_one(id_query, teamGameDao, options)
    except Exception as e:
        print(e)

def updatePlayerGames(game_id, game_participants, player_id, date_played, teams_col, id_query):
    playerGameDao = {
        '_id': game_id,
        'champion': game_participants[player_id],
        'datePlayed': date_played
    }
    gamesPlayed = list(teams_col.find(id_query))[0]['games']
    game_ids = set([game['_id'] for game in gamesPlayed])

    if game_id not in game_ids:
        append_values = { '$push': { 'games': playerGameDao } }
        try:
            teams_col.update_one(id_query, append_values)
        except Exception as e:
            print(e)
        
def parse_game_participants(players, target_id):
    target_team = list(filter(lambda player: player['puuid'] == target_id, players))[0]['teamId']
    team = {}
    for player in players:
        if player['teamId'] == target_team:
            team[player['puuid']] = champ_map[str(player['championId'])]

    return team

def main():
    scout_games(TEAMS)

### minimize api calls, store the summoner ID
### minimize database calls
### pararellize teams and palyers


main()
