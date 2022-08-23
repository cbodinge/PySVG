class SVG:
    def __init__(self, w: int, h: int):
        self._children = []
        self.size = (w, h)
        self.defs = []

        self.top = True

        self.tab = 3 * ' '

        self.active = True

    def add_child(self, child, label: str = ''):
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

        return defs

    def copy(self):
        new = SVG(self.size[0], self.size[1])

        new.tab = self.tab
        new.defs = self.defs[:]

        for child in self._children:
            c = child.child_ref.copy()
            new.add_child(c, child.label)

        return new

    def construct(self):
        if not self.active:
            return ''

        comment = '\n<!--%s ************************************************************************************-->\n'
        if self.top:
            svg = ['<svg width="%s" height="%s" xmlns="http://www.w3.org/2000/svg">' % self.size, self._build_defs()]
        else:
            svg = ['<svg width="%s" height="%s">' % self.size, self._build_defs()]

        for child in self._children:
            if child.active:
                child_svg = self.tab + child.construct().replace('\n', '\n' + self.tab)
                if child.label == '':
                    row = [child.construct()]
                else:
                    row = [comment % child.label,
                           child_svg]

                svg.append('\n'.join(row))

        svg.append('</svg>')

        self._children = []

        return '\n'.join(svg)


class Child:
    def __init__(self, child):
        self.child_ref = child
        self.label = ''

    @property
    def active(self):
        try:
            return self.child_ref.active
        except AttributeError:
            return False


class Section:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

        self._children = []

        self.tab = 3 * ' '

        self.active = True

    def add_child(self, child, label: str = ''):
        new_child = Child(child)
        new_child.label = label
        self._children.append(new_child)

    def copy(self, new=None):
        if new is not None:
            new = Section(self.x, self.y)

        new.tab = self.tab

        for child in self._children:
            c = child.child_ref.copy()
            new.add_child(c, child.label)

        return new

    def construct(self):
        if not self.active:
            return ''

        comment = '\n<!--%s-->\n'
        svg = ['<g transform="matrix(1,0,0,1,%s,%s)"> ' % (self.x, self.y)]

        for child in self._children:
            if child.active:
                child_svg = self.tab + child.construct().replace('\n', '\n' + self.tab)
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
        super().__init__(0, 0)
        self._svg = SVG(0, 0)

        self._svg.top = False

    @property
    def w(self):
        return self._svg.size[0]

    @w.setter
    def w(self, w):
        self._svg.size = (w, self.h)

    @property
    def h(self):
        return self._svg.size[1]

    @h.setter
    def h(self, h):
        self._svg.size = (self.w, h)

    def add_child(self, child, label: str = ''):
        self._svg.add_child(child, label)

    def construct(self):
        self.add_child(self._svg)
        super().construct()

    def copy(self, **kwargs):
        new = Embedded()
        new._svg = self._svg.copy()

        new.tab = self.tab

        new.w = self.w
        new.h = self.h

        return new



