from agents.root_agent import RootAgent
from heirarchy_impl.monitor import interact
import gym
import numpy as np

env = gym.make('Taxi-v2')
agent = RootAgent()
avg_rewards, best_avg_reward = interact(env, agent)
