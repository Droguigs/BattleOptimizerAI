import asyncio
import numpy as np
import os

from poke_env.player import RandomPlayer
from poke_env.teambuilder import Teambuilder


class RandomTeamFromPool(Teambuilder):
    def __init__(self, teams):
        for team in teams:
            if self.parse_showdown_team(team):
                self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

    def yield_team(self):
        return np.random.choice(self.teams)
    
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "JSON/team_data/json_team_")
indexes = list(range(2000, 2000*70+1, 2000))

def drop_lines(string):
    return string.replace("\n\n", "")

async def main():
    teams = []

    for index in indexes:
        with open(path + f"{index}.txt", 'r') as file:
            lines = file.read()
            split_lines = lines.split("___")
            for team in split_lines:
                helper = team.split("\n\n\n")
                for split_team in helper:
                    formatted_team = drop_lines(split_team)
                    teams.append(formatted_team)

    custom_builder = RandomTeamFromPool(teams)

    # We create two players
    player_1 = RandomPlayer(
        battle_format="gen8ou",
        team=custom_builder,
        max_concurrent_battles=10,
    )
    player_2 = RandomPlayer(
        battle_format="gen8ou",
        team=custom_builder,
        max_concurrent_battles=10,
    )

    await player_1.battle_against(player_2, n_battles=5)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())