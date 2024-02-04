from database2 import *


def get_all_row():
    try:
        with conn().cursor() as cursor:
            select_sql = "select * FROM docinfo_org.doc_id2 where done is TRUE order by id;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


list_of_dicts = get_all_row()


print(len(list_of_dicts))
unique_dicts = []
seen_tuples = set()

for d in list_of_dicts:
    # Convert each dictionary to a tuple and check for duplicates
    # nested_list = (d['search_name'], d['gender'], d['locations_in_profile'], d['educations'], d['certification'], d['licenses'], d['actions'])
    nested_list = (d['search_name'], d['gender'], d['locations_in_profile'], d['educations'])
    # d_tuple = tuple(sorted(d.items()))
    print(d['locations'])
    if nested_list not in seen_tuples:
        unique_dicts.append(d)
        seen_tuples.add(nested_list)

print(len(unique_dicts))


def insert_docid3():
    try:
        with conn().cursor() as cursor:
            for d in unique_dicts:
                try:

                    del d['id']
                    del d['extracted_location_path_1']
                    del d['extracted_location_path_2']
                    del d['extracted_location_path_3']
                    del d['extracted_location_path_4']
                    values_ = tuple(d.values())
                    columns = ', '.join(d.keys())
                    values = ', '.join(['%s'] * len(d))
                    query = f"INSERT INTO doc_id_master ({columns}) VALUES ({values})"
                    cursor.execute(query, values_)
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


insert_docid3()

