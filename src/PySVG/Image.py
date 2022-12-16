from pathlib import Path

class Image:
    def __init__(self, x: float, y: float, path: str):
        self.x = x
        self.y = y
        self.height = 0
        self.width = 0
        self.path = Path(path)

        self.active = True

    def construct(self):
        """
        Constructs the SVG string representation of this element. All parameters that are None are ignored.

        :return: the SVG string for this element. If this element isn't active then this returns an empty string.
        :rtype: str
        """

        parameters = {'href': self.path,
                      'x': self.x,
                      'y': self.y}

        entries = []

        for key, val in parameters.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        return '<image %s />' % (entries,)
