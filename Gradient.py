class Linear:
    """
    Creates a Linear Gradient Object. The Gradient is defined in the *defs* section of the SVG and referenced by name
    in the parameters of the desired elements
    """

    def __init__(self, name: str):
        """
        :param name: a string identifying this gradient. The name is how gradients are referenced in the target elements
        """
        self._stops = []
        self.name = name
        self.orientation = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 1}
        self.active = True

    def add_stop(self, percent: float, color: tuple[int, int, int], opacity: float = 1.0):
        """
        Adds a stop to define gradient behavior. Stops are isstances of the `Gradient.Stop` class.
        This function appends the new `Stop` instance reference to the `Linear._stops` list.

        :param float percent: Dictates where the stop is as a percentage of the total distance that the gradient will cover.

        :param tuple color: RGB values defining the color at this stop.

        :param float opacity: Decimal value defining the opacity at this stop.
        """
        stop = Stop(percent, color, opacity)
        self._stops.append(stop)

    def construct(self):
        """
        Builds the gradient definition that will be instituted in the defs section of the parent SVG.

        :return: String representation of this gradient object.
        :rtype: str
        """

        svg = []
        if self.active and self._stops != []:
            stops = [stop.construct() for stop in self._stops]

            svg = ['<linearGradient id="%s"' % (self.name,)] + \
                  ['x1="%(x1)s" x2="%(x2)s" y1="%(y1)s" y2="%(y2)s">' % self.orientation] + stops + [
                      '</linearGradient>']

        return '\n'.join(svg)


class Stop:
    """
    Stops dictate the behavior of their parent gradient.
    """
    def __init__(self, percent: float = 0.0, color: tuple[int, int, int] = (0, 0, 0), opacity: float = 1):
        """
        :param float percent: Dictates where the stop is as a percentage of the total distance that the gradient will cover.

        :param tuple color: RGB values defining the color at this stop.

        :param float opacity: Decimal value defining the opacity at this stop.
        """
        self._color = None
        self.color = color

        self._opacity = opacity
        self._percent = percent

    @property
    def percent(self):
        """
        Get or Set the relative location of this stop on the gradient. Values are a decimal representing a percent
        (must be between 0 and 1).

        :rtype: float
        """
        return self._percent

    @percent.setter
    def percent(self, percent: float):
        if percent < 0:
            percent = 0
        elif percent > 1:
            percent = 1

        self._percent = percent

    @property
    def opacity(self):
        """
        Get or Set the opacity at this stop on the gradient. Values are a decimal representing a percent
        (must be between 0 and 1).

        :rtype: float
        """
        return self._percent

    @opacity.setter
    def opacity(self, opacity: float):
        if opacity < 0:
            opacity = 0
        elif opacity > 1:
            opacity = 1

        self._opacity = opacity

    @property
    def color(self):
        """
        Get or Set a tuple of r,g,b values for this stop on the gradient.
        """
        if self._color is not None:
            color = self._color
            color = [color[1:3], color[3:5], color[5:7]]
            color = [int(hexval, 16) for hexval in color]
            color = tuple(color)
        else:
            color = None
        return color

    @color.setter
    def color(self, color: tuple[int, int, int]):
        if color is not None:
            self._color = '#' + '%02x%02x%02x' % color
        else:
            self._color = None

    def construct(self):
        """
        Builds the stop defined by this object (a row in the parent gradient definition).

        :return: String representation of this Stop
        :rtype: str
        """
        rlist = (str(self.percent), self._color, str(self.opacity))
        row = '<stop offset="%s" stop-color="%s" stop-opacity="%s"/>' % rlist

        return row
