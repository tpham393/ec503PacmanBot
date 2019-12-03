from policyIteration_multGhosts import *

state = coord2state(1,2,[2,0],[1,2]);
print(state);
p_x, p_y, g_x, g_y = state2coord(state)
print(p_x, p_y);
print(g_x, g_y);