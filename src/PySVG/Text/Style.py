class Style:
    def __init__(self):
        self.children = []
        self.tab = '  '

    def add_child(self, child):
        self.children.append(child)

    def construct(self):
        svg = ['<style>']
        for c in self.children:
            child_svg = self.tab + c.construct().replace('\n', '\n' + self.tab)
            row = [child_svg]

            svg.append('\n'.join(row))

        svg.append('</style>')

        return '\n'.join(svg)

    def add_font(self, font):
        self.add_child(Font(font))


class Font:
    def __init__(self, font):
        self.font = font

    def construct(self):
        svg = ['@font-face{',
               f'font-family:"{self.font.family}-{self.font.weight}";',
               f'src:url(data:application/font-woff;charset=utf8;base64,{self.font.getBase64()}) format("woff");}}']

        return '\n'.join(svg)
