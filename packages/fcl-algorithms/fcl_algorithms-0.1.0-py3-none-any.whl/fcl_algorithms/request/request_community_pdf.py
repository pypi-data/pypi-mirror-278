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

    def whitetext(self, text, x_coord, y_coord):
        self.set_xy(x_coord, y_coord)
        self.set_text_color(250, 250, 250)
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
pdf.imagex("./pdf_contents_c/base.png", 0, 0, 210, 275)
#######################

try:
    stats_path = "./pdf_contents_c/comm_text_" + request_id + ".txt"
    f = open(stats_path)
    f.close()
except IOError:
    pdf.output("./pdf_contents_c/test_" + request_id + ".pdf", 'F')
    exit()


#######################
#   2) INCLUDE STATS
stats_path = "./pdf_contents_c/comm_text_" + request_id + ".txt"
with open(stats_path) as file:
    stats_dic = json.load(file)

type_translate = {"0":"Unknown", "1":"Miners", "2":"Exchanges", "3":"Black Market", "4":"Origin",
                  "5":"State Backed Illicit", "6":"Scams and Ransomware"}

# Report the summary statistics
stats_dic["date"] = stats_dic["date"].replace("_", "/")
pdf.bluetext(stats_dic["date"], 73, 42)

pdf.redtext(stats_dic["comm_name"], 73, 37)
pdf.bluetext(stats_dic["comm_rank"], 73, 48)
pdf.bluetext(type_translate[str(stats_dic["comm_type"])], 73, 53)
pdf.bluetext(str(stats_dic["comm_size"]), 73, 59)
pdf.bluetext(str(stats_dic["comm_link_with"]), 73, 64)
pdf.bluetext(stats_dic["comm_vol_with"], 73, 70)

pdf.bluetext(stats_dic["comm_link_in"], 175, 43)
pdf.bluetext(stats_dic["comm_link_out"], 175, 49)
pdf.bluetext(stats_dic["comm_vol_in"], 175, 54)
pdf.bluetext(stats_dic["comm_vol_out"], 175, 60)

# Report the key wallets in community:
for i in range(11):
    pdf.redtext(str(stats_dic["key_wallets"][i]), 10, (185 + (i * 6)))
    pdf.bluetext(type_translate[stats_dic["key_types"][i]], 125, (185 + (i * 6)))
    pdf.bluetext(str(stats_dic["key_size"][i]), 149, (185 + (i * 6)))
    pdf.bluetext(str(stats_dic["key_vol_in"][i]), 164, (185 + (i * 6)))
    pdf.bluetext(str(stats_dic["key_vol_out"][i]), 184, (185 + (i * 6)))
#######################


#######################
#  3) INCLUDE VISUALS
# Grab the global graph
pdf.imagex("./pdf_contents_c/full_graph_" + request_id + ".png", 120, 108, 70, 50)
# Grab the community graph
pdf.imagex("./pdf_contents_c/comm_graph_" + request_id + ".png", 20, 108, 70, 50)
#######################


#######################
#   4) SAVE PDF
pdf.output("./pdf_contents_c/test_" + request_id + ".pdf", 'F')
#######################


#######################
#   5) ELIMINATE STATS
if os.path.exists("./pdf_contents_c/comm_text_" + request_id + ".txt"):
    os.remove("./pdf_contents_c/comm_text_" + request_id + ".txt")
if os.path.exists("./pdf_contents_c/full_graph_" + request_id + ".png"):
    os.remove("./pdf_contents_c/full_graph_" + request_id + ".png")
if os.path.exists("./pdf_contents_c/comm_graph_" + request_id + ".png"):
    os.remove("./pdf_contents_c/comm_graph_" + request_id + ".png")
#######################


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))