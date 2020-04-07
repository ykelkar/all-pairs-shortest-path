# All Pairs Shortest Path
Finds the shortest path using these algorithms:
1. Bellman-Ford (shortest path from single source vertex to every other vertex)
2. Floyd-Warshall algorithms (shortest path distance between each pair of vertices in G)

## Usage
Run the program with the following command format:

	python bellman_ford.py -<f|b|both> <input_file>

The first argument decalres that the file runs in python.

The second argument chooses the python file to run.

The third argument selects which algorithm to use:

	-f--> Floyd Warshall
	
	-b --> Bellman Ford
	
	-both --> runs both the Bellman Ford and the Floyd Warshall recursion

The fourth argument selects the input file from which the vertices are read from.
