import csv
import time

import pymysql


state_map = {
"AL": "Alabama",
"AK": "Alaska",
"AS": "American Samoa",
"AZ": "Arizona",
"AR": "Arkansas",
"CA": "California",
"CO": "Colorado",
"CT": "Connecticut",
"DE": "Delaware",
"DC": "District Of Columbia",
"FM": "Federated States Of Micronesia",
"FL": "Florida",
"GA": "Georgia",
"GU": "Guam",
"HI": "Hawaii",
"ID": "Idaho",
"IL": "Illinois",
"IN": "Indiana",
"IA": "Iowa",
"KS": "Kansas",
"KY": "Kentucky",
"LA": "Louisiana",
"ME": "Maine",
"MH": "Marshall Islands",
"MD": "Maryland",
"MA": "Massachusetts",
"MI": "Michigan",
"MN": "Minnesota",
"MS": "Mississippi",
"MO": "Missouri",
"MT": "Montana",
"NE": "Nebraska",
"NV": "Nevada",
"NH": "New Hampshire",
"NJ": "New Jersey",
"NM": "New Mexico",
"NY": "New York",
"NC": "North Carolina",
"ND": "North Dakota",
"MP": "Northern Mariana Islands",
"OH": "Ohio",
"OK": "Oklahoma",
"OR": "Oregon",
"PW": "Palau",
"PA": "Pennsylvania",
"PR": "Puerto Rico",
"RI": "Rhode Island",
"SC": "South Carolina",
"SD": "South Dakota",
"TN": "Tennessee",
"TX": "Texas",
"UT": "Utah",
"VT": "Vermont",
"VI": "Virgin Islands",
"VA": "Virginia",
"WA": "Washington",
"WV": "West Virginia",
"WI": "Wisconsin",
"WY": "Wyoming"
}


def conn():
    return pymysql.connect(host='localhost',
                           user='myrvtrader',
                           password='Rvtrader123!',
                           database='docinfo_org',
                           charset='utf8mb4',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


def update_doc_id(row_id, locations_in_profile, educations, certification, licenses, actions, done=True):
    try:
        with conn().cursor() as cursor:
            update = 'UPDATE `doc_id_master` SET `locations_in_profile`=%s, `educations`=%s, `certification`=%s, `licenses`=%s, `actions`=%s, done=%s WHERE `id` =%s;'
            cursor.execute(update, (locations_in_profile, educations, certification, licenses, actions, done, str(row_id)))
            print(f"saved successfully {row_id}")
    except Exception as e:
        print(e)


def get_doc_id():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM docinfo_org.doc_id_master where done is NULL order by id desc limit 100;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()

            for item in data_:
                rowid = item['id']
                update_docid(rowid, False)
            return data_
    except Exception as e:
        print(e)


def insert_into_doc_info_table(long_data):
    try:
        with conn().cursor() as cursor:
            insert_sql = 'INSERT INTO `docinfo_input` (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
            # insert_sql = "INSERT INTO `pharmasave_store` (`store_id`, `shopnumber`, `title`, `address1`, `pharmasave_link`, `pharmasave_web`) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute_many(long_data)
    except Exception as e:
        print(e)
        # pass


def insert_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty, href, search_name, gender, location, row_id):

    try:
        with conn().cursor() as cursor:
            insert_sql = "INSERT INTO `doc_id_master` (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`, `href`, `search_name`, `gender`, `locations`, `row_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_sql, (npi, full_name, first_name, middle_name, last_name, age, state, specialty, href, search_name, gender, location, row_id))
            print("success", npi, full_name, first_name, middle_name, last_name, age, state, specialty, href, search_name, gender, location, row_id)
    except Exception as e:
        print("duplicate: ", npi, full_name, first_name, middle_name, last_name, age, state, specialty, href, search_name, gender, location, row_id)
        # pass


def update_input2(row_id, done=True):
    try:
        with conn().cursor() as cursor:
            update = "UPDATE `docinfo_input2` SET `done` = %s WHERE `id` = %s;"
            cursor.execute(update, (done, row_id))
    except Exception as e:
        print(e)


