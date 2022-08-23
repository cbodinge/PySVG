class Linear:
    def __init__(self, name: str):
        self._stops = []
        self.name = name
        self.orientation = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 1}
        self.active = True

    def add_stop(self, percent: float, color: list[int, int, int], opacity: float = 1.0):
        if percent < 0:
            percent = 0
        elif percent > 1:
            percent = 1

        color = list(color)
        for i in range(len(color)):
            if color[i] < 0:
                color[i] = 0
            elif color[i] > 255:
                color[i] = 255

        color = '#' + '%02x%02x%02x' % tuple(color)

        if opacity < 0:
            opacity = 0
        elif opacity > 1:
            opacity = 1

        self._stops.append([percent, color, opacity])

    def construct(self):
        svg = []
        if self.active and self._stops != []:
            stop_str = '<stop offset="%s" stop-color="%s" stop-opacity="%s"/>'
            stops = [stop_str % tuple(stop) for stop in self._stops]

            svg = ['<linearGradient id="%s"' % (self.name,)] + \
                  ['x1="%(x1)s" x2="%(x2)s" y1="%(y1)s" y2="%(y2)s">' % self.orientation] + \
                  stops + ['</linearGradient>']

        return '\n'.join(svg)
