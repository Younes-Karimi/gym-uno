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
		#pass
 
	def step(self, action):
		#pass
		print("Hello from step!!!")
		self.render()
 
	def reset(self):
		pass
 
	def render(self, mode='human'):
		#pass
		assert mode in ['human', 'state_pixels', 'rgb_array']
		screen_width = 600
		screen_height = 400
		boxwidth = 50.0
		cartwidth = 100.0
		cartheight = 120.0
		print("self.viewer = " + repr(self.viewer))
		if self.viewer is None:
			from gym.envs.classic_control import rendering
			self.viewer = rendering.Viewer(screen_width, screen_height)
			
			l,r,t,b = -cartwidth/2, cartwidth/2, cartheight/2, -cartheight/2
			axleoffset =cartheight/4.0
			cart = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
			cart.set_color(.8,.6,.4)
			self.carttrans = rendering.Transform(translation=(100, 100))
			cart.add_attr(self.carttrans)
			self.viewer.add_geom(cart)
			#self.carttrans.set_translation(100, 100)
			'''
			l,r,t,b = -polewidth/2,polewidth/2,polelen-polewidth/2,-polewidth/2
			pole = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
			pole.set_color(.8,.6,.4)
			self.poletrans = rendering.Transform(translation=(0, axleoffset))
			pole.add_attr(self.poletrans)
			pole.add_attr(self.carttrans)
			self.viewer.add_geom(pole)
			'''
			self.track = rendering.Line((100,0), (100,screen_height))
			self.track.set_color(0,0,0)
			self.viewer.add_geom(self.track)
			
			arr = None
			win = self.viewer.window
			self.score_label = pyglet.text.Label('Hello, world',
						  font_name='Times New Roman',
						  font_size=36,
						  x=win.width//2, y=win.height//2,
						  anchor_x='center', anchor_y='center')
			#self.transform = rendering.Transform()
			
			
			win.switch_to()
			win.dispatch_events()
			win.clear()
			print("mode == " + mode)
			#@win.event
			#self.on_draw()
			#self.score_label.draw()
			#self.render_indicators(WINDOW_W, WINDOW_H)
			
			#t = self.transform
			pixel_scale = 1
			if hasattr(win.context, '_nscontext'):
				pixel_scale = win.context._nscontext.view().backingScaleFactor()
			VP_W = int(pixel_scale * WINDOW_W)
			VP_H = int(pixel_scale * WINDOW_H)
			#gl.glViewport(0, 0, VP_W, VP_H)
			gl.glViewport(0, 0, screen_width, screen_height)
			for geom in self.viewer.onetime_geoms:
				geom.render()
			self.viewer.onetime_geoms = []
						  
			for i in range (1,100):
				#gl.glBegin(gl.GL_QUADS)
				'''
				s = screen_width/40.0
				h = screen_height/40.0
				gl.glColor4f(0,0,0,1)
				gl.glVertex3f(screen_width, 0, 0)
				gl.glVertex3f(screen_width, 5*h, 0)
				gl.glVertex3f(0, 5*h, 0)
				gl.glVertex3f(0, 0, 0)
				'''
				self.score_label.draw()
				if mode == 'human':
					win.flip()
					#return self.viewer.isopen
				
			
			image_data = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
			arr = np.fromstring(image_data.data, dtype=np.uint8, sep='')
			
			
			#win = self.viewer.window
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
			
			
			#arr = arr.reshape(VP_H, VP_W, 4)
			#arr = arr[::-1, :, 0:3]

		self.counter += 1
		if self.counter < 5:
			self.step('act')
		#return arr
		return self.viewer.render(return_rgb_array = mode=='rgb_array')
	'''
	def render_indicators(self, W, H):
		gl.glBegin(gl.GL_QUADS)
		s = W/40.0
		h = H/40.0
		gl.glColor4f(0,0,0,1)
		gl.glVertex3f(W, 0, 0)
		gl.glVertex3f(W, 5*h, 0)
		gl.glVertex3f(0, 5*h, 0)
		gl.glVertex3f(0, 0, 0)
		def vertical_ind(place, val, color):
			gl.glColor4f(color[0], color[1], color[2], 1)
			gl.glVertex3f((place+0)*s, h + h*val, 0)
			gl.glVertex3f((place+1)*s, h + h*val, 0)
			gl.glVertex3f((place+1)*s, h, 0)
			gl.glVertex3f((place+0)*s, h, 0)
		def horiz_ind(place, val, color):
			gl.glColor4f(color[0], color[1], color[2], 1)
			gl.glVertex3f((place+0)*s, 4*h , 0)
			gl.glVertex3f((place+val)*s, 4*h, 0)
			gl.glVertex3f((place+val)*s, 2*h, 0)
			gl.glVertex3f((place+0)*s, 2*h, 0)
		
		true_speed = np.sqrt(np.square(self.car.hull.linearVelocity[0]) + np.square(self.car.hull.linearVelocity[1]))
		vertical_ind(5, 0.02*true_speed, (1,1,1))
		vertical_ind(7, 0.01*self.car.wheels[0].omega, (0.0,0,1)) # ABS sensors
		vertical_ind(8, 0.01*self.car.wheels[1].omega, (0.0,0,1))
		vertical_ind(9, 0.01*self.car.wheels[2].omega, (0.2,0,1))
		vertical_ind(10,0.01*self.car.wheels[3].omega, (0.2,0,1))
		horiz_ind(20, -10.0*self.car.wheels[0].joint.angle, (0,1,0))
		horiz_ind(30, -0.8*self.car.hull.angularVelocity, (1,0,0))
		
		gl.glEnd()
		self.score_label.text = "%04i" % self.reward
		self.score_label.draw()
	'''
	
	#@win.event
	def on_draw(self):
		#window.clear()
		#label.draw()
		while(True):
			self.score_label.draw()
		
	def close(self):
		if self.viewer:
			self.viewer.close()
			self.viewer = None
		
'''
if __name__=="__main__":
	from pyglet.window import key
	a = np.array( [0.0, 0.0, 0.0] )
	def key_press(k, mod):
		global restart
		if k==0xff0d: restart = True
		if k==key.LEFT:  a[0] = -1.0
		if k==key.RIGHT: a[0] = +1.0
		if k==key.UP:    a[1] = +1.0
		if k==key.DOWN:  a[2] = +0.8   # set 1.0 for wheels to block to zero rotation
	def key_release(k, mod):
		if k==key.LEFT  and a[0]==-1.0: a[0] = 0
		if k==key.RIGHT and a[0]==+1.0: a[0] = 0
		if k==key.UP:    a[1] = 0
		if k==key.DOWN:  a[2] = 0
	env = CarRacing()
	env.render()
	env.viewer.window.on_key_press = key_press
	env.viewer.window.on_key_release = key_release
	record_video = False
	if record_video:
		from gym.wrappers.monitor import Monitor
		env = Monitor(env, '/tmp/video-test', force=True)
	isopen = True
	while isopen:
		env.reset()
		total_reward = 0.0
		steps = 0
		restart = False
		while True:
			s, r, done, info = env.step(a)
			total_reward += r
			if steps % 200 == 0 or done:
				print("\naction " + str(["{:+0.2f}".format(x) for x in a]))
				print("step {} total_reward {:+0.2f}".format(steps, total_reward))
				#import matplotlib.pyplot as plt
				#plt.imshow(s)
				#plt.savefig("test.jpeg")
			steps += 1
			isopen = env.render()
			if done or restart or isopen == False: break
	env.close()
'''	
		
		
		
		
		
		
		
		