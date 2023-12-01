import pandas as pd

from database2 import conn

import json


def get_doc_id():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM `doc_id2` where done is TRUE;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


data = get_doc_id()
new_data = []
n = 0
for data_dict in data:
    n += 1
    print(n)
    new_data_dict = {}
    for key, value in data_dict.items():
        # print(f"{key} = {key}")
        if key == 'specialty':
            key = 'specialization'
            new_data_dict[key] = value
        elif key == 'actions' or key == 'done' or key == 'id' or key == 'row_id':
            continue
        elif key == 'full_name':
            key = 'csv_full_name'
            new_data_dict[key] = value
        elif key == 'href':
            key = 'doc_id'
            new_data_dict[key] = value
        elif key == 'locations':
            value = json.loads(value)
            location = " | ".join(item for item in value)
            new_data_dict[key] = location
        elif key == 'search_name':
            key = 'dFull_Name'
            new_data_dict[key] = value
            if ',' in value:
                name_splited = value.split(',')
                dCreds = name_splited[1]
                new_data_dict['dCreds'] = dCreds
                first_middle_last = name_splited[0].split(' ')
                if len(first_middle_last) == 3:
                    dFirst_name = first_middle_last[0]
                    dMiddle_name = first_middle_last[1]
                    dLast_name = first_middle_last[2]
                    new_data_dict['dFirst_name'] = dFirst_name
                    new_data_dict['dMiddle_name'] = dMiddle_name
                    new_data_dict['dLast_name'] = dLast_name
                elif len(first_middle_last) == 2:
                    dFirst_name = first_middle_last[0]
                    dMiddle_name = ''
                    dLast_name = first_middle_last[1]
                    new_data_dict['dFirst_name'] = dFirst_name
                    new_data_dict['dMiddle_name'] = dMiddle_name
                    new_data_dict['dLast_name'] = dLast_name
        elif key == 'gender':
            key = 'dGender'
            new_data_dict[key] = value
        elif key == 'locations_in_profile':
            value = json.loads(value)
            location = " | ".join(item for item in value)
            key = 'dReported_Locations'
            new_data_dict[key] = location
        elif key == 'educations':
            if value:
                value = json.loads(value)
                educations_json = value[0].split("\n")
                educations_institute = educations_json[0]
                educations_year = educations_json[1].replace('Year of Graduation:', '').strip()
                key = 'dEducations'
                new_data_dict[key] = educations_institute
                key = 'Year of Graduation'
                new_data_dict[key] = educations_year
        elif key == 'certification':
            if value:
                value = json.loads(value)
                certification = " | ".join(item.strip(' *') for item in value)
                new_data_dict[key] = certification
        elif key == 'licenses':
            value = json.loads(value)
            licenses = " | ".join(item for item in value)
            new_data_dict[key] = licenses
        else:
            new_data_dict[key] = value
    new_data.append(new_data_dict)
    # locations = item['locations_in_profile']
    # educations = item['educations']
    # year_of_graduation = item['certification']
    # certifications = item['locations_in_profile']
    # licenses = item['licenses']
    # print(locations)
    # print(educations)
    # print(year_of_graduation)
    # print(certifications)
    # print(licenses)


df = pd.DataFrame(new_data)
excel_file_path = '500k_profiles.xlsx'
df.to_excel(excel_file_path, index=False)


