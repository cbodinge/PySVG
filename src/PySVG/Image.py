class Image:
    def __init__(self, x: float, y: float, path: str):
        self.x = x
        self.y = y
        self.path = path

    def construct(self):
        """
        Constructs the SVG string representation of this element. All parameters that are None are ignored.

        :return: the SVG string for this element. If this element isn't active then this returns an empty string.
        :rtype: str
        """

        parameters = {'x': self.x,
                      'y': self.y,
                      'href': self.path}

        entries = []

        for key, val in parameters.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        return '<image %s />' % (entries,)