def update_docid(row_id, done=True):
    try:
        with conn().cursor() as cursor:
            update = "UPDATE `doc_id_master` SET `done` = %s WHERE `id` = %s;"
            cursor.execute(update, (done, row_id))
    except Exception as e:
        print(e)


def select_all():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM docinfo_org.docinfo_input2 where done is NULL limit 100;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            for item in data_:
                rowid = item['id']
                update_input2(rowid, False)
            return data_
    except Exception as e:
        print(e)


csv_file = '500k_docinfo.csv'
data = []
# with open(csv_file, 'r', newline='') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         data.append(row)
#     time.sleep(5)
#     n = 0
#     data_to_insert = []
#     for row in data:
#         n += 1
#         # print(n)
#         # insert_into_doc_info_table(row['NPI'], row['Full Name'], row['First Name'], row['Middle Name'], row['Last Name'], row['State'], row['Age'], row['specialty'])
#         npi = row['NPI']
#         full_name = row['Full Name']
#         first_name = row['First Name']
#         middle_name = row['Middle Name']
#         last_name = row['Last Name']
#         state_code = row['State']
#         state = None
#         try:
#             state = state_map[state_code]
#         except:
#             print(n, state_code)
#
#         age = row['Age']
#         specialty = row['specialty']
#         # insert_into_doc_info_table(npi, full_name, first_name, middle_name, last_name, age, state, specialty)
#         data_dict = {
#             'npi': npi,
#             'full_name': full_name,
#             'first_name': first_name,
#             'middle_name': middle_name,
#             'last_name': last_name,
#             'state': state,
#             'age': age,
#             'specialty': specialty
#         }
#         data_to_insert.append(data_dict)
#         if n > 500000:
#             break
#     # cursor = conn().cursor()
#     # insert_query = 'INSERT INTO `docinfo_input2` (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
#     # cursor.executemany(insert_query, [(item["npi"], item["full_name"], item["first_name"], item["middle_name"], item["last_name"], item["age"], item["state"], item["specialty"]) for item in data_to_insert])
#     # conn().commit()
#     # conn().close()



state_map_2 = {"Alabama": "AL",
               "Alaska": "AK",
               "American Samoa": "AS",
               "Arizona": "AZ",
               "Arkansas": "AR",
               "California": "CA",
               "Colorado": "CO",
               "Connecticut": "CT",
               "Delaware": "DE",
               "District Of Columbia": "DC",
               "Federated States Of Micronesia": "FM",
               "Florida": "FL",
               "Georgia": "GA",
               "Guam": "GU",
               "Hawaii": "HI",
               "Idaho": "ID",
               "Illinois": "IL",
               "Indiana": "IN",
               "Iowa": "IA",
               "Kansas": "KS",
               "Kentucky": "KY",
               "Louisiana": "LA",
               "Maine": "ME",
               "Marshall Islands": "MH",
               "Maryland": "MD",
               "Massachusetts": "MA",
               "Michigan": "MI",
               "Minnesota": "MN",
               "Mississippi": "MS",
               "Missouri": "MO",
               "Montana": "MT",
               "Nebraska": "NE",
               "Nevada": "NV",
               "New Hampshire": "NH",
               "New Jersey": "NJ",
               "New Mexico": "NM",
               "New York": "NY",
               "North Carolina": "NC",
               "North Dakota": "ND",
               "Northern Mariana Islands": "MP",
               "Ohio": "OH",
               "Oklahoma": "OK",
               "Oregon": "OR",
               "Palau": "PW",
               "Pennsylvania": "PA",
               "Puerto Rico": "PR",
               "Rhode Island": "RI",
               "South Carolina": "SC",
               "South Dakota": "SD",
               "Tennessee": "TN",
               "Texas": "TX",
               "Utah": "UT",
               "Vermont": "VT",
               "Virgin Islands": "VI",
               "Virginia": "VA",
               "Washington": "WA",
               "West Virginia": "WV",
               "Wisconsin": "WI",
               "Wyoming": "WY"
               }

