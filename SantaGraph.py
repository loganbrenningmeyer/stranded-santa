import matplotlib.pyplot as plt
from matplotlib import animation

import sys, math

#Initialize matplotlib plot
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
ax.set_box_aspect([6378.1, 6378.1, 6378.1])
#Hide grids and axis panes
ax.grid(True)
ax.set_axis_off() 

"""
Creates a graph represented as a dictionary
The keys of the graph are each of the cities, and the items
are separate dictionaries which hold adjacent_city/distance pairs
to keep track of neighboring nodes and their edges
"""
class Graph(object):
        def __init__(self, nodes, cityRoutes):
                self.nodes = nodes
                self.graph = self.buildGraph(nodes, cityRoutes)
                
        def buildGraph(self, nodes, cityRoutes):
                #Declares the graph as an empty dictionary
                graph = {}
                #For each city, set its key in the graph dictionary
                #as an empty dictionary to store distances/connections to adjacent cities
                for node in nodes:
                        graph[node] = {}
                        
                graph.update(cityRoutes)
                
                #Ensures that the graph is undirected, meaning edges travel from A to B and B to A
                for node, edges in graph.items():
                        #For each neighboring node, if the neighbor doesn't already
                        #have the source node as a neighbor, set it along with the distance
                        for neighbor, distance in edges.items():
                                if graph[neighbor].get(node, False) == False:
                                        graph[neighbor][node] = distance
                                        
                return graph
        
        #Returns the list of every city in the graph
        def get_nodes(self):
                return self.nodes
        
        #Returns a list of nodes neighboring the provided node
        def getNeighbors(self, node):
                #Empty array to store neighboring nodes
                neighbors = []
                #For each node in the graph, if the node exists as a neighbor 
                #to the provided node (the neighbor is a key in the node's item dictionary)
                #then append the neighboring node to the neighbors list
                for neighbor in self.nodes:
                        if self.graph[node].get(neighbor, False) != False:
                                neighbors.append(neighbor)
                return neighbors
        
        #Returns the distance stored in the graph between two city nodes
        def value(self, cityA, cityB):
                return self.graph[cityA][cityB]


def printPath(prevNodeInPath, shortestDistance, source, destination):
        path = []
        node = destination
        
        #Because prevNodeInPath is sorted in reverse, append from
        #the array until you reach the source node
        while node != source:
                path.append(node)
                node = prevNodeInPath[node]
        
        path.append(source)

        #Puts the path in the proper order because prevNodeInPath was backward
        path.reverse()
        
        print(f"\nHo ho ho! The best path from {source} to {destination} is {shortestDistance[destination]:.2f}km!\n")
        print(" -> ".join(path))

        return path

def dijkstra_algorithm(graph, source):
        #Creates a list of all unvisited nodes in the graph
        nodes = list(graph.get_nodes())
        
        #Dictionary to store the shortest total distance to
        #every node from the source node 
        shortestDistance = {}
        
        #Dictionary to store the shortest path taken to 
        #every node from the source node as key/value pairs node/prevNode
        prevNodeInPath = {}
        
        #Unvisited nodes initially have a shortestDistance of infinity to signify that they
        #haven't been explored. To express that, use sys.maxsize as the largest possible value  
        for node in nodes:
                shortestDistance[node] = sys.maxsize
        #Initialize the source node's value to 0 (its distance from itself is 0)
        shortestDistance[source] = 0
        
        #While nodes exist in the nodes list to be visited, keep running
        while nodes:
                #Finds the node with the current lowest shortestDistance from the source
                #Begins with the source node, but with each iteration the current minimum is removed and 
                #thus marked as fully explored
                minNode = None
                for node in nodes:
                        #Sets initial minimum
                        if minNode == None:
                                minNode = node
                        #Updates minimum if current node in loop has a lower shortestDistance
                        elif shortestDistance[node] < shortestDistance[minNode]:
                                minNode = node
                        
                #Once the minNode is found, obtain a list of its adjacent nodes (neighboring
                #cities connected by roads)
                neighbors = graph.getNeighbors(minNode)
                #For each neighbor, determine the new shortestDistance (newDistance) if the neighbor were
                #added to the chain. If newDistance is less than the current shortestDistance to the neighbor 
                #(keep in mind all shortestDistance are set initialized to sys.maxsize) then update the new shortestDistance to newDistance
                for neighbor in neighbors:
                        #Current distance + the distance between the current node and the neighboring node
                        newDistance = shortestDistance[minNode] + graph.value(minNode, neighbor)
                        if newDistance < shortestDistance[neighbor]:
                                shortestDistance[neighbor] = newDistance
                                #As the path to the neighbor is shorter, update
                                #the path in prevNodeInPath
                                prevNodeInPath[neighbor] = minNode
        
                #Remove the current minNode after it has been fully explored
                nodes.remove(minNode)
        
        return prevNodeInPath, shortestDistance

#Returns the distance between two cities given their (x, y, z) coordinates
def distance(cityA, cityB):
        return math.sqrt((cityB[0] - cityA[0])**2 + 
                         (cityB[1] - cityA[1])**2 + 
                         (cityB[2] - cityA[2])**2)

#Dictionary that holds the decimal format longitude and latitude of cities
longLat={"Tokyo, Japan": [35.689722, 139.692222],
        "Delhi, India": [28.61, 77.23],
        "Shanghai, China": [31.228611, 121.474722],
        "São Paulo, Brazil": [-23.55, -46.633333],
        "Mexico City, Mexico": [19.433333, -99.133333],
        "Cairo, Egypt": [30.044444, 31.235833],
        "Mumbai, India": [19.076111, 72.8775],
        "Beijing, China": [39.906667, 116.3975],
        "Dhaka, Bangladesh": [23.763889, 90.388889],
        "Osaka, Japan": [34.693889, 135.502222],
        "New York, USA": [40.712778, -74.006111],
        "Karachi, Pakistan": [24.86, 67.01],
        "Buenos Aires, Argentina": [-34.603333, -58.381667],
        "Chongqing, China": [29.5637, 106.5504],
        "Istanbul, Turkey": [41.013611, 28.955],
        "Kolkata, India": [22.5675, 88.37],
        "Manila, Philippines": [14.5958, 120.9772],
        "Lagos, Nigeria": [6.455027, 3.384082],
        "Rio de Janeiro, Brazil": [-22.911366, -43.205916],
        "Tianjin, China": [39.1336, 117.2054],
        "Kinshasa, DR Congo": [-4.325, 15.322222],
        "Guangzhou, China": [23.13, 113.26],
        "Los Angeles, USA": [34.05, -118.25],
        "Moscow, Russia": [55.755833, 37.617222],
        "Shenzhen, China": [22.5415, 114.0596],
        "Lahore, Pakistan": [31.549722, 74.343611],
        "Bangalore, India": [12.978889, 77.591667],
        "Paris, France": [48.856613, 2.352222],
        "Bogotá, Colombia": [4.711111, -74.072222],
        "Jakarta, Indonesia": [-6.175, 106.8275],
        "Chennai, India": [13.082694, 80.270694],
        "Lima, Peru": [-12.06, -77.0375],
        "Bangkok, Thailand": [13.7525, 100.494167],
        "Seoul, South Korea": [37.56, 126.99],
        "Nagoya, Japan": [35.183333, 136.9],
        "Hyderabad, India": [17.361667, 78.474722],
        "London, United Kingdom": [51.507222, -0.1275],
        "Tehran, Iran": [35.689167, 51.388889],
        "Chicago, USA": [41.881944, -87.627778],
        "Chengdu, China": [30.66, 104.063333]}

#Coordinates of cities converted from longitude and latitude
#to (x, y, z) coordinates in the same order as the dictionary
cityCoords=[[-3950.33, 3351.05, 3720.95],
            [1237.67, 5460.83, 3054.12],
            [-2847.63, 4651.51, 3306.75],
            [4014.85, -4250.53, -2548.36],
            [-954.73, -5938.48, 2122.06],
            [4720.78, 2863.04, 3193.33],
            [1774.69, 5760.68, 2084.51],
            [-2175.22, 4382.44, 4091.80],
            [-39.62, 5837.19, 2570.17],
            [-3740.50, 3675.50, 3630.36],
            [1332.08, -4647.39, 4160.23],
            [2260.27, 5327.44, 2681.37],
            [2752.27, -4470.55, -3622.07],
            [-1580.31, 5317.88, 3146.90],
            [4211.04, 2329.90, 4185.55],
            [167.53, 5887.33, 2447.73],
            [-3176.84, 5291.93, 1607.27],
            [6326.61, 374.11, 717.05],
            [4282.22, -4022.10, -2483.04],
            [-2261.83, 4400.04, 4025.41],
            [6133.87, 1680.59, -481.00],
            [-2316.27, 5388.68, 2505.44],
            [-2501.29, -4655.13, 3571.20],
            [2842.94, 2190.72, 5272.44],
            [-2401.61, 5379.04, 2445.06],
            [1466.82, 5233.67, 3337.27],
            [1335.50, 6069.98, 1432.47],
            [4192.91, 172.23, 4803.13],
            [1744.40, -6112.51, 523.84],
            [-1835.69, 6069.57, -686.06],
            [1049.88, 6123.20, 1443.73],
            [1399.12, -6078.39, -1332.61],
            [-1128.37, 6091.63, 1516.25],
            [-3042.08, 4038.45, 3888.04],
            [-3806.26, 3561.84, 3675.03],
            [1216.29, 5964.77, 1903.24],
            [3969.82, -8.83, 4992.05],
            [3232.64, 4047.85, 3720.90],
            [196.55, -4744.57, 4258.01],
            [-1333.18, 5322.05, 3252.46]]

#Landmass outline coordinates
#North and South America
northSouth=[[-2048.68, -654.64, 6004.54],
            [-2574.48, -561.82, 5808.32],
            [-3544.07, -979.43, 5211.57],
            [-2492.93, -1967.38, 5531.26],
            [-2417.92, -3473.76, 4771.46],
            [-2746.81, -4026.84, 4113.36],
            [-2538.55, -4642.11, 3561.84],
            [-2013.39, -5527.04, 2465.40],
            [-682.86, -6105.36, 1714.19],
            [1353.29, -6187.10, 754.04],
            [958.53, -6286.63, -489.61],
            [1277.08, -6086.33, -1416.26],
            [2020.42, -5692.61, -2047.50],
            [1021.55, -3945.26, -4906.27],
            [1391.20, -3357.69, -5241.25],
            [1542.55, -3337.87, -5211.46],
            [1447.66, -3784.10, -4925.96],
            [2064.92, -4221.56, -4312.16],
            [2757.77, -4257.40, -3866.45],
            [4200.26, -3875.55, -2831.62],
            [5189.58, -3636.70, -723.06],
            [4907.45, -4067.40, -230.96],
            [4077.00, -4903.23, 128.83],
            [3780.22, -5099.50, 620.71],
            [2836.46, -5593.12, 1162.62],
            [1957.62, -5920.12, 1341.68],
            [1412.66, -6143.92, 967.88],
            [1141.69, -6181.35, 1080.59],
            [918.59, -6231.29, 1003.69],
            [686.27, -6208.96, 1287.64],
            [687.53, -6096.76, 1742.69],
            [172.83, -6120.21, 1786.99],
            [310.17, -5924.25, 2342.47],
            [-453.11, -6020.96, 2054.98],
            [-809.35, -5856.86, 2392.13],
            [-564.53, -5559.34, 3074.93],
            [582.30, -5499.78, 3177.02],
            [860.40, -5696.97, 2735.77],
            [940.47, -5694.53, 2714.41],
            [838.10, -5340.97, 3384.04],
            [1285.56, -5012.53, 3728.55],
            [1366.70, -4623.98, 4175.05],
            [2528.52, -3397.07, 4769.34],
            [1372.16, -2859.39, 5533.64],
            [769.23, -2877.75, 5639.77],
            [647.20, -2975.27, 5604.38],
            [732.25, -3458.21, 5308.93],
            [373.99, -3597.36, 5253.50],
            [-180.89, -3345.74, 5427.11],
            [-236.13, -3095.44, 5571.59],
            [352.90, -2463.22, 5872.66],
            [325.44, -2227.66, 5967.56],
            [490.37, -2167.57, 5978.41],
            [734.19, -2351.17, 5883.29],
            [620.62, -2577.22, 5801.11],
            [628.00, -2672.74, 5756.93],
            [1174.28, -2698.06, 5658.77],
            [1227.40, -2564.11, 5709.55],
            [1178.40, -2212.95, 5864.67],
            [393.38, -1762.51, 6117.10],
            [779.58, -1325.25, 6190.00],
            [1652.34, -2146.74, 5774.20],
            [2332.66, -2178.15, 5522.18],
            [1993.12, -1258.68, 5926.50],
            [2000.56, -795.35, 6003.78],
            [933.62, -203.64, 6306.11],
            [587.73, -386.28, 6339.20],
            [462.07, -728.78, 6319.46],
            [201.85, -726.21, 6333.41],
            [-702.38, -1210.08, 6222.74],
            [-1558.06, -1671.89, 5954.61],
            [-2048.68, -654.64, 6004.54]]
