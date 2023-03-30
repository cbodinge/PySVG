from .Paths import Path
from math import pi, tan


class Rect(Path):
    """
    Repressents a rectangle SVG element. Subclass of `Paths.Path`

    """

    def __init__(self, x=0, y=0, w='100%', h='100%'):
        """
        :param x: x coordinate of the left, bottom coordinate of the rectangle.
        :param y: y coordinate of the left, bottom coordinate of the rectangle.
        :param w: Width of the rectangle.
        :param h: Height of the rectangle.

        All location/size parameters Can be pixels, percent, or any of the supported units
        (see `Units Documentation <https://developer.mozilla.org/en-US/docs/Web/CSS/length-percentage>`_
        for details on what units are supported). Default is pixel values.
        """

        super().__init__()
        self._x = x
        self._y = y
        self._w = w
        self._h = h

        self._rx = None
        self._ry = None

        self.fill_opacity = 0

    @property
    def x(self):
        """
        x coordinate of the left, bottom coordinate of the rectangle.
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        """
        y coordinate of the left, bottom coordinate of the rectangle.
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def w(self):
        """
        Width of the rectangle.
        """
        return self._w

    @w.setter
    def w(self, w):
        self._w = w

    @property
    def h(self):
        """
        Height of the rectangle.
        """
        return self._h

    @h.setter
    def h(self, h):
        self._h = h

    @property
    def rx(self):
        """
        points of edge rounding
        """
        return self._rx

    @rx.setter
    def rx(self, rx):
        self._rx = rx

    @property
    def ry(self):
        """
        points of edge rounding
        """
        return self._ry

    @ry.setter
    def ry(self, ry):
        self._ry = ry

    def copy(self, item=None):
        if item is None:
            item = Rect()

        item._x = self._x
        item._y = self._y
        item._w = self._w
        item._h = self._h

        item._rx = self._rx
        item._ry = self._ry

        item = super().copy(item)

        return item

    def inherit(self, item):
        self._x = item.x
        self._y = item.y
        self._w = item.w
        self._h = item.h

        self._rx = item.rx
        self._ry = item.ry

        super().inherit(item)

    def construct(self, **kwargs):
        if not self.active:
            return ''

        parameters = {'x': self.x,
                      'y': self.y,
                      'rx': self.rx,
                      'ry': self.ry,
                      'width': self.w,
                      'height': self.h}

        entries = super().construct(parameters)

        row = '<rect %s />' % (entries,)

        return row


class Circle(Path):
    def __init__(self, x=0, y=0, r=0):
        """
        :param x: x coordinate of the center of the circle.
        :param y: y coordinate of the center of the circle.
        :param r: radius of the circle.

        All location/size parameters Can be pixels, percent, or any of the supported units
        (see `Units Documentation <https://developer.mozilla.org/en-US/docs/Web/CSS/length-percentage>`_
        for details on what units are supported). Default is pixel values.
        """
        super().__init__()

        self._x = x
        self._y = y
        self._r = r

    @property
    def x(self):
        """
        x coordinate of the center of the circle.
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        """
        y coordinate of the center of the circle.
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def r(self):
        """
        radius of circle.
        """
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    def copy(self, item=None):
        if item is None:
            item = Circle()

        item.x = self.x
        item.y = self.y
        item.r = self.r

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        parameters = {'cx': self.x,
                      'cy': self.y,
                      'r': self.r}

        entries = super().construct(parameters)

        row = '<circle %s />' % (entries,)

        return row


