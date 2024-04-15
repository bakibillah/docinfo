from openpyxl import Workbook
from database2 import conn
import json
import pandas as pd
import os

data = []
chunk_size = 250000


def get_doc_id():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM `doc_id3` where `done` is TRUE;"
            cursor.execute(select_sql)
            _data_ = cursor.fetchall()
            return _data_
    except Exception as e:
        print(e)


data_ = get_doc_id()
new_data = []
n = 0
for data_dict in data_:
    n += 1

    id_ = data_dict['id']

    # if 800000 < n:
    #     continue
    # print(n)

    new_data_dict = {}
    for key, value in data_dict.items():
        # print(f"{key} = {key}")
        if key == 'specialty':
            key = 'specialization'
            new_data_dict[key] = value
        elif key in ['done', 'id', 'row_id', 'extracted_location_path_1', 'extracted_location_path_2', 'extracted_location_path_4', 'extracted_location_path_5']:
            continue
        elif key == 'full_name':
            key = 'csv_full_name'
            new_data_dict[key] = value
        elif key == 'href':
            key = 'doc_id'
            new_data_dict[key] = value
        elif key == 'locations':
            value = json.loads(value)
            location = " | ".join(item for item in value if item != '-')
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
                elif len(first_middle_last) == 4:
                    dFirst_name = first_middle_last[0]
                    dMiddle_name = first_middle_last[1] + ' ' + first_middle_last[2]
                    dLast_name = first_middle_last[3]
                    new_data_dict['dFirst_name'] = dFirst_name
                    new_data_dict['dMiddle_name'] = dMiddle_name
                    new_data_dict['dLast_name'] = dLast_name
                elif len(first_middle_last) == 5:
                    dFirst_name = first_middle_last[0]
                    dMiddle_name = first_middle_last[1] + ' ' + first_middle_last[2] + ' ' + first_middle_last[3]
                    dLast_name = first_middle_last[4]
                    new_data_dict['dFirst_name'] = dFirst_name
                    new_data_dict['dMiddle_name'] = dMiddle_name
                    new_data_dict['dLast_name'] = dLast_name
                else:
                    dFirst_name = first_middle_last[0]
                    dLast_name = first_middle_last[len(first_middle_last) -1]
                    dMiddle_name = first_middle_last[1:-1]
                    result_string = ' '.join(dMiddle_name)
                    new_data_dict['dFirst_name'] = dFirst_name
                    new_data_dict['dMiddle_name'] = result_string
                    new_data_dict['dLast_name'] = dLast_name
                    # print(new_data_dict['dFirst_name'], new_data_dict['dMiddle_name'], new_data_dict['dLast_name'])

        elif key == 'gender':
            key = 'dGender'
            new_data_dict[key] = value
        elif key == 'locations_in_profile':
            value = json.loads(value)
            # print(f"{n}: {len(value)}")
            location = " | ".join(item for item in value if item != '-')
            print(n, location)
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
            else:
                key = 'dEducations'
                new_data_dict[key] = None
                key = 'Year of Graduation'
                new_data_dict[key] = None
        elif key == 'certification':
            if value:
                value = json.loads(value)
                certification = " | ".join(item.strip(' *') for item in value)
                new_data_dict[key] = certification
            else:
                new_data_dict[key] = None
        elif key == 'licenses':
            value = json.loads(value)
            licenses = " | ".join(item for item in value)
            new_data_dict[key] = licenses
        else:
            new_data_dict[key] = value
    data.append(new_data_dict)


df = pd.DataFrame(data)

# Specify the Excel file path
excel_file_path = '000-250k.xlsx'


if os.path.isfile(excel_file_path):
    with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a') as writer:
        for i in range(0, len(df), chunk_size):
            chunk_df = df.iloc[i:i + chunk_size]
            sheet_name = f'Sheet_{i // chunk_size + 1}'
            chunk_df.to_excel(writer, sheet_name=sheet_name, index=False, header=(i == 0))
# else:
#     df.iloc[:chunk_size].to_excel(excel_file_path, index=False, header=True)


print(f'Data written to {excel_file_path}')
