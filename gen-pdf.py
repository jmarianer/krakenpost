import pickle
from fpdf import FPDF

class myPdf:
    i = 3
    j = 1
    ox = 0
    oy = 0
    pdf = FPDF('L', 'pt', 'Letter')

    def __init__(self):
        self.pdf.set_font('Arial')

    def next_card(self):
        self.i += 1
        if self.i == 4:
            self.i = 0
            self.j += 1
            if self.j == 2:
                self.pdf.add_page()
                self.pdf.line(0, 306, 792, 306)
                self.pdf.line(198, 0, 198, 612)
                self.pdf.line(396, 0, 396, 612)
                self.pdf.line(594, 0, 594, 612)
                self.pdf.line(792, 0, 792, 612)
                self.j = 0

        self.ox = 198 * self.i
        self.oy = 306 * self.j

    def rect(self, x, y, w, h):
        self.pdf.rect(self.ox + x, self.oy + y, w, h)

    def line(self, x1, y1, x2, y2):
        self.pdf.line(self.ox + x1, self.oy + y1, self.ox + x2, self.oy + y2)

    def bgimage(self, name):
        self.pdf.image(name, self.ox, self.oy, 252, 144)

    def verttext(self, x, text, size):
        while True:
            self.pdf.set_font('Arial', 'B', size)
            width = self.pdf.get_string_width(text)
            if width < 144: break
            size -= 1
        self.pdf.rotate(90, 0, 0)
        self.pdf.text(-(self.oy + 72 + width/2), self.ox + x, text)
        self.pdf.rotate(0)

    def horiztext(self, x, y, text, style='', size=10):
        self.pdf.set_font('Arial', style, size)
        self.pdf.text(self.ox + x, self.oy + y, text)

pdf = myPdf()

with open('teammates.pickle', 'rb') as f:
    teammates = pickle.load(f)

    #pdf.bgimage('background.png')
    #pdf.verttext(53, 'Team 35', 20)
for name, mates in teammates.items():
    for i, (_, preferred, cabin, considerations) in enumerate(mates):
        if i % 21 == 0:
            pdf.next_card()
            pdf.horiztext(10, 25, f'Teammates for { name.split()[0] }', 'B', 12)
        pdf.rect(23, 40 + (i % 21) * 12, 4, 4)
        pdf.horiztext(30, 45 +(i % 21) * 12, f'{ preferred.split()[0] } ({ cabin })'.encode('ascii', 'ignore').decode('ascii'))
pdf.pdf.output('foo.pdf', 'F')

