from SVG import Section
from Draw import Rect, Generic_Path
from graphing.Graph import Plot, Icon, cart2pixel_y, cart2pixel_x


class Scatter(Section):
    def __init__(self, parent: Plot, x: list[float], y: list[float], icon: Icon):
        super().__init__(0, 0)
        self.icon = icon
        self.parent = parent

        self.ox, self.oy = x[:], y[:]

    def get_xy(self, dx=0, dy=0):
        x = cart2pixel_x(self.ox, self.parent.xmin, self.parent.xmax, self.parent.w)
        y = cart2pixel_y(self.oy, self.parent.ymin, self.parent.ymax, self.parent.h)

        x = [i + dx for i in x]
        y = [i + dy for i in y]

        return x, y

    def set_sizes(self):
        pass

    def construct(self):
        # Plot points using self.icon as point symbol
        w, h = self.icon.w, self.icon.h
        x, y = self.get_xy(-w / 2, -h / 2)

        for i in range(len(self.ox)):
            icon = self.icon.copy()
            icon.x = x[i]
            icon.y = y[i]
            self.add_child(icon)

        return super().construct()


class ScatterLines(Scatter):
    def __init__(self, parent: Plot, x: list[float], y: list[float], icon: Icon, line: Generic_Path):
        super().__init__(parent, x, y, icon)

        self.line = line

    def construct(self):
        x, y = self.get_xy()
        xy = list(zip(x, y))
        xy.sort()
        x, y = zip(*xy)

        points = [('M', x[0], y[0])]

        for i in range(1, len(xy)):
            points.append(('L', x[i], y[i]))

        self.line.points = points

        self.add_child(self.line)

        return super().construct()


class PlotBox(Section):
    def __init__(self, parent: Plot, pnt1, pnt2):
        super().__init__(0, 0)
        self.rect = Rect()
        self.line = Generic_Path()

        self.x1, self.y1 = pnt1
        self.x2, self.y2 = pnt2

        self.parent = parent

    def set_sizes(self):
        x = cart2pixel_x([self.x1, self.x2], self.parent.xmin, self.parent.xmax, self.parent.w)
        y = cart2pixel_y([self.y1, self.y2], self.parent.ymin, self.parent.ymax, self.parent.h)

        x1, x2 = min(x), max(x)
        y1, y2 = min(y), max(y)

        self.x = x1
        self.y = y1

        w = x2 - x1
        h = y2 - y1

        self.rect.x, self.rect.y, self.rect.w, self.rect.h = 0, 0, w, h
        self.line.points = [('M', 0, h / 2), ('L', self.parent.w, h / 2)]

    def construct(self):
        self.set_sizes()
        self.add_child(self.rect)
        self.add_child(self.line)

        svg = super().construct()

        return svg


class Error_Bars(Section):
    def __init__(self, parent: Plot, x, y, r):
        super().__init__(0, 0)
        self.bar = Generic_Path()
        self.w, self.h = 1, r

        self.cx, self.cy = x, y

        self.parent = parent
        self.active = True

    def set_sizes(self):
        x, y = self.w, 2 * self.h

        y0, y1 = cart2pixel_y([0, y], self.parent.ymin, self.parent.ymax, self.parent.h)
        x0, x1 = cart2pixel_x([0, x], self.parent.xmin, self.parent.xmax, self.parent.w)

        x = abs(x1 - x0)
        y = abs(y1 - y0)

        self.bar.points = [('M', 0, 0),
                           ('L', x, 0),
                           ('M', x / 2, 0),
                           ('L', x / 2, y),
                           ('M', x, y),
                           ('L', 0, y)]

        self.bar.fill_opacity = 0

        self.x = cart2pixel_x([self.cx], self.parent.xmin, self.parent.xmax, self.parent.w)[0] - x / 2
        self.y = cart2pixel_y([self.cy], self.parent.ymin, self.parent.ymax, self.parent.h)[0] - y / 2

    def construct(self):
        self.set_sizes()
        self.add_child(self.bar)

        svg = super().construct()

        return svg


class Error_Bars_Top(Error_Bars):
    def set_sizes(self):
        x, y = self.w, self.h

        y0, y1 = cart2pixel_y([0, y], self.parent.ymin, self.parent.ymax, self.parent.h)
        x0, x1 = cart2pixel_x([0, x], self.parent.xmin, self.parent.xmax, self.parent.w)

        x = abs(x1 - x0)
        y = abs(y1 - y0)

        if self.h > 0:
            self.bar.points = [('M', 0, 0),
                               ('L', x, 0),
                               ('M', x / 2, 0),
                               ('L', x / 2, y)]
            self.y = cart2pixel_y([self.cy], self.parent.ymin, self.parent.ymax, self.parent.h)[0] - y

        elif self.h < 0:
            self.bar.points = [('M', x / 2, 0),
                               ('L', x / 2, y),
                               ('M', 0, y),
                               ('L', x, y)]
            self.y = cart2pixel_y([self.cy], self.parent.ymin, self.parent.ymax, self.parent.h)[0]

        self.bar.fill_opacity = 0

        self.x = cart2pixel_x([self.cx], self.parent.xmin, self.parent.xmax, self.parent.w)[0] - x / 2


class PlotLine(Section):
    def __init__(self, parent: Plot, pnt1: tuple[float, float], pnt2: tuple[float, float]):
        super().__init__(0, 0)
        self.bar = Generic_Path()

        self.x1, self.y1 = pnt1
        self.x2, self.y2 = pnt2

        self.parent = parent
        self.active = True

    def _update(self):
        x = cart2pixel_x([self.x1, self.x2], self.parent.xmin, self.parent.xmax, self.parent.w)
        y = cart2pixel_y([self.y1, self.y2], self.parent.ymin, self.parent.ymax, self.parent.h)

        self.bar.points = ('M', x[0], y[0])
        self.bar.points = ('L', x[1], y[1])

    def construct(self):
        self._update()
        self.add_child(self.bar)
        return super().construct()
