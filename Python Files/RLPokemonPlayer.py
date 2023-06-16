import asyncio
import os

from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers.legacy import Adam

from poke_env.player import (
    RandomPlayer,
    MaxBasePowerPlayer,
)

from SingleRLPlayer import SimpleRLPlayer
from RandomTeamFromPool import RandomPlayer

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "JSON/json_teams/json_team_")
# indexes = range(141204)

async def main():
    teams = []
    for i in range(101):
        with open(path + f"{i}.txt", 'r') as file:
            teams.append(file.read())

    # Create one environment for training and one for evaluation

    opponent = RandomPlayer(battle_format= "gen8randombattle")
    train_env = SimpleRLPlayer(
        battle_format="gen8randombattle", opponent=opponent, start_challenging=True
    )

    opponent = RandomPlayer(battle_format="gen8randombattle")

    eval_env = SimpleRLPlayer(battle_format="gen8randombattle", opponent=opponent, start_challenging=True)

    # Compute dimensions
    n_action = train_env.action_space.n
    input_shape = (1,) + train_env.observation_space.shape

    # Create model
    model = Sequential()
    model.add(Dense(128, activation="elu", input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(64, activation="elu"))
    model.add(Dense(n_action, activation="linear"))

    # Defining the DQN
    memory = SequentialMemory(limit=5, window_length=1)

    policy = LinearAnnealedPolicy(
        EpsGreedyQPolicy(),
        attr="eps",
        value_max=1.0,
        value_min=0.05,
        value_test=0.0,
        nb_steps=5,
    )

    dqn = DQNAgent(
        model=model,
        nb_actions=n_action,
        policy=policy,
        memory=memory,
        nb_steps_warmup=2500,
        gamma=0.5,
        target_model_update=1,
        delta_clip=0.01,
        enable_double_dqn=True,
    )
    dqn.compile(Adam(learning_rate=0.00025), metrics=["mae"])

    # Training the model
    dqn.fit(train_env, nb_steps=10000)
    train_env.close()

    # Evaluating the model
    print("Results against random player:")
    eval_env.did_print_team = False
    dqn.test(eval_env, nb_episodes=1, verbose=False, visualize=True)
    print(
        f"DQN Evaluation: {eval_env.n_won_battles} victories out of {eval_env.n_finished_battles} episodes"
    )

    second_opponent = MaxBasePowerPlayer(battle_format="gen8randombattle")
    eval_env.reset_env(restart=True, opponent=second_opponent)
    print("Results against max base power player:")
    dqn.test(eval_env, nb_episodes=1, verbose=False, visualize=True)
    print(
        f"DQN Evaluation: {eval_env.n_won_battles} victories out of {eval_env.n_finished_battles} episodes"
    )

    eval_env.reset_env(restart=True)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())