import pandas as pd
import pymysql
from sqlalchemy import create_engine

# Read CSV file into a DataFrame
csv_file_path = './input_files/Remaining_NPI.csv'
# df = pd.read_csv(csv_file_path)
# df2 = df.where(pd.notna(df), None)
import csv

data_list = list()

with open(csv_file_path, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
        data_list.append(row)


def conn():
    return pymysql.connect(host='localhost',
                           user='mdbaki',
                           password='TalhaZubayer789*',
                           database='docinfo_org',
                           charset='utf8mb4',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


try:
    with conn().cursor() as cursor:
        count = 0
        for row in data_list:
            count += 1
            if count == 1:
                continue
            try:
                # NPI, first_name, middle_name, last_name, specialty
                insert_query = (f"INSERT INTO docinfo_input2 (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`)\n"
                                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")
                cursor.execute(insert_query, (row[0], None, row[1], row[2], row[3], None, None, row[4]))
                # cursor.execute(insert_query, (row["npi"], row["csv_full_name"], row["first_name"], row["middle_name"], row["last_name"], row["age"], row["LicenseState"], row["Taxonomy Description"]))
            except Exception as e:
                print(e)
except Exception as e:
    print(e)

