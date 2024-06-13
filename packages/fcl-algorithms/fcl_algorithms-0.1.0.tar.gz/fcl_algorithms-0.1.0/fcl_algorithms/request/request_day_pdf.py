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
pdf.imagex("./pdf_contents_g/base.png", 0, 0, 210, 275)
#######################

try:
    stats_path = "./pdf_contents_g/date_text_" + request_id + ".txt"
    f = open(stats_path)
    f.close()
except IOError:
    pdf.output("./pdf_contents_g/test_" + request_id + ".pdf", 'F')
    exit()



#######################
#   2) INCLUDE STATS
stats_path = "./pdf_contents_g/date_text_" + request_id + ".txt"
with open(stats_path) as file:
    stats_dic = json.load(file)

# Report the summary statistics
stats_dic["date"] = stats_dic["date"].replace("_", "/")
pdf.bluetext(stats_dic["date"], 73, 37)

pdf.bluetext(stats_dic["total_transactions"], 73, 42)
pdf.bluetext(stats_dic["total_address"], 73, 48)
pdf.bluetext(stats_dic["total_wallet"], 73, 53)
pdf.bluetext(stats_dic["total_vol"], 73, 59)
pdf.bluetext(stats_dic["total_coms"], 73, 64)

# Report the type splits
vol_tot = float(stats_dic["total_vol"])
vol_ot = round(stats_dic["splits"][0]*0.00000001, 4)
vol_min = round(stats_dic["splits"][1]*0.00000001, 4)
vol_ex = round(stats_dic["splits"][2]*0.00000001, 4)
vol_bk = round(stats_dic["splits"][3]*0.00000001, 4)
vol_or = round(stats_dic["splits"][4]*0.00000001, 4)
vol_st = round(stats_dic["splits"][5]*0.00000001, 4)
vol_scam = round(stats_dic["splits"][6]*0.00000001, 4)

vol_ot = round((vol_ot/vol_tot)*100, 1)
vol_min = round((vol_min/vol_tot)*100, 1)
vol_ex = round((vol_ex/vol_tot)*100, 1)
vol_bk = round((vol_bk/vol_tot)*100, 1)
vol_or = round((vol_or/vol_tot)*100, 1)
vol_st = round((vol_st/vol_tot)*100, 1)
vol_scam = round((vol_scam/vol_tot)*100, 1)

vol_ot = str(vol_ot) + "%"
vol_min = str(vol_min) + "%"
vol_ex = str(vol_ex) + "%"
vol_bk = str(vol_bk) + "%"
vol_or = str(vol_or) + "%"
vol_st = str(vol_st) + "%"
vol_scam = str(vol_scam) + "%"


pdf.whitetext(vol_ot, 161, 52)
pdf.blacktext(vol_min, 112, 52)
pdf.blacktext(vol_ex, 111, 64)
pdf.whitetext(vol_bk, 161, 64)
pdf.blacktext(vol_or, 112, 41)
pdf.whitetext(vol_st, 161, 41)
pdf.blacktext(vol_scam, 112, 75)

# Report the key communitites
type_translate = {"0":"Unknown", "1":"Miners", "2":"Exchanges", "3":"Black Market", "4":"Origin",
                  "5":"State Backed Illicit", "6":"Scams and Ransomware"}

for i in range(5):
    pdf.redtext(str(i + 1), 110, (112 + (i * 10)))
    pdf.redtext("("+type_translate[stats_dic["comm_type"][i]]+")", 170, (112+(i*10)))
    pdf.bluetext(str(stats_dic["comm_size"][i]), 110, (117 + (i * 10)))
    pdf.bluetext(str(stats_dic["comm_vol_with"][i]), 130, (117 + (i * 10)))
    pdf.bluetext(str(stats_dic["comm_vol_in"][i]), 160, (117 + (i * 10)))
    pdf.bluetext(str(stats_dic["comm_vol_out"][i]), 180, (117 + (i * 10)))

# Report the key wallets
for i in range(5):
    pdf.redtext(stats_dic["wallets_key"][i], 14, (112+(i*10)))
    pdf.bluetext(str(stats_dic["wallets_size"][i]), 14, (117 + (i * 10)))
    pdf.bluetext(str(stats_dic["wallets_in_v"][i]), 45, (117 + (i * 10)))
    pdf.bluetext(str(stats_dic["wallets_out_v"][i]), 75, (117 + (i * 10)))
#######################


#######################
#  3) INCLUDE VISUALS
# Grab the global graph
pdf.imagex("./pdf_contents_g/full_graph_" + request_id + ".png", 45, 175, 120, 80)
#######################


#######################
#   4) SAVE PDF
pdf.output("./pdf_contents_g/test_" + request_id + ".pdf", 'F')
#######################


#######################
#   5) ELIMINATE STATS
if os.path.exists("./pdf_contents_g/date_text_" + request_id + ".txt"):
    os.remove("./pdf_contents_g/date_text_" + request_id + ".txt")
if os.path.exists("./pdf_contents_g/full_graph_" + request_id + ".png"):
    os.remove("./pdf_contents_g/full_graph_" + request_id + ".png")
#######################

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))


# Put the pdf file together.
#pdf = PDF(orientation='P', unit='mm', format='A4')
#pdf.add_page()
#pdf.lines()
#pdf.imagex("./assets/fcl_logo.png", 20.0, 10.0, 1700/80, 1700/80)
#pdf.titles("FindCryptoLinks: Address Report")
#pdf.texts("./pdf_contents_a/address_text_"+request_id+".txt", 10, 50)

#pdf.imagex("./pdf_contents_a/address_network_"+request_id+".png", 30.0, 100.0, 64, 48)
#pdf.stats("./pdf_contents_a/info_text_"+request_id+".txt", 100.0, 100.0)

#pdf.output("./pdf_contents_a/test_" + request_id + ".pdf", 'F')