import itertools, math, copy
import numpy as np
import random
from overcooked_ai_py.mdp.actions import Action, Direction


class Agent(object):
    def action(self, state):
        """
        Should return an action, and an action info dictionary.
        If collecting trajectories of the agent with OvercookedEnv, the action
        info data will be included in the trajectory data under `ep_infos`.

        This allows agents to optionally store useful information about them
        in the trajectory for further analysis.
        """
        return NotImplementedError()

    def actions(self, states, agent_indices):
        """
        A multi-state version of the action method. This enables for parallized
        implementations that can potentially give speedups in action prediction.

        Args:
            states (list): list of OvercookedStates for which we want actions for
            agent_indices (list): list to inform which agent we are requesting the action for in each state

        Returns:
            [(action, action_info), (action, action_info), ...]: the actions and action infos for each state-agent_index pair
        """
        return NotImplementedError()

    @staticmethod
    def a_probs_from_action(action):
        action_idx = Action.ACTION_TO_INDEX[action]
        return np.eye(Action.NUM_ACTIONS)[action_idx]

    @staticmethod
    def check_action_probs(action_probs, tolerance=1e-4):
        """Check that action probabilities sum to ≈ 1.0"""
        probs_sum = sum(action_probs)
        assert math.isclose(
            probs_sum, 1.0, rel_tol=tolerance
        ), "Action probabilities {} should sum up to approximately 1 but sum up to {}".format(
            list(action_probs), probs_sum)

    def set_agent_index(self, agent_index):
        self.agent_index = agent_index

    def set_mdp(self, mdp):
        self.mdp = mdp

    def reset(self):
        pass


class RandomAgent(Agent):
    """
    An agent that randomly picks motion actions.
    NOTE: Does not perform interact actions, unless specified
    """
    def __init__(self,
                 sim_threads=None,
                 all_actions=False,
                 custom_wait_prob=None):
        self.sim_threads = sim_threads
        self.all_actions = all_actions
        self.custom_wait_prob = custom_wait_prob

    def action(self, state):
        action_probs = np.zeros(Action.NUM_ACTIONS)
        legal_actions = list(Action.MOTION_ACTIONS)
        if self.all_actions:
            legal_actions = Action.ALL_ACTIONS
        legal_actions_indices = np.array(
            [Action.ACTION_TO_INDEX[motion_a] for motion_a in legal_actions])
        action_probs[legal_actions_indices] = 1 / len(legal_actions_indices)

        if self.custom_wait_prob is not None:
            stay = Action.STAY
            if np.random.random() < self.custom_wait_prob:
                return stay, {"action_probs": Agent.a_probs_from_action(stay)}
            else:
                action_probs = Action.remove_indices_and_renormalize(
                    action_probs, [Action.ACTION_TO_INDEX[stay]])

        return Action.sample(action_probs), {"action_probs": action_probs}

    def actions(self, states, agent_indices):
        return [self.action(state) for state in states]

    def direct_action(self, obs):
        return [np.random.randint(4) for _ in range(self.sim_threads)]


class HumanPlayer(Agent):
    """Agent to be controlled by human player.
    """
    def __init__(self, ):
        self.prev_state = None

    def update_logs(self, state, action):
        """Update necessary logs for calculating bcs."""
        if action == Action.STAY:
            state.players[self.agent_index].active_log += [0]
        else:
            state.players[self.agent_index].active_log += [1]

        # get stuck if the players position and orientations do not change.
        if self.prev_state is not None and state.players_pos_and_or == self.prev_state.players_pos_and_or:
            state.players[self.agent_index].stuck_log += [1]
        else:
            state.players[self.agent_index].stuck_log += [0]

        self.prev_state = state

    def reset(self):
        super().reset()
        self.prev_state = None