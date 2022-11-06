# Stranded Santa

Santa is stranded! His sleigh is in the workshop and now he must deliver presents on foot. 
This program determines the shortest path between two given cities and animates the journey between them.

## City/Route Plotting
Converts latitude and longitude cooridinates of the [40 highest populated cities](https://en.wikipedia.org/wiki/List_of_largest_cities) to (x,y,z) coordinates using these conversion formulas:
  - $x = R * cos(lat) * cos(long)$
  - $y = R * cos(lat) * sin(long)$
  - $z = R * sin(lat)$

Routes were drawn based on cities' general proximity to each other. Each city has roughly 3-5 connections to adjacent cities.

##