#Europe, Asia, and Africa
eurasiaAfrica =[[1902.63, 817.55, 6032.56],
                [2852.66, 340.95, 5694.40],
                [3083.17, 276.68, 5576.53],
                [3700.62, 587.09, 5161.48],
                [3818.51, 357.79, 5096.19],
                [4049.18, 203.55, 4923.70],
                [4222.56, -202.65, 4775.88],
                [4394.31, -115.84, 4621.34],
                [4632.08, -122.11, 4382.82],
                [4572.28, -736.05, 4385.50],
                [5024.29, -804.51, 3845.71],
                [5123.67, -537.50, 3760.22],
                [5255.28, -628.29, 3559.13],
                [5309.12, -869.83, 3425.89],
                [5438.12, -921.29, 3202.84],
                [5661.80, -1733.58, 2370.41],
                [5894.68, -1816.56, 1622.66],
                [6304.10, -840.56, 481.64],
                [6282.77, 997.90, 459.52],
                [6295.10, 1010.11, -177.76],
                [6053.14, 1487.01, -1352.19],
                [5936.11, 1235.22, -1979.12],
                [4926.86, 1774.49, -3641.08],
                [4744.06, 2431.00, -3502.04],
                [4744.63, 3367.67, -2612.94],
                [4921.23, 3422.98, -2178.26],
                [4664.32, 4004.03, -1700.61],
                [4930.28, 3999.83, -611.46],
                [4218.22, 4747.46, 590.30],
                [3911.12, 4864.25, 1312.40],
                [4488.19, 4381.17, 1158.31],
                [4521.41, 4268.34, 1420.68],
                [4738.99, 3913.93, 1703.89],
                [4791.46, 3669.68, 2062.88],
                [4733.37, 3542.12, 2393.47],
                [4711.33, 3122.78, 2954.96],
                [4605.78, 3225.45, 3010.55],
                [4596.00, 3790.77, 2277.50],
                [4490.15, 4139.63, 1839.08],
                [4521.41, 4268.34, 1420.68],
                [3642.95, 4921.90, 1784.38],
                [2977.89, 5093.41, 2422.71],
                [2254.46, 5312.78, 2715.13],
                [1399.28, 6159.30, 886.11],
                [930.70, 6270.36, 704.70],
                [1021.19, 6053.43, 1730.11],
                [-126.32, 5888.43, 2447.56],
                [-490.00, 6112.37, 1754.71],
                [-764.56, 6063.01, 1826.35],
                [-900.15, 6244.08, 938.80],
                [-1265.71, 6243.44, 312.44],
                [-1562.55, 6181.50, 166.17],
                [-1458.59, 6184.21, 555.20],
                [-1273.23, 6204.72, 748.69],
                [-1064.56, 6202.82, 1035.30],
                [-1103.17, 6131.53, 1366.58],
                [-1276.21, 6089.68, 1402.57],
                [-1610.78, 6074.99, 1086.31],
                [-1616.35, 6095.99, 952.07],
                [-1792.89, 6026.85, 1069.04],
                [-2054.07, 5897.94, 1294.32],
                [-2009.52, 5828.80, 1633.12],
                [-1622.65, 5804.73, 2086.21],
                [-1884.52, 5620.95, 2352.36],
                [-2125.17, 5544.20, 2329.30],
                [-2620.73, 5256.03, 2487.19],
                [-2842.19, 4991.44, 2772.66],
                [-2946.89, 4666.95, 3196.18],
                [-2825.38, 4593.49, 3405.46],
                [-2652.54, 4553.19, 3593.41],
                [-2548.08, 4563.21, 3655.75],
                [-2612.24, 4407.86, 3798.31],
                [-2739.11, 4298.48, 3834.12],
                [-2729.52, 4260.79, 3882.72],
                [-2880.97, 4100.10, 3945.80],
                [-3131.24, 4230.83, 3602.16],
                [-3318.57, 3961.33, 3738.33],
                [-3016.43, 3872.52, 4072.46],
                [-3181.46, 3442.27, 4325.42],
                [-3236.14, 2716.72, 4777.76],
                [-2973.78, 2396.81, 5108.04],
                [-2605.65, 2563.73, 5226.66],
                [-2587.23, 1951.81, 5493.35],
                [-2948.90, 1389.67, 5482.06],
                [-2792.64, 1144.35, 5618.88],
                [-3011.08, 1002.93, 5532.42],
                [-3203.57, 1433.32, 5325.68],
                [-3687.85, 1586.73, 4956.03],
                [-3505.26, 1129.33, 5207.49],
                [-3259.20, 982.37, 5393.77],
                [-3100.62, 760.47, 5521.59],
                [-3100.76, 510.88, 5550.18],
                [-2933.19, 134.86, 5662.01],
                [-2926.39, 17.03, 5667.11],
                [-2740.85, 78.22, 5758.63],
                [-2630.55, -105.31, 5809.41],
                [-2737.42, -347.90, 5750.28],
                [-2534.08, -460.23, 5834.96],
                [-2189.25, 153.10, 5988.65],
                [-2061.64, 752.25, 5988.65],
                [-1936.22, 726.02, 6033.58],
                [-1787.79, 980.68, 6043.36],
                [-1609.88, 1040.32, 6083.27],
                [-1458.46, 1182.28, 6095.51],
                [-1431.00, 1417.86, 6051.62],
                [-1258.99, 1536.44, 6060.90],
                [-735.19, 1623.73, 6123.98],
                [-549.73, 1344.99, 6210.39],
                [77.21, 1603.53, 6172.75],
                [648.65, 1732.53, 6103.91],
                [1763.79, 1535.63, 5933.89],
                [1902.63, 817.55, 6032.56]]

mediterranean =[[4151.71, 3001.73, 3799.09],
                [4204.90, 2878.98, 3835.42],
                [4322.78, 2799.69, 3762.38],
                [4516.05, 2374.16, 3827.38],
                [4336.64, 2145.11, 4155.98],
                [4470.30, 1906.63, 4130.54],
                [4582.42, 2035.07, 3942.09],
                [4721.25, 1926.21, 3831.40],
                [4570.68, 1642.42, 4134.19],
                [4461.17, 1578.28, 4276.35],
                [4322.51, 1168.93, 4541.99],
                [4330.73, 1034.72, 4566.65],
                [4417.88, 963.86, 4498.16],
                [4561.11, 1175.72, 4300.48],
                [4603.93, 1517.25, 4145.11],
                [4643.56, 1545.55, 4090.09],
                [4638.90, 1427.99, 4137.83],
                [4698.90, 1400.93, 4078.96],
                [4727.63, 1465.52, 4022.67],
                [4840.57, 1375.85, 3918.69],
                [4929.40, 1327.84, 3823.35],
                [4922.53, 1130.04, 3895.11],
                [4886.51, 1136.99, 3938.20],
                [4812.96, 1327.06, 3969.19],
                [4723.74, 1337.62, 4071.51],
                [4678.25, 1006.18, 4216.84],
                [4533.74, 780.27, 4417.75],
                [4512.70, 694.42, 4453.47],
                [4850.55, 23.15, 4141.47],
                [4995.57, -25.42, 3965.33],
                [5098.48, -191.94, 3827.38],
                [5094.40, -449.06, 3811.24],
                [5131.48, -534.04, 3750.05],
                [5187.22, -416.03, 3687.79],
                [5103.11, 286.32, 3815.29],
                [5008.15, 856.84, 3855.44],
                [5032.89, 989.34, 3790.97],
                [5181.39, 1002.62, 3581.63],
                [5207.12, 1733.12, 3249.98],
                [5087.29, 1856.43, 3369.46],
                [4946.80, 2052.45, 3463.63],
                [4594.67, 2975.78, 3273.20],
                [4407.83, 3082.20, 3428.00],
                [4173.17, 3048.69, 3737.69],
                [4151.71, 3001.73, 3799.09]]

japan= [[-3596.67, 2881.97, 4408.90],
        [-3553.09, 3023.10, 4349.32],
        [-3778.75, 3221.50, 4002.90],
        [-3704.83, 3472.84, 3859.25],
        [-3662.44, 3608.98, 3773.85],
        [-3527.65, 3803.23, 3710.97],
        [-3389.43, 4112.76, 3503.88],
        [-3515.01, 4172.63, 3303.65],
        [-3610.21, 4096.33, 3296.45],
        [-3584.96, 3998.96, 3440.43],
        [-3814.17, 3705.22, 3521.87],
        [-3910.51, 3498.66, 3625.94],
        [-4032.16, 3307.35, 3671.96],
        [-3951.10, 3152.44, 3889.87],
        [-3892.49, 3008.82, 4059.03],
        [-3713.30, 2951.39, 4263.90],
        [-3713.82, 2895.69, 4301.47],
        [-3809.90, 2833.03, 4258.96],
        [-3789.20, 2733.47, 4341.69],
        [-3834.73, 2606.36, 4379.71],
        [-3756.52, 2602.16, 4449.44],
        [-3672.83, 2691.42, 4466.17],
        [-3520.89, 2763.79, 4543.68],
        [-3517.95, 2801.60, 4522.75],
        [-3596.67, 2881.97, 4408.90]]

philippines =  [[-3057.90, 5209.25, 2047.70],
                [-3033.83, 5331.95, 1745.39],
                [-3197.97, 5348.09, 1360.53],
                [-3398.72, 5315.07, 937.52],
                [-3543.21, 5260.32, 674.45],
                [-3692.79, 5163.41, 618.61],
                [-3787.23, 5069.56, 797.88],
                [-3613.14, 5072.62, 1376.20],
                [-3480.93, 5112.51, 1557.40],
                [-3292.02, 5218.69, 1614.93],
                [-3295.54, 5127.60, 1878.10],
                [-3245.70, 5097.34, 2040.26],
                [-3057.90, 5209.25, 2047.70]]

indonesia =[[-3650.47, 5226.07, 205.89],
            [-3555.83, 5293.83, 107.57],
            [-3271.57, 5472.97, 153.46],
            [-3187.44, 5523.95, 79.71],
            [-3059.10, 5583.10, -388.73],
            [-3127.60, 5544.67, -393.63],
            [-3111.47, 5532.67, -623.31],
            [-3224.74, 5467.79, -620.06],
            [-3212.99, 5499.43, -336.43],
            [-3279.37, 5460.50, -329.89],
            [-3353.56, 5390.67, -611.94],
            [-3471.39, 5314.43, -621.69],
            [-3489.04, 5320.52, -445.86],
            [-3372.53, 5408.76, -226.79],
            [-3529.98, 5311.21, -102.27],
            [-3494.72, 5335.16, -56.37],
            [-3236.86, 5494.79, -100.63],
            [-3238.62, 5494.55, 37.08],
            [-3590.25, 5271.55, 32.16],
            [-3692.43, 5197.42, 181.32],
            [-3650.47, 5226.07, 205.89]]

indonesia2=[[-2861.18, 5648.60, 766.26],
            [-2118.06, 6011.89, 226.12],
            [-2042.50, 6041.43, 97.42],
            [-2205.96, 5974.74, -341.08],
            [-2665.28, 5777.72, -440.87],
            [-2857.32, 5689.96, -374.48],
            [-3043.72, 5603.54, 127.61],
            [-3076.06, 5564.08, 508.98],
            [-3066.14, 5552.63, 668.78],
            [-2861.18, 5648.60, 766.26]]

indonesia3=[[-2730.12, 5689.60, -924.68],
            [-2615.15, 5733.77, -982.38],
            [-1686.85, 6103.87, -759.87],
            [-1225.98, 6251.50, -309.73],
            [-951.61, 6304.12, 180.77],
            [-561.05, 6326.41, 584.71],
            [-594.67, 6317.36, 646.18],
            [-837.32, 6295.65, 586.42],
            [-1173.26, 6263.11, 277.71],
            [-1538.04, 6189.86, -15.08],
            [-1769.95, 6117.35, -354.21],
            [-1782.62, 6099.36, -547.96],
            [-1907.63, 6056.23, -602.66],
            [-2242.34, 5928.15, -713.48],
            [-2612.02, 5757.16, -844.19],
            [-2730.12, 5689.60, -924.68]]

uk =   [[3306.64, -182.75, 5450.96],
        [3311.38, -291.89, 5443.32],
        [3600.21, -403.10, 5249.39],
        [3663.66, -651.90, 5180.03],
        [3862.98, -695.54, 5027.30],
        [3922.09, -652.34, 4987.16],
        [3870.12, -453.42, 5049.43],
        [3726.29, -413.35, 5159.85],
        [3670.92, -319.55, 5206.00],
        [3701.26, -225.34, 5189.42],
        [3786.76, -225.20, 5127.37],
        [3799.13, -295.74, 5114.61],
        [3886.10, -291.51, 5049.10],
        [3931.45, -350.59, 5010.09],
        [4042.27, -366.20, 4919.97],
        [4060.59, -333.33, 4907.21],
        [4012.25, 57.98, 4957.69],
        [3978.49, 102.28, 4984.10],
        [3865.19, 107.53, 5072.37],
        [3825.62, 22.99, 5103.36],
        [3544.44, -145.94, 5300.55],
        [3421.90, -102.07, 5381.48],
        [3400.83, -107.01, 5394.72],
        [3398.67, -229.12, 5392.28],
        [3330.05, -173.57, 5436.99],
        [3306.64, -182.75, 5450.96]]

australia =[[-4963.61, 3821.52, -1199.46],
            [-4705.01, 3872.72, -1882.84],
            [-4411.63, 4309.35, -1627.02],
            [-4587.86, 4229.14, -1321.38],
            [-4040.39, 4767.00, -1277.15],
            [-3868.56, 4841.58, -1507.81],
            [-3713.64, 4971.23, -1475.09],
            [-3557.56, 5061.37, -1551.29],
            [-3101.45, 5170.24, -2080.82],
            [-2521.55, 5394.73, -2284.47],
            [-2277.19, 5370.08, -2580.08],
            [-2216.84, 4765.27, -3613.59],
            [-2425.86, 4616.53, -3671.92],
            [-3545.35, 4071.39, -3396.24],
            [-3815.63, 3584.05, -3643.59],
            [-3908.80, 3072.46, -3995.18],
            [-4360.18, 2538.09, -3902.19],
            [-5083.68, 2513.60, -2918.60],
            [-5157.02, 2627.56, -2679.79],
            [-5131.41, 3098.97, -2178.35],
            [-5040.91, 3357.23, -1999.60],
            [-5003.82, 3634.68, -1559.17],
            [-4963.61, 3821.52, -1199.46]]

#List of all cities
nodes = ["Tokyo, Japan", "Delhi, India", "Shanghai, China", "São Paulo, Brazil", "Mexico City, Mexico", 
         "Cairo, Egypt", "Mumbai, India", "Beijing, China", "Dhaka, Bangladesh", "Osaka, Japan",
         "New York, USA", "Karachi, Pakistan", "Buenos Aires, Argentina", "Chongqing, China", "Istanbul, Turkey",
         "Kolkata, India", "Manila, Philippines", "Lagos, Nigeria", "Rio de Janeiro, Brazil", "Tianjin, China",
         "Kinshasa, DR Congo", "Guangzhou, China", "Los Angeles, USA", "Moscow, Russia", "Shenzhen, China",
         "Lahore, Pakistan", "Bangalore, India", "Paris, France", "Bogotá, Colombia", "Jakarta, Indonesia",
         "Chennai, India", "Lima, Peru", "Bangkok, Thailand", "Seoul, South Korea", "Nagoya, Japan",
         "Hyderabad, India", "London, United Kingdom", "Tehran, Iran", "Chicago, USA", "Chengdu, China"]

#Declare and initialize all routes connecting cities
#Dictionary of key value pairs where key=city, value=dictionary{city, distance}
cityRoutes = {}
for node in nodes:
    cityRoutes[node] = {}
    
cityRoutes["Tokyo, Japan"]["Osaka, Japan"] = distance(cityCoords[0], cityCoords[9])
cityRoutes["Tokyo, Japan"]["Nagoya, Japan"] = distance(cityCoords[0], cityCoords[34])
cityRoutes["Tokyo, Japan"]["Seoul, South Korea"] = distance(cityCoords[0], cityCoords[33])

cityRoutes["Delhi, India"]["Karachi, Pakistan"] = distance(cityCoords[1], cityCoords[11])
cityRoutes["Delhi, India"]["Kolkata, India"] = distance(cityCoords[1], cityCoords[15])
cityRoutes["Delhi, India"]["Hyderabad, India"] = distance(cityCoords[1], cityCoords[35])

cityRoutes["Shanghai, China"]["Seoul, South Korea"] = distance(cityCoords[2], cityCoords[33])
cityRoutes["Shanghai, China"]["Chongqing, China"] = distance(cityCoords[2], cityCoords[13])
cityRoutes["Shanghai, China"]["Beijing, China"] = distance(cityCoords[2], cityCoords[7])
cityRoutes["Shanghai, China"]["Tianjin, China"] = distance(cityCoords[2], cityCoords[19])
cityRoutes["Shanghai, China"]["Guangzhou, China"] = distance(cityCoords[2], cityCoords[21])

cityRoutes["São Paulo, Brazil"]["Rio de Janeiro, Brazil"] = distance(cityCoords[3], cityCoords[18])
cityRoutes["São Paulo, Brazil"]["Buenos Aires, Argentina"] = distance(cityCoords[3], cityCoords[12])
cityRoutes["São Paulo, Brazil"]["Bogotá, Colombia"] = distance(cityCoords[3], cityCoords[28])

cityRoutes["Mexico City, Mexico"]["Bogotá, Colombia"] = distance(cityCoords[4], cityCoords[28])
cityRoutes["Mexico City, Mexico"]["Los Angeles, USA"] = distance(cityCoords[4], cityCoords[22])

cityRoutes["Cairo, Egypt"]["Istanbul, Turkey"] = distance(cityCoords[5], cityCoords[14])
cityRoutes["Cairo, Egypt"]["Tehran, Iran"] = distance(cityCoords[5], cityCoords[37])
cityRoutes["Cairo, Egypt"]["Lagos, Nigeria"] = distance(cityCoords[5], cityCoords[17])
cityRoutes["Cairo, Egypt"]["Kinshasa, DR Congo"] = distance(cityCoords[5], cityCoords[20])

