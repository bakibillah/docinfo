import json

from database2 import *


def get_all_row():
    try:
        with conn().cursor() as cursor:
            select_sql = "select * FROM docinfo_org.doc_id3 order by id limit 249342;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


def get_all_row3():
    try:
        with conn().cursor() as cursor:
            select_sql = "select * FROM docinfo_org.doc_id2 order by id limit 260000;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


list_of_dicts = get_all_row()
# list_of_dicts3 = get_all_row3()
update_query = "UPDATE `docinfo_org`.`doc_id` SET `locations`=%s, `locations_in_profile` =%s WHERE `id` =%s;"


def insert_docid3():
    try:
        with conn().cursor() as cursor:
            count = 0
            for d in list_of_dicts:
                try:
                    count += 1
                    first = json.loads(d['locations_in_profile'])
                    locations_ = [item for item in first if item != '-']
                    if len(locations_) < 5:
                        print('stop')
                        continue

                    # print(f"{count}-{list_of_dicts[count]['id']}-{list_of_dicts[count]['locations_in_profile']} --{list_of_dicts3[count]['id']}- {list_of_dicts[count]['locations_in_profile']}")

                    update_query = "UPDATE `docinfo_org`.`doc_id2` SET `locations`=%s, `locations_in_profile` =%s WHERE `id` =%s;"
                    # select_query = "SELECT `locations_in_profile` FROM `docinfo_org`.`doc_id2` WHERE `id` =%s;"
                    update = cursor.execute(update_query, (d['locations'], d['locations_in_profile'], d['id']))
                    print(f"{update} row id : {d['id']}")
                    # cursor.execute(select_query, (d['id']))
                    # data_ = cursor.fetchone()
                    # print(f"{count}: {d['id']} - {d['locations_in_profile']}- {data_['locations_in_profile']}")
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


insert_docid3()

