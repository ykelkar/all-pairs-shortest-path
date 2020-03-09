import re
import sys
import time
from math import sqrt
from operator import itemgetter

pointRE = re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")

def dist(p1, p2):
    return (((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2))**(.5) # rewrite of distance formula
#----------------------------------------------------------------------

# Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    min_distance = 0
    if len(points) < 2:
        return min_distance

    # initial distance of p1 and p2 
    min_distance = dist(points[0],points[1]) 
    
    # nested loops
    # point p, where p[0] = x, p[1] = y
    # i = p1, j = p2
    for i in range(0, len(points)-1):
        for j in range(i+1, len(points)):
            cur_dist = dist(points[i], points[j])
            if cur_dist < min_distance:
                min_distance = cur_dist
    return min_distance
#----------------------------------------------------------------------

# Run the divide-and-conquor nearest neighbor 
def nearest_neighbor(points):
    points = sorted(points, key=itemgetter(0)) # points sorted by x
    return nearest_neighbor_recursion(points)
#----------------------------------------------------------------------

# Divide and conquer recurse part
def nearest_neighbor_recursion(points):
    min_distance = 0
    num_p = len(points)

    if num_p <= 3:
        return brute_force_nearest_neighbor(points)
    else:
        half = int(num_p/2)      # half way
        xpl = points[:half]      # x points left half
        xpr = points[half:]      # x points right half

        med = xpl[-1]            # median point

        dist_l = nearest_neighbor_recursion(xpl)    # distance right half
        dist_r = nearest_neighbor_recursion(xpr)    # distance left half
        min_distance = min(dist_l, dist_r)

        stp = [] # strip for points in the middle
        y_pnt = sorted(points, key=itemgetter(1)) # points sorted by y

        # fill strip with points
        for pnt in y_pnt:
            if abs(pnt[0] - med[0]) < min_distance:
                stp.append(pnt)

        num_stp = len(stp)

        # look in the strip for a smaller distance
        if num_stp > 1:
            for i in range(num_stp-1):
                for j in range(i+1, min(i+8, num_stp)):
                    if dist(stp[i],stp[j]) < min_distance:
                        min_distance = dist(stp[i],stp[j])

    return min_distance
#----------------------------------------------------------------------

def read_file(filename):
    points = []
    # File format
    # x1 y1
    # x2 y2
    # ...
    in_file = open(filename,'r')
    for line in in_file.readlines():
        line = line.strip()
        point_match = pointRE.match(line)
        if point_match:
            x = float(point_match.group(1)) # cast float
            y = float(point_match.group(2)) # cast float
            points.append((x,y))
    # print(points)
    return points
#----------------------------------------------------------------------

def main(filename,algorithm):
    algorithm = algorithm[1:]
    print(algorithm)
    points = read_file(filename)
    out_file = open( (filename[:-4] + "_distance.txt"), "a+")

    if algorithm == 'dc':
        dc = nearest_neighbor(points)
        out_file.write(str(dc))
        print("Divide and Conquer: ", dc)

    if algorithm == 'bf':
        bf = brute_force_nearest_neighbor(points)
        out_file.write(str(bf))
        print("Brute Force: ", bf)

    if algorithm == 'both':
        deec = nearest_neighbor(points)
        beef = brute_force_nearest_neighbor(points)
        out_file.write(str(deec) + "\n" + str(beef) )
        print("Divide and Conquer: ", deec)
        print("Brute Force: ", beef)

    if algorithm == 'time': # extra timing testing flag
        out_file.write(filename + "\n")
        start = time.clock()
        out_file.write("Divide and Conquer: " + str(nearest_neighbor(points)) + "\n")
        fin = time.clock()
        out_file.write("Time: " + str(fin-start) + " sec"+ "\n")
        out_file.write("\n")
        start = time.clock()
        out_file.write("Brute Force: " + str(brute_force_nearest_neighbor(points)) + "\n")
        fin = time.clock()
        out_file.write("Time: " + str(fin-start) + " sec" + "\n")
        
    out_file.close()
#----------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python nearest_neighbor.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python nearest_neighbor.py -<dc|bf|both> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
