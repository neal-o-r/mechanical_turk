# Mechanical Turk

A chess playing bot. Currently can play in a few ways, in increasing order of ability:
 
	* Randomly 
	* Evaluate one move ahead
	* Evaluate n moves ahead with iteratively deepened minimax.
	* Evaluate n moves ahead with iteratively deepened alpha-beta pruned minimax.

Adding transposition tables and using MTD-f would probably improve things, but as it stands given 2 seconds thought per move it's about as good as I am and it's starting to freak me out.
