# Stranded Santa
## Mizzou Hackathon 2022

Santa is stranded! His sleigh is in the workshop and now he must deliver presents on foot. 
This program determines the shortest path between two given cities and animates the journey between them so Santa can deliver presents on time.

<img src=https://media.giphy.com/media/KgBosvIkQs7al4TVXx/giphy.gif width=50%>

## City/Route Plotting
Converts latitude and longitude coordinates of the [40 highest populated cities](https://en.wikipedia.org/wiki/List_of_largest_cities) to (x,y,z) coordinates using these conversion formulas (where $R = 6378.1km$, Earth's radius):
  - $x = R * cos(lat) * cos(long)$
  - $y = R * cos(lat) * sin(long)$
  - $z = R * sin(lat)$

Routes were drawn based on cities' general proximity to each other. Each city has roughly 3-5 connections to adjacent cities.

## Finding the Shortest Path
Using the network of routes we determined, we can construct a graph. The graph is implemented as a dictionary where the keys are the cities ("City, Country"), and the values are dictionaries containing adjacent cities and the distance to them {"City, Country" : 5}.

With the graph, we can determine the shortest path to other cities from the origin city using Djikstra's algorithm. The program begins at the origin city, moving onto the nearest of its neighboring cities, keeping track of the shortest paths found so far from the source city to other cities. The program continues to check every neighbor of every city, ultimately determining the shortest possible path of all paths from the origin city to the destination.
  - The graph is sparse, containing 40 vertices (cities) and 54 edges (routes). 
  - With our graph implementation, Djikstra's algorithm has a time complexity of $O(V^2)$.
    - Could be improved to $O(E * log(V))$ with the use of a min heap.

## Animating Path
By plotting cities and landmasses using the Earth's real latitude and longitude, we were able to use latitude and longitude values to rotate matplotlib's camera in order to keep cities centered on the plot. For instance, to center Tokyo whose $latitude = 139.69°$ and $longitude = 35.69°$, set matplotlib's camera azimuth rotation to 139.69° and elevation to 35.69°.

We decided to set the movement between each city to be 10 frames long, meaning the change in rotation from frame to frame can be found simply by dividing the distance between two cities by 10. By incrementing by this amount each frame, the simulated path remains centered on the camera while moving between the origin and destination.
