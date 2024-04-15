import pymysql


def conn():
    return pymysql.connect(host='localhost',
                           user='mdbaki',
                           password='TalhaZubayer789*',
                           database='search_people_free',
                           charset='utf8mb4',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


def get_all_row():
    try:
        with conn().cursor() as cursor:
            select_sql = "select * FROM search_people_free.search_people_free_db order by id;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


list_of_dicts = get_all_row()

# insert_query = """
#     INSERT INTO search_pf_details_sample2
#     (`npi`, `full_name`, `first_name`, `middle_name`, `last_name`, `age`, `state`, `specialty`, `search_name`, `gender`, `href`, `locations`, `row_id`, `locations_in_profile`, `educations`, `certification`, `licenses`, `actions`, `done`, `extracted_location_path_1`, `extracted_location_path_2`, `extracted_location_path_4`, `extracted_location_path_5`)
#     VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s)
# """


# print(len(list_of_dicts))
# unique_dicts = []
# seen_tuples = set()

# for d in list_of_dicts:
#     nested_list = (d['search_name'], d['gender'], d['locations_in_profile'], d['educations'], d['certification'], d['licenses'], d['actions'])
#     d_tuple = tuple(sorted(d.items()))
#     if d_tuple not in seen_tuples:
#         unique_dicts.append(d)
#         seen_tuples.add(d_tuple)


def insert_docid3():
    try:
        with conn().cursor() as cursor:
            for d in list_of_dicts:
                try:
                    rowid = d['id']
                    # del d['id']
                    # del d['extracted_location_path_1']
                    # del d['extracted_location_path_2']
                    # del d['extracted_location_path_3']
                    # del d['extracted_location_path_4']
                    columns = ', '.join(d.keys())
                    values = ', '.join(['%s'] * len(d))
                    query = f"INSERT INTO search_people_free_db_unique ({columns}) VALUES ({values})"
                    cursor.execute(query, tuple(d.values()))
                    # print(f"Inserted {d['search_name']} into doc_id_master.")
                except pymysql.IntegrityError:
                    print(f"duplicate: {rowid}")
                except Exception as e:
                    print(f"error for: {rowid} error message: {e}")
    except Exception as e:
        print(e)


insert_docid3()

