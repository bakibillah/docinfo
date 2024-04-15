"""
here i am counting the match from the multiple results

"""
import json
import pymysql
from database2 import state_map_2


# from database2 import conn


def conn():
    return pymysql.connect(host='localhost',
                           user='mdbaki',
                           password='TalhaZubayer789*',
                           database='search_people_free',
                           charset='utf8mb4',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


def update_searchpeoplefree_(match_count, matched_city, rowid):
    try:
        with conn().cursor() as cursor:
            update = f'UPDATE `search_people_free`.`search_people_free_db_one_result` SET `match1` =%s, `match1_list`=%s WHERE `id` =%s;'
            result = cursor.execute(update, (match_count, json.dumps(matched_city), rowid))
            print(f"updated one row: {result}")
    except Exception as e:
        print(e)


def select_all():
    try:
        with conn().cursor() as cursor:
            select_sql = '''
                            SELECT `search_people_free_db_one_result`.`id` ,`search_people_free_db_one_result`.`listofaddress1`, `search_people_free_db`.`search_name`, `search_people_free_db`.`locations_in_profile`, `search_people_free_db`.`row_id`, `search_people_free_db`.`id`
                            FROM `search_people_free_db_one_result`
                            JOIN `search_people_free_db` ON `search_people_free_db_one_result`.`row_id` = `search_people_free_db`.`id`
                            limit 10000;
            '''
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


# multiple_match = select_all()
# print(multiple_match)
# n = 0
# for each in multiple_match:
#     row_id = each['id']
#     del each['id']
#     matches_values = list(each.values())
#     matches_values = [item for item in matches_values if item is not None]
#     # print(matches_values)
#     highest_value = max(matches_values, default=None)
#
#     # print("The highest value is:", highest_value)
#
#     count_of_element = matches_values.count(highest_value)
#     if count_of_element > 1:
#         print(f"The multiple highest value is:, {highest_value} in {matches_values}")
#         update_searchpeoplefree_(single_match='no', rowid=row_id)
#     else:
#         print(f"The single highest value is:, {highest_value} in {matches_values}")
#         update_searchpeoplefree_(single_match='yes', rowid=row_id)


# def select_all():
#     try:
#         with conn().cursor() as cursor:
#             select_sql = "SELECT * FROM `docinfo_org`.`search_people2` where listofaddress2 is not null;"
#             cursor.execute(select_sql)
#             data_ = cursor.fetchall()
#             return data_
#     except Exception as e:
#         print(e)
#
#
# def update_searchpeoplefree(match, match_list, num, row_id):
#     try:
#         with conn().cursor() as cursor:
#             update = f'UPDATE `search_people2` SET `match{num}` =%s, `match{num}_list` =%s WHERE `id` =%s;'
#             result = cursor.execute(update, (match, match_list, row_id))
#             print(f"updated one row: {result}")
#     except Exception as e:
#         print(e)


n = 0
for item in select_all():
    canada = False
    n += 1
    row_id = item['id']
    d_location = item['locations_in_profile']
    if d_location is None:
        continue

    locations = json.loads(d_location)
    locations = [item.strip() for item in locations if item != '-']
    dlocations_list = []
    state_code = None
    for item_ in locations:
        state = item_.split(',')[1].strip()
        city = item_.split(',')[0].strip()
        try:
            state_code = state_map_2[state]
        except KeyError:
            print(f"keywrror for: {state_code}")
            canada = True
            break
        dlocations_list.append(f'{city}, {state_code}')
    # print(f"dlocations: {dlocations_list}")
    if canada:
        continue
    #
    listofaddress1 = item['listofaddress1']
    listofaddress1_header = item['header_address']

    listofaddress2 = item['listofaddress2']
    listofaddress3 = item['listofaddress3']
    listofaddress4 = item['listofaddress4']
    listofaddress5 = item['listofaddress5']
    listofaddress6 = item['listofaddress6']
    listofaddress7 = item['listofaddress7']
    listofaddress8 = item['listofaddress8']

    if listofaddress1 != None:
        listofaddress1_list = json.loads(listofaddress1)
        address_list = [item_[0].split(',') for item_ in listofaddress1_list]
        processed_addresses = []

        for address in address_list:
            city = address[len(address) - 2].strip()
            zip_code = address[len(address) - 1].strip()
            state = zip_code[:2]
            processed_addresses.append(f'{city}, {state}')
        # print("Processed addresses:", processed_addresses)
        common_elements = set(processed_addresses).intersection(dlocations_list)
        if len(common_elements) == 0:
            print('match1: 0')
            update_searchpeoplefree_(match_count=0, matched_city=None, rowid=row_id)
        else:
            print('match1: ', len(common_elements), list(common_elements))
            match_count = len(common_elements)
            matched_city = list(common_elements)
            update_searchpeoplefree_(match_count, matched_city, row_id)

    # if listofaddress2 is not None:
#         listofaddress2_list = json.loads(listofaddress2)
#         address_list = [item_.split(',') for item_ in listofaddress2_list]
#         processed_addresses = []
#
#         for address in address_list:
#             city = address[len(address)-2].strip()
#             zip_code = address[len(address)-1].strip()
#             state = zip_code[:2]
#             processed_addresses.append(f'{city}, {state}')
#         common_elements = set(processed_addresses).intersection(dlocations_list)
#         if len(common_elements) == 0:
#             print('match2: 0')
#             update_searchpeoplefree(match=0, match_list=None, num=2, row_id=row_id)
#         else:
#             print('match2: ', len(common_elements), list(common_elements))
#             update_searchpeoplefree(match=len(common_elements), match_list=json.dumps(list(common_elements)), num=2,
#                                     row_id=row_id)
#
#     if listofaddress3 is not None:
#         listofaddress3_list = json.loads(listofaddress3)
#         address_list = [item_.split(',') for item_ in listofaddress3_list]
#         processed_addresses = []
#
#         for address in address_list:
#             city = address[len(address)-2].strip()
#             zip_code = address[len(address)-1].strip()
#             state = zip_code[:2]
#             processed_addresses.append(f'{city}, {state}')
#         common_elements = set(processed_addresses).intersection(dlocations_list)
#         if len(common_elements) == 0:
#             print('match3: 0')
#             update_searchpeoplefree(match=0, match_list=None, num=3, row_id=row_id)
#         else:
#             print('match3: ', len(common_elements), list(common_elements))
#             update_searchpeoplefree(match=len(common_elements), match_list=json.dumps(list(common_elements)), num=3,
#                                     row_id=row_id)
#
#     if listofaddress4 is not None:
#         listofaddress4_list = json.loads(listofaddress4)
#         address_list = [item_.split(',') for item_ in listofaddress4_list]
#         processed_addresses = []
#
#         for address in address_list:
#             city = address[len(address)-2].strip()
#             zip_code = address[len(address)-1].strip()
#             state = zip_code[:2]
#             processed_addresses.append(f'{city}, {state}')
#         common_elements = set(processed_addresses).intersection(dlocations_list)
#         if len(common_elements) == 0:
#             print('match4: 0')
#             update_searchpeoplefree(match=0, match_list=None, num=4, row_id=row_id)
#         else:
#             print('match4: ', len(common_elements), list(common_elements))
#             update_searchpeoplefree(match=len(common_elements), match_list=json.dumps(list(common_elements)), num=4,
#                                     row_id=row_id)
#
#     if listofaddress5 is not None:
#         listofaddress5_list = json.loads(listofaddress5)
#         address_list = [item_.split(',') for item_ in listofaddress5_list]
#         processed_addresses = []
#
#         for address in address_list:
#             city = address[len(address)-2].strip()
#             zip_code = address[len(address)-1].strip()
#             state = zip_code[:2]
#             processed_addresses.append(f'{city}, {state}')
#         common_elements = set(processed_addresses).intersection(dlocations_list)
#         if len(common_elements) == 0:
#             print('match5: 0')
#             update_searchpeoplefree(match=0, match_list=None, num=5, row_id=row_id)
#         else:
#             print('match5: ', len(common_elements), list(common_elements))
#             update_searchpeoplefree(match=len(common_elements), match_list=json.dumps(list(common_elements)), num=5,
#                                     row_id=row_id)
#
#     if listofaddress6 is not None:
#         listofaddress6_list = json.loads(listofaddress6)
#         address_list = [item_.split(',') for item_ in listofaddress6_list]
#         processed_addresses = []
#
#         for address in address_list:
#             city = address[len(address)-2].strip()
#             zip_code = address[len(address)-1].strip()
#             state = zip_code[:2]
#             processed_addresses.append(f'{city}, {state}')
#
#         common_elements = set(processed_addresses).intersection(dlocations_list)
#         if len(common_elements) == 0:
#             print('match6: 0')
#             update_searchpeoplefree(match=0, match_list=None, num=6, row_id=row_id)
#         else:
#             print('match6: ', len(common_elements), list(common_elements))
#             update_searchpeoplefree(match=len(common_elements), match_list=json.dumps(list(common_elements)), num=6,
#                                     row_id=row_id)
#
#     if listofaddress7 is not None:
#         listofaddress7_list = json.loads(listofaddress7)
#         address_list = [item_.split(',') for item_ in listofaddress7_list]
#         processed_addresses = []
#
#         for address in address_list:
#             city = address[len(address)-2].strip()
#             zip_code = address[len(address)-1].strip()
#             state = zip_code[:2]
#             processed_addresses.append(f'{city}, {state}')
#         # print("Processed addresses:", processed_addresses)
#         common_elements = set(processed_addresses).intersection(dlocations_list)
#         if len(common_elements) == 0:
#             print('match7: 0')
#             update_searchpeoplefree(match=0, match_list=None, num=7, row_id=row_id)
#         else:
#             print('match7: ', len(common_elements), list(common_elements))
#             update_searchpeoplefree(match=len(common_elements), match_list=json.dumps(list(common_elements)), num=7,
#                                     row_id=row_id)
#
#     if listofaddress8 is not None:
#         listofaddress8_list = json.loads(listofaddress8)
#         address_list = [item_.split(',') for item_ in listofaddress8_list]
#         processed_addresses = []
#
#         for address in address_list:
#             city = address[len(address)-2].strip()
#             zip_code = address[len(address)-1].strip()
#             state = zip_code[:2]
#             processed_addresses.append(f'{city}, {state}')
#
#         common_elements = set(processed_addresses).intersection(dlocations_list)
#         if len(common_elements) == 0:
#             print('match8: 0')
#             update_searchpeoplefree(match=0, match_list=None, num=8, row_id=row_id)
#         else:
#             print('match8: ', len(common_elements), list(common_elements))
#             update_searchpeoplefree(match=len(common_elements), match_list=json.dumps(list(common_elements)), num=8,
#                                     row_id=row_id)
