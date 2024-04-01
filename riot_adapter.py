import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
headers = {'X-Riot-Token': api_key}
def check_in_game(puuid):
    url = f'https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}'
    game = requests.get(url, headers=headers).json()
    return game

def get_player_puuid(player):
    player_ids = list(map(str.strip, player.split('#')))
    game_name = player_ids[0]
    tag_line = player_ids[1]
    url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
    player = requests.get(url, headers=headers).json()
    return player['puuid']

# def main():
    # player = 'soulbert#koggy'
    # id = get_player_puuid(player)
    # game = check_in_game(id)

    # print(game)