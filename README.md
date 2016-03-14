#### Required 
* `Python >= 2.7.x`
* `Numpy >= 1.8.1`

#### How to use
There are two example files that show how to invoke the solver.
But if you would like to know what is needed then:

* Make a script in python that defines:
	* size of the board as an int.
	* a dictionary of relationships between cells.
		* Note that the cells are zero indexed. So positions are from `0` to `size-1` inclusive.
		* The keys must be tuples of size two
			* Each item in this tuple is another tuple of size two defining the location of the cell. Note that the cells must be adjacent, and the solver doesn't check for impossible input from the user.
				* View **Example 1**
		* The value must be a string defining if the first cell is `"__lt__"` or `"__gt__"` the second cell.
			* There are variables in the solver the makes this easier. There are:
				* Original Math Definition:
					* `LESS`
					* `GREATER`
				* Variables that are in the direction they are point twowards. (This was made to reduce errors when defining the cell to cell relationships.)
					* `UP`
					* `DOWN`
					* `LEFT`
					* `RIGHT`
				* View **Example 2**
	* an optional dictionary that defines if any of the cells have preset values.
		* The key is just a single cell
		* The value is value that the cell should have.
		* View **Example 3**

* Pass the defined variables into the `solve` functions.
	* `solve` requires the following parameters are required:
		* `size` as an `int`
		* `relationships` as a `dict`
	* `solve` has the following optional parameters:
		* `known_positions` as a `dict`
			* Defualt is `{}` (an empty `dict`).
		* `first_solution` as a `bool` if you want the search to end after the first solution is found.
			* If `false` then the program keeps going until it ends the serach.
			* Defualt is `true`
		* `prompt` as a `bool` if you want to be prompted to see the board before the search starts.
			* Regardless of setting, the board is printed out to `stdout` in a human readable format.
			* Useful if you just want to double check if you have entered in the data correctly.
			* If set to `false`, then the solver immidately justs seraching.
				* Useful when programming in several instances of the board.
			* Defualt is `true`

##### Notes
* The solver does some extra double checking for if an edit is valid.
	* This may slow the solver down.
		* Pass in the `-O` flag when running the program.
			* Ex: `python -O my_script.py`


##### Example 1
```python
cell_1 = (1,2);
cell_2 = (1,3);
key = (cell_1, cell_2)
```

##### Example 2
```python
from futoshiki_solver import solve,LESS,GREATER,UP,DOWN,LEFT,RIGHT
relationships = {}
relationships[(0,0),(0,1)]=LESS
relationships[(0,1),(0,2)]=GREATER
relationships[(1,5),(1,6)]=RIGHT
relationships[(3,3),(3,4)]=LEFT
relationships[(3,4),(4,4)]=UP
relationships[(4,4),(5,4)]=DOWN
```

##### Example 3
```python
known_positions = {}
known_positions[2,3]=3
```