import pandas as pd
from pymysql import IntegrityError

from database2 import conn, update_doc_id
import json


def update_location_data(row_id_, locations_in_profile_, n):
    try:
        with conn().cursor() as cursor:
            update1 = 'UPDATE `doc_id3` SET `locations_in_profile`=%s WHERE `row_id` =%s;'
            cursor.execute(update1, (locations_in_profile_, row_id_))
            update2 = 'UPDATE `doc_id4` SET `updated` =%s WHERE `id` =%s;'
            cursor.execute(update2, (True, row_id_))
            print(f"{n}: corrected location in docid3 at row: {row_id_}, id number in docid4: {id_}")
    except Exception as e:
        print(e)
        # pass


def get_doc_id():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM `doc_id_master` limit 1000000;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


data = get_doc_id()
new_data = []
search_name_set = dict()
duplicate_name = []
n = 0
edu_duplicate_count = 0
delete_id_list = []
one_location_count = 0
for item in data:

    id_ = item['id']
    # row_id = item['row_id']
    done = item['done']
    educations = item['educations']
    locations_in_profile = item['locations']
    search_name = item['search_name']
    try:
        if search_name_set[search_name]:
            duplicate_name.append(search_name)
            existing_locations = json.loads(search_name_set[search_name][0])
            new_locations = json.loads(item['locations'])
            if len(new_locations) == 0:
                continue
            edu = search_name_set[search_name][1]
            if edu is not None and educations is not None:
                if educations == edu:
                    edu_duplicate_count += 1
                    print(f"{edu_duplicate_count}: {search_name}")
                    delete_id_list.append(id_)
            # if existing_locations[0] == new_locations[0]:
                # one_location_count += 1
                # print(f"{one_location_count}: {search_name}")

                # else:
                    # edu_duplicate_count += 1
                    # print(f"{edu_duplicate_count}: {search_name}")
                # if existing_locations[1] == new_locations[1]:
                #     edu = search_name_set[search_name][1]
                #     if edu is not None and educations is not None:
                #         if educations == edu:
                #             edu_duplicate_count += 1
                #             print(f"{edu_duplicate_count}: {search_name}")
                #             delete_id_list.append(id_)
                #     else:
                #         edu_duplicate_count += 1
                #         print(f"{edu_duplicate_count}: {search_name}")
                #         delete_id_list.append(id_)
                    # if existing_locations[2] == new_locations[2]:
                    #     if existing_locations[3] == new_locations[3]:
                    #         print(search_name, new_locations, existing_locations)
    except KeyError:
        search_name_set[search_name] = [locations_in_profile, educations]
    # locations_in_profile = item['locations']
    # locations_in_profile_list = []
    # locations_in_profile_list_ = []

    # try:
    #     locations_in_profile_list = json.loads(locations_in_profile)
    #     if len(locations_in_profile_list) < 4:
    #         locations_ = []
    #         for index in range(4):
    #             try:
    #                 locations_.append(locations_in_profile_list[index])
    #             except IndexError:
    #                 locations_.append("-")
    #         n += 1
    #         print(n, id_, locations_in_profile_list, locations_)
    #         item['locations'] = json.dumps(locations_)
            # update_location_data(id_, locations_in_profile, n)
    # except Exception as e:
    #     pass

print(len(search_name_set.keys()))
# print(search_name_set)
print(len(duplicate_name))
# print(duplicate_name)
print(delete_id_list)


def insert_docid3():
    try:
        with conn().cursor() as cursor:
            for d in data:
                del d['id']
                del d['extracted_location_path_1']
                del d['extracted_location_path_2']
                del d['extracted_location_path_3']
                del d['extracted_location_path_4']

                columns = ', '.join(d.keys())
                values = ', '.join(['%s'] * len(d))
                query = f"INSERT INTO doc_id_master2 ({columns}) VALUES ({values})"
                try:
                    cursor.execute(query, tuple(d.values()))
                except IntegrityError:
                    pass
    except Exception as e:
        print(e)


# insert_docid3()


