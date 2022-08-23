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
        return self._stroke_width

    @stroke_width.setter
    def stroke_width(self, width: int):
        if width is not None:
            if width >= 0:
                self._stroke_width = width
        else:
            self._stroke_width = None

    @property
    def stroke_opacity(self):
        return self.stroke_opacity

    @stroke_opacity.setter
    def stroke_opacity(self, opacity: float):
        if opacity is not None:
            if opacity >= 0:
                self._stroke_opacity = opacity
        else:
            self._stroke_opacity = None

    @property
    def stroke_dasharray(self):
        da = self._stroke_dasharray.split(' ')
        if da is not None:
            da = [int(i) for i in da]

        return da

    @stroke_dasharray.setter
    def stroke_dasharray(self, dasharray: list[int]):
        self._stroke_dasharray = ' '.join([str(i) for i in dasharray])

    def copy(self, item=None):
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