cityRoutes["Mumbai, India"]["Karachi, Pakistan"] = distance(cityCoords[6], cityCoords[11])
cityRoutes["Mumbai, India"]["Hyderabad, India"] = distance(cityCoords[6], cityCoords[35])
cityRoutes["Mumbai, India"]["Bangalore, India"] = distance(cityCoords[6], cityCoords[26])

#cityRoutes["Beijing, China"]["Shanghai, China"] = distance(cityCoords[7], cityCoords[2])
cityRoutes["Beijing, China"]["Tianjin, China"] = distance(cityCoords[7], cityCoords[19])

cityRoutes["Dhaka, Bangladesh"]["Kolkata, India"] = distance(cityCoords[8], cityCoords[15])
#cityRoutes["Dhaka, Bangladesh"]["Delhi, India"] = distance(cityCoords[8], cityCoords[1])
cityRoutes["Dhaka, Bangladesh"]["Chengdu, China"] = distance(cityCoords[8], cityCoords[39])
cityRoutes["Dhaka, Bangladesh"]["Chongqing, China"] = distance(cityCoords[8], cityCoords[13])
cityRoutes["Dhaka, Bangladesh"]["Bangkok, Thailand"] = distance(cityCoords[8], cityCoords[32])

cityRoutes["Osaka, Japan"]["Nagoya, Japan"] = distance(cityCoords[9], cityCoords[34])

cityRoutes["New York, USA"]["Chicago, USA"] = distance(cityCoords[10], cityCoords[38])
cityRoutes["New York, USA"]["London, United Kingdom"] = distance(cityCoords[10], cityCoords[36])

cityRoutes["Karachi, Pakistan"]["Lahore, Pakistan"] = distance(cityCoords[11], cityCoords[25])
cityRoutes["Karachi, Pakistan"]["Tehran, Iran"] = distance(cityCoords[11], cityCoords[37])

cityRoutes["Buenos Aires, Argentina"]["Rio de Janeiro, Brazil"] = distance(cityCoords[12], cityCoords[18])
cityRoutes["Buenos Aires, Argentina"]["Lima, Peru"] = distance(cityCoords[12], cityCoords[31])

cityRoutes["Chongqing, China"]["Chengdu, China"] = distance(cityCoords[13], cityCoords[39])
cityRoutes["Chongqing, China"]["Guangzhou, China"] = distance(cityCoords[13], cityCoords[21])

cityRoutes["Istanbul, Turkey"]["Moscow, Russia"] = distance(cityCoords[14], cityCoords[23])
cityRoutes["Istanbul, Turkey"]["Paris, France"] = distance(cityCoords[14], cityCoords[27])

cityRoutes["Kolkata, India"]["Chennai, India"] = distance(cityCoords[15], cityCoords[30])
cityRoutes["Kolkata, India"]["Hyderabad, India"] = distance(cityCoords[15], cityCoords[35])

cityRoutes["Manila, Philippines"]["Jakarta, Indonesia"] = distance(cityCoords[16], cityCoords[29])
cityRoutes["Manila, Philippines"]["Bangkok, Thailand"] = distance(cityCoords[16], cityCoords[32])
cityRoutes["Manila, Philippines"]["Shenzhen, China"] = distance(cityCoords[16], cityCoords[24])

cityRoutes["Lagos, Nigeria"]["Kinshasa, DR Congo"] = distance(cityCoords[17], cityCoords[20])

cityRoutes["Guangzhou, China"]["Shenzhen, China"] = distance(cityCoords[21], cityCoords[24])

cityRoutes["Los Angeles, USA"]["Chicago, USA"] = distance(cityCoords[22], cityCoords[38])

cityRoutes["Moscow, Russia"]["Paris, France"] = distance(cityCoords[23], cityCoords[27])

cityRoutes["Bangalore, India"]["Chennai, India"] = distance(cityCoords[26], cityCoords[30])
cityRoutes["Bangalore, India"]["Hyderabad, India"] = distance(cityCoords[26], cityCoords[35])

cityRoutes["Paris, France"]["London, United Kingdom"] = distance(cityCoords[27], cityCoords[36])

cityRoutes["Bogotá, Colombia"]["Lima, Peru"] = distance(cityCoords[28], cityCoords[31])

cityRoutes["Jakarta, Indonesia"]["Bangkok, Thailand"] = distance(cityCoords[29], cityCoords[32])

cityRoutes["Chennai, India"]["Hyderabad, India"] = distance(cityCoords[30], cityCoords[35])

#Plots all 40 cities in orange, cities along the path will later be recolored red
def plotCities():
        #Plot top 40 populated cities
        ax.scatter(cityCoords[0][0], cityCoords[0][1], cityCoords[0][2], color='orange')
        ax.scatter(cityCoords[1][0], cityCoords[1][1], cityCoords[1][2], color='orange')
        ax.scatter(cityCoords[2][0], cityCoords[2][1], cityCoords[2][2], color='orange')
        ax.scatter(cityCoords[3][0], cityCoords[3][1], cityCoords[3][2], color='orange')
        ax.scatter(cityCoords[4][0], cityCoords[4][1], cityCoords[4][2], color='orange')
        ax.scatter(cityCoords[5][0], cityCoords[5][1], cityCoords[5][2], color='orange')
        ax.scatter(cityCoords[6][0], cityCoords[6][1], cityCoords[6][2], color='orange')
        ax.scatter(cityCoords[7][0], cityCoords[7][1], cityCoords[7][2], color='orange')
        ax.scatter(cityCoords[8][0], cityCoords[8][1], cityCoords[8][2], color='orange')
        ax.scatter(cityCoords[9][0], cityCoords[9][1], cityCoords[9][2], color='orange')
        ax.scatter(cityCoords[10][0], cityCoords[10][1], cityCoords[10][2], color='orange')
        ax.scatter(cityCoords[11][0], cityCoords[11][1], cityCoords[11][2], color='orange')
        ax.scatter(cityCoords[12][0], cityCoords[12][1], cityCoords[12][2], color='orange')
        ax.scatter(cityCoords[13][0], cityCoords[13][1], cityCoords[13][2], color='orange')
        ax.scatter(cityCoords[14][0], cityCoords[14][1], cityCoords[14][2], color='orange')
        ax.scatter(cityCoords[15][0], cityCoords[15][1], cityCoords[15][2], color='orange')
        ax.scatter(cityCoords[16][0], cityCoords[16][1], cityCoords[16][2], color='orange')
        ax.scatter(cityCoords[17][0], cityCoords[17][1], cityCoords[17][2], color='orange')
        ax.scatter(cityCoords[18][0], cityCoords[18][1], cityCoords[18][2], color='orange')
        ax.scatter(cityCoords[19][0], cityCoords[19][1], cityCoords[19][2], color='orange')
        ax.scatter(cityCoords[20][0], cityCoords[20][1], cityCoords[20][2], color='orange')
        ax.scatter(cityCoords[21][0], cityCoords[21][1], cityCoords[21][2], color='orange')
        ax.scatter(cityCoords[22][0], cityCoords[22][1], cityCoords[22][2], color='orange')
        ax.scatter(cityCoords[23][0], cityCoords[23][1], cityCoords[23][2], color='orange')
        ax.scatter(cityCoords[24][0], cityCoords[24][1], cityCoords[24][2], color='orange')
        ax.scatter(cityCoords[25][0], cityCoords[25][1], cityCoords[25][2], color='orange')
        ax.scatter(cityCoords[26][0], cityCoords[26][1], cityCoords[26][2], color='orange')
        ax.scatter(cityCoords[27][0], cityCoords[27][1], cityCoords[27][2], color='orange')
        ax.scatter(cityCoords[28][0], cityCoords[28][1], cityCoords[28][2], color='orange')
        ax.scatter(cityCoords[29][0], cityCoords[29][1], cityCoords[29][2], color='orange')
        ax.scatter(cityCoords[30][0], cityCoords[30][1], cityCoords[30][2], color='orange')
        ax.scatter(cityCoords[31][0], cityCoords[31][1], cityCoords[31][2], color='orange')
        ax.scatter(cityCoords[32][0], cityCoords[32][1], cityCoords[32][2], color='orange')
        ax.scatter(cityCoords[33][0], cityCoords[33][1], cityCoords[33][2], color='orange')
        ax.scatter(cityCoords[34][0], cityCoords[34][1], cityCoords[34][2], color='orange')
        ax.scatter(cityCoords[35][0], cityCoords[35][1], cityCoords[35][2], color='orange')
        ax.scatter(cityCoords[36][0], cityCoords[36][1], cityCoords[36][2], color='orange')
        ax.scatter(cityCoords[37][0], cityCoords[37][1], cityCoords[37][2], color='orange')
        ax.scatter(cityCoords[38][0], cityCoords[38][1], cityCoords[38][2], color='orange')
        ax.scatter(cityCoords[39][0], cityCoords[39][1], cityCoords[39][2], color='orange')

        #North Pole
        ax.scatter(0, 0, 6378, color='deepskyblue')

