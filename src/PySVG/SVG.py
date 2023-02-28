from math import sin, cos, pi


class SVG:
    def __init__(self, w: float, h: float):
        """
        Creates an SVG container for children to be added to.

        :param w: width of the SVG in pixels
        :param h: height of the SVG in pixels
        """
        self._children = []
        self.size = (w, h)
        self.defs = []

        self._top = True

        self.tab = 3 * ' '

        self.active = True

    @property
    def top(self):
        """
        True if this class instance is the top level SVG, False if it is embedded.
        """
        return self._top

    @top.setter
    def top(self, top: bool):
        self._top = top

    def insert_child(self, child, index: int = 0, label: str = ''):
        """
        Append a child instance to this SVG

        :param child: Usually a subclass of Paths.Path. Needs to have a ``construct()`` method

        :param index: position to insert child in list of children

        :param label: A label that is applied if set in the svg file to make troubleshooting/organization more efficient
        """
        new_child = Child(child)
        new_child.label = label
        self._children.insert(index, new_child)

    def add_child(self, child, label: str = ''):
        """
        Append a child instance to this SVG

        :param child: Usually a subclass of Paths.Path. Needs to have a ``construct()`` method

        :param label: A label that is applied if set in the svg file to make troubleshooting/organization more efficient
        """
        new_child = Child(child)
        new_child.label = label
        self._children.append(new_child)

    def _build_defs(self):
        defs = []
        if self.defs:
            defs.append(self.tab + '<defs>')
            for d in self.defs:
                defs.append(2 * self.tab + d.construct())
            defs.append(self.tab + '</defs>')

            return '\n'.join(defs)

    def copy(self):
        """
        Creates a new SVG.SVG instance and copies all of its children recursively.

        :return: ``SVG.SVG`` The instance handle for the copied object
        """
        new = SVG(self.size[0], self.size[1])

        new.tab = self.tab
        new.defs = self.defs[:]

        for child in self._children:
            c = child.child_ref.copy()
            new.add_child(c, child.label)

        return new

    def construct(self):
        """
        Recursively triggers ``construct()`` method in all children. An svg element string is generated for each
        child and appended to the parent. This class returns a complete SVG string

        :return: SVG in string form
        :rtype: str
        """
        if not self.active:
            return ''

        comment = '\n<!--%s ************************************************************************************-->\n'
        if self.top:
            svg = ['<svg width="%s" height="%s" xmlns="http://www.w3.org/2000/svg">' % self.size, self._build_defs()]
        else:
            svg = ['<svg width="%s" height="%s">' % self.size, self._build_defs()]

        for child in self._children:
            if child.active:
                c = child.child_ref
                child_svg = self.tab + c.construct().replace('\n', '\n' + self.tab)
                if child.label == '':
                    row = [child_svg]
                else:
                    row = [comment % child.label,
                           child_svg]

                svg.append('\n'.join(row))

        svg.append('</svg>')

        self._children = []

        svg = [i for i in svg if i]

        return '\n'.join(svg)


class Child:
    def __init__(self, child):
        """
        Holding Class for the children of ``SVG.SVG`` and ``SVG.Section``.

        child is usually a ``Paths.Path`` object.

        :param child:
        """
        self.child_ref = child
        self.label = ''

    @property
    def active(self) -> bool:
        """
        Ensures that all children can be evaluated for the active property.

        :return: When this property exists for the child reference then returns the child reference value; otherwise returns False.

        :rtype: bool
        """
        try:
            return self.child_ref.active
        except AttributeError:
            return False


