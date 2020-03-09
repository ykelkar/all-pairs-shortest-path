Run the program with the following command format:

	python nearest_neighbor.py -<dc|bf|both> <input_file>

The first argument decalres that the file runs in python.

The second argument chooses the python file to run.

The third argument selects which algorithm to use:
	-bf --> brute_force_nearest_neighbor
	-dc --> nearest_neighbor recursion (divide-and-conquer)
	-both --> runs both the brute_force_nearest_neighbor and the nearest_neighbor recursion

The fourth argument selects the input file from which the data points are read from.