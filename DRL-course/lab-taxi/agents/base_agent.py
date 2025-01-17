import random

import numpy as np
from collections import defaultdict


class BaseAgent:
    def __init__(self, name, nA, alpha=1, gamma=1, epsilon_init=0.5, epsilon_decay=0.99995, epsilon_limit=0.0001,
                 sarsa="MAX"):
        """ Initialize agent.

        Params
        ======
        - nA: number of actions available to the agent
        """
        self.name = name
        self.nA = nA
        self.Q = defaultdict(lambda: np.zeros(self.nA))
        self.alpha = alpha
        self.alpha_decay = 0.9999
        self.alpha_limit = 0.01
        self.gamma = gamma
        self.eps = epsilon_init
        self.eps_decay = epsilon_decay
        self.eps_limit = epsilon_limit
        self.next_action = np.random.choice(self.nA)
        self.select_action_to_method = self.select_action_eps_greedy
        self.hit_e = False
        self.hit_a = False
        self.episode_number = 1
        if sarsa == "NORMAL":
            self.method = self.sarsa
            self.select_action_to_method = self.select_action_sarsa
        elif sarsa == "EXPECTED":
            self.method = self.sarsa_expected
        else:
            self.method = self.sarsa_max

    def decode_state(self, state):
        """
        Decoding the state to show the grid values
        :param state:
        :return: taxi_row, taxi_col, pass_idx, dest_idx
        """
        out = []
        out.append(state % 4)
        state = state // 4
        out.append(state % 5)
        state = state // 5
        out.append(state % 5)
        state = state // 5
        out.append(state)
        if not 0 <= state < 5:
            debug = 0
        assert 0 <= state < 5
        return reversed(out)

    @staticmethod
    def color_to_pos(color):
        if color == 0:  # RED
            pos = (0, 0)
        elif color == 1:  # GREEN
            pos = (0, 4)
        elif color == 2:  # YELLOW
            pos = (4, 0)
        elif color == 3:
            pos = (4, 3)
        elif color == 4:
            pos = (-1, -1)
        else:
            pos = None
        return pos

    def select_action(self, state):
        """ Given the state, select an action.

        Params
        ======
        - state: the current state of the environment

        Returns
        =======
        - action: an integer, compatible with the task's action space
        """
        return self.select_action_to_method(state)

    def select_action_sarsa(self, state):
        """ Given the state, select an action.
            Save this action for next iteration.
        Params
        ======
        - state: the current state of the environment

        Returns
        =======
        - action: an integer, compatible with the task's action space
        """
        action = self.next_action
        self.next_action = self.select_action_eps_greedy(state)
        return action

    def select_action_eps_greedy(self, state):
        """ Given the state, select an action.

        Params
        ======
        - state: the current state of the environment

        Returns
        =======
        - action: an integer, compatible with the task's action space
        """
        if random.random() > self.eps:
            return np.argmax(self.Q[state])
        else:
            return np.random.choice(self.nA)

    def step(self, state, action, reward, next_state, done):
        """ Update the agent's knowledge, using the most recently sampled tuple.

        Params
        ======
        - state: the previous state of the environment
        - action: the agent's previous choice of action
        - reward: last reward received
        - next_state: the current state of the environment
        - done: whether the episode is complete (True or False)
        """
        taxi_row, taxi_col, pass_idx, dest_idx = self.decode_state(state)
        self.update_Q_table(state, action, reward, next_state, done)
        # Update epsilon:
        if done:
            self.episode_number += 1
            self.eps = max(self.eps_limit, self.eps * self.eps_decay)
            self.alpha = max(self.alpha * self.alpha_decay, self.alpha_limit)

            # print("\n", self.eps)
            if not self.hit_e and self.eps == self.eps_limit:
                self.hit_e = True
                print("\n", self.name, "epsilon limit is hit")
            if not self.hit_a and self.alpha == self.alpha_limit:
                self.hit_a = True
                print("\n", self.name, "alpha limit is hit")

    def update_Q_table(self, state, action, reward, next_state, done):
        current = self.Q[state][action]
        Q_next = 0
        if not done:
            Q_next = self.method(next_state)
        target = reward + (self.gamma * Q_next)
        self.Q[state][action] = current + self.alpha * (target - current)

    def sarsa(self, next_state):
        next_action = self.select_action_to_method(next_state)
        Q_next = self.Q[next_state][next_action]
        return Q_next

    def sarsa_max(self, next_state):
        max_action = np.argmax(self.Q[next_state])
        Q_next = self.Q[next_state][max_action]
        return Q_next

    def sarsa_expected(self, next_state):
        policy_s = np.ones(self.nA) * (self.eps / self.nA)
        policy_s[np.argmax(self.Q[next_state])] = (1 - self.eps) + (self.eps / self.nA)
        Q_next = np.dot(self.Q[next_state], policy_s)
        return Q_next
