from Draw import Rect, Generic_Path
from SVG import SVG, Section, Embedded
from Text import Text


def cart2pixel_x(x: list[float], xmin: float, xmax: float, w: float, pad: float = 1.0, delta: float = 0) \
        -> list[float]:
    if w != 0:
        dx = (pad * xmax - xmin) / w
        if dx != 0:
            return [((xi - xmin) / dx) + delta for xi in x]
        else:
            return x
    else:
        return x


def cart2pixel_y(y: list[float], ymin: float, ymax: float, h: float, pad: float = 1.0) -> list[float]:
    if h != 0:
        dy = (pad * ymax - ymin) / h
        if dy != 0:
            return [h - ((yi - ymin) / dy) for yi in y]
        else:
            return y
    else:
        return y


class Icon(Embedded):
    def __init__(self, svg_object, w: int, h: int):
        super().__init__()
        self.w = w
        self.h = h

        self.add_child(svg_object)


class Graph(SVG):
    def __init__(self, w, h):
        """
        Graph is an SVG Object representing a generic graph.
        A Graph is made up of several parts: Plot Area, x Axis, yaxis, legend, Title.
        Parameters
        ----------
        w
        h
        """
        # Graph Parameters
        super().__init__(w, h)
        self.background = Rect()

        # Title
        self.title = Text()

        # General Text
        self.text = Text()

        self.plot = Plot()
        self.legend = Legend(self)
        self.frame = Frame(self.plot)

        self.set_sizes()

    def set_plot_extrema(self, xmin: float = None, xmax: float = None, ymin: float = None, ymax: float = None):
        if xmin is not None:
            self.plot.xmin = xmin

        if xmax is not None:
            self.plot.xmax = xmax

        if ymin is not None:
            self.plot.ymin = ymin

        if ymax is not None:
            self.plot.ymax = ymax

    def set_sizes(self):
        """
        Sets the sizes for the Graph and all of its children.
        ----------------------------------------------------------------------
        """
        w, h = self.size
        dy = 0.10 * h

        self.plot.x = 100
        self.plot.y = dy
        self.plot.w = w - self.plot.x
        self.plot.h = h - 100 - self.plot.y

        self.legend.x = w * 0.75
        self.legend.y = dy
        self.legend.w = w * 0.20
        self.legend.h = .5 * (h - 2 * dy)

    def construct(self):
        # Title
        self.add_child(self.background)
        self.add_child(self.title)

        self.add_child(self.plot, 'Plot')
        self.add_child(self.legend, 'Legend')
        self.add_child(self.frame, 'Frame')

        self.set_sizes()

        return super().construct()


class Legend(Embedded):
    def __init__(self, parent: Graph):
        super().__init__()
        self.children = []

        self.dy = 10

        self.parent = parent

        self.background = Rect()
        self.text = parent.text.copy()

        self.active = True

    class Item(Section):
        def __init__(self, text: Text, icon: Icon):
            """
            Represents an entry into the legend.
            """
            super().__init__(0, 0)
            self.icon = icon
            self.text = text
            self.active = True

        def construct(self):
            w, h = self.icon.w, self.icon.h

            self.text.x, self.text.y = 2 * w, h / 2
            self.text.text = self.name

            self.add_child(self.text)
            self.add_child(self.icon)

            return super().construct()

    def add_item(self, name: str, icon: Icon):
        text = self.text.copy()
        text.text = name

        self.add_child(self.Item(text, icon))

    def set_sizes(self, rect=None):
        if rect is not None:
            self.x, self.y, self.w, self.h = rect

    def construct(self):
        if not self.active:
            return ''

        i = 0
        for child in self._children:
            if type(child) == self.Item:
                child.x, child.y = 10, i * 2 * self.dy
                i += 1

        svg = super().construct()

        return svg


class Plot(Embedded):
    def __init__(self):
        super().__init__()
        self.children = []

        self.xmin, self.xmax, self.ymin, self.ymax = 0, 1, 0, 1

        self.background = Rect()

        self.top, self.bottom, self.left, self.right = True, True, True, True

        self.active = True

    def construct(self):
        """
        Plot Item (pi) must have a construct() method to call
        Returns
        -------

        """
        self.add_child(self.background)

        for child in self.children:
            self.add_child(child)

        svg = super().construct()

        return svg


