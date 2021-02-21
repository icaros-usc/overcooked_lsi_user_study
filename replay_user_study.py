import os
import ast
import time
import argparse
import pandas as pd
from overcooked_ai_py.agents.agent import HumanPlayer
from overcooked_ai_py.mdp.overcooked_env import OvercookedEnv
from overcooked_ai_py.mdp.overcooked_mdp import OvercookedGridworld

HUMAN_STUDY_ENV_HORIZON = 150

SUB_STUDY_TYPES = [
    'even_workloads',
    'uneven_workloads',
    'high_team_fluency',
    'low_team_fluency',
]

NON_TRIAL_STUDY_TYPES = [
    'all',
    *SUB_STUDY_TYPES,
]

DETAILED_STUDY_TYPES = [f"{x}-{i}" for x in SUB_STUDY_TYPES for i in range(3)]

ALL_STUDY_TYPES = [
    'all',
    'trial',
    *SUB_STUDY_TYPES,
]

CONFIG = {
    "start_order_list": ['onion'] * 2,
    "cook_time": 10,
    "num_items_for_soup": 3,
    "delivery_reward": 20,
    "rew_shaping_params": None
}


def lvl_str2grid(lvl_str):
    """
    Turns pure string formatted lvl to grid format compatible with overcooked-AI env
    """
    return [layout_row.strip() for layout_row in lvl_str.split("\n")][:-1]


def init_env(lvl_str, horizon):
    grid = lvl_str2grid(lvl_str)
    mdp = OvercookedGridworld.from_grid(grid, CONFIG)
    env = OvercookedEnv.from_mdp(mdp, info_level=0, horizon=horizon)
    return env


def load_human_log_data(log_index):
    human_log_csv = os.path.join("user_study/result", log_index,
                                 "human_log_refined.csv")
    if not os.path.exists(human_log_csv):
        print("Log dir does not exit.")
        exit(1)
    human_log_data = pd.read_csv(human_log_csv)
    return human_log_csv, human_log_data


def replay_with_joint_actions(lvl_str, joint_actions, plot=True):
    """Replay a game play with given level and joint actions.

    Args:
        joint_actions (list of tuple of tuple): Joint actions.
    """
    env = init_env(lvl_str, horizon=HUMAN_STUDY_ENV_HORIZON)
    done = False
    # Hacky: use human agent for replay.
    ai_agent = HumanPlayer()
    player = HumanPlayer()

    ai_agent.set_agent_index(0)
    ai_agent.set_mdp(env.mdp)
    player.set_agent_index(1)
    player.set_mdp(env.mdp)
    i = 0
    last_state = None
    total_sparse_reward = 0
    checkpoints = [env.horizon - 1] * env.num_orders
    cur_order = 0

    while not done:
        if plot:
            env.render()
            time.sleep(0.2)
        ai_agent.update_logs(env.state, joint_actions[i][0])
        player.update_logs(env.state, joint_actions[i][1])
        next_state, timestep_sparse_reward, done, info = env.step(
            joint_actions[i])
        total_sparse_reward += timestep_sparse_reward

        if timestep_sparse_reward > 0:
            checkpoints[cur_order] = i
            cur_order += 1
        # print(joint_actions[i])
        last_state = next_state
        i += 1

    # recalculate the bcs
    workloads = next_state.get_player_workload()
    concurr_active = next_state.cal_concurrent_active_sum()
    stuck_time = next_state.cal_total_stuck_time()
    return workloads, concurr_active, stuck_time, checkpoints, i


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l',
                        '--log_index',
                        help='Integer: index of the study log',
                        required=False,
                        default=-1)
    parser.add_argument('-type',
                        help='Integer: type of the game level.',
                        required=False,
                        default=None)
    opt = parser.parse_args()

    # replay the specified study
    log_index = opt.log_index
    lvl_type = opt.type

    if not lvl_type in DETAILED_STUDY_TYPES:
        print("Level type not found, must be one of", DETAILED_STUDY_TYPES)
        exit(1)

    # get level string and logged joint actions from log file
    _, human_log_data = load_human_log_data(log_index)
    lvl_str = human_log_data[human_log_data["lvl_type"] ==
                             lvl_type]["lvl_str"].iloc[0]
    joint_actions = ast.literal_eval(human_log_data[
        human_log_data["lvl_type"] == lvl_type]["joint_actions"].iloc[0])

    # replay the game
    replay_with_joint_actions(lvl_str, joint_actions)
