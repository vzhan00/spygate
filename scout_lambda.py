import json
from mongo_adapter import MongoAdapter
from riot_adapter import check_in_game
from teams import TEAMS

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
        team_col = teams_database[team['team']]
        players = team_col.find()
        puuids = set([player['_id'] for player in players])
        for player in players:
            game = check_in_game(player['_id'])

            if 'status' in game: #or game['gameType'] != 'CUSTOM':
                print(game)
                continue 
            
            target_team = parse_game_participants(game['participants'], player['_id'])
            players_in_team = 0
            for id in target_team.keys():
                if players_in_team >= 2:
                    break
                if id in puuids:
                    players_in_team += 0

            if players_in_team < 2:
                ### add to their own game
                break
            
            gameDao = {
                'gameId': game['gameId'],
                # seconds
                'gameLength': game['gameLength'],
                # epoch milliseconds
                'gameStartTime': game['gameStartTime'],
                'championsPlayed': championsPlayed,
                'bannedChampions': game['bannedChampions']
            }   
            
def parse_game_participants(players, target_id):
    target_team = list(filter(lambda player: player['puuid'] == target_id, players))[0]['teamId']
    team = {}
    for player in players:
        if player['teamId'] == target_team:
            team[player['puuid']] = champ_map[str(player['championId'])]

    return team

def main():
    # player = 'soulbert#koggy'
    # id = get_player_puuid(player)
    # game = check_in_game(id)

    # print(game)
    scout_games(TEAMS)

### minimize api calls, store the summoner ID
### minimize database calls
### pararellize teams and palyers


main()