#Plots the landmass outlines
def plotLandmass():
        #plot North and South America
        ax.plot([northSouth[0][0], northSouth[1][0]], [northSouth[0][1], northSouth[1][1]], [northSouth[0][2], northSouth[1][2]], color='green')
        ax.plot([northSouth[1][0], northSouth[2][0]], [northSouth[1][1], northSouth[2][1]], [northSouth[1][2], northSouth[2][2]], color='green')
        ax.plot([northSouth[2][0], northSouth[3][0]], [northSouth[2][1], northSouth[3][1]], [northSouth[2][2], northSouth[3][2]], color='green')
        ax.plot([northSouth[3][0], northSouth[4][0]], [northSouth[3][1], northSouth[4][1]], [northSouth[3][2], northSouth[4][2]], color='green')
        ax.plot([northSouth[4][0], northSouth[5][0]], [northSouth[4][1], northSouth[5][1]], [northSouth[4][2], northSouth[5][2]], color='green')
        ax.plot([northSouth[5][0], northSouth[6][0]], [northSouth[5][1], northSouth[6][1]], [northSouth[5][2], northSouth[6][2]], color='green')
        ax.plot([northSouth[6][0], northSouth[7][0]], [northSouth[6][1], northSouth[7][1]], [northSouth[6][2], northSouth[7][2]], color='green')
        ax.plot([northSouth[7][0], northSouth[8][0]], [northSouth[7][1], northSouth[8][1]], [northSouth[7][2], northSouth[8][2]], color='green')
        ax.plot([northSouth[8][0], northSouth[9][0]], [northSouth[8][1], northSouth[9][1]], [northSouth[8][2], northSouth[9][2]], color='green')
        ax.plot([northSouth[9][0], northSouth[10][0]], [northSouth[9][1], northSouth[10][1]], [northSouth[9][2], northSouth[10][2]], color='green')
        ax.plot([northSouth[10][0], northSouth[11][0]], [northSouth[10][1], northSouth[11][1]], [northSouth[10][2], northSouth[11][2]], color='green')
        ax.plot([northSouth[11][0], northSouth[12][0]], [northSouth[11][1], northSouth[12][1]], [northSouth[11][2], northSouth[12][2]], color='green')
        ax.plot([northSouth[12][0], northSouth[13][0]], [northSouth[12][1], northSouth[13][1]], [northSouth[12][2], northSouth[13][2]], color='green')
        ax.plot([northSouth[13][0], northSouth[14][0]], [northSouth[13][1], northSouth[14][1]], [northSouth[13][2], northSouth[14][2]], color='green')
        ax.plot([northSouth[14][0], northSouth[15][0]], [northSouth[14][1], northSouth[15][1]], [northSouth[14][2], northSouth[15][2]], color='green')
        ax.plot([northSouth[15][0], northSouth[16][0]], [northSouth[15][1], northSouth[16][1]], [northSouth[15][2], northSouth[16][2]], color='green')
        ax.plot([northSouth[16][0], northSouth[17][0]], [northSouth[16][1], northSouth[17][1]], [northSouth[16][2], northSouth[17][2]], color='green')
        ax.plot([northSouth[17][0], northSouth[18][0]], [northSouth[17][1], northSouth[18][1]], [northSouth[17][2], northSouth[18][2]], color='green')
        ax.plot([northSouth[18][0], northSouth[19][0]], [northSouth[18][1], northSouth[19][1]], [northSouth[18][2], northSouth[19][2]], color='green')
        ax.plot([northSouth[19][0], northSouth[20][0]], [northSouth[19][1], northSouth[20][1]], [northSouth[19][2], northSouth[20][2]], color='green')
        ax.plot([northSouth[20][0], northSouth[21][0]], [northSouth[20][1], northSouth[21][1]], [northSouth[20][2], northSouth[21][2]], color='green')
        ax.plot([northSouth[21][0], northSouth[22][0]], [northSouth[21][1], northSouth[22][1]], [northSouth[21][2], northSouth[22][2]], color='green')
        ax.plot([northSouth[22][0], northSouth[23][0]], [northSouth[22][1], northSouth[23][1]], [northSouth[22][2], northSouth[23][2]], color='green')
        ax.plot([northSouth[23][0], northSouth[24][0]], [northSouth[23][1], northSouth[24][1]], [northSouth[23][2], northSouth[24][2]], color='green')
        ax.plot([northSouth[24][0], northSouth[25][0]], [northSouth[24][1], northSouth[25][1]], [northSouth[24][2], northSouth[25][2]], color='green')
        ax.plot([northSouth[25][0], northSouth[26][0]], [northSouth[25][1], northSouth[26][1]], [northSouth[25][2], northSouth[26][2]], color='green')
        ax.plot([northSouth[26][0], northSouth[27][0]], [northSouth[26][1], northSouth[27][1]], [northSouth[26][2], northSouth[27][2]], color='green')
        ax.plot([northSouth[27][0], northSouth[28][0]], [northSouth[27][1], northSouth[28][1]], [northSouth[27][2], northSouth[28][2]], color='green')
        ax.plot([northSouth[28][0], northSouth[29][0]], [northSouth[28][1], northSouth[29][1]], [northSouth[28][2], northSouth[29][2]], color='green')
        ax.plot([northSouth[29][0], northSouth[30][0]], [northSouth[29][1], northSouth[30][1]], [northSouth[29][2], northSouth[30][2]], color='green')
        ax.plot([northSouth[30][0], northSouth[31][0]], [northSouth[30][1], northSouth[31][1]], [northSouth[30][2], northSouth[31][2]], color='green')
        ax.plot([northSouth[31][0], northSouth[32][0]], [northSouth[31][1], northSouth[32][1]], [northSouth[31][2], northSouth[32][2]], color='green')
        ax.plot([northSouth[32][0], northSouth[33][0]], [northSouth[32][1], northSouth[33][1]], [northSouth[32][2], northSouth[33][2]], color='green')
        ax.plot([northSouth[33][0], northSouth[34][0]], [northSouth[33][1], northSouth[34][1]], [northSouth[33][2], northSouth[34][2]], color='green')
        ax.plot([northSouth[34][0], northSouth[35][0]], [northSouth[34][1], northSouth[35][1]], [northSouth[34][2], northSouth[35][2]], color='green')
        ax.plot([northSouth[35][0], northSouth[36][0]], [northSouth[35][1], northSouth[36][1]], [northSouth[35][2], northSouth[36][2]], color='green')
        ax.plot([northSouth[36][0], northSouth[37][0]], [northSouth[36][1], northSouth[37][1]], [northSouth[36][2], northSouth[37][2]], color='green')
        ax.plot([northSouth[37][0], northSouth[38][0]], [northSouth[37][1], northSouth[38][1]], [northSouth[37][2], northSouth[38][2]], color='green')
        ax.plot([northSouth[38][0], northSouth[39][0]], [northSouth[38][1], northSouth[39][1]], [northSouth[38][2], northSouth[39][2]], color='green')
        ax.plot([northSouth[39][0], northSouth[40][0]], [northSouth[39][1], northSouth[40][1]], [northSouth[39][2], northSouth[40][2]], color='green')
        ax.plot([northSouth[40][0], northSouth[41][0]], [northSouth[40][1], northSouth[41][1]], [northSouth[40][2], northSouth[41][2]], color='green')
        ax.plot([northSouth[41][0], northSouth[42][0]], [northSouth[41][1], northSouth[42][1]], [northSouth[41][2], northSouth[42][2]], color='green')
        ax.plot([northSouth[42][0], northSouth[43][0]], [northSouth[42][1], northSouth[43][1]], [northSouth[42][2], northSouth[43][2]], color='green')
        ax.plot([northSouth[43][0], northSouth[44][0]], [northSouth[43][1], northSouth[44][1]], [northSouth[43][2], northSouth[44][2]], color='green')
        ax.plot([northSouth[44][0], northSouth[45][0]], [northSouth[44][1], northSouth[45][1]], [northSouth[44][2], northSouth[45][2]], color='green')
        ax.plot([northSouth[45][0], northSouth[46][0]], [northSouth[45][1], northSouth[46][1]], [northSouth[45][2], northSouth[46][2]], color='green')
        ax.plot([northSouth[46][0], northSouth[47][0]], [northSouth[46][1], northSouth[47][1]], [northSouth[46][2], northSouth[47][2]], color='green')
        ax.plot([northSouth[47][0], northSouth[48][0]], [northSouth[47][1], northSouth[48][1]], [northSouth[47][2], northSouth[48][2]], color='green')
        ax.plot([northSouth[48][0], northSouth[49][0]], [northSouth[48][1], northSouth[49][1]], [northSouth[48][2], northSouth[49][2]], color='green')
        ax.plot([northSouth[49][0], northSouth[50][0]], [northSouth[49][1], northSouth[50][1]], [northSouth[49][2], northSouth[50][2]], color='green')
        ax.plot([northSouth[50][0], northSouth[51][0]], [northSouth[50][1], northSouth[51][1]], [northSouth[50][2], northSouth[51][2]], color='green')
        ax.plot([northSouth[51][0], northSouth[52][0]], [northSouth[51][1], northSouth[52][1]], [northSouth[51][2], northSouth[52][2]], color='green')
        ax.plot([northSouth[52][0], northSouth[53][0]], [northSouth[52][1], northSouth[53][1]], [northSouth[52][2], northSouth[53][2]], color='green')
        ax.plot([northSouth[53][0], northSouth[54][0]], [northSouth[53][1], northSouth[54][1]], [northSouth[53][2], northSouth[54][2]], color='green')
        ax.plot([northSouth[54][0], northSouth[55][0]], [northSouth[54][1], northSouth[55][1]], [northSouth[54][2], northSouth[55][2]], color='green')
        ax.plot([northSouth[55][0], northSouth[56][0]], [northSouth[55][1], northSouth[56][1]], [northSouth[55][2], northSouth[56][2]], color='green')
        ax.plot([northSouth[56][0], northSouth[57][0]], [northSouth[56][1], northSouth[57][1]], [northSouth[56][2], northSouth[57][2]], color='green')
        ax.plot([northSouth[57][0], northSouth[58][0]], [northSouth[57][1], northSouth[58][1]], [northSouth[57][2], northSouth[58][2]], color='green')
        ax.plot([northSouth[58][0], northSouth[59][0]], [northSouth[58][1], northSouth[59][1]], [northSouth[58][2], northSouth[59][2]], color='green')
        ax.plot([northSouth[59][0], northSouth[60][0]], [northSouth[59][1], northSouth[60][1]], [northSouth[59][2], northSouth[60][2]], color='green')
        ax.plot([northSouth[60][0], northSouth[61][0]], [northSouth[60][1], northSouth[61][1]], [northSouth[60][2], northSouth[61][2]], color='green')
        ax.plot([northSouth[61][0], northSouth[62][0]], [northSouth[61][1], northSouth[62][1]], [northSouth[61][2], northSouth[62][2]], color='green')
        ax.plot([northSouth[62][0], northSouth[63][0]], [northSouth[62][1], northSouth[63][1]], [northSouth[62][2], northSouth[63][2]], color='green')
        ax.plot([northSouth[63][0], northSouth[64][0]], [northSouth[63][1], northSouth[64][1]], [northSouth[63][2], northSouth[64][2]], color='green')
        ax.plot([northSouth[64][0], northSouth[65][0]], [northSouth[64][1], northSouth[65][1]], [northSouth[64][2], northSouth[65][2]], color='green')
        ax.plot([northSouth[65][0], northSouth[66][0]], [northSouth[65][1], northSouth[66][1]], [northSouth[65][2], northSouth[66][2]], color='green')
        ax.plot([northSouth[66][0], northSouth[67][0]], [northSouth[66][1], northSouth[67][1]], [northSouth[66][2], northSouth[67][2]], color='green')
        ax.plot([northSouth[67][0], northSouth[68][0]], [northSouth[67][1], northSouth[68][1]], [northSouth[67][2], northSouth[68][2]], color='green')
        ax.plot([northSouth[68][0], northSouth[69][0]], [northSouth[68][1], northSouth[69][1]], [northSouth[68][2], northSouth[69][2]], color='green')
        ax.plot([northSouth[69][0], northSouth[70][0]], [northSouth[69][1], northSouth[70][1]], [northSouth[69][2], northSouth[70][2]], color='green')

        #plot Europe, Asia, Africa
        ax.plot([eurasiaAfrica[0][0], eurasiaAfrica[1][0]], [eurasiaAfrica[0][1], eurasiaAfrica[1][1]], [eurasiaAfrica[0][2], eurasiaAfrica[1][2]], color='green')
        ax.plot([eurasiaAfrica[1][0], eurasiaAfrica[2][0]], [eurasiaAfrica[1][1], eurasiaAfrica[2][1]], [eurasiaAfrica[1][2], eurasiaAfrica[2][2]], color='green')
        ax.plot([eurasiaAfrica[2][0], eurasiaAfrica[3][0]], [eurasiaAfrica[2][1], eurasiaAfrica[3][1]], [eurasiaAfrica[2][2], eurasiaAfrica[3][2]], color='green')
        ax.plot([eurasiaAfrica[3][0], eurasiaAfrica[4][0]], [eurasiaAfrica[3][1], eurasiaAfrica[4][1]], [eurasiaAfrica[3][2], eurasiaAfrica[4][2]], color='green')
        ax.plot([eurasiaAfrica[4][0], eurasiaAfrica[5][0]], [eurasiaAfrica[4][1], eurasiaAfrica[5][1]], [eurasiaAfrica[4][2], eurasiaAfrica[5][2]], color='green')
        ax.plot([eurasiaAfrica[5][0], eurasiaAfrica[6][0]], [eurasiaAfrica[5][1], eurasiaAfrica[6][1]], [eurasiaAfrica[5][2], eurasiaAfrica[6][2]], color='green')
        ax.plot([eurasiaAfrica[6][0], eurasiaAfrica[7][0]], [eurasiaAfrica[6][1], eurasiaAfrica[7][1]], [eurasiaAfrica[6][2], eurasiaAfrica[7][2]], color='green')
        ax.plot([eurasiaAfrica[7][0], eurasiaAfrica[8][0]], [eurasiaAfrica[7][1], eurasiaAfrica[8][1]], [eurasiaAfrica[7][2], eurasiaAfrica[8][2]], color='green')
        ax.plot([eurasiaAfrica[8][0], eurasiaAfrica[9][0]], [eurasiaAfrica[8][1], eurasiaAfrica[9][1]], [eurasiaAfrica[8][2], eurasiaAfrica[9][2]], color='green')
        ax.plot([eurasiaAfrica[9][0], eurasiaAfrica[10][0]], [eurasiaAfrica[9][1], eurasiaAfrica[10][1]], [eurasiaAfrica[9][2], eurasiaAfrica[10][2]], color='green')
        ax.plot([eurasiaAfrica[10][0], eurasiaAfrica[11][0]], [eurasiaAfrica[10][1], eurasiaAfrica[11][1]], [eurasiaAfrica[10][2], eurasiaAfrica[11][2]], color='green')
        ax.plot([eurasiaAfrica[11][0], eurasiaAfrica[12][0]], [eurasiaAfrica[11][1], eurasiaAfrica[12][1]], [eurasiaAfrica[11][2], eurasiaAfrica[12][2]], color='green')
        ax.plot([eurasiaAfrica[12][0], eurasiaAfrica[13][0]], [eurasiaAfrica[12][1], eurasiaAfrica[13][1]], [eurasiaAfrica[12][2], eurasiaAfrica[13][2]], color='green')
        ax.plot([eurasiaAfrica[13][0], eurasiaAfrica[14][0]], [eurasiaAfrica[13][1], eurasiaAfrica[14][1]], [eurasiaAfrica[13][2], eurasiaAfrica[14][2]], color='green')
        ax.plot([eurasiaAfrica[14][0], eurasiaAfrica[15][0]], [eurasiaAfrica[14][1], eurasiaAfrica[15][1]], [eurasiaAfrica[14][2], eurasiaAfrica[15][2]], color='green')
        ax.plot([eurasiaAfrica[15][0], eurasiaAfrica[16][0]], [eurasiaAfrica[15][1], eurasiaAfrica[16][1]], [eurasiaAfrica[15][2], eurasiaAfrica[16][2]], color='green')
        ax.plot([eurasiaAfrica[16][0], eurasiaAfrica[17][0]], [eurasiaAfrica[16][1], eurasiaAfrica[17][1]], [eurasiaAfrica[16][2], eurasiaAfrica[17][2]], color='green')
        ax.plot([eurasiaAfrica[17][0], eurasiaAfrica[18][0]], [eurasiaAfrica[17][1], eurasiaAfrica[18][1]], [eurasiaAfrica[17][2], eurasiaAfrica[18][2]], color='green')
        ax.plot([eurasiaAfrica[18][0], eurasiaAfrica[19][0]], [eurasiaAfrica[18][1], eurasiaAfrica[19][1]], [eurasiaAfrica[18][2], eurasiaAfrica[19][2]], color='green')
        ax.plot([eurasiaAfrica[19][0], eurasiaAfrica[20][0]], [eurasiaAfrica[19][1], eurasiaAfrica[20][1]], [eurasiaAfrica[19][2], eurasiaAfrica[20][2]], color='green')
        ax.plot([eurasiaAfrica[20][0], eurasiaAfrica[21][0]], [eurasiaAfrica[20][1], eurasiaAfrica[21][1]], [eurasiaAfrica[20][2], eurasiaAfrica[21][2]], color='green')
        ax.plot([eurasiaAfrica[21][0], eurasiaAfrica[22][0]], [eurasiaAfrica[21][1], eurasiaAfrica[22][1]], [eurasiaAfrica[21][2], eurasiaAfrica[22][2]], color='green')
        ax.plot([eurasiaAfrica[22][0], eurasiaAfrica[23][0]], [eurasiaAfrica[22][1], eurasiaAfrica[23][1]], [eurasiaAfrica[22][2], eurasiaAfrica[23][2]], color='green')
        ax.plot([eurasiaAfrica[23][0], eurasiaAfrica[24][0]], [eurasiaAfrica[23][1], eurasiaAfrica[24][1]], [eurasiaAfrica[23][2], eurasiaAfrica[24][2]], color='green')
        ax.plot([eurasiaAfrica[24][0], eurasiaAfrica[25][0]], [eurasiaAfrica[24][1], eurasiaAfrica[25][1]], [eurasiaAfrica[24][2], eurasiaAfrica[25][2]], color='green')
        ax.plot([eurasiaAfrica[25][0], eurasiaAfrica[26][0]], [eurasiaAfrica[25][1], eurasiaAfrica[26][1]], [eurasiaAfrica[25][2], eurasiaAfrica[26][2]], color='green')
        ax.plot([eurasiaAfrica[26][0], eurasiaAfrica[27][0]], [eurasiaAfrica[26][1], eurasiaAfrica[27][1]], [eurasiaAfrica[26][2], eurasiaAfrica[27][2]], color='green')
        ax.plot([eurasiaAfrica[27][0], eurasiaAfrica[28][0]], [eurasiaAfrica[27][1], eurasiaAfrica[28][1]], [eurasiaAfrica[27][2], eurasiaAfrica[28][2]], color='green')
        ax.plot([eurasiaAfrica[28][0], eurasiaAfrica[29][0]], [eurasiaAfrica[28][1], eurasiaAfrica[29][1]], [eurasiaAfrica[28][2], eurasiaAfrica[29][2]], color='green')
        ax.plot([eurasiaAfrica[29][0], eurasiaAfrica[30][0]], [eurasiaAfrica[29][1], eurasiaAfrica[30][1]], [eurasiaAfrica[29][2], eurasiaAfrica[30][2]], color='green')
        ax.plot([eurasiaAfrica[30][0], eurasiaAfrica[31][0]], [eurasiaAfrica[30][1], eurasiaAfrica[31][1]], [eurasiaAfrica[30][2], eurasiaAfrica[31][2]], color='green')
        ax.plot([eurasiaAfrica[31][0], eurasiaAfrica[32][0]], [eurasiaAfrica[31][1], eurasiaAfrica[32][1]], [eurasiaAfrica[31][2], eurasiaAfrica[32][2]], color='green')
        ax.plot([eurasiaAfrica[32][0], eurasiaAfrica[33][0]], [eurasiaAfrica[32][1], eurasiaAfrica[33][1]], [eurasiaAfrica[32][2], eurasiaAfrica[33][2]], color='green')
        ax.plot([eurasiaAfrica[33][0], eurasiaAfrica[34][0]], [eurasiaAfrica[33][1], eurasiaAfrica[34][1]], [eurasiaAfrica[33][2], eurasiaAfrica[34][2]], color='green')
        ax.plot([eurasiaAfrica[34][0], eurasiaAfrica[35][0]], [eurasiaAfrica[34][1], eurasiaAfrica[35][1]], [eurasiaAfrica[34][2], eurasiaAfrica[35][2]], color='green')
        ax.plot([eurasiaAfrica[35][0], eurasiaAfrica[36][0]], [eurasiaAfrica[35][1], eurasiaAfrica[36][1]], [eurasiaAfrica[35][2], eurasiaAfrica[36][2]], color='green')
        ax.plot([eurasiaAfrica[36][0], eurasiaAfrica[37][0]], [eurasiaAfrica[36][1], eurasiaAfrica[37][1]], [eurasiaAfrica[36][2], eurasiaAfrica[37][2]], color='green')
        ax.plot([eurasiaAfrica[37][0], eurasiaAfrica[38][0]], [eurasiaAfrica[37][1], eurasiaAfrica[38][1]], [eurasiaAfrica[37][2], eurasiaAfrica[38][2]], color='green')
        ax.plot([eurasiaAfrica[38][0], eurasiaAfrica[39][0]], [eurasiaAfrica[38][1], eurasiaAfrica[39][1]], [eurasiaAfrica[38][2], eurasiaAfrica[39][2]], color='green')
        ax.plot([eurasiaAfrica[39][0], eurasiaAfrica[40][0]], [eurasiaAfrica[39][1], eurasiaAfrica[40][1]], [eurasiaAfrica[39][2], eurasiaAfrica[40][2]], color='green')
        ax.plot([eurasiaAfrica[40][0], eurasiaAfrica[41][0]], [eurasiaAfrica[40][1], eurasiaAfrica[41][1]], [eurasiaAfrica[40][2], eurasiaAfrica[41][2]], color='green')
        ax.plot([eurasiaAfrica[41][0], eurasiaAfrica[42][0]], [eurasiaAfrica[41][1], eurasiaAfrica[42][1]], [eurasiaAfrica[41][2], eurasiaAfrica[42][2]], color='green')
        ax.plot([eurasiaAfrica[42][0], eurasiaAfrica[43][0]], [eurasiaAfrica[42][1], eurasiaAfrica[43][1]], [eurasiaAfrica[42][2], eurasiaAfrica[43][2]], color='green')
        ax.plot([eurasiaAfrica[43][0], eurasiaAfrica[44][0]], [eurasiaAfrica[43][1], eurasiaAfrica[44][1]], [eurasiaAfrica[43][2], eurasiaAfrica[44][2]], color='green')
        ax.plot([eurasiaAfrica[44][0], eurasiaAfrica[45][0]], [eurasiaAfrica[44][1], eurasiaAfrica[45][1]], [eurasiaAfrica[44][2], eurasiaAfrica[45][2]], color='green')
        ax.plot([eurasiaAfrica[45][0], eurasiaAfrica[46][0]], [eurasiaAfrica[45][1], eurasiaAfrica[46][1]], [eurasiaAfrica[45][2], eurasiaAfrica[46][2]], color='green')
        ax.plot([eurasiaAfrica[46][0], eurasiaAfrica[47][0]], [eurasiaAfrica[46][1], eurasiaAfrica[47][1]], [eurasiaAfrica[46][2], eurasiaAfrica[47][2]], color='green')
        ax.plot([eurasiaAfrica[47][0], eurasiaAfrica[48][0]], [eurasiaAfrica[47][1], eurasiaAfrica[48][1]], [eurasiaAfrica[47][2], eurasiaAfrica[48][2]], color='green')
        ax.plot([eurasiaAfrica[48][0], eurasiaAfrica[49][0]], [eurasiaAfrica[48][1], eurasiaAfrica[49][1]], [eurasiaAfrica[48][2], eurasiaAfrica[49][2]], color='green')
        ax.plot([eurasiaAfrica[49][0], eurasiaAfrica[50][0]], [eurasiaAfrica[49][1], eurasiaAfrica[50][1]], [eurasiaAfrica[49][2], eurasiaAfrica[50][2]], color='green')
        ax.plot([eurasiaAfrica[50][0], eurasiaAfrica[51][0]], [eurasiaAfrica[50][1], eurasiaAfrica[51][1]], [eurasiaAfrica[50][2], eurasiaAfrica[51][2]], color='green')
        ax.plot([eurasiaAfrica[51][0], eurasiaAfrica[52][0]], [eurasiaAfrica[51][1], eurasiaAfrica[52][1]], [eurasiaAfrica[51][2], eurasiaAfrica[52][2]], color='green')
        ax.plot([eurasiaAfrica[52][0], eurasiaAfrica[53][0]], [eurasiaAfrica[52][1], eurasiaAfrica[53][1]], [eurasiaAfrica[52][2], eurasiaAfrica[53][2]], color='green')
        ax.plot([eurasiaAfrica[53][0], eurasiaAfrica[54][0]], [eurasiaAfrica[53][1], eurasiaAfrica[54][1]], [eurasiaAfrica[53][2], eurasiaAfrica[54][2]], color='green')
        ax.plot([eurasiaAfrica[54][0], eurasiaAfrica[55][0]], [eurasiaAfrica[54][1], eurasiaAfrica[55][1]], [eurasiaAfrica[54][2], eurasiaAfrica[55][2]], color='green')
        ax.plot([eurasiaAfrica[55][0], eurasiaAfrica[56][0]], [eurasiaAfrica[55][1], eurasiaAfrica[56][1]], [eurasiaAfrica[55][2], eurasiaAfrica[56][2]], color='green')
        ax.plot([eurasiaAfrica[56][0], eurasiaAfrica[57][0]], [eurasiaAfrica[56][1], eurasiaAfrica[57][1]], [eurasiaAfrica[56][2], eurasiaAfrica[57][2]], color='green')
        ax.plot([eurasiaAfrica[57][0], eurasiaAfrica[58][0]], [eurasiaAfrica[57][1], eurasiaAfrica[58][1]], [eurasiaAfrica[57][2], eurasiaAfrica[58][2]], color='green')
        ax.plot([eurasiaAfrica[58][0], eurasiaAfrica[59][0]], [eurasiaAfrica[58][1], eurasiaAfrica[59][1]], [eurasiaAfrica[58][2], eurasiaAfrica[59][2]], color='green')
        ax.plot([eurasiaAfrica[59][0], eurasiaAfrica[60][0]], [eurasiaAfrica[59][1], eurasiaAfrica[60][1]], [eurasiaAfrica[59][2], eurasiaAfrica[60][2]], color='green')
        ax.plot([eurasiaAfrica[60][0], eurasiaAfrica[61][0]], [eurasiaAfrica[60][1], eurasiaAfrica[61][1]], [eurasiaAfrica[60][2], eurasiaAfrica[61][2]], color='green')
        ax.plot([eurasiaAfrica[61][0], eurasiaAfrica[62][0]], [eurasiaAfrica[61][1], eurasiaAfrica[62][1]], [eurasiaAfrica[61][2], eurasiaAfrica[62][2]], color='green')
        ax.plot([eurasiaAfrica[62][0], eurasiaAfrica[63][0]], [eurasiaAfrica[62][1], eurasiaAfrica[63][1]], [eurasiaAfrica[62][2], eurasiaAfrica[63][2]], color='green')
        ax.plot([eurasiaAfrica[63][0], eurasiaAfrica[64][0]], [eurasiaAfrica[63][1], eurasiaAfrica[64][1]], [eurasiaAfrica[63][2], eurasiaAfrica[64][2]], color='green')
        ax.plot([eurasiaAfrica[64][0], eurasiaAfrica[65][0]], [eurasiaAfrica[64][1], eurasiaAfrica[65][1]], [eurasiaAfrica[64][2], eurasiaAfrica[65][2]], color='green')
        ax.plot([eurasiaAfrica[65][0], eurasiaAfrica[66][0]], [eurasiaAfrica[65][1], eurasiaAfrica[66][1]], [eurasiaAfrica[65][2], eurasiaAfrica[66][2]], color='green')
        ax.plot([eurasiaAfrica[66][0], eurasiaAfrica[67][0]], [eurasiaAfrica[66][1], eurasiaAfrica[67][1]], [eurasiaAfrica[66][2], eurasiaAfrica[67][2]], color='green')
        ax.plot([eurasiaAfrica[67][0], eurasiaAfrica[68][0]], [eurasiaAfrica[67][1], eurasiaAfrica[68][1]], [eurasiaAfrica[67][2], eurasiaAfrica[68][2]], color='green')
        ax.plot([eurasiaAfrica[68][0], eurasiaAfrica[69][0]], [eurasiaAfrica[68][1], eurasiaAfrica[69][1]], [eurasiaAfrica[68][2], eurasiaAfrica[69][2]], color='green')
        ax.plot([eurasiaAfrica[69][0], eurasiaAfrica[70][0]], [eurasiaAfrica[69][1], eurasiaAfrica[70][1]], [eurasiaAfrica[69][2], eurasiaAfrica[70][2]], color='green')
        ax.plot([eurasiaAfrica[70][0], eurasiaAfrica[71][0]], [eurasiaAfrica[70][1], eurasiaAfrica[71][1]], [eurasiaAfrica[70][2], eurasiaAfrica[71][2]], color='green')
        ax.plot([eurasiaAfrica[71][0], eurasiaAfrica[72][0]], [eurasiaAfrica[71][1], eurasiaAfrica[72][1]], [eurasiaAfrica[71][2], eurasiaAfrica[72][2]], color='green')
        ax.plot([eurasiaAfrica[72][0], eurasiaAfrica[73][0]], [eurasiaAfrica[72][1], eurasiaAfrica[73][1]], [eurasiaAfrica[72][2], eurasiaAfrica[73][2]], color='green')
        ax.plot([eurasiaAfrica[73][0], eurasiaAfrica[74][0]], [eurasiaAfrica[73][1], eurasiaAfrica[74][1]], [eurasiaAfrica[73][2], eurasiaAfrica[74][2]], color='green')
        ax.plot([eurasiaAfrica[74][0], eurasiaAfrica[75][0]], [eurasiaAfrica[74][1], eurasiaAfrica[75][1]], [eurasiaAfrica[74][2], eurasiaAfrica[75][2]], color='green')
        ax.plot([eurasiaAfrica[75][0], eurasiaAfrica[76][0]], [eurasiaAfrica[75][1], eurasiaAfrica[76][1]], [eurasiaAfrica[75][2], eurasiaAfrica[76][2]], color='green')
        ax.plot([eurasiaAfrica[76][0], eurasiaAfrica[77][0]], [eurasiaAfrica[76][1], eurasiaAfrica[77][1]], [eurasiaAfrica[76][2], eurasiaAfrica[77][2]], color='green')
        ax.plot([eurasiaAfrica[77][0], eurasiaAfrica[78][0]], [eurasiaAfrica[77][1], eurasiaAfrica[78][1]], [eurasiaAfrica[77][2], eurasiaAfrica[78][2]], color='green')
        ax.plot([eurasiaAfrica[78][0], eurasiaAfrica[79][0]], [eurasiaAfrica[78][1], eurasiaAfrica[79][1]], [eurasiaAfrica[78][2], eurasiaAfrica[79][2]], color='green')
        ax.plot([eurasiaAfrica[79][0], eurasiaAfrica[80][0]], [eurasiaAfrica[79][1], eurasiaAfrica[80][1]], [eurasiaAfrica[79][2], eurasiaAfrica[80][2]], color='green')
        ax.plot([eurasiaAfrica[80][0], eurasiaAfrica[81][0]], [eurasiaAfrica[80][1], eurasiaAfrica[81][1]], [eurasiaAfrica[80][2], eurasiaAfrica[81][2]], color='green')
        ax.plot([eurasiaAfrica[81][0], eurasiaAfrica[82][0]], [eurasiaAfrica[81][1], eurasiaAfrica[82][1]], [eurasiaAfrica[81][2], eurasiaAfrica[82][2]], color='green')
        ax.plot([eurasiaAfrica[82][0], eurasiaAfrica[83][0]], [eurasiaAfrica[82][1], eurasiaAfrica[83][1]], [eurasiaAfrica[82][2], eurasiaAfrica[83][2]], color='green')
        ax.plot([eurasiaAfrica[83][0], eurasiaAfrica[84][0]], [eurasiaAfrica[83][1], eurasiaAfrica[84][1]], [eurasiaAfrica[83][2], eurasiaAfrica[84][2]], color='green')
        ax.plot([eurasiaAfrica[84][0], eurasiaAfrica[85][0]], [eurasiaAfrica[84][1], eurasiaAfrica[85][1]], [eurasiaAfrica[84][2], eurasiaAfrica[85][2]], color='green')
        ax.plot([eurasiaAfrica[85][0], eurasiaAfrica[86][0]], [eurasiaAfrica[85][1], eurasiaAfrica[86][1]], [eurasiaAfrica[85][2], eurasiaAfrica[86][2]], color='green')
        ax.plot([eurasiaAfrica[86][0], eurasiaAfrica[87][0]], [eurasiaAfrica[86][1], eurasiaAfrica[87][1]], [eurasiaAfrica[86][2], eurasiaAfrica[87][2]], color='green')
        ax.plot([eurasiaAfrica[87][0], eurasiaAfrica[88][0]], [eurasiaAfrica[87][1], eurasiaAfrica[88][1]], [eurasiaAfrica[87][2], eurasiaAfrica[88][2]], color='green')
        ax.plot([eurasiaAfrica[88][0], eurasiaAfrica[89][0]], [eurasiaAfrica[88][1], eurasiaAfrica[89][1]], [eurasiaAfrica[88][2], eurasiaAfrica[89][2]], color='green')
        ax.plot([eurasiaAfrica[89][0], eurasiaAfrica[90][0]], [eurasiaAfrica[89][1], eurasiaAfrica[90][1]], [eurasiaAfrica[89][2], eurasiaAfrica[90][2]], color='green')
        ax.plot([eurasiaAfrica[90][0], eurasiaAfrica[91][0]], [eurasiaAfrica[90][1], eurasiaAfrica[91][1]], [eurasiaAfrica[90][2], eurasiaAfrica[91][2]], color='green')
        ax.plot([eurasiaAfrica[91][0], eurasiaAfrica[92][0]], [eurasiaAfrica[91][1], eurasiaAfrica[92][1]], [eurasiaAfrica[91][2], eurasiaAfrica[92][2]], color='green')
        ax.plot([eurasiaAfrica[92][0], eurasiaAfrica[93][0]], [eurasiaAfrica[92][1], eurasiaAfrica[93][1]], [eurasiaAfrica[92][2], eurasiaAfrica[93][2]], color='green')
        ax.plot([eurasiaAfrica[93][0], eurasiaAfrica[94][0]], [eurasiaAfrica[93][1], eurasiaAfrica[94][1]], [eurasiaAfrica[93][2], eurasiaAfrica[94][2]], color='green')
        ax.plot([eurasiaAfrica[94][0], eurasiaAfrica[95][0]], [eurasiaAfrica[94][1], eurasiaAfrica[95][1]], [eurasiaAfrica[94][2], eurasiaAfrica[95][2]], color='green')
        ax.plot([eurasiaAfrica[95][0], eurasiaAfrica[96][0]], [eurasiaAfrica[95][1], eurasiaAfrica[96][1]], [eurasiaAfrica[95][2], eurasiaAfrica[96][2]], color='green')
        ax.plot([eurasiaAfrica[96][0], eurasiaAfrica[97][0]], [eurasiaAfrica[96][1], eurasiaAfrica[97][1]], [eurasiaAfrica[96][2], eurasiaAfrica[97][2]], color='green')
        ax.plot([eurasiaAfrica[97][0], eurasiaAfrica[98][0]], [eurasiaAfrica[97][1], eurasiaAfrica[98][1]], [eurasiaAfrica[97][2], eurasiaAfrica[98][2]], color='green')
        ax.plot([eurasiaAfrica[98][0], eurasiaAfrica[99][0]], [eurasiaAfrica[98][1], eurasiaAfrica[99][1]], [eurasiaAfrica[98][2], eurasiaAfrica[99][2]], color='green')
        ax.plot([eurasiaAfrica[99][0], eurasiaAfrica[100][0]], [eurasiaAfrica[99][1], eurasiaAfrica[100][1]], [eurasiaAfrica[99][2], eurasiaAfrica[100][2]], color='green')
        ax.plot([eurasiaAfrica[100][0], eurasiaAfrica[101][0]], [eurasiaAfrica[100][1], eurasiaAfrica[101][1]], [eurasiaAfrica[100][2], eurasiaAfrica[101][2]], color='green')
        ax.plot([eurasiaAfrica[101][0], eurasiaAfrica[102][0]], [eurasiaAfrica[101][1], eurasiaAfrica[102][1]], [eurasiaAfrica[101][2], eurasiaAfrica[102][2]], color='green')
        ax.plot([eurasiaAfrica[102][0], eurasiaAfrica[103][0]], [eurasiaAfrica[102][1], eurasiaAfrica[103][1]], [eurasiaAfrica[102][2], eurasiaAfrica[103][2]], color='green')
        ax.plot([eurasiaAfrica[103][0], eurasiaAfrica[104][0]], [eurasiaAfrica[103][1], eurasiaAfrica[104][1]], [eurasiaAfrica[103][2], eurasiaAfrica[104][2]], color='green')
        ax.plot([eurasiaAfrica[104][0], eurasiaAfrica[105][0]], [eurasiaAfrica[104][1], eurasiaAfrica[105][1]], [eurasiaAfrica[104][2], eurasiaAfrica[105][2]], color='green')
        ax.plot([eurasiaAfrica[105][0], eurasiaAfrica[106][0]], [eurasiaAfrica[105][1], eurasiaAfrica[106][1]], [eurasiaAfrica[105][2], eurasiaAfrica[106][2]], color='green')
        ax.plot([eurasiaAfrica[106][0], eurasiaAfrica[107][0]], [eurasiaAfrica[106][1], eurasiaAfrica[107][1]], [eurasiaAfrica[106][2], eurasiaAfrica[107][2]], color='green')
        ax.plot([eurasiaAfrica[107][0], eurasiaAfrica[108][0]], [eurasiaAfrica[107][1], eurasiaAfrica[108][1]], [eurasiaAfrica[107][2], eurasiaAfrica[108][2]], color='green')
        ax.plot([eurasiaAfrica[108][0], eurasiaAfrica[109][0]], [eurasiaAfrica[108][1], eurasiaAfrica[109][1]], [eurasiaAfrica[108][2], eurasiaAfrica[109][2]], color='green')
        ax.plot([eurasiaAfrica[109][0], eurasiaAfrica[110][0]], [eurasiaAfrica[109][1], eurasiaAfrica[110][1]], [eurasiaAfrica[109][2], eurasiaAfrica[110][2]], color='green')
        ax.plot([eurasiaAfrica[110][0], eurasiaAfrica[111][0]], [eurasiaAfrica[110][1], eurasiaAfrica[111][1]], [eurasiaAfrica[110][2], eurasiaAfrica[111][2]], color='green')

        #mediterranean sea
        ax.plot([mediterranean[0][0], mediterranean[1][0]], [mediterranean[0][1], mediterranean[1][1]], [mediterranean[0][2], mediterranean[1][2]], color='green')
        ax.plot([mediterranean[1][0], mediterranean[2][0]], [mediterranean[1][1], mediterranean[2][1]], [mediterranean[1][2], mediterranean[2][2]], color='green')
        ax.plot([mediterranean[2][0], mediterranean[3][0]], [mediterranean[2][1], mediterranean[3][1]], [mediterranean[2][2], mediterranean[3][2]], color='green')
        ax.plot([mediterranean[3][0], mediterranean[4][0]], [mediterranean[3][1], mediterranean[4][1]], [mediterranean[3][2], mediterranean[4][2]], color='green')
        ax.plot([mediterranean[4][0], mediterranean[5][0]], [mediterranean[4][1], mediterranean[5][1]], [mediterranean[4][2], mediterranean[5][2]], color='green')
        ax.plot([mediterranean[5][0], mediterranean[6][0]], [mediterranean[5][1], mediterranean[6][1]], [mediterranean[5][2], mediterranean[6][2]], color='green')
        ax.plot([mediterranean[6][0], mediterranean[7][0]], [mediterranean[6][1], mediterranean[7][1]], [mediterranean[6][2], mediterranean[7][2]], color='green')
        ax.plot([mediterranean[7][0], mediterranean[8][0]], [mediterranean[7][1], mediterranean[8][1]], [mediterranean[7][2], mediterranean[8][2]], color='green')
        ax.plot([mediterranean[8][0], mediterranean[9][0]], [mediterranean[8][1], mediterranean[9][1]], [mediterranean[8][2], mediterranean[9][2]], color='green')
        ax.plot([mediterranean[9][0], mediterranean[10][0]], [mediterranean[9][1], mediterranean[10][1]], [mediterranean[9][2], mediterranean[10][2]], color='green')
        ax.plot([mediterranean[10][0], mediterranean[11][0]], [mediterranean[10][1], mediterranean[11][1]], [mediterranean[10][2], mediterranean[11][2]], color='green')
        ax.plot([mediterranean[11][0], mediterranean[12][0]], [mediterranean[11][1], mediterranean[12][1]], [mediterranean[11][2], mediterranean[12][2]], color='green')
        ax.plot([mediterranean[12][0], mediterranean[13][0]], [mediterranean[12][1], mediterranean[13][1]], [mediterranean[12][2], mediterranean[13][2]], color='green')
        ax.plot([mediterranean[13][0], mediterranean[14][0]], [mediterranean[13][1], mediterranean[14][1]], [mediterranean[13][2], mediterranean[14][2]], color='green')
        ax.plot([mediterranean[14][0], mediterranean[15][0]], [mediterranean[14][1], mediterranean[15][1]], [mediterranean[14][2], mediterranean[15][2]], color='green')
        ax.plot([mediterranean[15][0], mediterranean[16][0]], [mediterranean[15][1], mediterranean[16][1]], [mediterranean[15][2], mediterranean[16][2]], color='green')
        ax.plot([mediterranean[16][0], mediterranean[17][0]], [mediterranean[16][1], mediterranean[17][1]], [mediterranean[16][2], mediterranean[17][2]], color='green')
        ax.plot([mediterranean[17][0], mediterranean[18][0]], [mediterranean[17][1], mediterranean[18][1]], [mediterranean[17][2], mediterranean[18][2]], color='green')
        ax.plot([mediterranean[18][0], mediterranean[19][0]], [mediterranean[18][1], mediterranean[19][1]], [mediterranean[18][2], mediterranean[19][2]], color='green')
        ax.plot([mediterranean[19][0], mediterranean[20][0]], [mediterranean[19][1], mediterranean[20][1]], [mediterranean[19][2], mediterranean[20][2]], color='green')
        ax.plot([mediterranean[20][0], mediterranean[21][0]], [mediterranean[20][1], mediterranean[21][1]], [mediterranean[20][2], mediterranean[21][2]], color='green')
        ax.plot([mediterranean[21][0], mediterranean[22][0]], [mediterranean[21][1], mediterranean[22][1]], [mediterranean[21][2], mediterranean[22][2]], color='green')
        ax.plot([mediterranean[22][0], mediterranean[23][0]], [mediterranean[22][1], mediterranean[23][1]], [mediterranean[22][2], mediterranean[23][2]], color='green')
        ax.plot([mediterranean[23][0], mediterranean[24][0]], [mediterranean[23][1], mediterranean[24][1]], [mediterranean[23][2], mediterranean[24][2]], color='green')
        ax.plot([mediterranean[24][0], mediterranean[25][0]], [mediterranean[24][1], mediterranean[25][1]], [mediterranean[24][2], mediterranean[25][2]], color='green')
        ax.plot([mediterranean[25][0], mediterranean[26][0]], [mediterranean[25][1], mediterranean[26][1]], [mediterranean[25][2], mediterranean[26][2]], color='green')
        ax.plot([mediterranean[26][0], mediterranean[27][0]], [mediterranean[26][1], mediterranean[27][1]], [mediterranean[26][2], mediterranean[27][2]], color='green')
        ax.plot([mediterranean[27][0], mediterranean[28][0]], [mediterranean[27][1], mediterranean[28][1]], [mediterranean[27][2], mediterranean[28][2]], color='green')
        ax.plot([mediterranean[28][0], mediterranean[29][0]], [mediterranean[28][1], mediterranean[29][1]], [mediterranean[28][2], mediterranean[29][2]], color='green')
        ax.plot([mediterranean[29][0], mediterranean[30][0]], [mediterranean[29][1], mediterranean[30][1]], [mediterranean[29][2], mediterranean[30][2]], color='green')
        ax.plot([mediterranean[30][0], mediterranean[31][0]], [mediterranean[30][1], mediterranean[31][1]], [mediterranean[30][2], mediterranean[31][2]], color='green')
        ax.plot([mediterranean[31][0], mediterranean[32][0]], [mediterranean[31][1], mediterranean[32][1]], [mediterranean[31][2], mediterranean[32][2]], color='green')
        ax.plot([mediterranean[32][0], mediterranean[33][0]], [mediterranean[32][1], mediterranean[33][1]], [mediterranean[32][2], mediterranean[33][2]], color='green')
        ax.plot([mediterranean[33][0], mediterranean[34][0]], [mediterranean[33][1], mediterranean[34][1]], [mediterranean[33][2], mediterranean[34][2]], color='green')
        ax.plot([mediterranean[34][0], mediterranean[35][0]], [mediterranean[34][1], mediterranean[35][1]], [mediterranean[34][2], mediterranean[35][2]], color='green')
        ax.plot([mediterranean[35][0], mediterranean[36][0]], [mediterranean[35][1], mediterranean[36][1]], [mediterranean[35][2], mediterranean[36][2]], color='green')
        ax.plot([mediterranean[36][0], mediterranean[37][0]], [mediterranean[36][1], mediterranean[37][1]], [mediterranean[36][2], mediterranean[37][2]], color='green')
        ax.plot([mediterranean[37][0], mediterranean[38][0]], [mediterranean[37][1], mediterranean[38][1]], [mediterranean[37][2], mediterranean[38][2]], color='green')
        ax.plot([mediterranean[38][0], mediterranean[39][0]], [mediterranean[38][1], mediterranean[39][1]], [mediterranean[38][2], mediterranean[39][2]], color='green')
        ax.plot([mediterranean[39][0], mediterranean[40][0]], [mediterranean[39][1], mediterranean[40][1]], [mediterranean[39][2], mediterranean[40][2]], color='green')
        ax.plot([mediterranean[40][0], mediterranean[41][0]], [mediterranean[40][1], mediterranean[41][1]], [mediterranean[40][2], mediterranean[41][2]], color='green')
        ax.plot([mediterranean[41][0], mediterranean[42][0]], [mediterranean[41][1], mediterranean[42][1]], [mediterranean[41][2], mediterranean[42][2]], color='green')
        ax.plot([mediterranean[42][0], mediterranean[43][0]], [mediterranean[42][1], mediterranean[43][1]], [mediterranean[42][2], mediterranean[43][2]], color='green')
        ax.plot([mediterranean[43][0], mediterranean[44][0]], [mediterranean[43][1], mediterranean[44][1]], [mediterranean[43][2], mediterranean[44][2]], color='green')

        #UK
        ax.plot([uk[0][0], uk[1][0]], [uk[0][1], uk[1][1]], [uk[0][2], uk[1][2]], color='green')
        ax.plot([uk[1][0], uk[2][0]], [uk[1][1], uk[2][1]], [uk[1][2], uk[2][2]], color='green')
        ax.plot([uk[2][0], uk[3][0]], [uk[2][1], uk[3][1]], [uk[2][2], uk[3][2]], color='green')
        ax.plot([uk[3][0], uk[4][0]], [uk[3][1], uk[4][1]], [uk[3][2], uk[4][2]], color='green')
        ax.plot([uk[4][0], uk[5][0]], [uk[4][1], uk[5][1]], [uk[4][2], uk[5][2]], color='green')
        ax.plot([uk[5][0], uk[6][0]], [uk[5][1], uk[6][1]], [uk[5][2], uk[6][2]], color='green')
        ax.plot([uk[6][0], uk[7][0]], [uk[6][1], uk[7][1]], [uk[6][2], uk[7][2]], color='green')
        ax.plot([uk[7][0], uk[8][0]], [uk[7][1], uk[8][1]], [uk[7][2], uk[8][2]], color='green')
        ax.plot([uk[8][0], uk[9][0]], [uk[8][1], uk[9][1]], [uk[8][2], uk[9][2]], color='green')
        ax.plot([uk[9][0], uk[10][0]], [uk[9][1], uk[10][1]], [uk[9][2], uk[10][2]], color='green')
        ax.plot([uk[10][0], uk[11][0]], [uk[10][1], uk[11][1]], [uk[10][2], uk[11][2]], color='green')
        ax.plot([uk[11][0], uk[12][0]], [uk[11][1], uk[12][1]], [uk[11][2], uk[12][2]], color='green')
        ax.plot([uk[12][0], uk[13][0]], [uk[12][1], uk[13][1]], [uk[12][2], uk[13][2]], color='green')
        ax.plot([uk[13][0], uk[14][0]], [uk[13][1], uk[14][1]], [uk[13][2], uk[14][2]], color='green')
        ax.plot([uk[14][0], uk[15][0]], [uk[14][1], uk[15][1]], [uk[14][2], uk[15][2]], color='green')
        ax.plot([uk[15][0], uk[16][0]], [uk[15][1], uk[16][1]], [uk[15][2], uk[16][2]], color='green')
        ax.plot([uk[16][0], uk[17][0]], [uk[16][1], uk[17][1]], [uk[16][2], uk[17][2]], color='green')
        ax.plot([uk[17][0], uk[18][0]], [uk[17][1], uk[18][1]], [uk[17][2], uk[18][2]], color='green')
        ax.plot([uk[18][0], uk[19][0]], [uk[18][1], uk[19][1]], [uk[18][2], uk[19][2]], color='green')
        ax.plot([uk[19][0], uk[20][0]], [uk[19][1], uk[20][1]], [uk[19][2], uk[20][2]], color='green')
        ax.plot([uk[20][0], uk[21][0]], [uk[20][1], uk[21][1]], [uk[20][2], uk[21][2]], color='green')
        ax.plot([uk[21][0], uk[22][0]], [uk[21][1], uk[22][1]], [uk[21][2], uk[22][2]], color='green')
        ax.plot([uk[22][0], uk[23][0]], [uk[22][1], uk[23][1]], [uk[22][2], uk[23][2]], color='green')
        ax.plot([uk[23][0], uk[24][0]], [uk[23][1], uk[24][1]], [uk[23][2], uk[24][2]], color='green')
        ax.plot([uk[24][0], uk[25][0]], [uk[24][1], uk[25][1]], [uk[24][2], uk[25][2]], color='green')

        #Japan
        ax.plot([japan[0][0], japan[1][0]], [japan[0][1], japan[1][1]], [japan[0][2], japan[1][2]], color='green')
        ax.plot([japan[1][0], japan[2][0]], [japan[1][1], japan[2][1]], [japan[1][2], japan[2][2]], color='green')
        ax.plot([japan[2][0], japan[3][0]], [japan[2][1], japan[3][1]], [japan[2][2], japan[3][2]], color='green')
        ax.plot([japan[3][0], japan[4][0]], [japan[3][1], japan[4][1]], [japan[3][2], japan[4][2]], color='green')
        ax.plot([japan[4][0], japan[5][0]], [japan[4][1], japan[5][1]], [japan[4][2], japan[5][2]], color='green')
        ax.plot([japan[5][0], japan[6][0]], [japan[5][1], japan[6][1]], [japan[5][2], japan[6][2]], color='green')
        ax.plot([japan[6][0], japan[7][0]], [japan[6][1], japan[7][1]], [japan[6][2], japan[7][2]], color='green')
        ax.plot([japan[7][0], japan[8][0]], [japan[7][1], japan[8][1]], [japan[7][2], japan[8][2]], color='green')
        ax.plot([japan[8][0], japan[9][0]], [japan[8][1], japan[9][1]], [japan[8][2], japan[9][2]], color='green')
        ax.plot([japan[9][0], japan[10][0]], [japan[9][1], japan[10][1]], [japan[9][2], japan[10][2]], color='green')
        ax.plot([japan[10][0], japan[11][0]], [japan[10][1], japan[11][1]], [japan[10][2], japan[11][2]], color='green')
        ax.plot([japan[11][0], japan[12][0]], [japan[11][1], japan[12][1]], [japan[11][2], japan[12][2]], color='green')
        ax.plot([japan[12][0], japan[13][0]], [japan[12][1], japan[13][1]], [japan[12][2], japan[13][2]], color='green')
        ax.plot([japan[13][0], japan[14][0]], [japan[13][1], japan[14][1]], [japan[13][2], japan[14][2]], color='green')
        ax.plot([japan[14][0], japan[15][0]], [japan[14][1], japan[15][1]], [japan[14][2], japan[15][2]], color='green')
        ax.plot([japan[15][0], japan[16][0]], [japan[15][1], japan[16][1]], [japan[15][2], japan[16][2]], color='green')
        ax.plot([japan[16][0], japan[17][0]], [japan[16][1], japan[17][1]], [japan[16][2], japan[17][2]], color='green')
        ax.plot([japan[17][0], japan[18][0]], [japan[17][1], japan[18][1]], [japan[17][2], japan[18][2]], color='green')
        ax.plot([japan[18][0], japan[19][0]], [japan[18][1], japan[19][1]], [japan[18][2], japan[19][2]], color='green')
        ax.plot([japan[19][0], japan[20][0]], [japan[19][1], japan[20][1]], [japan[19][2], japan[20][2]], color='green')
        ax.plot([japan[20][0], japan[21][0]], [japan[20][1], japan[21][1]], [japan[20][2], japan[21][2]], color='green')
        ax.plot([japan[21][0], japan[22][0]], [japan[21][1], japan[22][1]], [japan[21][2], japan[22][2]], color='green')
        ax.plot([japan[22][0], japan[23][0]], [japan[22][1], japan[23][1]], [japan[22][2], japan[23][2]], color='green')
        ax.plot([japan[23][0], japan[24][0]], [japan[23][1], japan[24][1]], [japan[23][2], japan[24][2]], color='green')

        #Philippines
        ax.plot([philippines[0][0], philippines[1][0]], [philippines[0][1], philippines[1][1]], [philippines[0][2], philippines[1][2]], color='green')
        ax.plot([philippines[1][0], philippines[2][0]], [philippines[1][1], philippines[2][1]], [philippines[1][2], philippines[2][2]], color='green')
        ax.plot([philippines[2][0], philippines[3][0]], [philippines[2][1], philippines[3][1]], [philippines[2][2], philippines[3][2]], color='green')
        ax.plot([philippines[3][0], philippines[4][0]], [philippines[3][1], philippines[4][1]], [philippines[3][2], philippines[4][2]], color='green')
        ax.plot([philippines[4][0], philippines[5][0]], [philippines[4][1], philippines[5][1]], [philippines[4][2], philippines[5][2]], color='green')
        ax.plot([philippines[5][0], philippines[6][0]], [philippines[5][1], philippines[6][1]], [philippines[5][2], philippines[6][2]], color='green')
        ax.plot([philippines[6][0], philippines[7][0]], [philippines[6][1], philippines[7][1]], [philippines[6][2], philippines[7][2]], color='green')
        ax.plot([philippines[7][0], philippines[8][0]], [philippines[7][1], philippines[8][1]], [philippines[7][2], philippines[8][2]], color='green')
        ax.plot([philippines[8][0], philippines[9][0]], [philippines[8][1], philippines[9][1]], [philippines[8][2], philippines[9][2]], color='green')
        ax.plot([philippines[9][0], philippines[10][0]], [philippines[9][1], philippines[10][1]], [philippines[9][2], philippines[10][2]], color='green')
        ax.plot([philippines[10][0], philippines[11][0]], [philippines[10][1], philippines[11][1]], [philippines[10][2], philippines[11][2]], color='green')
        ax.plot([philippines[11][0], philippines[12][0]], [philippines[11][1], philippines[12][1]], [philippines[11][2], philippines[12][2]], color='green')

        #Indonesia
        ax.plot([indonesia[0][0], indonesia[1][0]], [indonesia[0][1], indonesia[1][1]], [indonesia[0][2], indonesia[1][2]], color='green')
        ax.plot([indonesia[1][0], indonesia[2][0]], [indonesia[1][1], indonesia[2][1]], [indonesia[1][2], indonesia[2][2]], color='green')
        ax.plot([indonesia[2][0], indonesia[3][0]], [indonesia[2][1], indonesia[3][1]], [indonesia[2][2], indonesia[3][2]], color='green')
        ax.plot([indonesia[3][0], indonesia[4][0]], [indonesia[3][1], indonesia[4][1]], [indonesia[3][2], indonesia[4][2]], color='green')
        ax.plot([indonesia[4][0], indonesia[5][0]], [indonesia[4][1], indonesia[5][1]], [indonesia[4][2], indonesia[5][2]], color='green')
        ax.plot([indonesia[5][0], indonesia[6][0]], [indonesia[5][1], indonesia[6][1]], [indonesia[5][2], indonesia[6][2]], color='green')
        ax.plot([indonesia[6][0], indonesia[7][0]], [indonesia[6][1], indonesia[7][1]], [indonesia[6][2], indonesia[7][2]], color='green')
        ax.plot([indonesia[7][0], indonesia[8][0]], [indonesia[7][1], indonesia[8][1]], [indonesia[7][2], indonesia[8][2]], color='green')
        ax.plot([indonesia[8][0], indonesia[9][0]], [indonesia[8][1], indonesia[9][1]], [indonesia[8][2], indonesia[9][2]], color='green')
        ax.plot([indonesia[9][0], indonesia[10][0]], [indonesia[9][1], indonesia[10][1]], [indonesia[9][2], indonesia[10][2]], color='green')
        ax.plot([indonesia[10][0], indonesia[11][0]], [indonesia[10][1], indonesia[11][1]], [indonesia[10][2], indonesia[11][2]], color='green')
        ax.plot([indonesia[11][0], indonesia[12][0]], [indonesia[11][1], indonesia[12][1]], [indonesia[11][2], indonesia[12][2]], color='green')
        ax.plot([indonesia[12][0], indonesia[13][0]], [indonesia[12][1], indonesia[13][1]], [indonesia[12][2], indonesia[13][2]], color='green')
        ax.plot([indonesia[13][0], indonesia[14][0]], [indonesia[13][1], indonesia[14][1]], [indonesia[13][2], indonesia[14][2]], color='green')
        ax.plot([indonesia[14][0], indonesia[15][0]], [indonesia[14][1], indonesia[15][1]], [indonesia[14][2], indonesia[15][2]], color='green')
        ax.plot([indonesia[15][0], indonesia[16][0]], [indonesia[15][1], indonesia[16][1]], [indonesia[15][2], indonesia[16][2]], color='green')
        ax.plot([indonesia[16][0], indonesia[17][0]], [indonesia[16][1], indonesia[17][1]], [indonesia[16][2], indonesia[17][2]], color='green')
        ax.plot([indonesia[17][0], indonesia[18][0]], [indonesia[17][1], indonesia[18][1]], [indonesia[17][2], indonesia[18][2]], color='green')
        ax.plot([indonesia[18][0], indonesia[19][0]], [indonesia[18][1], indonesia[19][1]], [indonesia[18][2], indonesia[19][2]], color='green')
        ax.plot([indonesia[19][0], indonesia[20][0]], [indonesia[19][1], indonesia[20][1]], [indonesia[19][2], indonesia[20][2]], color='green')

        ax.plot([indonesia2[0][0], indonesia2[1][0]], [indonesia2[0][1], indonesia2[1][1]], [indonesia2[0][2], indonesia2[1][2]], color='green')
        ax.plot([indonesia2[1][0], indonesia2[2][0]], [indonesia2[1][1], indonesia2[2][1]], [indonesia2[1][2], indonesia2[2][2]], color='green')
        ax.plot([indonesia2[2][0], indonesia2[3][0]], [indonesia2[2][1], indonesia2[3][1]], [indonesia2[2][2], indonesia2[3][2]], color='green')
        ax.plot([indonesia2[3][0], indonesia2[4][0]], [indonesia2[3][1], indonesia2[4][1]], [indonesia2[3][2], indonesia2[4][2]], color='green')
        ax.plot([indonesia2[4][0], indonesia2[5][0]], [indonesia2[4][1], indonesia2[5][1]], [indonesia2[4][2], indonesia2[5][2]], color='green')
        ax.plot([indonesia2[5][0], indonesia2[6][0]], [indonesia2[5][1], indonesia2[6][1]], [indonesia2[5][2], indonesia2[6][2]], color='green')
        ax.plot([indonesia2[6][0], indonesia2[7][0]], [indonesia2[6][1], indonesia2[7][1]], [indonesia2[6][2], indonesia2[7][2]], color='green')
        ax.plot([indonesia2[7][0], indonesia2[8][0]], [indonesia2[7][1], indonesia2[8][1]], [indonesia2[7][2], indonesia2[8][2]], color='green')
        ax.plot([indonesia2[8][0], indonesia2[9][0]], [indonesia2[8][1], indonesia2[9][1]], [indonesia2[8][2], indonesia2[9][2]], color='green')

        ax.plot([indonesia3[0][0], indonesia3[1][0]], [indonesia3[0][1], indonesia3[1][1]], [indonesia3[0][2], indonesia3[1][2]], color='green')
        ax.plot([indonesia3[1][0], indonesia3[2][0]], [indonesia3[1][1], indonesia3[2][1]], [indonesia3[1][2], indonesia3[2][2]], color='green')
        ax.plot([indonesia3[2][0], indonesia3[3][0]], [indonesia3[2][1], indonesia3[3][1]], [indonesia3[2][2], indonesia3[3][2]], color='green')
        ax.plot([indonesia3[3][0], indonesia3[4][0]], [indonesia3[3][1], indonesia3[4][1]], [indonesia3[3][2], indonesia3[4][2]], color='green')
        ax.plot([indonesia3[4][0], indonesia3[5][0]], [indonesia3[4][1], indonesia3[5][1]], [indonesia3[4][2], indonesia3[5][2]], color='green')
        ax.plot([indonesia3[5][0], indonesia3[6][0]], [indonesia3[5][1], indonesia3[6][1]], [indonesia3[5][2], indonesia3[6][2]], color='green')
        ax.plot([indonesia3[6][0], indonesia3[7][0]], [indonesia3[6][1], indonesia3[7][1]], [indonesia3[6][2], indonesia3[7][2]], color='green')
        ax.plot([indonesia3[7][0], indonesia3[8][0]], [indonesia3[7][1], indonesia3[8][1]], [indonesia3[7][2], indonesia3[8][2]], color='green')
        ax.plot([indonesia3[8][0], indonesia3[9][0]], [indonesia3[8][1], indonesia3[9][1]], [indonesia3[8][2], indonesia3[9][2]], color='green')
        ax.plot([indonesia3[9][0], indonesia3[10][0]], [indonesia3[9][1], indonesia3[10][1]], [indonesia3[9][2], indonesia3[10][2]], color='green')
        ax.plot([indonesia3[10][0], indonesia3[11][0]], [indonesia3[10][1], indonesia3[11][1]], [indonesia3[10][2], indonesia3[11][2]], color='green')
        ax.plot([indonesia3[11][0], indonesia3[12][0]], [indonesia3[11][1], indonesia3[12][1]], [indonesia3[11][2], indonesia3[12][2]], color='green')
        ax.plot([indonesia3[12][0], indonesia3[13][0]], [indonesia3[12][1], indonesia3[13][1]], [indonesia3[12][2], indonesia3[13][2]], color='green')
        ax.plot([indonesia3[13][0], indonesia3[14][0]], [indonesia3[13][1], indonesia3[14][1]], [indonesia3[13][2], indonesia3[14][2]], color='green')
        ax.plot([indonesia3[14][0], indonesia3[15][0]], [indonesia3[14][1], indonesia3[15][1]], [indonesia3[14][2], indonesia3[15][2]], color='green')

        #Australia
        ax.plot([australia[0][0], australia[1][0]], [australia[0][1], australia[1][1]], [australia[0][2], australia[1][2]], color='green')
        ax.plot([australia[1][0], australia[2][0]], [australia[1][1], australia[2][1]], [australia[1][2], australia[2][2]], color='green')
        ax.plot([australia[2][0], australia[3][0]], [australia[2][1], australia[3][1]], [australia[2][2], australia[3][2]], color='green')
        ax.plot([australia[3][0], australia[4][0]], [australia[3][1], australia[4][1]], [australia[3][2], australia[4][2]], color='green')
        ax.plot([australia[4][0], australia[5][0]], [australia[4][1], australia[5][1]], [australia[4][2], australia[5][2]], color='green')
        ax.plot([australia[5][0], australia[6][0]], [australia[5][1], australia[6][1]], [australia[5][2], australia[6][2]], color='green')
        ax.plot([australia[6][0], australia[7][0]], [australia[6][1], australia[7][1]], [australia[6][2], australia[7][2]], color='green')
        ax.plot([australia[7][0], australia[8][0]], [australia[7][1], australia[8][1]], [australia[7][2], australia[8][2]], color='green')
        ax.plot([australia[8][0], australia[9][0]], [australia[8][1], australia[9][1]], [australia[8][2], australia[9][2]], color='green')
        ax.plot([australia[9][0], australia[10][0]], [australia[9][1], australia[10][1]], [australia[9][2], australia[10][2]], color='green')
        ax.plot([australia[10][0], australia[11][0]], [australia[10][1], australia[11][1]], [australia[10][2], australia[11][2]], color='green')
        ax.plot([australia[11][0], australia[12][0]], [australia[11][1], australia[12][1]], [australia[11][2], australia[12][2]], color='green')
        ax.plot([australia[12][0], australia[13][0]], [australia[12][1], australia[13][1]], [australia[12][2], australia[13][2]], color='green')
        ax.plot([australia[13][0], australia[14][0]], [australia[13][1], australia[14][1]], [australia[13][2], australia[14][2]], color='green')
        ax.plot([australia[14][0], australia[15][0]], [australia[14][1], australia[15][1]], [australia[14][2], australia[15][2]], color='green')
        ax.plot([australia[15][0], australia[16][0]], [australia[15][1], australia[16][1]], [australia[15][2], australia[16][2]], color='green')
        ax.plot([australia[16][0], australia[17][0]], [australia[16][1], australia[17][1]], [australia[16][2], australia[17][2]], color='green')
        ax.plot([australia[17][0], australia[18][0]], [australia[17][1], australia[18][1]], [australia[17][2], australia[18][2]], color='green')
        ax.plot([australia[18][0], australia[19][0]], [australia[18][1], australia[19][1]], [australia[18][2], australia[19][2]], color='green')
        ax.plot([australia[19][0], australia[20][0]], [australia[19][1], australia[20][1]], [australia[19][2], australia[20][2]], color='green')
        ax.plot([australia[20][0], australia[21][0]], [australia[20][1], australia[21][1]], [australia[20][2], australia[21][2]], color='green')
        ax.plot([australia[21][0], australia[22][0]], [australia[21][1], australia[22][1]], [australia[21][2], australia[22][2]], color='green')

