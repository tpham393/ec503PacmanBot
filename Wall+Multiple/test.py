import game_funcs as g
from game import Game
from environment import *

g = Game();
env = PacmanEnv(num_ghosts=1, grid_len=7, grid=g.grid);

for i in range(env.num_states):
	for j in range(4):
		for prob, next_state, reward, done in env.P[i][j]:
			if (reward == 1000):
				print("state",i)

