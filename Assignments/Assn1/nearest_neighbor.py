# -*- coding: utf-8 -*-
# Yash Kelkar
# 861168896
# CS 141 Assignment 1

import sys
from math import sqrt
import re
from operator import itemgetter

pointRE = re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")

def dist(p1, p2):
    return sqrt(pow((p1[0]-p2[0]),2) + pow((p1[1]-p2[1]),2))

#Run the divide-and-conquor nearest neighbor 
def nearest_neighbor(points):
    return nearest_neighbor_recursion(points)

#--------------------------------------------MY-CODE--------------------------------------------
#Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    min_distance = dist(points[0], points[1])

    for x in range(0, len(points)-1):           
        for y in range(x + 1, len(points)):
            distance = dist(points[x], points[y])
            if distance < min_distance:          # Update min_distance to smaller distance 
                min_distance = distance
    return min_distance

#Divide and conquer recurse part
def nearest_neighbor_recursion(points):
    min_distance = 0                             # Initialize min_distance
    distance = 0
    middle_points = []                           # segment of points in the middle
    points_size = len(points)                    # Size of array 
    x_sorted = sorted(points, key = itemgetter(0)) # Sort points by x values

    if points_size <= 3:                         # If size of array less than or equal to 3, relatively same run time as recursion
        return brute_force_nearest_neighbor(x_sorted)
    else:
        # Find a value x for which exactly half the points have xi < x, and half have xi > x. On
        # this basis, split the points into two groups L and R.
        half_points = points_size/2        
                                                 
        x_L = x_sorted[:half_points]             # left half of sorted x
        x_R = x_sorted[half_points:]             # right half of sorted x

        median = x_L[-1]                         # median point of 

        # Recursively find the closest pair in L and in R. Say these pairs are pL, qL ∈ L and pR, qR ∈ R,
        # with distances dist_L and dist_R respectively.
        dist_L = nearest_neighbor_recursion(x_L) 
        dist_R = nearest_neighbor_recursion(x_R) 

        if dist_R < dist_L:                      # Let distance be the smaller of dist_R and dist_L
            distance = dist_R
        else: 
            distance = dist_L

        y_sorted = sorted(points, key = itemgetter(1)) # Sort points by y values
        
        # Now, go through this sorted list, and for each point, compute its distance to the
        # subsequent points in the list. Let pM, qM be the closest pair found in this way.
        for value in y_sorted:
            if (value[0] - median[0]) < distance:
                middle_points.append(value)

        num_middle_points = len(middle_points)
        min_distance = distance

        # The answer is one of the three pairs {pL, qL}, {pR, qR}, {pM, qM}, whichever is closest.
        for x in range(num_middle_points - 1):
            for y in range(x + 1, min(x + 2, num_middle_points)):
                if dist(middle_points[x], middle_points[y]) < min_distance:
                    min_distance = dist(middle_points[x], middle_points[y])

    return min_distance
#--------------------------------------------MY-CODE--------------------------------------------
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
            x = float(point_match.group(1)) # Change to float to account for decimal values
            y = float(point_match.group(2)) # ^^same for x and y
            points.append((x, y))
    # print(points)
    return points
        
def main(filename, algorithm):
    algorithm = algorithm[1:]
    points = read_file(filename)
    output_name = filename[:-4]             # deletes the ".txt" substring of filename
    text_file = open(output_name + "_distance.txt", "w")    # creates a text file named after the input file (input_distance.txt)
    if algorithm == 'dc':
        print("Divide and Conquer: ", nearest_neighbor(points))
        text_file.write(str(nearest_neighbor(points)))      # writes the converted value from float to str to the created output file 
    if algorithm == 'bf':
        print("Brute Force: ", brute_force_nearest_neighbor(points))
        text_file.write(str(brute_force_nearest_neighbor(points)))  # writes the converted value from float to str to the created output file 
    if algorithm == 'both':
        print("Divide and Conquer: ", nearest_neighbor(points))
        text_file.write(str(nearest_neighbor(points)))      # writes the converted value from float to str to the created output file 
        print("Brute Force: ", brute_force_nearest_neighbor(points))
        text_file.write("\n" + str(brute_force_nearest_neighbor(points)))   # writes the converted value from float to str to the created output file with a newline above
    text_file.close()                                   # closes output file

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    main(sys.argv[2], sys.argv[1])