class Section:
    def __init__(self, x: float, y: float):
        """
            Represents a **<g>** element. x and y will perform a translation on every element in this section.

            :param x: translates this section right/left
            :param y: translates this section up/down
        """

        self.x, self.y = x, y
        self.xc, self.yc = 0, 0

        self._children = []

        self.tab = 3 * ' '

        self.angle = 0
        self.xscale = 1
        self.yscale = 1

        self.active = True

    def add_child(self, child, label: str = ''):
        """
        Append a child instance to this SVG

        :param child: Usually a subclass of Paths.Path. Needs to have a ``construct()`` method

        :param label: A label that is applied if set in the svg file to make troubleshooting/organization more efficient
        """
        new_child = Child(child)
        new_child.label = label
        self._children.append(new_child)

    def insert_child(self, child, index: int = 0, label: str = ''):
        """
        Append a child instance to this SVG

        :param child: Usually a subclass of Paths.Path. Needs to have a ``construct()`` method

        :param index: position to insert child in list of children

        :param label: A label that is applied if set in the svg file to make troubleshooting/organization more efficient
        """
        new_child = Child(child)
        new_child.label = label
        self._children.insert(index, new_child)

    def copy(self, new=None):
        """
            Creates a new ``SVG.SVG`` instance and copies all of its children recursively.

            :return: ``SVG.SVG`` The instance handle for the copied object
        """
        if new is not None:
            new = Section(self.x, self.y)

        new.tab = self.tab

        for child in self._children:
            c = child.child_ref.copy()
            new.add_child(c, child.label)

        return new

    def tranform(self):
        x, y = self.x, self.y

        xc, yc = self.xc, self.yc

        xs, ys = self.xscale, self.yscale

        c = cos(pi * self.angle / 180)
        s = sin(pi * self.angle / 180)

        xn = x + xc * (1 + xs * s - xs * c)
        yn = y + yc * (1 - ys * s - ys * c)

        return [f'<g transform="matrix({xs * c},{ys * s},{xs * -s},{ys * c},{xn},{yn})">']

    def construct(self):
        """
            Recursively triggers ``construct()`` method in all children. An svg element string is generated for each
            child and appended to the parent. This class returns a complete SVG **<g>** section.

            :return: SVG in string form
            :rtype: str
        """
        if not self.active:
            return ''

        svg = self.tranform()

        comment = '\n<!--%s-->\n'

        for child in self._children:
            if child.active:
                c = child.child_ref
                child_svg = self.tab + c.construct().replace('\n', '\n' + self.tab)
                if child.label == '':
                    row = [child_svg]
                else:
                    row = [comment % child.label,
                           child_svg]

                svg.append('\n'.join(row))

        svg.append('</g>')

        self._children = []

        return '\n'.join(svg)


class Embedded(Section):
    def __init__(self):
        """
        Convenience Class for creating SVGs that are embedded in other SVGs. This implementation is a subclass of the
        ``SVG.Section`` with a native child that is type ``SVG.SVG``.
        """
        super().__init__(0, 0)
        self._svg = SVG(0, 0)
        self._svg.top = False
        self.w, self.h = 0, 0

    @property
    def w(self):
        """Width of the embedded SVG in pixels"""
        return self._svg.size[0]

    @w.setter
    def w(self, w):
        self._svg.size = (w, self.h)

    @property
    def h(self):
        """Height of the embedded SVG in pixels"""
        return self._svg.size[1]

    @h.setter
    def h(self, h):
        self._svg.size = (self.w, h)

    @property
    def defs(self):
        return self._svg.defs

    @defs.setter
    def defs(self, defs):
        self._svg.defs = defs

    def add_child(self, child, label: str = ''):
        self._svg.add_child(child, label)

    def insert_child(self, child, index: int = 0, label: str = ''):
        self._svg.insert_child(child, index, label)

    def construct(self):
        """
            Recursively triggers ``construct()`` method in all children. An svg element string is generated for each
            child and appended to the *native* ``SVG.SVG`` *child object*.

            :return: SVG in string form
            :rtype: str
        """
        super().add_child(self._svg)

        return super().construct()

    def copy(self, **kwargs):
        new = Embedded()
        new._svg = self._svg.copy()

        new.tab = self.tab

        new.w = self.w
        new.h = self.h

        return new
