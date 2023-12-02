from ..Data_Structures import Node, Graph
from math import sin, cos, pi


class SVG(Node):
    def __init__(self, w=0, h=0, xmlns=''):
        super().__init__('svg')
        self.w = w
        self.h = h

        self.type = 'svg'
        self.xmlns = xmlns
        self.active = True

    def construct(self, depth):
        tab = '   ' * depth
        header = [f'{tab}<svg width="{self.w}" height="{self.h}" {self.xmlns}>']
        footer = [f'{tab}</svg>']

        depth += 1
        body = [i for i in [node.construct(depth) for node in self.edges] if i != '']

        return f'\n'.join(header + body + footer)


class G(Node):
    def __init__(self, x=0, y=0, angle=0):
        super().__init__('g')
        self.x = x
        self.y = y

        self.xc = 0
        self.yc = 0

        self.xscale = 1
        self.yscale = 1

        self.angle = angle
        self.type = 'g'
        self.active = True

    def header(self):
        x, y = self.x, self.y

        xc, yc = self.xc, self.yc

        xs, ys = self.xscale, self.yscale

        c = cos(pi * self.angle / 180)
        s = sin(pi * self.angle / 180)

        xn = x + xc * (1 + xs * s - xs * c)
        yn = y + yc * (1 - ys * s - ys * c)

        return f'<g transform="matrix({xs * c},{ys * s},{xs * -s},{ys * c},{xn},{yn})">'

    def construct(self, depth):
        tab = '   ' * depth
        header = [f'{tab}{self.header()}']
        footer = [f'{tab}</g>']

        depth += 1
        body = [i for i in [node.construct(depth) for node in self.edges] if i != '']

        return f'\n'.join(header + body + footer)


class Tree(Graph):
    def __init__(self):
        super().__init__()
        self.root = None

    def addChild(self, child: Node):
        if self.root is not None:
            self.root.add_child(child)
        else:
            self.root = child

    def addSection(self, child: 'Tree'):
        if child.root.name == 'svg':
            child.root.xmlns = ''

        self.addChild(child.root)


class Document(Tree):
    def __init__(self, **kwargs):
        super().__init__()
        self.root = SVG(xmlns='xmlns="http://www.w3.org/2000/svg"', **kwargs)


class Section(Tree):
    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__()
        self.root = G(x=x, y=y)
        self.svg = SVG(w=w, h=h)
        self.root.add_child(self.svg)

    def addChild(self, child: Node):
        self.svg.add_child(child)

    @property
    def x(self):
        return self.root.x

    @x.setter
    def x(self, x):
        self.root.x = x

    @property
    def y(self):
        return self.root.y

    @y.setter
    def y(self, y):
        self.root.y = y

    @property
    def w(self):
        return self.svg.w

    @w.setter
    def w(self, w):
        self.svg.w = w

    @property
    def h(self):
        return self.svg.h

    @h.setter
    def h(self, h):
        self.svg.h = h
