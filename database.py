import csv
import time

import pymysql


def conn():
    return pymysql.connect(host='localhost',
                           user='mdbaki',
                           password='TalhaZubayer789*',
                           database='docinfo_org',
                           charset='utf8mb4',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


def insert_into_doc_info_table(npi, full_name, first_name, middle_name, last_name, age, state, specialty):
    try:
        with conn().cursor() as cursor:
            insert_sql = 'INSERT INTO `docinfo_input` (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
            # insert_sql = "INSERT INTO `pharmasave_store` (`store_id`, `shopnumber`, `title`, `address1`, `pharmasave_link`, `pharmasave_web`) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_sql, (npi, full_name, first_name, middle_name, last_name, age, state, specialty))
    except Exception as e:
        print(e)
        # pass


csv_file = '500k_docinfo.csv'
data = []
with open(csv_file, 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)
    time.sleep(5)
    n = 0
    for row in data:
        n += 1
        print(n)
        # if n == 10:
        #     break
        # print(row)
        # print(row['NPI'])
        # print(row['Full Name'])
        # print(row['First Name'])
        # print(row['Middle Name'])
        # print(row['Last Name'])
        # print(row['State'])
        # print(row['Age'])
        # print(row['specialty'])
        # insert_into_doc_info_table(row['NPI'], row['Full Name'], row['First Name'], row['Middle Name'], row['Last Name'], row['State'], row['Age'], row['specialty'])
        # insert_into_doc_info_table(row['NPI'], row['Full Name'], row['First Name'], row['Middle Name'], row['Last Name'], row['State'], row['Age'], row['specialty'])
        npi = row['NPI']
        full_name = row['Full Name']
        first_name = row['First Name']
        middle_name = row['Middle Name']
        last_name = row['Last Name']
        state = row['State']
        age = row['Age']
        specialty = row['specialty']
        insert_into_doc_info_table(npi, full_name, first_name, middle_name, last_name, age, state, specialty)
