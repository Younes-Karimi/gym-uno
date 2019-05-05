import gym
import gym_uno
import numpy as np

env = gym.make('Uno-v0')

# env.reset()
# #for _ in range(4):
# env.render()
# #	print("action")
#     #env.step(env.action_space.sample()) # take a random action
# env.close() 

action_space = ['pick_from_deck', 'put_on_pile']

observation = env.reset()
for _ in range(1000):
  env.render()
  action = action_space[np.random.choice(len(action_space))] # your agent here (this takes random actions)
  observation, reward, done, info = env.step(action)

  if done:
    observation = env.reset()
env.close()