#Plots all of the routes connecting neighboring cities
#Because the graph is undirected, can ignore duplicates
def plotRoutes():
        #Tokyo, Japan
        ax.plot([cityCoords[0][0], cityCoords[9][0]], [cityCoords[0][1], cityCoords[9][1]], [cityCoords[0][2], cityCoords[9][2]], color='gold')
        ax.plot([cityCoords[0][0], cityCoords[34][0]], [cityCoords[0][1], cityCoords[34][1]], [cityCoords[0][2], cityCoords[34][2]], color='gold')
        ax.plot([cityCoords[0][0], cityCoords[33][0]], [cityCoords[0][1], cityCoords[33][1]], [cityCoords[0][2], cityCoords[33][2]], color='gold')
        #Delhi, India
        ax.plot([cityCoords[1][0], cityCoords[11][0]], [cityCoords[1][1], cityCoords[11][1]], [cityCoords[1][2], cityCoords[11][2]], color='gold')
        ax.plot([cityCoords[1][0], cityCoords[15][0]], [cityCoords[1][1], cityCoords[15][1]], [cityCoords[1][2], cityCoords[15][2]], color='gold')
        ax.plot([cityCoords[1][0], cityCoords[35][0]], [cityCoords[1][1], cityCoords[35][1]], [cityCoords[1][2], cityCoords[35][2]], color='gold')
        #Shanghai, China
        ax.plot([cityCoords[2][0], cityCoords[33][0]], [cityCoords[2][1], cityCoords[33][1]], [cityCoords[2][2], cityCoords[33][2]], color='gold')
        ax.plot([cityCoords[2][0], cityCoords[13][0]], [cityCoords[2][1], cityCoords[13][1]], [cityCoords[2][2], cityCoords[13][2]], color='gold')
        ax.plot([cityCoords[2][0], cityCoords[7][0]], [cityCoords[2][1], cityCoords[7][1]], [cityCoords[2][2], cityCoords[7][2]], color='gold')
        ax.plot([cityCoords[2][0], cityCoords[19][0]], [cityCoords[2][1], cityCoords[19][1]], [cityCoords[2][2], cityCoords[19][2]], color='gold')
        ax.plot([cityCoords[2][0], cityCoords[21][0]], [cityCoords[2][1], cityCoords[21][1]], [cityCoords[2][2], cityCoords[21][2]], color='gold')
        #Sao Paulo, Brazil
        ax.plot([cityCoords[3][0], cityCoords[18][0]], [cityCoords[3][1], cityCoords[18][1]], [cityCoords[3][2], cityCoords[18][2]], color='gold')
        ax.plot([cityCoords[3][0], cityCoords[12][0]], [cityCoords[3][1], cityCoords[12][1]], [cityCoords[3][2], cityCoords[12][2]], color='gold')
        ax.plot([cityCoords[3][0], cityCoords[28][0]], [cityCoords[3][1], cityCoords[28][1]], [cityCoords[3][2], cityCoords[28][2]], color='gold')
        #Mexico City, Mexico
        ax.plot([cityCoords[4][0], cityCoords[28][0]], [cityCoords[4][1], cityCoords[28][1]], [cityCoords[4][2], cityCoords[28][2]], color='gold')
        ax.plot([cityCoords[4][0], cityCoords[22][0]], [cityCoords[4][1], cityCoords[22][1]], [cityCoords[4][2], cityCoords[22][2]], color='gold')
        #Cairo, Egypt
        ax.plot([cityCoords[5][0], cityCoords[14][0]], [cityCoords[5][1], cityCoords[14][1]], [cityCoords[5][2], cityCoords[14][2]], color='gold')
        ax.plot([cityCoords[5][0], cityCoords[37][0]], [cityCoords[5][1], cityCoords[37][1]], [cityCoords[5][2], cityCoords[37][2]], color='gold')
        ax.plot([cityCoords[5][0], cityCoords[17][0]], [cityCoords[5][1], cityCoords[17][1]], [cityCoords[5][2], cityCoords[17][2]], color='gold')
        ax.plot([cityCoords[5][0], cityCoords[20][0]], [cityCoords[5][1], cityCoords[20][1]], [cityCoords[5][2], cityCoords[20][2]], color='gold')
        #Mumbai, India
        ax.plot([cityCoords[6][0], cityCoords[11][0]], [cityCoords[6][1], cityCoords[11][1]], [cityCoords[6][2], cityCoords[11][2]], color='gold')
        ax.plot([cityCoords[6][0], cityCoords[35][0]], [cityCoords[6][1], cityCoords[35][1]], [cityCoords[6][2], cityCoords[35][2]], color='gold')
        ax.plot([cityCoords[6][0], cityCoords[26][0]], [cityCoords[6][1], cityCoords[26][1]], [cityCoords[6][2], cityCoords[26][2]], color='gold')
        #Beijing, China
        ax.plot([cityCoords[7][0], cityCoords[19][0]], [cityCoords[7][1], cityCoords[19][1]], [cityCoords[7][2], cityCoords[19][2]], color='gold')
        #Dhaka, Bangladesh
        ax.plot([cityCoords[8][0], cityCoords[15][0]], [cityCoords[8][1], cityCoords[15][1]], [cityCoords[8][2], cityCoords[15][2]], color='gold')
        ax.plot([cityCoords[8][0], cityCoords[39][0]], [cityCoords[8][1], cityCoords[39][1]], [cityCoords[8][2], cityCoords[39][2]], color='gold')
        ax.plot([cityCoords[8][0], cityCoords[13][0]], [cityCoords[8][1], cityCoords[13][1]], [cityCoords[8][2], cityCoords[13][2]], color='gold')
        ax.plot([cityCoords[8][0], cityCoords[32][0]], [cityCoords[8][1], cityCoords[32][1]], [cityCoords[8][2], cityCoords[32][2]], color='gold')
        #Osaka, Japan
        ax.plot([cityCoords[9][0], cityCoords[34][0]], [cityCoords[9][1], cityCoords[34][1]], [cityCoords[9][2], cityCoords[34][2]], color='gold')
        #New York, USA
        ax.plot([cityCoords[10][0], cityCoords[38][0]], [cityCoords[10][1], cityCoords[38][1]], [cityCoords[10][2], cityCoords[38][2]], color='gold')
        ax.plot([cityCoords[10][0], cityCoords[36][0]], [cityCoords[10][1], cityCoords[36][1]], [cityCoords[10][2], cityCoords[36][2]], color='gold')
        #Karachi, Pakistan
        ax.plot([cityCoords[11][0], cityCoords[25][0]], [cityCoords[11][1], cityCoords[25][1]], [cityCoords[11][2], cityCoords[25][2]], color='gold')
        ax.plot([cityCoords[11][0], cityCoords[37][0]], [cityCoords[11][1], cityCoords[37][1]], [cityCoords[11][2], cityCoords[37][2]], color='gold')
        #Buenos Aires, Argentina
        ax.plot([cityCoords[12][0], cityCoords[18][0]], [cityCoords[12][1], cityCoords[18][1]], [cityCoords[12][2], cityCoords[18][2]], color='gold')
        ax.plot([cityCoords[12][0], cityCoords[31][0]], [cityCoords[12][1], cityCoords[31][1]], [cityCoords[12][2], cityCoords[31][2]], color='gold')
        #Chongqing, China
        ax.plot([cityCoords[13][0], cityCoords[39][0]], [cityCoords[13][1], cityCoords[39][1]], [cityCoords[13][2], cityCoords[39][2]], color='gold')
        ax.plot([cityCoords[13][0], cityCoords[21][0]], [cityCoords[13][1], cityCoords[21][1]], [cityCoords[13][2], cityCoords[21][2]], color='gold')
        #Istanbul, Turkey
        ax.plot([cityCoords[14][0], cityCoords[23][0]], [cityCoords[14][1], cityCoords[23][1]], [cityCoords[14][2], cityCoords[23][2]], color='gold')
        ax.plot([cityCoords[14][0], cityCoords[27][0]], [cityCoords[14][1], cityCoords[27][1]], [cityCoords[14][2], cityCoords[27][2]], color='gold')
        #Kolkata, India
        ax.plot([cityCoords[15][0], cityCoords[30][0]], [cityCoords[15][1], cityCoords[30][1]], [cityCoords[15][2], cityCoords[30][2]], color='gold')
        ax.plot([cityCoords[15][0], cityCoords[35][0]], [cityCoords[15][1], cityCoords[35][1]], [cityCoords[15][2], cityCoords[35][2]], color='gold')
        #Manila, Philippines
        ax.plot([cityCoords[16][0], cityCoords[29][0]], [cityCoords[16][1], cityCoords[29][1]], [cityCoords[16][2], cityCoords[29][2]], color='gold')
        ax.plot([cityCoords[16][0], cityCoords[32][0]], [cityCoords[16][1], cityCoords[32][1]], [cityCoords[16][2], cityCoords[32][2]], color='gold')
        ax.plot([cityCoords[16][0], cityCoords[24][0]], [cityCoords[16][1], cityCoords[24][1]], [cityCoords[16][2], cityCoords[24][2]], color='gold')
        #Lagos, Nigeria
        ax.plot([cityCoords[17][0], cityCoords[20][0]], [cityCoords[17][1], cityCoords[20][1]], [cityCoords[17][2], cityCoords[20][2]], color='gold')
        #Rio de Janeiro (18) (plotted)
        #Tianjin, China (19) (plotted)
        #Kinshasa, DR Congo (20) (plotted)
        #Guangzhou, China
        ax.plot([cityCoords[21][0], cityCoords[24][0]], [cityCoords[21][1], cityCoords[24][1]], [cityCoords[21][2], cityCoords[24][2]], color='gold')
        #Los Angeles, USA
        ax.plot([cityCoords[22][0], cityCoords[38][0]], [cityCoords[22][1], cityCoords[38][1]], [cityCoords[22][2], cityCoords[38][2]], color='gold')
        #Moscow, Russia
        ax.plot([cityCoords[23][0], cityCoords[27][0]], [cityCoords[23][1], cityCoords[27][1]], [cityCoords[23][2], cityCoords[27][2]], color='gold')
        #Shenzhen, China (24) (plotted)
        #Lahore, Pakistan (25) (plotted)
        #Bangalore, India
        ax.plot([cityCoords[26][0], cityCoords[30][0]], [cityCoords[26][1], cityCoords[30][1]], [cityCoords[26][2], cityCoords[30][2]], color='gold')
        ax.plot([cityCoords[26][0], cityCoords[35][0]], [cityCoords[26][1], cityCoords[35][1]], [cityCoords[26][2], cityCoords[35][2]], color='gold')
        #Paris, France
        ax.plot([cityCoords[27][0], cityCoords[36][0]], [cityCoords[27][1], cityCoords[36][1]], [cityCoords[27][2], cityCoords[36][2]], color='gold')
        #Bogotá, Colombia
        ax.plot([cityCoords[28][0], cityCoords[31][0]], [cityCoords[28][1], cityCoords[31][1]], [cityCoords[28][2], cityCoords[31][2]], color='gold')
        #Jakarta, Indonesia
        ax.plot([cityCoords[29][0], cityCoords[32][0]], [cityCoords[29][1], cityCoords[32][1]], [cityCoords[29][2], cityCoords[32][2]], color='gold')
        #Chennai, India
        ax.plot([cityCoords[30][0], cityCoords[35][0]], [cityCoords[30][1], cityCoords[35][1]], [cityCoords[30][2], cityCoords[35][2]], color='gold')
        #Lima, Peru (31) (plotted)
        #Bangkok, Thailand (32) (plotted)
        #Seoul, South Korea (33) (plotted)
        #Nagoya, Japan (34) (plotted)
        #Hyderabad, India (35) (plotted)
        #London, United Kingdom (36) (plotted)
        #Tehran, Iran (37) (plotted)
        #Chicago, USA (38) (plotted)
        #Chengdu, China (39) (plotted)

