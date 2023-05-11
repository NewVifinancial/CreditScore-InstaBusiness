############ All you need to modify is below ############
import django
from datetime import datetime, date
import csv


# Full path and name to your csv file
csv_filepathname=r"C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\StrippedMomotoCSV.csv"
# Full path to the directory immediately above your django project directory
your_djangoproject_home= r"C:\Users\Chakdahah\Downloads\Django-main\Django-main"
############ All you need to modify is above ############

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='analytics_project.settings'
django.setup()

from loans.models import Transactions
# , Calculation, CreditScore


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



        

    # lawyer_school=School.objects.get(name=row[4])
    # lawyer.school=lawyer_school

    # lawyer.year_graduated=row[5]
    # lawyer.save()