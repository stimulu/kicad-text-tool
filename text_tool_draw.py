
from .freetype import *
import pcbnew
import copy 
import random

SCALE = 10000.0
NB_SEG_APPROX = 10

class Point:
    """Describe a point in 2D space"""
    def __init__(self, x=0, y=0, pt=None):
        if pt is None:
            self.x = x
            self.y = y
        else:
            self.x = pt.x
            self.y = pt.y
    def __str__(self):
        return "<Point x: "+str(self.x) + "\ty: " + str(self.y) + ">"

    def as_tuple(self):
        return (self.x, self.y)

class Poly:
    """Describe a polygon in 2D space"""
    def __init__(self, poly=None, pt=None):
        self.points = []
        if pt is not None:
            self.points.append(Point(pt=pt))
        elif poly is not None:
            for pt in poly.points:
                self.points.append(Point(pt=pt))

    def add(self, point):
        self.points.append(point)

    def last(self):
        return Point(pt=self.points[-1])

    def is_hole(self):
        last_point = self.last()
        area = 0.0
        for pt in self.points:
            area = area + (pt.x - last_point.x) * (pt.y + last_point.y)
            last_point = Point(pt=pt)
        # print(area)
        return (area > 0.0)

    def is_point_inside(self, pt):
        n = len(self.points)
        inside =False

        p1x,p1y = self.points[0].as_tuple()
        for i in range(n+1):
            p2x,p2y = self.points[i % n].as_tuple()
            if pt.y > min(p1y,p2y):
                if pt.y <= max(p1y,p2y):
                    if pt.x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (pt.y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or pt.x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    """ Draw a poly as an outline """
    def draw(self, board, layer):
        start_pt = self.last()
        for pt in self.points:
            self.draw_seg(board, layer, start_pt, pt)
            start_pt = pt

    def draw_seg(self, board, layer, a, b):
        seg = pcbnew.DRAWSEGMENT(board)
        board.Add(seg)
        seg.SetStart(pcbnew.wxPoint(a.x*SCALE, -a.y*SCALE))
        seg.SetEnd(pcbnew.wxPoint(b.x*SCALE, -b.y*SCALE))
        seg.SetLayer(layer)

class Shape():
    """Describe a shape constitued of one bound and zero or more holes"""
    def __init__(self, bound=None):
        self.bound = bound
        self.holes = []

    def add_hole(self, hole):
        self.holes.append(hole)

    def is_point_inside(self, pt):
        return self.bound.is_point_inside(pt)

    """ Orders polys into Shapes """
    @staticmethod
    def get_anchor(shapes):
        a = Point()
        for sh in shapes:
            for pt in sh.bound.points:
                a.x = min(a.x, pt.x)
                a.y = min(a.x, pt.y)
        return a

    """ Orders polys into Shapes """
    @staticmethod
    def get_shapes(polys, reverse=False):

        len_polys = len(polys)
        bounds = []
        holes = []
        for poly in polys:
            if len(poly.points) is not 0:
                if not reverse != poly.is_hole():
                    holes.append(poly)
                else:
                    bounds.append(Shape(bound=poly))
            else:
                len_polys -= 1

        holes_added = 0;
        for bound in bounds:
            for hole in holes:
                if bound.is_point_inside(hole.last()):
                   bound.add_hole(hole)
                   holes_added += 1
        # check everoby has been accountd for
        if len_polys == holes_added + len(bounds):
            return bounds
        else:
            if not reverse:
                return Shape.get_shapes(polys, reverse=True)
            else:
                print("FAILED ordering bounds and holes")
                return []

class Text():
    def __init__(self, text, face, size=12.0):
        self.text = text
        self.face = face
        self.size = size

    def draw(self, board, layer, origin=Point(), net=0):

        zone_container = None
        shape_poly_set = None

        previous = 0
        pen = Point(pt=origin)
        previous = 0
        for c in self.text:

            self.face.set_char_size( int(self.size*64.0) )
            self.face.load_char(c)
            kerning = self.face.get_kerning(previous, c)

            zone_container, shape_poly_set = Glyph(c, self.face, self.size).draw(board, layer, pen, zone_container, shape_poly_set)

            previous = c
            pen.x += kerning.x * SCALE
            pen.x += self.face.glyph.advance.x * SCALE
            pen.y += self.face.glyph.advance.y * SCALE

        pcbnew.ZONE_FILLER(board).Fill(board.Zones())
        return zone_container


class Glyph():
    def __init__(self, char, face, size=12.0):
        self.char = char
        self.polys = []

        face.set_char_size( int(size*64.0) )
        face.load_char( char )
        ctx = {'poly':None}
        face.glyph.outline.decompose(ctx, move_to=self.move_to, line_to=self.line_to, conic_to=self.conic_to, cubic_to=self.cubic_to)
        
        self.polys.append(Poly(ctx['poly'])) # add last poly
        ctx['poly'] = None

        self.shapes = Shape.get_shapes(self.polys)
        if len(self.shapes) is not 0:
            self.anchor_point = self.shapes[0].bound.points[0]

    def draw(self, board, layer, origin=Point(), zone_container=None,  shape_poly_set=None,  net=0):

        for shape in self.shapes:
            shapeid = None
            bound = shape.bound.points
            if not shape_poly_set:
                zone_container = board.InsertArea(net, 0, layer,
                                                  int( origin.x + bound[0].x * SCALE),
                                                  int( origin.y - bound[0].y * SCALE),
                                                  pcbnew.ZONE_CONTAINER.DIAGONAL_EDGE)
                zone_container.SetMinThickness(0)
                zone_container.SetPriority(95)
                shape_poly_set = zone_container.Outline()
                shapeid = random.randint(3000, 65635)
            else:
                shapeid = shape_poly_set.NewOutline()
                shape_poly_set.Append(int( origin.x + bound[0].x * SCALE),
                                      int( origin.y - bound[0].y * SCALE),
                                      shapeid)

            for pt in bound[1:]:
                shape_poly_set.Append(int( origin.x + pt.x * SCALE), int( origin.y - pt.y * SCALE))

            for hole in shape.holes:
                holeid = shape_poly_set.NewHole()
                for pt in hole.points:
                    shape_poly_set.Append(int( origin.x + pt.x * SCALE), int( origin.y - pt.y * SCALE), -1, holeid)

            zone_container.Hatch()
        return (zone_container, shape_poly_set)

    def draw_outline(self, board, layer):
        for pl in self.polys:
            pl.draw(board, layer)
    
    def move_to(self, a, ctx):
        # print("MOVE_TO")
        if ctx['poly'] is not None:
            self.polys.append(Poly(ctx['poly']))
        ctx['poly'] = Poly(pt=a)

    def line_to(self, a, ctx):
        ctx['poly'].add(Point(pt=a))

    def conic_to(self, a, b, ctx):
        poly = ctx['poly']
        # approximate/convert conic bezier (quadratic) to cubic
        c1 = Point(
                   poly.last().x + (2.0/3.0 * (a.x - poly.last().x)),
                   poly.last().y + (2.0/3.0 * (a.y - poly.last().y)))
        c2 = Point(
                   b.x + (2.0/3.0 * (a.x - b.x)),
                   b.y + (2.0/3.0 * (a.y - b.y)))

        self.cubic_to(c1, c2, b, ctx)

    def cubic_to(self, a, b, c, ctx):
        poly = ctx['poly']
        start_pt = poly.last()

        # interpolate segments along bezier curve
        for x in range(1, NB_SEG_APPROX):
            poly.add(Glyph.BezierCubicXY(start_pt, a, b, c, x/NB_SEG_APPROX))
        poly.add(Point(pt=c))

    @staticmethod
    def BezierCubicXY(p0, p1, p2, p3, t):
        x = pow(1 - t, 3) * p0.x + 3 * pow(1 - t, 2) * t * p1.x + 3 * (1 - t) * pow(t, 2) * p2.x + pow(t, 3) * p3.x;
        y = pow(1 - t, 3) * p0.y + 3 * pow(1 - t, 2) * t * p1.y + 3 * (1 - t) * pow(t, 2) * p2.y + pow(t, 3) * p3.y;
        return Point(x, y)


