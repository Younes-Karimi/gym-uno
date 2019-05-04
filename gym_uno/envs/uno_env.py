import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pyglet
from pyglet.window import gl
from pyglet.window import key

import numpy as np
import tkinter as tk


#WINDOW_H = 200
WINDOW_W = 1000
WINDOW_H = 800
 
 
class UnoEnv(gym.Env):  
	metadata = {
		'render.modes': ['human', 'rgb_array', 'state_pixels'],
		'video.frames_per_second' : 50
	}  
	def __init__(self):
		self.viewer = None
		self.reward = 50
		self.car = None
		self.counter = 0
		self.moves = 0
		self.points = 0
		self.possible_cards = ["1G", "2G", "1R", "2R", "1Y", "2Y", "1B", "2B"]
		self.num_total_cards = len(self.possible_cards)
		self.num_pile_cards = 1
		self.num_agent_cards = 3
		self.num_deck_cards = self.num_total_cards - (self.num_agent_cards + self.num_pile_cards)
		self.agent_cards = np.random.choice(self.possible_cards, self.num_agent_cards, replace=False).tolist()
		self.deck_cards = np.random.choice(list(set(self.possible_cards) - set(self.agent_cards)), self.num_deck_cards, replace=False).tolist()
		self.pile_card = list(set(self.possible_cards) - set(self.agent_cards + self.deck_cards))[0]
		self.score_label = ''
 
	def step(self, action):
		#pass
		print("Hello from step!!!")
		#print("self.action_space == ", self.action_space)
		#assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
		assert action in ['pick_from_deck', 'put_on_pile'], "%r (%s) invalid"%(action, type(action))
        #state = self.state
        #x, x_dot, theta, theta_dot = state
		self.render()
 
	def reset(self):
		pass
 
	def render(self, mode='human'):
		#pass
		assert mode in ['human', 'state_pixels', 'rgb_array']
		screen_width = 800
		screen_height = 600
		boxwidth = 50.0
		cartwidth = 100.0
		cartheight = 120.0
		print("self.viewer = " + repr(self.viewer))
		if self.viewer is None:
			from gym.envs.classic_control import rendering
			self.viewer = rendering.Viewer(screen_width, screen_height)
						
			win = self.viewer.window
			self.fillScoreLabel(win)
			
			self.document = pyglet.text.document.FormattedDocument(self.score_label.text)
			self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255), font_name = 'Times New Roman', font_size=20))
			self.score_label = pyglet.text.layout.TextLayout(self.document,screen_width,screen_height,multiline=True)

			win.switch_to()
			win.dispatch_events()
			win.clear()
			print("mode == " + mode)
			for i in range (1,100):
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
					  
		else:
			#self.viewer.close()
			#from gym.envs.classic_control import rendering
			#self.viewer = rendering.Viewer(screen_width, screen_height)
			
			win = self.viewer.window
			win.switch_to()
			win.dispatch_events()
			win.clear()
			win.flip()
			self.score_label3 = pyglet.text.Label('ABCDEFG',
						  font_name='Times New Roman',
						  font_size=30,
						  x=win.width//4, y=win.height//4,
						  anchor_x='center', anchor_y='center')
			win.switch_to()
			win.dispatch_events()
			win.clear()
			
			for i in range (1,100):
				self.score_label3.draw()
				if mode == 'human':
					win.flip()		

			win.switch_to()
			win.dispatch_events()
			win.clear()
			win.flip()
			self.score_label2 = pyglet.text.Label('TTTTTEST',
						  font_name='Times New Roman',
						  font_size=26,
						  x=win.width//3, y=win.height//3,
						  anchor_x='center', anchor_y='center')
			win.switch_to()
			win.dispatch_events()
			win.clear()
			
			for i in range (1,100):
				self.score_label2.draw()
				if mode == 'human':
					win.flip()	
			
		#self.counter += 1
		#if self.counter < 2:
		if self.num_agent_cards!=0 and self.num_deck_cards!=0:
			self.step('pick_from_deck')
		elif self.num_agent_cards==0 and self.num_deck_cards!=0:
			self.displayResult('win', win)
		elif self.num_deck_cards==0:
			self.displayResult('lose', win)
		else:
			print("ERROR!!!")
			exit()
		return self.viewer.render(return_rgb_array = mode=='rgb_array')			
		
	def fillScoreLabel(self,win):
		self.score_label = pyglet.text.Label('\n\t\t\t\tMoves: ' + str(self.moves),
					  font_name='Times New Roman',
					  font_size=26,
					  x=win.width//2, y=win.height-40,
					  anchor_x='center', anchor_y='center')			
		self.score_label.text = self.score_label.text + "\t\t\t\tPoints: " + str(self.points)
		self.score_label.text += "\n\n\n      ================= AGENT CARDS =================\n\n\t\t\t   "
		for card in self.agent_cards:
			self.score_label.text += card + "\t\t\t\t"

		self.score_label.text += "\n\n\n      ================= PILE TOP CARD ================\n\n\t\t\t\t\t\t\t\t"
		self.score_label.text += self.pile_card

		self.score_label.text += "\n\n\n      ===================== DECK ====================\n\n\t\t   top --> "
		for card in self.deck_cards:
			self.score_label.text += card + "\t\t\t"
	
	def close(self):
		if self.viewer:
			self.viewer.close()
			self.viewer = None
		
		
		
		
		
		
		
		
		