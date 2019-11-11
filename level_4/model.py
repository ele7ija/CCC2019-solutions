# Generic/Built-in Libs
from collections import namedtuple
from enum import Enum

class QUADRANT(Enum):
    TL = 1
    TR = 2
    BL = 3
    BR = 4

class AXIS(Enum):
    X = 1
    Y = 2

Point = namedtuple('Point', ['x', 'y'])

class Ray:
    __slots__ = ['o', 'd']

    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction
    
    def __init__(self, origin_x, origin_y, dir_x, dir_y):
        self.o = Point(origin_x, origin_y)
        self.d = Point(dir_x, dir_y)

    def create_funs(self):
        '''
        Creates a linear function and it's inverse. Functions represent
        the Ray's direction. Inverse function is to be used later to 
        find the intersection of the Ray and a 1x1 box.
        '''
        k = self.d.y / self.d.x if self.d.x != 0 else None
        n = self.o.y - k * self.o.x if k != None else None
        
        # print("k: {}, n: {}".format(str(k), str(n)))

        fun_exists = True
        fun_inv_exists = True

        # case when direction of the ray is given in shape (0, c)
        # aka when ray is parallel to the y-axis (fun doesn't exist)
        if self.d.x != 0:
            def fun(x):
                return k * x + n
        else:
            fun_exists = False

        # case when direction of the Ray is given in shape (c, 0)
        # aka when ray is parallel to the x-axis (inv fun doesn't exist)
        if k != 0:
            if k == None:
                # (self.o.x, Y) is in f => f-1(y) = self.o.x
                def fun_inv(y):
                    return self.o.x    
            else:
                def fun_inv(y):
                    return (y - n) / k
        else:
            fun_inv_exists = False
        
        if not fun_exists:
            return None, fun_inv
        if not fun_inv_exists:
            return fun, None
        return fun, fun_inv



    def get_cells(self, rows, cols):
        f, f_inv = self.create_funs()

        # returns indexes of cells that ought to be visited
        cell_indexes = self._get_indexes(rows, cols)
        visited_cells = []
        for cell in cell_indexes:
            if self._visited(cell, f, f_inv):
                visited_cells.append(cell)
        
        return visited_cells

    # This could be rewritten as a property
    @property
    def quadrant(self):
        if self.d.x < 0:
            if self.d.y >= 0:
                return QUADRANT.TL 
            else: return QUADRANT.BL
        else:
            if self.d.y >= 0:
                return QUADRANT.TR
            else:
                return QUADRANT.BR

    @property
    def dom_axis(self):
        if abs(self.d.x) >= abs(self.d.y):
            return AXIS.X
        else:
            return AXIS.Y

    def _get_indexes(self, rows, cols):
        indexes = []

        if self.quadrant == QUADRANT.TL:
            # i se smanjuje, j povecava
            if self.dom_axis == AXIS.X:
                for j in range(self.o.y, cols, 1):
                    for i in range(self.o.x, -1, -1):
                        indexes.append(Point(i, j))
            else:
                for i in range(self.o.x, -1, -1):
                    for j in range(self.o.y, cols, 1):
                        indexes.append(Point(i, j))
        elif self.quadrant == QUADRANT.TR:
            # i se povecava, j povecava
            if self.dom_axis == AXIS.X:
                for j in range(self.o.y, cols, 1):
                    for i in range(self.o.x, rows, 1):
                        indexes.append(Point(i, j))
            else:
                for i in range(self.o.x, rows, 1):
                    for j in range(self.o.y, cols, 1):
                        indexes.append(Point(i, j))
        elif self.quadrant == QUADRANT.BL:
            # i se smanjuje, j smanjuje
            if self.dom_axis == AXIS.X:
                for j in range(self.o.y, -1, -1):
                    for i in range(self.o.x, -1, -1):
                        indexes.append(Point(i, j))
            else:
                for i in range(self.o.x, -1, -1):
                    for j in range(self.o.y, -1, -1):
                        indexes.append(Point(i, j))
        elif self.quadrant == QUADRANT.BR:
            # i se povecava, j smanjuje
            if self.dom_axis == AXIS.X:
                for j in range(self.o.y, -1, -1):
                    for i in range(self.o.x, rows, 1):
                        indexes.append(Point(i, j))
            else:
                for i in range(self.o.x, rows, 1):
                    for j in range(self.o.y, -1, -1):
                        indexes.append(Point(i, j))

        return indexes

    def _visited(self, cell, f, f_inv):

        bl_point = Point(cell.x - 0.5, cell.y - 0.5)
        tl_point = Point(cell.x - 0.5, cell.y + 0.5)
        tr_point = Point(cell.x + 0.5, cell.y + 0.5)
        br_point = Point(cell.x + 0.5, cell.y - 0.5)

        # Four cases - L, R, T or B visited
        if self._h_visited(bl_point, tl_point, f):
            return True
        elif self._h_visited(br_point, tr_point, f):
            return True
        elif self._v_visited(bl_point, br_point, f_inv):
            return True
        elif self._v_visited(tl_point, tr_point, f_inv):
            return True
    
    def _h_visited(self, bottom_point, top_point, f):
        # Case when d = (0, c)
        if not f:
            return False

        f_hor = f(bottom_point.x) # equal to f(top_point.x)
        if f_hor >= bottom_point.y and f_hor <= top_point.y:
            return True

    def _v_visited(self, left_point, right_point, f_inv):
        if f_inv == None:
            return False

        f_inv_ver = f_inv(left_point.y) # equal to f_inv(right_point.y)
        if f_inv_ver >= left_point.x and f_inv_ver <= right_point.x:
            return True


    def __str__(self):
        return "Ray(o=" + str(self.o) + ", d=" + str(self.d) + ")"