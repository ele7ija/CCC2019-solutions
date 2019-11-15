'''
    Note:
        - Country ID is an integer [0, n-1], it is unique and every x from [0, n-1]
        has is a valid Country ID
'''

# Generic/Built-in Libs
from collections import namedtuple
from enum import Enum
from math import sqrt
import heapq

Solar = namedtuple('Solar', ['country', 'price'])
Cell = namedtuple('Cell', ['x', 'y', 'altitude', 'country'])
Point = namedtuple('Point', ['x', 'y'])

MAX_DIST = 1000000

class Matrix:
    def __init__(self):
        self.matrix = []
    
    def append(self, lst):
        self.matrix.append(lst)

    def get_column(self, i):
        return self.matrix[i]

    def __str__(self):
        s = ""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                s += str(self.matrix[i][j]) + "\t"
            s += "\n"
        return s

    @property
    def cols(self):
        return len(self.matrix)

    @property
    def rows(self):
        return len(self.matrix[0])


    def _on_border(self, cell):
        # is it on the edge of the matrix
        if (cell.x == 0 or cell.y == 0 or cell.x == self.rows - 1 or cell.y == self.cols - 1):
            return True
        
        # is one of it's neighbours a cell from a different country
        if (self.matrix[cell.y][cell.x-1].country != cell.country):
            return True
        if (self.matrix[cell.y][cell.x+1].country != cell.country):
            return True
        if (self.matrix[cell.y-1][cell.x].country != cell.country):
            return True
        if (self.matrix[cell.y+1][cell.x].country != cell.country):
            return True

        return False


    def _mhtn_dist(self, cell1, cell2):
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

    def _find_closest(self, cell, cells):
        min_dist = self.rows + self.cols + 2
        closest_cell = None
        for cell2 in cells:
            # IMPORTANT
            if self._on_border(cell2):
                continue
            dist = self._mhtn_dist(cell, cell2) 
            if dist < min_dist:
                min_dist = dist
                closest_cell = cell2
            elif dist == min_dist:
                if cell2.x < closest_cell.x:
                    min_dist = dist
                    closest_cell = cell2
        return closest_cell


    def find_capitals(self):
        # Find the average x, average y
        # 
        # Country_data = namedtuple('Country_data', ['xsum', 'ysum', 'n', 'cells'])
        # 
        data = {}
        for row in self.matrix:
            for cell in row:
                if cell.country in data:
                    data[cell.country][0] += cell.x
                    data[cell.country][1] += cell.y
                    data[cell.country][2] += 1
                    data[cell.country][3].append(cell)
                else:
                    data[cell.country] = [
                        cell.x,
                        cell.y,
                        1,
                        [cell]]

        capitals = []
        country_cells = {}
        for i in range(len(data.keys())):
            c_d = data[i]

            avg_c = Cell(x=c_d[0] // c_d[2], y=c_d[1] // c_d[2], country=i, altitude=None)

            # if the average cell belongs to the country
            if self.matrix[avg_c.y][avg_c.x].country == i:
                # and is not on the border
                if not self._on_border(avg_c):
                    capitals.append(avg_c)
                # and is on the border
                else:
                    capitals.append(self._find_closest(avg_c, data[i][3]))
            else:
                capitals.append(self._find_closest(avg_c, data[i][3]))

            country_cells[i] = data[i][3]
        
        return capitals, country_cells

    def find_neighbours(self, capitals, country_cells):
        neighbours = {}
        for capital in capitals:
            neighbours[capital.country] = []
            for cell in country_cells[capital.country]:
                if (cell.x == 0 or cell.y == 0 or cell.x == self.rows - 1 or cell.y == self.cols - 1):
                    continue

                if (self.matrix[cell.y][cell.x-1].country != cell.country):
                    neighbours[capital.country].append(self.matrix[cell.y][cell.x-1].country)
                if (self.matrix[cell.y][cell.x+1].country != cell.country):
                    neighbours[capital.country].append(self.matrix[cell.y][cell.x+1].country)
                if (self.matrix[cell.y-1][cell.x].country != cell.country):
                    neighbours[capital.country].append(self.matrix[cell.y-1][cell.x].country)
                if (self.matrix[cell.y+1][cell.x].country != cell.country):
                    neighbours[capital.country].append(self.matrix[cell.y+1][cell.x].country)
            neighbours[capital.country] = list(set(neighbours[capital.country]))
        return neighbours


def _euclidean_distance(x1, y1, x2, y2):
    return int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))


def min_distance(country_id, capitals, neighbours):
    '''
    Using Dijkstra's shortest path algorithm finds the shortest path from
    capital of the country with the country_id ID, hoping over neighbouring countries.

    params: 
        neigbours: dictionary (country_id -> list of neighbouring countries' ids)
    '''
    # the given capital
    capital = capitals[country_id]
    
    # set of visited capitals
    visited = set() 

    # mapping from any capital to its distance from the given capital
    capitals_dist = {cap:MAX_DIST for cap in capitals}
    capitals_dist[capital] = 0

    # heap mantaining the unvisited nodes sorted by distance
    unvisited = [(0, capital)]

    while not len(unvisited) == 0:
        # Get the capital which has the smallest distance of the unvisited
        # capitals.
        c = heapq.heappop(unvisited)[1]
        
        # Calculate the values for the neighbouring capitals
        for n_country in neighbours[c.country]:
            n_capital = capitals[n_country]
            if n_capital in visited:
                # print("Capital: " + str(capitals[n_country]) + " already visited")
                continue

            e_d = _euclidean_distance(c.x, c.y, n_capital.x, n_capital.y)
            new_dist = capitals_dist[c] + e_d
            # print("Distance between capitals: {} and {} is: {}".format(c, n_capital, new_dist))
            if new_dist < capitals_dist[n_capital]:
                capitals_dist[n_capital] = new_dist

                # Add to the heap of unvisited capitals
                if n_capital not in unvisited:
                    heapq.heappush(unvisited, (capitals_dist[n_capital], n_capital))
                else:
                    unvisited.remove(n_capital)
                    heapq.heappush(unvisited, (capitals_dist[n_capital], n_capital))
        visited.add(c)

    return capitals_dist


def calculate_cost(solar, md, capitals):
    capital = capitals[solar.country]
    dist = md[capital]
    return solar.price + dist
        