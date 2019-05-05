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

    print('Episode: %d\n' % _)
    env.render()
    action = action_space[np.random.choice(len(action_space))] # your agent here (this takes random actions)
    observation, points, moves, done = env.step(action)

    if done is not None:
        if done == 'win':
            print("Win!\nObservastion: %s\nPoints: %d\nMoves: %d\n\n" %(observation, points, moves))
        elif done == 'lose':
            print("Lose!\nObservastion: %s\nPoints: %d\nMoves: %d\n\n" %(observation, points, moves))
        env.closeWin()
        observation = env.reset()
env.close()