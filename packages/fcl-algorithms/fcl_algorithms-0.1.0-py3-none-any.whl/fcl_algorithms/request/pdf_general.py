from fpdf import FPDF


class PDF(FPDF):
    def lines(self):
        self.rect(5.0, 5.0, 200.0, 287.0)

    def imagex(self, path, x_coord, y_coord, x_dim, y_dim):
        self.set_xy(x_coord, y_coord)
        self.image(path, link='', type='', w=x_dim, h=y_dim)

    def titles(self, text):
        self.set_xy(0.0, 0.0)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=210.0, h=40.0, align='C', txt=text, border=0)

    def texts(self, name, x_coord, y_coord):
        with open(name, 'rb') as xy:
            txt = xy.read().decode('latin-1')
        self.set_xy(x_coord, y_coord)
        self.set_text_color(36.0, 36.0, 36.0)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 12)
        self.multi_cell(0, 10, txt)

    def stats(self, name, x_coord, y_coord):
        with open(name, 'rb') as xy:
            txt = xy.read().decode('latin-1')
        self.set_xy(x_coord, y_coord)
        self.set_text_color(39, 106, 251)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 14)
        self.multi_cell(0, 10, txt)

# Put the pdf file together.
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.lines()
pdf.imagex("./assets/fcl_logo.png", 20.0, 10.0, 1700/80, 1700/80)
pdf.titles("FindCryptoLinks: General Report")
pdf.texts("./pdf_contents_g/general_text.txt", 10, 50)

pdf.stats("./pdf_contents_g/info_text.txt", 100.0, 100.0)


pdf.output('./pdf_contents_g/test.pdf', 'F')
