#!/usr/bin/python
from futoshiki_solver import solve,RIGHT,LEFT,UP,DOWN

size = 7

relationships = {
	# Left-Right Relationship
	# Zeroth Row
	((0,0),(0,1)):None,
	((0,1),(0,2)):None,
	((0,2),(0,3)):None,
	((0,3),(0,4)):None,
	((0,4),(0,5)):None,
	((0,5),(0,6)):None,

	# First Row
	((1,0),(1,1)):None,
	((1,1),(1,2)):None,
	((1,2),(1,3)):None,
	((1,3),(1,4)):None,
	((1,4),(1,5)):None,
	((1,5),(1,6)):RIGHT,

	# Second Row
	((2,0),(2,1)):LEFT,
	((2,1),(2,2)):None,
	((2,2),(2,3)):None,
	((2,3),(2,4)):RIGHT,
	((2,4),(2,5)):None,
	((2,5),(2,6)):RIGHT,

	# Third Row
	((3,0),(3,1)):None,
	((3,1),(3,2)):None,
	((3,2),(3,3)):None,
	((3,3),(3,4)):LEFT,
	((3,4),(3,5)):None,
	((3,5),(3,6)):None,

	# Fourth Row
	((4,0),(4,1)):LEFT,
	((4,1),(4,2)):None,
	((4,2),(4,3)):None,
	((4,3),(4,4)):RIGHT,
	((4,4),(4,5)):LEFT,
	((4,5),(4,6)):None,

	# Fifth Row
	((5,0),(5,1)):None,
	((5,1),(5,2)):None,
	((5,2),(5,3)):None,
	((5,3),(5,4)):None,
	((5,4),(5,5)):None,
	((5,5),(5,6)):None,

	# Sixth Row
	((6,0),(6,1)):None,
	((6,1),(6,2)):None,
	((6,2),(6,3)):RIGHT,
	((6,3),(6,4)):None,
	((6,4),(6,5)):LEFT,
	((6,5),(6,6)):None,

	# Up Down Relationship
	# Zeroth Column
	((0,0),(1,0)):None,
	((1,0),(2,0)):UP,
	((2,0),(3,0)):None,
	((3,0),(4,0)):None,
	((4,0),(5,0)):None,
	((5,0),(6,0)):None,

	# First Column
	((0,1),(1,1)):DOWN,
	((1,1),(2,1)):DOWN,
	((2,1),(3,1)):None,
	((3,1),(4,1)):None,
	((4,1),(5,1)):None,
	((5,1),(6,1)):UP,

	# Second Column
	((0,2),(1,2)):UP,
	((1,2),(2,2)):UP,
	((2,2),(3,2)):UP,
	((3,2),(4,2)):None,
	((4,2),(5,2)):None,
	((5,2),(6,2)):None,

	# Third Column
	((0,3),(1,3)):DOWN,
	((1,3),(2,3)):DOWN,
	((2,3),(3,3)):None,
	((3,3),(4,3)):None,
	((4,3),(5,3)):None,
	((5,3),(6,3)):UP,

	# Fourth Column
	((0,4),(1,4)):None,
	((1,4),(2,4)):None,
	((2,4),(3,4)):None,
	((3,4),(4,4)):UP,
	((4,4),(5,4)):DOWN,
	((5,4),(6,4)):None,

	# Fifth Column
	((0,5),(1,5)):None,
	((1,5),(2,5)):None,
	((2,5),(3,5)):None,
	((3,5),(4,5)):None,
	((4,5),(5,5)):None,
	((5,5),(6,5)):DOWN,

	# Sixth Column
	((0,6),(1,6)):None,
	((1,6),(2,6)):None,
	((2,6),(3,6)):DOWN,
	((3,6),(4,6)):None,
	((4,6),(5,6)):None,
	((5,6),(6,6)):None,
}

known_positions = {
	
}


solve(
	size=size,
	relationships=relationships,
	known_positions=known_positions,
	first_solution=True,
	prompt=True,
)
