"""
Here i am removing row from search_people_free.search_people_free_db_one_result
to remove i first get the row id that is not present in search_people_free_db_unique
then delete the corresponding row from search_people_free_db_unique
"""

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
            select_sql = "select id FROM search_people_free.search_people_free_db_unique order by id limit 1000000;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


list_of_dicts = get_all_row()
id_list = [item["id"] for item in list_of_dicts]
_993434_list = [i for i in range(1, 993434)]
unique_id_2delete = list(set(_993434_list) - set(id_list))




def insert_docid3():
    try:
        with conn().cursor() as cursor:
            for rowid in unique_id_2delete:
                try:
                    query = f"DELETE FROM search_people_free_db_one_result where id =%s"
                    cursor.execute(query, rowid)
                except Exception as e:
                    print(f"error for: {rowid} error message: {e}")
    except Exception as e:
        print(e)


insert_docid3()

