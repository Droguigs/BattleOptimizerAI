import asyncio
import time

from poke_env.player import Player, RandomPlayer

class MaxDmgPlayer(Player):
    def choose_move(self, battle):
        # The player will att if it can
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, 
                            key=lambda move: move.base_power)
            return self.create_order(best_move)
        
        # if no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)
        
        def teampreview(self, battle):
            mon_performance = {}

            # for each of our pokemons
            for i, mon in enumerate(battle.team.values()):
                # We store their average performance against the opponent team
                mon_performance[i] = np.mean([
                    teampreview_performance(mon, opp)
                    for opp in battle.oponnent_team.values()
                ])

            # We sort our mons by performance
            ordered_mons = sorted(mon_performance, key=lambda k: -mon_performance[k])

            # we start with the one we consider best overall
            # we use i + 1 as python indexes start from 0 but ps indexes start from 1
            return "/team" + ''.join([str(i+1) for i in ordered_mons])

        def teampreview_performance(mon_a, mon_b):
            # we evaluate the performance on mon_a against mon_b as its type advantage
            a_on_b = b_on_a = -np.inf
            for type in mon_a.types:
                if type_:
                    a_on_b = max(a_on_b, type.damage_multiplier(*mon_b.types))
            # we do the same for mon_b over mon_a
            for type in mon_b.types:
                if type_:
                    b_on_a = max(b_on_a, type.damage_multiplier(*mon_a.types))
            # Our performance metric is the difference between the two
            return a_on_b - b_on_a
        
async def main():
    start = time.time()

    # Create 2 players
    random_player = RandomPlayer(battle_format="gen8randombattle")
    max_dmg_player = MaxDmgPlayer(battle_format="gen8randombattle")

    # Evaluating the player
    await max_dmg_player.battle_against(random_player, n_battles=100)

    print("Max damage player won %d / 100 battles [this took %f seconds]" % (max_dmg_player.n_won_battles, time.time() - start))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())