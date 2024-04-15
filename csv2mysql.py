import pymysql
import csv

# MySQL Connection Parameters
host = 'your_mysql_host'
user = 'your_mysql_user'
password = 'your_mysql_password'
database = 'your_mysql_database'

def conn():
    return pymysql.connect(host='localhost',
                           user='mdbaki',
                           password='TalhaZubayer789*',
                           database='docinfo_org',
                           charset='utf8mb4',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


# CSV File Path
csv_file_path = '/home/baki/PycharmProjects/docinfo/completed.csv'

# Establish a connection to the MySQL server
# connection = pymysql.connect(host=host, user=user, password=password, database=database)

try:
    with conn().cursor() as cursor:
        # Open the CSV file and create a CSV reader
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Skip the header row
            next(csv_reader)

            # Iterate through the CSV data and insert into MySQL
            n = 0
            for row in csv_reader:
                try:
                    sql = """
                        INSERT INTO `search_people2` (npi, csv_full_name, first_name, middle_name, last_name, Age, State1, specialization,
                                                    dFull_Name, FirstName, MiddleName, LastName, dCreds, dGender, dLocations, AgeRange, City, State)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, tuple(row))
                    n += 1
                    if n == 65:
                        print(n)
                # print(n)
                except Exception as e:
                    print(e)
        # Commit the changes
        # connection.commit()
except Exception as e:
    print(e)
# finally:
#     Close the connection
    # connection.close()
