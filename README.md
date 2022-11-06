# Stranded Santa

Santa is stranded! His sleigh is in the workshop and now he must deliver presents on foot. 
This program determines the shortest path between two given cities and animates the journey between them.

## City/Route Plotting
Converts latitude and longitude cooridinates of the [40 highest populated cities](https://en.wikipedia.org/wiki/List_of_largest_cities) to (x,y,z) coordinates using these conversion formulas:
  - $x = R * cos(lat) * cos(long)$
  - $y = R * cos(lat) * sin(long)$
  - $z = R * sin(lat)$

Routes were drawn based on cities' general proximity to each other. Each city has roughly 3-5 connections to adjacent cities.

## Finding the Shortest Path
Using the network of routes we determined, we can construct a graph. The graph is implemented as a dictionary where the keys are the cities ("City, Country"), and the values are dictionaries containing adjacent cities and the distance to them ("City, Country" : 5).

With the graph, we can determine the shortest path to other cities from the origin city using Djikstra's algorithm. The program begins at the origin city, moving onto the nearest of its neighboring cities, keeping track of the shortest paths found so far from the source city to other nodes. The program continues to check every neighbor of every node, ultimately determining the shortest possible path of all paths from the origin city to the destination.

## Animating Path

