import sys
import re
import time

graphRE = re.compile("(\\d+)\\s(\\d+)")
edgeRE = re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices = []
edges = []

# This will print the results in organized columns
def print_formal(value):
    x = 0
    g = len(vertices)
    for y in value:
    	print(y)
    	if x == g - 1:
    		print('')
    		x = 0
    		continue # this is stylistic so it prints 4 values at a time
    	x += 1

#---------------------------------------------------------------------------------------------------------------------
def BellmanFord(G):
    pathPairs = []
    # Fill in your Bellman-Ford algorithm here
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    tmp_vertices = []  
    g = len(vertices)
   
    for i in range(g):
        for j in range(g):
            tmp_vertices = Bellman_Ford_calc(G,i)
            #pathPairs.append( ( (i,j) , float(edges[i][j]) ) ) #to print with vertex pairs and weight
            pathPairs.append(float(edges[i][j]))

    print_formal(pathPairs)
    #print(pathPairs) #this 

    return pathPairs

#---------------------------------------------------------------------------------------------------------------------
#Algorithm Bellman-Ford (G(V,E),s)
#for each u in V
#	d[u] <- inf
#d[s] <- 0
#for i <- 1 to |V| - 1do
#	for each (u,v) in E do 
#		if d[v] > d[u] + w(u,v) then 
#		d[v] <- d[u] + w (u,v)
#for each (u,v) in E do 
#	if d[v] > d[u] + w(u,v) then 
#		return FALSE
#return d[], TRUE
#---------------------------------------------------------------------------------------------------------------------

def Bellman_Ford_calc(G,s):

    d = []
    g = len(vertices)

    # This for loop initializes the graph
    for i in range(g):
        d.append(float('inf'))
   
    d[s] = 0  

    # This for loop relaxes edges repeatedly
    for j in range(g):
        for u in range(g):
            for v in range(g):
                if (float(d[u]) + float(edges[u][v])) < float(d[v]):
                    d[v] = float(d[u]) + float(edges[u][v])

   # This for loop checks for negative-weight cycles
    for u in range(g):
        for v in range(g):
            if float(d[u]) + float(edges[u][v]) < float(d[v]):
            	print("Error: There exists a negative cycle")
                return false

    return d

#---------------------------------------------------------------------------------------------------------------------
#Algorithm AllPairs(G):
#	Input: A weighted directed graph G with n vertices numbered v1, v2, ..., vn
#	Output: A matrix D such that D[i,j] is distance from vi to vj in G
#	for i <- 1 to n do
#		for j <- 1 to n do
#			if i = j then 
#				Set D^0[i,i] <- 0 and continue looping 
#			if (vi,vj) is an edge in G then
#				Set D^0[i,j] <- w((vi,vj))
#			else 
#				Set D^0[i,j] <- w((vi,vj))
#	for i <- 1 to n do
#		for j <- 1 to n do 
#			for k <- 1 to n do 
#				Set D^k[i,j] <- min{D^(k-1) [i,j], D^(k-1)[i,k] + D^(k-1) [k,j]}
#	Return D^n
#---------------------------------------------------------------------------------------------------------------------

def FloydWarshall(G):

    pathPairs = []
    g = len(vertices)
    
    # set vertex to self = 0
    for i in range(g):
        edges[i][i] = 0

    for k in range(g):
        for i in range(g):
            for j in range(g):
                if float(edges[i][k]) == float('inf') or float(edges[k][j]) == float('inf'):
                    continue
                if float(edges[i][j]) > float(edges[i][k]) + float(edges[k][j]):
                    edges[i][j] = float(edges[i][k]) + float(edges[k][j])

    for i in range(g):
        for j in range(g):
            #pathPairs.append( ( (i,j) , float(edges[i][j]) ) ) #to print with vertex pairs and weight
            pathPairs.append(float(edges[i][j]))

    print_formal(pathPairs)
    #print(pathPairs) #to print regularly unorganize in one line

    return pathPairs

#---------------------------------------------------------------------------------------------------------------------

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile = open(filename,'r')
    line1 = inFile.readline()
    graphMatch = graphRE.match(line1)
    if not graphMatch:
        print(line1 + " not properly formatted")
        quit(1)
    vertices = list(range(int(graphMatch.group(1))))
    edges = []
    for i in range(len(vertices)):
        row = []
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch = edgeRE.match(line)
        if edgeMatch:
            source = edgeMatch.group(1)
            sink = edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between " + source + " and " + sink + " in a graph with " + vertices + " vertices")
                quit(1)
            weight = edgeMatch.group(3)
            edges[int(source)][int(sink)] = weight
    #Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)
#---------------------------------------------------------------------------------------------------------------------

def main(filename,algorithm):
    algorithm = algorithm[1:]
    G = readFile(filename)
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    output_name = filename[:-4]             # deletes the ".txt" substring of filename
    text_file = open(output_name + "_result.txt", "w")    # creates a text file named after the input file (input1.txt)
    if algorithm == 'b' or algorithm == 'B':
        #BellmanFord(G)
        text_file.write(str(BellmanFord(G)))      # writes the converted value from float to str to the created output file
    if algorithm == 'f' or algorithm == 'F':
        #FloydWarshall(G)
        text_file.write(str(FloydWarshall(G)))      # writes the converted value from float to str to the created output file
    if algorithm == "both":
        start = time.clock()
        #BellmanFord(G)
        text_file.write(str(BellmanFord(G)))
        end = time.clock()
        BFTime = end - start
        start = time.clock()
        #FloydWarshall(G)
        text_file.write("\n" + str(FloydWarshall(G)))
        end = time.clock()
        FWTime = end - start
        print("Bellman-Ford timing: " + str(BFTime))
        print("Floyd-Warshall timing: " + str(FWTime))
        text_file.write("\n" + "Bellman-Ford timing: " + str(BFTime))
        text_file.write("\n" + "Floyd-Warshall timing: " + str(FWTime))
#---------------------------------------------------------------------------------------------------------------------
        
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python bellman_ford.py -<f|b> <input_file>") # remember to rename the file later
        quit(1)
    main(sys.argv[2],sys.argv[1])
#-------------------------------------------------------------------------------------------------
