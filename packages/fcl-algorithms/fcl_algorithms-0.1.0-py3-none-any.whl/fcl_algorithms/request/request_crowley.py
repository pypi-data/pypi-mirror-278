
import sys
from datetime import datetime
from csv import writer

# Decide what location we want to use
file_location = "../fcl_data/"
##file_location = "/Volumes/DingosDiner/fcl_data/"

request_time = datetime.today()
request_email = "test@email.com"                        #sys.argv[1]            #                   "test@email.com"
request_date = "04_05_2022"                             #sys.argv[2]            #"dd_mm_yyyy"       "02_05_2022"
request_address = "1H8sDTTgJPBKw83EBZDLhXvetCbxZUMMZM"  #sys.argv[3]            #'address'
request_comm = "None"                                   #sys.argv[4]            # 'Name'

List = [request_time, request_email, request_date, request_address, request_comm]

file_path = file_location + "summary_stats/crowley.csv"
with open(file_path, 'a') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(List)
    f_object.close()