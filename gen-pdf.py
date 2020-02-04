from fpdf import FPDF

class myPdf:
    i = 1
    j = 4
    ox = 0
    oy = 0
    pdf = FPDF('P', 'pt', 'Letter')

    def __init__(self):
        self.pdf.set_font('Arial')

    def next_card(self):
        self.i += 1
        if self.i == 2:
            self.i = 0
            self.j += 1
            if self.j == 5:
                self.pdf.add_page()
                self.j = 0

        self.ox = 54 + 252 * self.i
        self.oy = 36 + 144 * self.j

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

    def horiztext(self, x, y, text):
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.text(self.ox + x, self.oy + y, text)

pdf = myPdf()

for i in range(10):
    pdf.next_card()
    pdf.bgimage('background.png')
    pdf.verttext(53, 'Team 35', 20)
    pdf.verttext(73, 'Lew Zealand', 16)
    for i, text in enumerate([
        'Megs Drinkwater (1234)',
        'Joey Marianer (5503)',
        'Angela Brett (5501)',
        'Marni Hager (10646)',
        'Laura Parcel (11714)',
        'Randy Parcel (11714)',
        'C. Monkey (11717)',
        'L. Monkey (11717)',
        ]):
        pdf.rect(106, 15 + i * 15, 4, 4)
        pdf.horiztext(113, 20 + i * 15, text)
pdf.pdf.output('foo.pdf', 'F')

