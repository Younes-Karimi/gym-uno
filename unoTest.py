import gym
import gym_uno
import itertools
import numpy as np



NOISE = True
EPISODES = 5


# env.reset()
# #for _ in range(4):
# env.render()
# #	print("action")
#     #env.step(env.action_space.sample()) # take a random action
# env.close() 

  
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
                        observation_space.append((sorted(list(agent_cards_subset)), pile_card[0], sorted(list(deck_cards_subset))))

    return observation_space



observation_space = observation_space_creator() # 16640 states

# observation = env.reset()
# for _ in range(1000):

#     print('Episode: %d\n' % _)
#     env.render()
#     action = action_space[np.random.choice(len(action_space))] # your agent here (this takes random actions)
#     observation, points, moves, done = env.step(action)

#     if done is not None:
        # if done == 'win':
        #     print("Win!\nObservastion: %s\nPoints: %d\nMoves: %d\n\n" %(observation, points, moves))
        # elif done == 'lose':
        #     print("Lose!\nObservastion: %s\nPoints: %d\nMoves: %d\n\n" %(observation, points, moves))
#         env.closeWin()
#         observation = env.reset()
# env.close()






action_space = ['pick_from_deck', 'put_on_pile']


# env = gym.make('FrozenLake8x8-v0')


# 1. Load Environment and Q-table structure
env = gym.make('Uno-v0')
Q = np.zeros([len(observation_space), len(action_space)])
# 2. Parameters of Q-leanring
eta = .628
gma = .9
rev_list = [] # rewards per episode calculate
# 3. Q-learning Algorithm
for i in range(EPISODES):
    # Reset environment
    current_state = env.reset()
    current_state = (sorted(current_state[0]), current_state[1], sorted(current_state[2]))

    # print(current_state)

    s = observation_space.index(current_state)
    rAll = 0
    d = False
    j = 0
    # #The Q-Table learning algorithm
    while j < 99:
    # while done is not None:
        env.render()
        j+=1
        # Choose action from Q table
        if NOISE:
            a = np.argmax(Q[s,:] + np.random.randn(1, len(action_space))*(1./(i+1)))
        else:
            a = np.argmax(Q[s,:])
        #Get new state & reward from environment
        new_state, r, moves, d = env.step(action_space[a])
        new_state = (sorted(new_state[0]), new_state[1], sorted(new_state[2]))
        s1 = observation_space.index(new_state)
        #Update Q-Table with new knowledge

        print('BBBBBEfore: ', Q[s,:])

        Q[s,a] = Q[s,a] + eta*(r + gma*np.max(Q[s1,:]) - Q[s,a])

        print('AAAAAfter: ', Q[s,:])

        rAll += r
        s = s1

        if d is not None:
            if d == 'win':
                print("Win!\nObservation: %s\nPoints: %d\nMoves: %d\n\n" %(current_state, r, moves))
            elif d == 'lose':
                print("Lose!\nObservstion: %s\nPoints: %d\nMoves: %d\n\n" %(current_state, r, moves))
            env.closeWin()
            # env.reset()
            break
    rev_list.append(rAll)
    # env.render()

env.close()
# print(observation_space[inde])
# print(observation_space.index(s))
# print(observation_space[observation_space.index(s)])








# print "Reward Sum on all episodes " + str(sum(rev_list)/epis)
# print "Final Values Q-Table"
# print Q


# [list(['2R', '1R', '2B']) '1G' list(['1B', '2G', '1Y', '2Y'])]
# [(), ('2B',), ('2Y', '2R', '1Y')]
# [('2B',), ('2Y',), ('1B', '2R')]