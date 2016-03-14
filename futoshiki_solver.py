import numpy as np
import datetime

LESS = "__lt__"
GREATER = "__gt__"

RIGHT = GREATER
LEFT = LESS
UP = LESS
DOWN = GREATER


class TableTracker:

	def __init__(self,num_rows, num_cols,fill_values,relationships,known_positions):

		self.num_rows = num_rows
		self.num_cols = num_cols
		self.table = make_table(num_rows, num_cols)
		self.known_positions = known_positions
		self.relationships=relationships
		self.fill_values= fill_values
		self.row_tracker = [
			{ value:False for value in fill_values}
			for _ in range(num_rows)
		]

		self.col_tracker = [
			{ value:False for value in fill_values}
			for _ in range(num_cols)
		]

		self.stack = []

		# initalize start values
		for (ii,jj),value in known_positions.iteritems():
			self.table[ii,jj] = value
			self.row_tracker[ii][value]=True
			self.col_tracker[jj][value]=True


	def available_values(self,ii,jj):
		possible_values = { value:True for value in self.fill_values }
		for key,value in self.row_tracker[ii].iteritems():
			if value:
				possible_values[key]=False

		for key,value in self.col_tracker[jj].iteritems():
			if value:
				possible_values[key]=False

		return [ np.int64(key) for key,value in possible_values.iteritems() if value]



	def find_unedited_cells(self):
		cells = []
		for ii in range(self.num_rows):
			for jj in range(self.num_cols):
				if self.table[ii,jj] == 0:
					cells.append((ii,jj))

		return cells


	def is_edit_valid(self,ii,jj,value):

		if value == 0:
			return True

		if self.row_tracker[ii][value]:
			return False

		if self.col_tracker[jj][value]:
			return False

		# Four adjacent cells
		adjacent_cells = [
			(ii+1,jj+0),
			(ii-1,jj+0),
			(ii+0,jj+1),
			(ii+0,jj-1),
		]

		cur_cell = (ii,jj)

		for cell in adjacent_cells:
			cell_pair = (cur_cell,cell)

			if cell_pair in self.relationships:
				relation = self.relationships[cell_pair]
				cell_value = self.table[cell]

				if cell_value != 0 and not getattr(value, relation)(cell_value):
					return False

		return True



	def make_edit(self,ii,jj,new_value,add_to_stack=False):

		if __debug__:
			if not self.is_edit_valid(ii, jj, new_value):
				print ii,jj,new_value
				raise Exception("Edit is not valid:")

		cell = (ii,jj)

		old_value = self.table[cell]

		if old_value != 0:
			self.row_tracker[ii][old_value]=False
			self.col_tracker[jj][old_value]=False			

		if new_value != 0:
			self.row_tracker[ii][new_value]=True
			self.col_tracker[jj][new_value]=True

		self.table[cell] = new_value

		if add_to_stack:
			stack_node = (cell,old_value,new_value)
			self.stack.append(stack_node)


	def pop_stack(self):

		if len(self.stack) == 0:
			return None
		
		(ii,jj),old_value,cur_value = self.stack.pop()

		self.make_edit(ii, jj, old_value,add_to_stack=False)


	def push_stack(self,ii,jj,new_value):
		self.make_edit(ii, jj, new_value,add_to_stack=True)



	def __str__(self):
		table = self.table
		num_rows = self.num_rows
		num_cols = self.num_cols
		relationships = self.relationships

		max_num = max( max(row) for row in table )

		num_digits = len(str(max_num))
		num_digits = max(num_digits,2)

		digit_print = "{{0:{num_digits}d}}".format(num_digits=num_digits)

		relation_length = 3

		row_string_length = num_digits*num_cols + (num_cols-1)*relation_length

		table_text_list = []

		def calc_relation_string_helper(current_cell,adjacent_cell,options):
			cell_pair = (current_cell,adjacent_cell)

			if cell_pair not in relationships:
				return options[None]

			elif relationships[cell_pair] == LESS:
				return options[LESS]

			elif relationships[cell_pair] == GREATER:
				return options[GREATER]

			else:
				raise Exception("Relationship Not Regonized.")

		def calc_horizontal_relation_string(
			current_cell,
			adjacent_cell,
			options = {
				None:" "*relation_length,
				LESS:" < ",
				GREATER:" > ",
			}
		):
			return calc_relation_string_helper(current_cell,adjacent_cell,options)

		def calc_vertical_relation_string(
			current_cell,
			adjacent_cell,
			options = {
				None:"  ",
				LESS:"/\\",
				GREATER:"\/",
			}
		):
			return calc_relation_string_helper(current_cell,adjacent_cell,options)


		for row_index,row in enumerate(table):
			row_text_list = []

			# print row data
			for col_index,value in enumerate(row):
				row_text_list.append( digit_print.format(value) )

				if col_index + 1 < num_cols:

					current_cell = (row_index,col_index)				
					adjacent_cell = (row_index,col_index+1)

					relation_char = calc_horizontal_relation_string(current_cell,adjacent_cell)

					row_text_list.append(relation_char)


			row_text_string = "".join(row_text_list)

			assert len(row_text_string) == row_string_length

			table_text_list.append(row_text_string)

			# print column relationships
			if row_index+1 < num_rows:
				col_text_list = []

				for col_index in range(num_cols):

					current_cell = (row_index,col_index)				
					adjacent_cell = (row_index+1,col_index)

					relation_char = calc_vertical_relation_string(current_cell,adjacent_cell)

					col_text_list.append(relation_char)

					if col_index + 1 < num_cols:
						col_text_list.append(calc_horizontal_relation_string(None,None))

				inter_row_relation_string = "".join(col_text_list)

				assert len(inter_row_relation_string) == row_string_length

				table_text_list.append(inter_row_relation_string)

		return "\n".join(table_text_list)


	def validate(self,verbose=False):
		if verbose:
			print ""

		validation_list = []

		def validate_cell_group(cell_group):
			is_valid = all(cell_group.itervalues())
			validation_list.append(is_valid)
			missing = ""
			if verbose:
				if not is_valid:
					missing_set = [ key for key,value in cell_group.iteritems() if not value ]
					missing = "missing: "+str(missing_set)
			return is_valid,missing

		# Validate Rows
		for index,row in enumerate(self.row_tracker):
			is_valid,missing = validate_cell_group(row)
			if verbose:
				print "Row",index,is_valid,missing

		# Validate Cols
		for index,col in enumerate(self.col_tracker):
			is_valid,missing = validate_cell_group(col)
			if verbose:
				print "Col",index,is_valid,missing

		# Validate Relationships
		for (cell_1,cell_2),relation in self.relationships.iteritems():
			value_1 = self.table[cell_1]
			value_2 = self.table[cell_2]
			is_valid = getattr(value_1, relation)(value_2)
			validation_list.append(is_valid)
			if verbose:
				print "Relation",cell_1,cell_2,relation,is_valid

		if len(validation_list) > 0:
			did_pass = all(validation_list)
		else:
			did_pass = False

		if verbose:
			if did_pass:
				print "Passed all validiation tests."
			else:
				print "Failed at least one validation test."

		return did_pass