class Generic_Path(Path):
    """
    Repressents a generic version of the path element of an SVG.

    Path elements are used to draw curves and shapes
    freely based on defined curve behavior and coordinates on which to draw. Subclass of `Paths.Path`.
    """

    def __init__(self):
        super().__init__()
        self._points = []

    @property
    def points(self):
        """
            List of points whose entries are typically of the form [`string`, `float`, `float`]

            List Entry[0]: String, letter that describes the behavior of the following points
            List Entry[1]: Typically the x value for the next drawn point
            List Entry[2]: Typically the y value for the next drawn point

            See `Paths Documentation <https://developer.mozilla.org/en-US/docs/Web/CSS/length-percentage>`_ for how
            to control the path form.
        """
        return self._points

    @points.setter
    def points(self, points: list[str, float, float]):
        self._points = points

    def copy(self, item=None):
        if item is None:
            item = Generic_Path()

        item.points = self.points

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        entries = super().construct()

        points = ', '.join([' '.join([str(p) for p in point if str(p) != '']) for point in self.points])

        row = '<path d="%s"' % (points,)

        row = row + ' ' + entries + '/>'

        return row


class Polygon(Path):
    """
    Repressents a polygon.

    Path elements are used to draw curves and shapes
    freely based coordinates on which to draw. Subclass of `Paths.Path`.
    """

    def __init__(self):
        super().__init__()
        self._points = []

    @property
    def points(self):
        """
            List of points whose entries are of the form [`float`, `float`]

            List Entry[0]: x value for the next drawn point
            List Entry[1]: y value for the next drawn point

            See `Polygon Documentation <https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polygon>`_
        """
        return self._points

    @points.setter
    def points(self, points: list[float, float]):
        self._points = points

    def copy(self, item=None):
        if item is None:
            item = Polygon()

        item.points = self.points

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        entries = super().construct()

        points = ', '.join([' '.join([str(p) for p in point if str(p) != '']) for point in self.points])

        row = '<polygon points="%s"' % (points,)

        row = row + ' ' + entries + '/>'

        return row


class Bezier(Path):
    def __init__(self):
        super().__init__()
        self.points = []

    def copy(self, item=None):
        if item is None:
            item = Bezier()

        item.points = self.points

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        entries = super().construct()

        points = self.points[:]
        point1 = points.pop(0)

        points = ', '.join([' '.join([str(p) for p in point if str(p) != '']) for point in points])

        row = '<path d="M %s %s C %s V 1000"' % (str(point1[0]), str(point1[1]), points)

        row = row + ' ' + entries + '/>'

        return row


class PartialCircle(Path):
    def __init__(self, x=0.0, y=0.0, r=0.0, theta1=0.0, theta2=0.0):
        """
        :param x: x coordinate of the center of the circle.
        :param y: y coordinate of the center of the circle.
        :param r: radius of the circle.
        :param theta1: angle between the circle center and the first point.
        :param theta2: angle between the first point and the second (angle of the arc).


        location/size parameters should be pixels.
        """
        super().__init__()

        self.x = x
        self.y = y
        self.r = r
        self.theta1 = theta1
        self.theta2 = theta2

    def _tan(self, theta):
        theta = theta % (2 * pi)
        _tan = tan(theta)
        sign = 1
        if pi / 2 < theta <= 3 * pi / 2:
            sign = -1

        y = sign * (self.r ** 2 / (1 + _tan ** 2)) ** 0.5
        x = _tan * y

        return x, y

    def copy(self, item=None):
        if item is None:
            item = PartialCircle()

        item.x = self.x
        item.y = self.y
        item.r = self.r
        item.theta1 = self.theta1
        item.theta2 = self.theta2

        item = super().copy(item)

        return item

    def construct(self, **kwargs):
        x1, y1 = self._tan(self.theta1)
        x1, y1 = self.x + x1, self.y - y1

        x2, y2 = self._tan(self.theta1 + self.theta2)
        x2, y2 = self.x + x2, self.y - y2

        flag = 0
        if self.theta2 > pi:
            flag = 1

        d = f'M {x1} {y1} A {self.r} {self.r} 0 {flag} 1 {x2} {y2} L {self.x} {self.y} Z'

        parameters = {'d': d}

        entries = super().construct(parameters)

        row = '<path %s />' % (entries,)

        return row