#Plots red lines/points for cities/routes along the shortest path
def plotPath(path):
        #Print highlighted lines/points for each line in the path
        for i in range(0, len(path)-1):
                ax.plot([cityCoords[list(longLat.keys()).index(path[i])][0], cityCoords[list(longLat.keys()).index(path[i+1])][0]], 
                        [cityCoords[list(longLat.keys()).index(path[i])][1], cityCoords[list(longLat.keys()).index(path[i+1])][1]],
                        [cityCoords[list(longLat.keys()).index(path[i])][2], cityCoords[list(longLat.keys()).index(path[i+1])][2]],
                        color='red')
                ax.scatter(cityCoords[list(longLat.keys()).index(path[i])][0], 
                        cityCoords[list(longLat.keys()).index(path[i])][1], 
                        cityCoords[list(longLat.keys()).index(path[i])][2], 
                        color='red')
        #plot highlighted destination point
        ax.scatter(cityCoords[list(longLat.keys()).index(path[len(path)-1])][0], 
                cityCoords[list(longLat.keys()).index(path[len(path)-1])][1], 
                cityCoords[list(longLat.keys()).index(path[len(path)-1])][2], 
                color='red')

def makeAnimation(path):
        #Array to store all animation frames 
        global animationArray
        animationArray = []
        #For each city in the path, calculate the degree of rotation for the frame in the animation
        for i in range(0, len(path)-1):
                longDiff = longLat[path[i+1]][0] - longLat[path[i]][0]
                latDiff = longLat[path[i+1]][1] - longLat[path[i]][1]
                longInc = longDiff/10
                latInc = latDiff/10
                #appends the rotation of the starting city for each move
                animationArray.append([longLat[path[i]][0], longLat[path[i]][1]])
                #for 10 frames
                for j in range(1, 11):
                        #appends rotation for each frame incremented by longInc and latInc
                        #to arrie at the destination in 10 frames
                        animationArray.append([longLat[path[i]][0] + longInc*j, longLat[path[i]][1] + latInc*j])

