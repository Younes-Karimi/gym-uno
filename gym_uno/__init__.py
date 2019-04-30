from gym.envs.registration import register
 
register(id='Uno-v0', 
    entry_point='gym_uno.envs:UnoEnv', 
)