class Path:
    def __init__(self):
        self._fill = None
        self._fill_opacity = 0

        self._stroke = None
        self._stroke_width = None
        self._stroke_opacity = None
        self._stroke_dasharray = None

        self._gradient = None

        self.active = True

    @property
    def fill(self):
        """
        Get or Set a tuple of r,g,b values for the fill of this element.
        """
        if self._fill is not None:
            color = self._fill
            color = [color[1:3], color[3:5], color[5:7]]
            color = [int(hexval, 16) for hexval in color]
            color = tuple(color)
        else:
            color = None
        return color

    @fill.setter
    def fill(self, fill: tuple[int, int, int]):
        if fill is not None:
            self._fill = '#' + '%02x%02x%02x' % fill
        else:
            self._fill = None

    @property
    def gradient(self):
        """Name of the gradient to define the fill with. Gradient will reference a ``Gradient.Linear`` object.
        ``Gradient.Linear`` objects need to be added to the defs field of the ``SVG.SVG`` object."""
        if self._gradient is not None:
            name = self._gradient[5:-1]
        else:
            name = None
        return name

    @gradient.setter
    def gradient(self, name: str):
        self._gradient = 'url(#%s)' % name

    @property
    def fill_opacity(self):
        """
        Number Value from 0 to 1 that controls the opacity of the fill.
        0 -> Totally Transparent
        1 -> Totally Opaque
        """
        return self._fill_opacity

    @fill_opacity.setter
    def fill_opacity(self, fill_opacity: float):
        if fill_opacity is not None:
            if fill_opacity >= 0:
                self._fill_opacity = fill_opacity
        else:
            self._fill_opacity = None

    @property
    def stroke(self):
        """
        Get or Set a tuple of r,g,b values for the stroke/outline of this element.
        :
        """
        if self._stroke is not None:
            color = self._stroke
            color = [color[1:3], color[3:5], color[5:7]]
            color = [int(hexval, 16) for hexval in color]
            color = tuple(color)
        else:
            color = None
        return color

    @stroke.setter
    def stroke(self, stroke: tuple[int, int, int]):
        if stroke is not None:
            self._stroke = '#' + '%02x%02x%02x' % stroke
        else:
            self._stroke = None

    @property
    def stroke_width(self):
        """
        Width of the stroke or outline of this element. Numeric Values.
        """
        return self._stroke_width

    @stroke_width.setter
    def stroke_width(self, width: float):
        if width is not None:
            if width >= 0:
                self._stroke_width = width
        else:
            self._stroke_width = None

    @property
    def stroke_opacity(self):
        """
        Number Value from 0 to 1 that controls the opacity of the stroke/outline.
        0 -> Totally Transparent
        1 -> Totally Opaque
        """
        return self._stroke_opacity

    @stroke_opacity.setter
    def stroke_opacity(self, opacity: float):
        if opacity is not None:
            if opacity >= 0:
                self._stroke_opacity = opacity
        else:
            self._stroke_opacity = None

    @property
    def stroke_dasharray(self):
        """Iterable of integers that defines the pattern of dashes to use. Each element in the iterable defines the
        width in pixels for the next dash element in the pattern. """
        da = self._stroke_dasharray.split(' ')
        if da is not None:
            da = [int(i) for i in da]

        return da

    @stroke_dasharray.setter
    def stroke_dasharray(self, dasharray: list[int]):
        self._stroke_dasharray = ' '.join([str(i) for i in dasharray])

    def copy(self, item=None):
        """
        Creates a copy of this element by either initializing a new object of this class or adjusting the properties
        of the item passed to this function to match this class instance.

        Complete copies of a subclass are achieved by applying this method recursively to fill
        out the properties defined at each subclass level.

        :param item: This Class
        :return: Copy of this class instance
        :rtype: This Class
        """

        if item is None:
            item = Path()

        item.fill = self.fill
        item.fill_opacity = self.fill_opacity

        item.stroke = self.stroke
        item.stroke_width = self.stroke_width
        item.stroke_opacity = self.stroke_opacity
        item.stroke_dasharray = self.stroke_dasharray

        item.gradient = self.gradient

        return item

    def construct(self, outer_pars: dict = None):
        """
        Constructs the SVG string representation of this element. All parameters that are None are ignored.

        :param outer_pars: parameters to pass to superclass calls of this function
        :return: the SVG string for this element. If this element isn't active then this returns an empty string.
        :rtype: str
        """

        if not self.active:
            return ''

        if self._gradient is not None:
            fill = self._gradient
        else:
            fill = self._fill

        parameters = {'fill': fill,
                      'fill-opacity': self._fill_opacity,
                      'stroke': self._stroke,
                      'stroke-opacity': self._stroke_opacity,
                      'stroke-width': self._stroke_width,
                      'stroke-dasharray': self._stroke_dasharray}

        if outer_pars is not None:
            parameters.update(outer_pars)

        entries = []

        for key, val in parameters.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        return entries