def main():
        print("\n                      ╔══════════════════╗")
        print(  "══════════════════════╣  STRANDED SANTA  ╠═════════════════════")
        print(  "                      ╚══════════════════╝")
        print("""Santa's sleigh is in the workshop, so this Christmas he has to
deliver presents on foot! Pick two cities to plot the shortest
path between them so Santa can deliver presents on time.""") 
        print(  "═══════════════════════════════════════════════════════════════\n")
        #Take user input for origin/destination
        print("""                        0. Tokyo, Japan
                        1. Delhi, India
                        2. Shanghai, China
                        3. São Paulo, Brazil
                        4. Mexico City, Mexico
                        5. Cairo, Egypt
                        6. Mumbai, India
                        7. Beijing, China
                        8. Dhaka, Bangladesh
                        9. Osaka, Japan
                        10. New York, USA
                        11. Karachi, Pakistan
                        12. Buenos Aires, Argentina
                        13. Chongqing, China
                        14. Istanbul, Turkey
                        15. Kolkata, India
                        16. Manila, Philippines
                        17. Lagos, Nigeria
                        18. Rio de Janeiro, Brazil
                        19. Tianjin, China
                        20. Kinshasa, DR Congo
                        21. Guangzhou, China
                        22. Los Angeles, USA
                        23. Moscow, Russia
                        24. Shenzhen, China
                        25. Lahore, Pakistan
                        26. Bangalore, India
                        27. Paris, France
                        28. Bogotá, Colombia
                        29. Jakarta, Indonesia
                        30. Chennai, India
                        31. Lima, Peru
                        32. Bangkok, Thailand
                        33. Seoul, South Korea
                        34. Nagoya, Japan
                        35. Hyderabad, India
                        36. London, United Kingdom
                        37. Tehran, Iran
                        38. Chicago, USA
                        39. Chengdu, China\n""")
        print(  "═══════════════════════════════════════════════════════════════\n")

        #Get origin city and destination from user input
        while (True):
                try:
                        source = input("Origin: ")
                        sourceCity = list(longLat.keys())[int(source)]
                        destination = input("Destination: ")
                        destinationCity = list(longLat.keys())[int(destination)]
                        break
                except:
                        print("Please input numbers between 0-39")
                        
        #Plot base city/land/route layout
        plotCities()
        plotLandmass()
        plotRoutes()
        #Initialize graph with set cityRoutes
        graph = Graph(nodes, cityRoutes)
        #Calculate all shortestPaths from the source
        prevNodeInPath, shortestDistance = dijkstra_algorithm(graph=graph, source=sourceCity)
        #Declare path array to hold order of cities to travel from source -> destination
        global path
        path = printPath(prevNodeInPath, shortestDistance, source=sourceCity, destination=destinationCity).copy()
        #Plot red path highlighting the shortest path
        plotPath(path)
        #Prepare animationArray for animating
        makeAnimation(path)

main()

#azimuth: latitude
#elevation: longitude
#Animate rotation
def animate(i):
        ax.view_init(azim=animationArray[i%len(animationArray)][1], elev=animationArray[i%len(animationArray)][0])
        ax.set_title(f'{path[0]} to {path[len(path)-1]}')
        return fig,

anim = animation.FuncAnimation(fig, animate,
                                frames=len(path)*10, interval=5, blit=False)

plt.show()
