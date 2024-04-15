import pandas as pd
from database2 import conn, update_doc_id
import json


def insert_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty, search_name, gender, href,
                  locations, row_id, locations_in_profile, educations, certification, licenses, actions, done):
    try:
        with conn().cursor() as cursor:
            insert_sql = ("INSERT INTO `doc_id3` (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`, `search_name`, `gender`,"
                          " `href`, `locations`, `row_id`, `locations_in_profile`, `educations`, `certification`, `licenses`, `actions`, `done`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
            cursor.execute(insert_sql, (npi, full_name, first_name, middle_name, last_name, age, state, specialty, search_name, gender, href,
                  locations, row_id, locations_in_profile, educations, certification, licenses, actions, done))
    except Exception as e:
        print(e)
        # pass


def get_doc_id():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM `doc_id2` ;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


data = get_doc_id()
new_data = []
n = 0
for item in data:
    n += 1
    id_ = item['id']
    print(n, id_)
    # if n < 250000:
    #     continue

    # row_id = item['id']
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
    location_list_ = []
    try:
        location_list = json.loads(locations)
        if not len(location_list) > 4:
            for index in range(4):
                try:
                    text = location_list[index]
                    location_list_.append(text)
                except IndexError:
                    location_list_.append("-")
        else:
            location_list_ = location_list
    except Exception as e:
        location_list_ = ['-', '-', '-', '-']
    locations = json.dumps(location_list_)
    row_id = item['row_id']
    locations_in_profile = item['locations_in_profile']
    locations_in_profile_list = []
    locations_in_profile_list_ = []

    try:
        locations_in_profile_list = json.loads(locations_in_profile)

        if not len(locations_in_profile_list) > 4:
            for index in range(4):
                try:
                    text = locations_in_profile_list[index]
                    locations_in_profile_list_.append(text)
                except IndexError:
                    locations_in_profile_list_.append("-")
        else:
            locations_in_profile_list_ = locations_in_profile_list
    except Exception as e:
        locations_in_profile_list_ = ['-', '-', '-', '-']
    locations_in_profile = json.dumps(locations_in_profile_list_)
    educations = item['educations']
    certification = item['certification']
    licenses = item['licenses']
    actions = item['actions']
    done = item['done']
    insert_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty, search_name, gender, href,
                  locations, row_id, locations_in_profile, educations, certification, licenses, actions, done)


