import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pyglet
from pyglet.window import gl
from pyglet.window import key

import numpy as np
import tkinter as tk


WINDOW_W = 800
WINDOW_H = 600
NUM_PILE_CARDS = 1
NUM_AGENT_CARDS = 3
POINT = 10
WIN_POINT = 101
DELAY = 5

 
class UnoEnv(gym.Env):  
	metadata = {
		'render.modes': ['human', 'rgb_array', 'state_pixels'],
		'video.frames_per_second' : 50
	}  

	def __init__(self):
		self.viewer = None
		self.car = None
		self.counter = 0
		self.moves = 0
		self.points = 0
		self.possible_cards = ["1G", "2G", "1R", "2R", "1Y", "2Y", "1B", "2B"]
		self.num_total_cards = len(self.possible_cards)
		self.num_deck_cards = self.num_total_cards - (NUM_AGENT_CARDS + NUM_PILE_CARDS)
		self.score_label = ''
		self.action_space = ['pick_from_deck', 'put_on_pile']
		# self.observation_space = 
		self.state = None
		self.win = None



	def _transition_function(self, action, agent_cards, pile_top, proper_agent_cards, deck_cards):

		action_type = {
			### If agent has a proper card and puts/removes ###
			### If agent does NOT have a proper card and puts/removes ###
			'has-proper-put': False, 
			'has-proper-remove': False,
			'no-proper-put': False,
			'no-proper-remove': False
		}

		if action == 'put_on_pile':		
			if len(proper_agent_cards) > 0:
				selection = np.random.choice(proper_agent_cards, 1, replace=False).tolist()[0]
				pile_top = selection
				agent_cards.remove(selection)
				action_type['has-proper-put'] = True
				self.points += POINT
				self.moves += 1
				return pile_top
			else:
				action_type['no-proper-put'] = True
				self.points -= 2 * POINT

		elif action == 'pick_from_deck':
			if len(proper_agent_cards) > 0:
				action_type['has-proper-remove'] = True
				self.points -= 2 * POINT
			else:
				action_type['no-proper-remove'] = True
				self.points -= POINT

			self.moves += 1				
			selection = np.random.choice(deck_cards, 1, replace=False).tolist()[0]
			deck_cards.remove(selection)
			agent_cards.append(selection)

		return pile_top



	def step(self, action):

		assert (action in self.action_space), ("%r (%s) invalid" % (action, type(action)))
		state = self.state
		agent_cards, pile_top, deck_cards = state

		pile_num = pile_top[0]
		pile_color = pile_top[1]

		proper_agent_cards = [card for card in agent_cards if (card[0] == pile_num) or (card[1] == pile_color)]

		pile_top = self._transition_function(action, agent_cards, pile_top, proper_agent_cards, deck_cards)

		self.state = (agent_cards, pile_top, deck_cards)

		
        # force = self.force_mag if action==1 else -self.force_mag
        # costheta = math.cos(theta)
        # sintheta = math.sin(theta)
        # temp = (force + self.polemass_length * theta_dot * theta_dot * sintheta) / self.total_mass
        # thetaacc = (self.gravity * sintheta - costheta* temp) / (self.length * (4.0/3.0 - self.masspole * costheta * costheta / self.total_mass))
        # xacc  = temp - self.polemass_length * thetaacc * costheta / self.total_mass


        # if self.kinematics_integrator == 'euler':
        #     x  = x + self.tau * x_dot
        #     x_dot = x_dot + self.tau * xacc
        #     theta = theta + self.tau * theta_dot
        #     theta_dot = theta_dot + self.tau * thetaacc
        # else: # semi-implicit euler
        #     x_dot = x_dot + self.tau * xacc
        #     x  = x + self.tau * x_dot
        #     theta_dot = theta_dot + self.tau * thetaacc
        #     theta = theta + self.tau * theta_dot
        # self.state = (x,x_dot,theta,theta_dot)


		done = None

		if len(agent_cards)==0 and len(deck_cards)!=0:
			done = 'win'
		elif len(deck_cards)==0:
			done = 'lose'
		# elif self.num_deck_cards==0:
		# 	self.displayResult('lose', win)


		# if NUM_AGENT_CARDS!=0 and self.num_deck_cards!=0:
		# 	self.step('pick_from_deck')
		# elif NUM_AGENT_CARDS==0 and self.num_deck_cards!=0:
		# 	self.displayResult('win', win)
		# elif self.num_deck_cards==0:
		# 	self.displayResult('lose', win)
		# else:
		# 	print("ERROR!!!")
		# 	exit()
		
		
		
		#done =  bool((len(agent_cards) < 1) or (len(agent_cards) > self.num_total_cards - 2))


        # if not done:
        #     reward = 1.0
        # elif self.steps_beyond_done is None:
        #     # Pole just fell!
        #     self.steps_beyond_done = 0
        #     reward = 1.0
        # else:
        #     if self.steps_beyond_done == 0:
        #         logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
        #     self.steps_beyond_done += 1
        #     reward = 0.0

		# self.render()
		
		return np.array(self.state), self.points, self.moves, done

 

	def reset(self):

		from gym.envs.classic_control import rendering
		self.viewer = rendering.Viewer(WINDOW_W, WINDOW_H)	
		self.win = self.viewer.window
		self.points = 0
		self.moves = 0

		agent_cards = np.random.choice(self.possible_cards, NUM_AGENT_CARDS, replace=False).tolist()
		deck_cards = np.random.choice(list(set(self.possible_cards) - set(agent_cards)), self.num_deck_cards, replace=False).tolist()
		pile_card = list(set(self.possible_cards) - set(agent_cards + deck_cards))[0]
		self.state = agent_cards, pile_card, deck_cards
        # self.steps_beyond_done = None
		# return np.array(self.state)
		return self.state
 


	def render(self, mode='human'):

		assert mode in ['human', 'state_pixels', 'rgb_array']
		
		# if self.viewer is None:
			
						
		#win = self.viewer.window
		win = self.win
		# self.fillScoreLabel(win)
		
		# self.document = pyglet.text.document.FormattedDocument(self.score_label.text)
		# self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255), font_name = 'Times New Roman', font_size=20))
		# self.score_label = pyglet.text.layout.TextLayout(self.document,WINDOW_W,WINDOW_H,multiline=True)

		#win = self.viewer.window
		win.switch_to()
		win.dispatch_events()
		win.clear()
		win.flip()

		self.fillScoreLabel(win)
		self.document = pyglet.text.document.FormattedDocument(self.score_label.text)
		self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255), font_name = 'Times New Roman', font_size=20))
		self.score_label = pyglet.text.layout.TextLayout(self.document,WINDOW_W,WINDOW_H,multiline=True)
		
		win.switch_to()
		win.dispatch_events()
		win.clear()

		for i in range (1, DELAY):
			self.score_label.draw()
			if mode == 'human':
				win.flip()				
			'''
			win.switch_to()
			win.dispatch_events()
			win.clear()
			win.flip()
			self.score_label2 = pyglet.text.Label('Points: ' + str(self.points),
						  font_name='Times New Roman',
						  font_size=16,
						  x=win.width//2, y=win.height-50,
						  anchor_x='center', anchor_y='center')
			win.switch_to()
			win.dispatch_events()
			win.clear()
			
			for i in range (1,100):
				self.score_label2.draw()
				if mode == 'human':
					win.flip()	
			'''


		# else:
		# 	#self.viewer.close()
		# 	#from gym.envs.classic_control import rendering
		# 	#self.viewer = rendering.Viewer(WINDOW_W, WINDOW_H)
			
		# 	win = self.viewer.window
		# 	win.switch_to()
		# 	win.dispatch_events()
		# 	win.clear()
		# 	win.flip()
		# 	self.score_label3 = pyglet.text.Label('ABCDEFG',
		# 				  font_name='Times New Roman',
		# 				  font_size=30,
		# 				  x=win.width//4, y=win.height//4,
		# 				  anchor_x='center', anchor_y='center')
		# 	win.switch_to()
		# 	win.dispatch_events()
		# 	win.clear()
			
		# 	for i in range (1,100):
		# 		self.score_label3.draw()
		# 		if mode == 'human':
		# 			win.flip()		

		# 	win.switch_to()
		# 	win.dispatch_events()
		# 	win.clear()
		# 	win.flip()
		# 	self.score_label2 = pyglet.text.Label('TTTTTEST',
		# 				  font_name='Times New Roman',
		# 				  font_size=26,
		# 				  x=win.width//3, y=win.height//3,
		# 				  anchor_x='center', anchor_y='center')
		# 	win.switch_to()
		# 	win.dispatch_events()
		# 	win.clear()
			
		# 	for i in range (1,100):
		# 		self.score_label2.draw()
		# 		if mode == 'human':
		# 			win.flip()	
			


		# self.counter += 1
		# if self.counter < 3:
		# 	self.step('pick_from_deck')


		# if NUM_AGENT_CARDS!=0 and self.num_deck_cards!=0:
		# 	self.step('pick_from_deck')
		# elif NUM_AGENT_CARDS==0 and self.num_deck_cards!=0:
		# 	self.displayResult('win', win)
		# elif self.num_deck_cards==0:
		# 	self.displayResult('lose', win)
		# else:
		# 	print("ERROR!!!")
		# 	exit()
		
		# return self.viewer.render(return_rgb_array = mode=='rgb_array')	

		self.win = win		
		return self.viewer.render()			
		


	def fillScoreLabel(self,win):

		agent_cards = self.state[0]
		pile_card = self.state[1]
		deck_cards = self.state[2]

		self.score_label = pyglet.text.Label('\n\t\t\t\tMoves: ' + str(self.moves),
					  font_name='Times New Roman',
					  font_size=26,
					  x=win.width//2, y=win.height-40,
					  anchor_x='center', anchor_y='center')			
		self.score_label.text = self.score_label.text + "\t\t\t\tPoints: " + str(self.points)
		self.score_label.text += "\n\n\n      ================= AGENT CARDS =================\n\n\t\t\t   "
		for card in agent_cards:
			self.score_label.text += card + "\t\t\t\t"

		self.score_label.text += "\n\n\n      ================= PILE TOP CARD ================\n\n\t\t\t\t\t\t\t\t"
		self.score_label.text += pile_card

		self.score_label.text += "\n\n\n      ===================== DECK ====================\n\n\t\t   top --> "
		for card in deck_cards:
			self.score_label.text += card + "\t\t\t"
	

	def closeWin(self):
		if self.win:
			self.win.close()
			self.win = None

	def close(self):
		if self.viewer:
			self.viewer.close()
			self.viewer = None
		
		
		
		
		
		
		
		
		