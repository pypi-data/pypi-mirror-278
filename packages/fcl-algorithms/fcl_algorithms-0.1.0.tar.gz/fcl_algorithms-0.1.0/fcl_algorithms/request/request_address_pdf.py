# This script will take the generated network statistics and visualisations and produce a pdf report that can be sent.
# The role of this pdf script is to build the PDF report so that it can later be sent to the person relevant.

# 1) Build the placeholder pdf file.
# 2) Load and insert statistics.
# 3) Save the completed pdf.


from fpdf import FPDF
import sys
import json
import time
import os

class PDF(FPDF):
    def lines(self):
        self.rect(5.0, 5.0, 200.0, 287.0)

    def imagex(self, path, x_coord, y_coord, x_dim, y_dim):
        self.set_xy(x_coord, y_coord)
        self.image(path, link='', type='', w=x_dim, h=y_dim)

    def redtext(self, text, x_coord, y_coord):
        self.set_xy(x_coord, y_coord)
        self.set_text_color(220, 50, 50)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 8)
        self.multi_cell(0, 10, text)

    def bluetext(self, text, x_coord, y_coord):
        self.set_xy(x_coord, y_coord)
        self.set_text_color(39, 106, 251)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 9)
        self.multi_cell(0, 10, text)

    def blacktext(self, text, x_coord, y_coord):
        self.set_xy(x_coord, y_coord)
        self.set_text_color(36.0, 36.0, 36.0)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 9)
        self.multi_cell(0, 10, text)

    def titles(self, text):
        self.set_xy(0.0, 0.0)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=210.0, h=40.0, align='C', txt=text, border=0)

    def stats(self, name, x_coord, y_coord):
        with open(name, 'rb') as xy:
            txt = xy.read().decode('latin-1')
        self.set_xy(x_coord, y_coord)
        self.set_text_color(36.0, 36.0, 36.0)
        self.add_font('Questrial', '', './assets/Questrial-Regular.ttf', uni=True)
        self.set_font('Questrial', '', 14)
        self.multi_cell(0, 10, txt)

startTime = time.time()

request_id = sys.argv[1]

#######################
#   1) BUILD PDF
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.imagex("./pdf_contents_a/base.png", 0, 0, 210, 275)
#######################

try:
    stats_path = "./pdf_contents_a/address_text_" + request_id + ".txt"
    f = open(stats_path)
    f.close()
except IOError:
    pdf.output("./pdf_contents_a/test_" + request_id + ".pdf", 'F')
    exit()


#######################
#   2) INCLUDE STATS
stats_path = "./pdf_contents_a/address_text_" + request_id + ".txt"
with open(stats_path) as file:
    stats_dic = json.load(file)


stats_dic["date"] = stats_dic["date"].replace("_", "/")


pdf.redtext(stats_dic["address"], 30, 38)
pdf.bluetext(stats_dic["date"], 80, 45)

if stats_dic["addr_wallet"]:
    pdf.imagex("./pdf_contents_a/green_tick.png", 80, 75, 4, 4)
else:
    pdf.imagex("./pdf_contents_a/red_cross.png", 80, 75, 4, 4)

pdf.bluetext(stats_dic["wallet_type"], 80, 79)
pdf.bluetext(stats_dic["wallet_size"], 80, 86)
pdf.bluetext(stats_dic["w_addr_deg_in"], 80, 93)
pdf.bluetext(stats_dic["w_addr_vol_in"], 80, 100)
pdf.bluetext(stats_dic["w_addr_deg_out"], 80, 107)
pdf.bluetext(stats_dic["w_addr_vol_out"], 80, 114)

i = 0
for item in stats_dic["wallet_intra_key"]:
    pdf.redtext(item, 14, (128+(i*7)))
    i += 1

i = 0
for item in stats_dic["wallet_full_key"]:
    pdf.redtext(item, 14, (156+(i*7)))
    i += 1

if stats_dic["is_commune"]:
    pdf.imagex("./pdf_contents_a/green_tick.png", 80, 180, 4, 4)
else:
    pdf.imagex("./pdf_contents_a/red_cross.png", 80, 180, 4, 4)

pdf.bluetext(stats_dic["comm_type"], 80, 184)
pdf.bluetext(stats_dic["comm_rank"], 80, 191)
pdf.bluetext(stats_dic["comm_size"], 80, 198)

i = 0
for item in stats_dic["comm_intra_key"]:
    pdf.redtext(item, 14, (212+(i*7)))
    i += 1

i = 0
for item in stats_dic["comm_full_key"]:
    pdf.redtext(item, 14, (240+(i*7)))
    i += 1
#######################


#######################
#  3) INCLUDE VISUALS
# Grab the wallet graph
pdf.imagex("./pdf_contents_a/wallet_graph_" + request_id + ".png", 120, 45, 70, 50)
# Grab the community graph
pdf.imagex("./pdf_contents_a/comm_graph_" + request_id + ".png", 120, 120, 70, 50)
# Grab the global graph
pdf.imagex("./pdf_contents_a/full_graph_" + request_id + ".png", 120, 200, 70, 50)
#######################


#######################
#   4) SAVE PDF
pdf.output("./pdf_contents_a/test_" + request_id + ".pdf", 'F')
#######################

#######################
#   5) ELIMINATE STATS
if os.path.exists("./pdf_contents_a/address_text_" + request_id + ".txt"):
    os.remove("./pdf_contents_a/address_text_" + request_id + ".txt")
if os.path.exists("./pdf_contents_a/wallet_graph_" + request_id + ".png"):
    os.remove("./pdf_contents_a/wallet_graph_" + request_id + ".png")
if os.path.exists("./pdf_contents_a/comm_graph_" + request_id + ".png"):
    os.remove("./pdf_contents_a/comm_graph_" + request_id + ".png")
if os.path.exists("./pdf_contents_a/full_graph_" + request_id + ".png"):
    os.remove("./pdf_contents_a/full_graph_" + request_id + ".png")
#######################

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

