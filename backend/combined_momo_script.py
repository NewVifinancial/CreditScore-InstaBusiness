############ All you need to modify is below ############
import django
from datetime import datetime
import csv
import sys,os
from loans.models import Transactions, Calculation, CreditScore


# Full path and name to your csv file
csv_filepathname=r"C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\StrippedMomotoCSV.csv"

csv_filepathname_calc=r"C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\elligible.csv"

csv_filepathname_score=r"C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\scoretable.csv"

# Full path to the directory immediately above your django project directory
your_djangoproject_home= r"C:\Users\Chakdahah\Downloads\Django-main\Django-main"
############ All you need to modify is above ############

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='analytics_project.settings'
django.setup()

def format_date(date_str):
    dt = datetime.strptime(date_str, "%d/%m/%Y").date()
    formatted_date_str = dt.strftime('%Y-%m-%d')
    return formatted_date_str


with open(csv_filepathname, "r") as csvfile:

    dataReader = csv.reader(csvfile)
    next(dataReader)

    for row in dataReader:
        # print(row[0])
        trans = Transactions()
        trans.transaction_date = format_date(row[1])

        trans.transaction_time =row[2]
        trans.from_acct = row[3]
        trans.from_name = row[4]
        trans.from_no =row[5]
        trans.trans_type = row[6]
        trans.amount = float(row[7])
        trans.fees = float(row[8])
        trans.ba_before = float(row[9])
        trans.bal_after = float(row[10])
        trans.to_no = row[11]
        trans.to_name = row[12]
        trans.to_acct =row[13]
        trans.f_id =float(row[14])
        trans.ref = row[15]
        trans.ova = row[16]

        trans.save()




with open(csv_filepathname_score, "r") as csvfile:

    dataReader = csv.reader(csvfile)
    next(dataReader)

    for row in dataReader:

        score = CreditScore()

        score.id_number = row[1]
        score.agent_name = row[2]
        score.len_of_serve_score =row[3]
        score.freq_act_score=row[4]
        score.freq_rebal_score = row[5]
        score.median_cash_in_score =row[6]
        score.mode_cash_in_score = row[7]
        score.median_cash_out_score = row[8]
        score.mode_cash_out_score = row[9]
        score.credit_score = row[10]
        score.eligibility = row[11]
      
        score.save()





with open(csv_filepathname_calc, "r") as csvfile:

    dataReader = csv.reader(csvfile)
    next(dataReader)

    for row in dataReader:

        calc = Calculation()
        
        calc.freq_activity =row[1]
        calc.freq_of_rebal = row[2]
        calc.mode_cash_in = float(row[3])
        calc.median_cash_in =float(row[4])
        calc.mode_cash_out = float(row[5])
        calc.median_cash_out = float(row[6])
      
        calc.save()