class Frame(Section):
    def __init__(self, plot: Plot):
        super().__init__(0, 0)
        self.border = Generic_Path()
        self.ax = self.Axis()
        self.ay = self.Axis()

        self.plot = plot

        self.left, self.right, self.top, self.bottom = False, False, False, False

        self.children = []

    class Axis:
        def __init__(self):
            self.lw = 4
            self.dist2text = 5
            self.ticks = []
            self.p_ticks = []
            self.angle = 0
            self.text = None
            self.title = None

    def _get_pixel(self, x=None, y=None):
        if x is not None and y is not None:
            return 0

        if x is not None and y is None:
            return cart2pixel_x([x], self.plot.xmin, self.plot.xmax, self.plot.w)[0] + self.plot.x

        if x is None and y is not None:
            return cart2pixel_y([y], self.plot.ymin, self.plot.ymax, self.plot.h)[0] + self.plot.y

        return 0

    def _set_ticks(self):
        self.ax.ticks.sort()
        self.ay.ticks.sort()

        xmin, xmax, ymin, ymax = self.plot.xmin, self.plot.xmax, self.plot.ymin, self.plot.ymax
        self.ax.p_ticks = [[self._get_pixel(x=x[0]), x[1], x[0]] for x in self.ax.ticks if xmin <= x[0] <= xmax]
        self.ay.p_ticks = [[self._get_pixel(y=y[0]), y[1], y[0]] for y in self.ay.ticks if ymin <= y[0] <= ymax]

    def _set_text(self, text: Text, label: str, x: float, y: float):
        if text is not None:
            text = text.copy()
            text.text = label
            text.x = x
            text.y = y

            self.children.append(text)

    def _set_titles(self):
        if self.ax.title is not None:
            self.add_child(self.ax.title)
            self.ax.title.transform = 0
            self.ax.title.anchor = 'middle'
            self.ax.title.baseline = 'central'
            self.ax.title.x, self.ax.title.y = '50%', '90%'

        if self.ay.title is not None:
            self.add_child(self.ay.title)
            self.ay.title.transform = -90
            self.ay.title.anchor = 'middle'
            self.ay.title.baseline = 'central'
            self.ay.title.x, self.ay.title.y = self.plot.x / 3, self.plot.y + self.plot.h / 2

    def _yticks(self):
        x2 = self.plot.x
        x1 = x2 - self.ay.lw

        ticks = self.ay.p_ticks[:]
        top, bot = None, None

        if ticks[0][2] == self.plot.ymin and not self.plot.bottom and self.plot.left and self.ay.lw > 0:
            bot = ticks.pop(0)

        if ticks[-1][2] == self.plot.ymax and not self.plot.top and self.plot.left and self.ay.lw > 0:
            top = ticks.pop(-1)

        if top is not None and bot is not None:
            self.border.points = ('M', x1, bot[0])
            self.border.points = ('L', x2, bot[0])
            self.border.points = ('L', x2, top[0])
            self.border.points = ('L', x1, top[0])
            self.left = True

        if top is None and bot is not None:
            self.border.points = ('M', x1, bot[0])
            self.border.points = ('L', x2, bot[0])
            self.border.points = ('L', x2, self.plot.y)
            self.left = True

        if top is not None and bot is None:
            self.border.points = ('M', x2, self.plot.y + self.plot.h)
            self.border.points = ('L', x2, top[0])
            self.border.points = ('L', x1, top[0])
            self.left = True

        if self.ay.lw > 0:
            for tick in ticks:
                y = tick[0]
                self.border.points = ('M', x1, y)
                self.border.points = ('L', x2, y)

        if self.ay.text is not None:
            ticks = self.ay.p_ticks[:]
            x1 = x1 - self.ay.dist2text
            for tick in ticks:
                self._set_text(self.ay.text, tick[1], x1, tick[0])

    def _xticks(self):
        y2 = self.plot.y + self.plot.h
        y1 = y2 + self.ax.lw

        ticks = self.ax.p_ticks[:]
        left, rght = None, None

        if self.ax.lw > 0:
            if ticks[0][2] == self.plot.xmin and not self.plot.left and self.plot.bottom and self.ax.lw > 0:
                left = ticks.pop(0)

            if ticks[-1][2] == self.plot.xmax and not self.plot.right and self.plot.bottom and self.ax.lw > 0:
                rght = ticks.pop(-1)

            if left is not None and rght is not None:
                self.border.points = ('M', left[0], y1,)
                self.border.points = ('L', left[0], y2,)
                self.border.points = ('L', rght[0], y2)
                self.border.points = ('L', rght[0], y1)
                self.bottom = True

            if left is None and rght is not None:
                self.border.points = ('M', self.plot.x, y2)
                self.border.points = ('L', rght[0], y2)
                self.border.points = ('L', rght[0], y1)
                self.bottom = True

            if left is not None and rght is None:
                self.border.points = ('M', left[0], y1,)
                self.border.points = ('L', left[0], y2,)
                self.border.points = ('L', self.plot.x + self.plot.w, y2)
                self.bottom = True

            for tick in ticks:
                x = tick[0]
                self.border.points = ('M', x, y1)
                self.border.points = ('L', x, y2)

        if self.ax.text is not None:
            ticks = self.ax.p_ticks[:]
            y = y1 + self.ax.dist2text
            for tick in ticks:
                self._set_text(self.ax.text, tick[1], tick[0], y)

    def _build_frame(self):
        self.children = []
        self._set_ticks()

        self._yticks()
        self._xticks()

        self._set_titles()

        if self.plot.top and not self.top:
            self.border.points = ('M', self.plot.x, self.plot.y)
            self.border.points = ('L', self.plot.x + self.plot.w, self.plot.y)

        if self.plot.right and not self.right:
            self.border.points = ('M', self.plot.x + self.plot.w, self.plot.y)
            self.border.points = ('L', self.plot.x + self.plot.w, self.plot.y + self.plot.h)

        if self.plot.bottom and not self.bottom:
            self.border.points = ('M', self.plot.x + self.plot.w, self.plot.y + self.plot.h)
            self.border.points = ('L', self.plot.x, self.plot.y + self.plot.h)

        if self.plot.left and not self.left:
            self.border.points = ('M', self.plot.x, self.plot.y + self.plot.h)
            self.border.points = ('', self.plot.x, self.plot.y)

        self.add_child(self.border)

    def construct(self):
        self._build_frame()
        return super().construct()