def solve(size,relationships,known_positions = {},first_solution = True,prompt=True):

	num_rows = size
	num_cols = size

	fill_values = [ ii for ii in range(1,size+1) ]

	relationships = make_symmetric(relationships)
	table_object = TableTracker(num_rows, num_cols,fill_values,relationships,known_positions)
	print "Starting Board"
	print table_object

	print ""
	if prompt:
		print "Please Check if the table is initalize properly."
		raw_input("Press \"ENTER\"/\"RETURN\" To Continue")

	start_time = datetime.datetime.now()

	print ""
	print "Calculating Solution"
	print "Stated:{now}".format(now=start_time) 
	print ""


	unedit_cells = table_object.find_unedited_cells()

	temp_dict = {"count":0}

	display_interval = 10**4

	def display_cur_time():
		cur_time = datetime.datetime.now()
		print "Current Time:{now}".format(now=cur_time)
		print "Duration:{length}".format(length=cur_time-start_time)

	def count_callback():
		temp_dict["count"] +=1
		count = temp_dict["count"]
		if count > 0 and count%display_interval == 0 :
			print count

	def solution_callback():
		print ""
		print table_object
		print ""
		print "Solution Found!"
		display_cur_time()
		if first_solution:
			print "Done"
			exit()
		else:
			print ""

	_solver_helper(table_object,0,unedit_cells,count_callback,solution_callback)

	print "Search Complete"
	display_cur_time()


def _solver_helper(table_object,index,unedit_cells,count_callback,solution_callback):
	
	cur_cell = unedit_cells[index]

	ii,jj = cur_cell

	available_values = table_object.available_values(ii,jj)

	for value in available_values:

		if table_object.is_edit_valid(ii,jj,value):

			table_object.push_stack(ii,jj,value)

			if index == len(unedit_cells)-1:
				count_callback()
				if table_object.validate():
					solution_callback()

			elif index+1 < len(unedit_cells):
				_solver_helper(table_object,index+1,unedit_cells,count_callback,solution_callback)

			table_object.pop_stack()



def make_symmetric(relationships):
	new_dict = {}

	for (cell_1,cell_2),relation in relationships.iteritems():
		
		if relation is None:
			continue

		opposite_relation = GREATER if relation==LESS else LESS

		new_dict[cell_1,cell_2] = relation
		new_dict[cell_2,cell_1] = opposite_relation

	return new_dict





def make_table(num_rows,num_cols):
	table = [  
		[
			0 for _ in range(num_cols)
		]
		for _ in range(num_rows)
	]

	return np.array(table)

