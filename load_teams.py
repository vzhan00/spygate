from riot_adapter import get_player_puuid
from teams import TEAMS
from mongo_adapter import MongoAdapter

mongo_client = MongoAdapter

teams_database = mongo_client['teams']
team_games_database = mongo_client['team_games']

def add_teams_to_mongo(teams):
    for team in teams:
        team_games_database[team['team']].drop()
        teams_database[team['team']].drop()

        teams_col = teams_database[team['team']]
        for player in team['players']:
            puuid = get_player_puuid(player)
            player_doc = {
                '_id': puuid,
                'player': player,
                'compChampions': []
            }

            teams_col.insert_one(player_doc)

def parse_teams(teams):
    parsed_teams = []
    for team in teams:
        players = parse_players(team['players'])
        parsed_team = { 'team': team['team'], 'players': players }
        parsed_teams.append(parsed_team)

    return parsed_teams


def parse_players(team):
    parsed_players = team.split(',')

    return parsed_players

def main():
    teams = parse_teams(TEAMS)
    add_teams_to_mongo(teams)

main()