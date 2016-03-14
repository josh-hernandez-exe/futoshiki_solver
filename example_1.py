#!/usr/bin/python
from futoshiki_solver import solve,LESS,GREATER

size = 6

relationships = {
	# Left-Right Relationship
	# Zeroth Row
	((0,0),(0,1)):LESS,
	((0,1),(0,2)):GREATER,
	((0,3),(0,4)):LESS,
	((0,4),(0,5)):LESS,

	# First Row
	((1,1),(1,2)):LESS,

	# Second Row
	((2,0),(2,1)):GREATER,

	# Third Row
	((3,0),(3,1)):GREATER,

	# Fourth Row
	((4,2),(4,3)):LESS,
	((4,3),(4,4)):GREATER,

	# Fifth Row
	## None

	# Up Down Relationship
	# Zeroth 
	## None

	# First Column
	## None 

	# Second Column
	((1,2),(2,2)):LESS,

	# Third Column
	## None

	# Fourth Column
	((0,4),(1,4)):GREATER,
	((4,4),(5,4)):GREATER,

	# Fifth Column
	((0,5),(1,5)):LESS,
	((1,5),(2,5)):GREATER,
	((2,5),(3,5)):GREATER,
	((3,5),(4,5)):GREATER,
	((4,5),(5,5)):GREATER,
}

known_positions = {
	
	(2,3):3,
	(4,3):5,

}

solve(
	size=size,
	relationships=relationships,
	known_positions=known_positions,
	first_solution=False,
	prompt=False,
)