import gym
import gym_uno
import itertools
import numpy as np

env = gym.make('Uno-v0')

# env.reset()
# #for _ in range(4):
# env.render()
# #	print("action")
#     #env.step(env.action_space.sample()) # take a random action
# env.close() 

action_space = ['pick_from_deck', 'put_on_pile']


  
def _findsubsets(s, n): 
    return list(itertools.combinations(s, n)) 


def observation_space_creator():

    observation_space = []
    possible_cards = ["1G", "2G", "1R", "2R", "1Y", "2Y", "1B", "2B"]

    for num_agent_cards in range(0, len(possible_cards)): # Possible number of card for the agent: 0-7
        agent_cards_subsets = _findsubsets(possible_cards, num_agent_cards) # finds all subsets with the cardinality of num_agent_cards

        for agent_cards_subset in agent_cards_subsets:
            pile_subsets = _findsubsets(list(set(possible_cards) - set(agent_cards_subset)), 1)

            for pile_card in pile_subsets:
                deck_range = (0,0)
                if num_agent_cards < 2:
                    deck_range = (1,5)
                elif num_agent_cards < 4:
                    deck_range = (0,5)
                else:
                    deck_range = (0, len(possible_cards) - len(agent_cards_subset))

                for num_deck_cards in range(deck_range[0], deck_range[1]):
                    deck_cards_subsets = _findsubsets(list(set(possible_cards) - set(agent_cards_subset) - set(pile_card)), num_deck_cards)

                    for deck_cards_subset in deck_cards_subsets:
                        observation_space.append([agent_cards_subset, pile_card, deck_cards_subset])

    return observation_space



observation_space = observation_space_creator()

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