import csv
import json
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


#
# def conn():
#     return pymysql.connect(host='localhost',
#                            user='smartbot',
#                            password='TalhaZubayer789*',
#                            database='docinfo_org',
#                            charset='utf8mb4',
#                            autocommit=True,
#                            cursorclass=pymysql.cursors.DictCursor)


def update_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty, search_name, gender, href,
                  locations, row_id, locations_in_profile, educations, certification, licenses, actions, done):
    try:
        with conn().cursor() as cursor:
            update = "INSERT INTO `doc_id2` (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`, `search_name`, `gender`, `href`, `locations`, `row_id`, `locations_in_profile`, `educations`, `certification`, `licenses`, `actions`, `done`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(update, (
            npi, full_name, first_name, middle_name, last_name, age, state, specialty, search_name, gender, href,
            locations, row_id, locations_in_profile, educations, certification, licenses, actions, done))
    except Exception as e:
        print(e)


def get_doc_id():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM docinfo_org.doc_id where done is TRUE;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


old_data = get_doc_id()
for item in old_data:
    # for item in range(1):
    # item = {'id': 650660, 'npi': '1851602593.0', 'full_name': 'Dr. Eboni C January', 'first_name': 'EBONI', 'middle_name': 'C',
    #  'last_name': 'JANUARY', 'age': '', 'state': 'Texas', 'specialty': 'Obstetrics',
    #  'search_name': 'Danielle Eboni Whittaker, MD', 'gender': 'Female', 'href': 'C2D7F58A-9D2D-4BC4-8066-001EABBEEA8C',
    #  'locations': '["Houston, Texas", "Stone Mountain, Georgia"]', 'row_id': 1,
    #  'locations_in_profile': '["Houston, Texas", "Stone Mountain, Georgia"]',
    #  'educations': '["Augusta University"]', 'certification': '["Pediatrics *"]',
    #  'licenses': '["Texas", "Georgia"]', 'actions': '["No Actions Found"]', 'done': 1}
    row_id = item['id']
    npi = item['npi']
    full_name = item['full_name']
    first_name = item['first_name']
    middle_name = item['middle_name']
    last_name = item['last_name']
    age = item['age']
    state = item['state']
    specialty = item['specialty']
    search_name = item['search_name']
    gender = item['gender']
    href = item['href']
    locations = item['locations']
    location_list = []
    try:
        locations_list = json.loads(locations)
        for index in range(4):
            try:
                text = locations_list[index]
                location_list.append(text)
            except IndexError:
                location_list.append("-")
    except Exception as e:
        print(e)
        location_list = ['-', '-', '-', '-']
    locations = json.dumps(location_list)
    locations_in_profile = item['locations_in_profile']
    locations_in_profile_list = []
    try:
        locations_list = json.loads(locations_in_profile)
        for index in range(4):
            try:
                text = locations_list[index]
                locations_in_profile_list.append(text)
            except IndexError:
                locations_in_profile_list.append("-")
    except Exception as e:
        print(e)
        locations_in_profile_list = ['-', '-', '-', '-']
    locations_in_profile = json.dumps(locations_in_profile_list)
    educations = item['educations']
    certification = item['certification']
    licenses = item['licenses']
    actions = item['actions']
    done = item['done']
    update_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty, search_name, gender, href,
                  locations, row_id, locations_in_profile, educations, certification, licenses, actions, done)