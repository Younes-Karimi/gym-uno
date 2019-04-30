import gym
import gym_uno
env = gym.make('Uno-v0')

env.reset()
#for _ in range(4):
env.render()
#	print("action")
    #env.step(env.action_space.sample()) # take a random action
env.close()