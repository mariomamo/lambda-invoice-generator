from reportlab.lib.colors import tan, green
from reportlab.platypus.flowables import Flowable


class HandAnnotation(Flowable):
    '''A hand flowable.'''

    def __init__(self, xoffset=0, size=None, fillcolor=tan, strokecolor=green):
        super().__init__()
        from reportlab.lib.units import inch
        if size is None: size = 4 * inch
        self.fillcolor, self.strokecolor = fillcolor, strokecolor
        self.xoffset = xoffset
        self.size = size
        # normal size is 4 inches
        self.scale = size / (4.0 * inch)

    def wrap(self, *args):
        return self.xoffset, self.size

    def draw(self):
        canvas = self.canv
        # canvas.setLineWidth(6)
        # canvas.setFillColor(self.fillcolor)
        # canvas.setStrokeColor(self.strokecolor)
        # canvas.translate(self.xoffset + self.size, 0)
        # canvas.rotate(90)
        # canvas.scale(self.scale, self.scale)
        canvas.rect(x=0, y=0, width=1, height=1, stroke=1)
        # hand(canvas, debug=0, fill=1)
