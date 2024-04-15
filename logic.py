import pandas as pd
import json
import gzip

STATE_ABBREVIATIONS = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District Of Columbia': 'DC', 'Puerto Rico': 'PR', 'Armed Forces Africa': 'AE', 'Armed Forces Americas': 'AA',
    'Armed Forces Canada': 'AE', 'Armed Forces Europe': 'AE', 'Armed Forces Middle East': 'AE',
    'Armed Forces Pacific': 'AP', 'Ontario': 'ON', 'Guam': 'GU', 'Armed Forces Afr/Can/Eur/Mid E': 'AE',
    'Virgin Islands': 'VI', 'Northern Mariana Islands': 'CNMI', 'British Columbia': 'BC',
    'Alberta': 'AB', 'Manitoba': 'MB', 'New Brunswick': 'NB', 'Newfoundland and Labrador': 'NL',
    'Nova Scotia': 'NS', 'Prince Edward Island': 'PE', 'Quebec': 'QC', 'Saskatchewan': 'SK',
    'Northwest Territories': 'NT', 'Yukon': 'YT', 'Nunavut': 'NU'
}


def convert_int_comma_separated(list_of_objects):
    try:
        comma_separated = ", ".join(list_of_objects)
    except Exception as e:
        comma_separated = ""
    return comma_separated


def get_current_mobile_number_and_phone_number(list_of_objects):
    mobile_number = {}
    phone_number = {}
    for phone in list_of_objects:
        if phone["phoneType"] == "Wireless":
            mobile_number[phone["phoneOrder"]] = {
                "mobileNumber": phone["phoneNumber"],
                "mobileNumberlastReportedDate": phone["lastReportedDate"]
            }
        elif phone["phoneType"] == "LandLine/Services":
            phone_number[phone["phoneOrder"]] = {
                "phoneNumber": phone["phoneNumber"],
                "phoneNumberlastReportedDate": phone["lastReportedDate"]
            }
    return {
        "mobile_number": mobile_number.get(min(mobile_number.keys(), default=0), {}),
        "phone_number": phone_number.get(min(phone_number.keys(), default=0), {})
    }


def get_current_address(list_of_objects):
    addresses = {}
    for address in list_of_objects:
        addresses[address["addressOrder"]] = {
            "fullAddress": address["fullAddress"],
            "lastReportedDate": address["lastReportedDate"]
        }
    return addresses[min(addresses.keys(), default=0)]


def get_list_of_states(locations):
    states = [st["state"] for st in locations]
    return states


def get_phone_number(mobile_details):
    phone_number = mobile_details.get("phone_number", {})
    return phone_number.get("phoneNumber", "")


def get_mobile_number(mobile_details):
    mobile_number = mobile_details.get("mobile_number", {})
    return mobile_number.get("mobileNumber", "")


def create_empty_person_data(payload):
    return {
        "pFirstName": payload["FirstName"],
        "pLastName": payload["LastName"],
        "pMiddleName": payload["MiddleName"],
        "pCity": payload.get("City", ""),
        "pState": payload.get("State", ""),
        "npi": payload["npi"],
        "pSpecialization": payload.get("specialization", ""),
        "FirstName": "",
        "MiddleName": "",
        "LastName": "",
        "FullName": "",
        "DoB": "",
        "Age": "",
        "City": "",
        "State": "",
        "HasDr": '',
        "EmailAddress": "",
        "PhoneNo": "",
        "FullAddress": "",
        "Cell": "",
    }


def parse_locations(dLocations):
    locations = [
        (loc.split(', ')[0].strip(), STATE_ABBREVIATIONS[loc.split(', ')[1].strip()])
        for loc in dLocations.split('|') if ', ' in loc
    ]
    return locations


def process_response_data(input_file_name):
    with gzip.open(input_file_name.replace(".xlsx", "_raw.json.gz"), 'rt', encoding='utf-8') as file:
        responses = json.load(file)

    input_df = pd.read_excel(input_file_name)

    file1_list = []
    file2_list = []
    not_matched_payload_data = []

    for index, row in input_df.iterrows():
        try:
            payload = {
                "FirstName": row.FirstName,
                "MiddleName": '' if pd.isnull(row.MiddleName) else row.MiddleName,
                "LastName": row.LastName,
                "npi": row.npi,
                "Addresses": [{"State": row.State, "City": '' if pd.isnull(row.City) else row.City}],
                "dLocations": row.dLocations if not pd.isnull(row.dLocations) else '',
                "Age": '' if pd.isnull(row.Age) or row.Age == '' else int(row.Age)
            }

            matching_objects = []  # List to store matching objects
            secondary_matches = []  # List to store objects matching secondary city and state

            for obj in responses[index]["persons"]:
                fn_match = payload["FirstName"].lower() == obj["name"]["firstName"].lower()
                ln_match = payload["LastName"].lower() == obj["name"]["lastName"].lower()
                mn_payload = payload.get("MiddleName", "")
                mn_response = obj["name"].get("middleName", "")
                mn_match = (not mn_payload and not mn_response) or (not mn_payload or not mn_response) or (
                            mn_payload and mn_response and mn_payload[0].lower() == mn_response[0].lower())

                aka_fn_match = aka_ln_match = aka_mn_match = ''

                # Iterate through all AKAs
                for aka in obj.get("akas", []):
                    aka_fn_match = aka_fn_match or (payload["FirstName"].lower() == aka["firstName"].lower())
                    aka_ln_match = aka_ln_match or (payload["LastName"].lower() == aka["lastName"].lower())

                    # Compare the middle name initial for AKAs
                    mn_payload_initial = payload.get("MiddleName", "")
                    mn_aka_initial = aka.get("middleName", "")
                    aka_mn_match = aka_mn_match or (
                                mn_payload_initial and mn_aka_initial and mn_payload_initial[0].lower() ==
                                mn_aka_initial[0].lower())

                locations = parse_locations(payload["dLocations"])
                response_locations_set = {(city.lower(), state.lower()) for city, state in locations}
                state_match = any((city.lower(), state.lower()) in response_locations_set for city, state in locations)

                payload_age = payload["Age"]
                response_age = obj.get("age", None)
                age_match = (not payload_age or not response_age) or (
                            payload_age and response_age and abs(int(payload_age) - int(response_age)) <= 1)

                # Check if all the conditions are met for a match
                if (fn_match or aka_fn_match) and (ln_match or aka_ln_match) and (
                mn_match) and state_match and age_match:
                    matching_objects.append(obj)

            # After all primary matches are gathered
            if len(matching_objects) >= 1:
                for match_obj in matching_objects:
                    for dLocation in parse_locations(payload["dLocations"]):
                        city, state = dLocation
                        state_match = (city.lower(), state.lower()) in response_locations_set

                        if state_match:
                            secondary_matches.append(match_obj)
                            break  # Break out of the loop when a match is found for any dLocation

            # Determine final matches
            if secondary_matches:
                final_matches = secondary_matches
                print(f"2ry Match - {payload['FirstName']},{payload['LastName']}")

            else:
                final_matches = matching_objects
                print(f"1ry Match - {payload['FirstName']},{payload['LastName']}")

            # Extract raw names and flatten the list
            raw_names = obj.get("akas", [])
            flattened_raw_names = [name.lower() for akas in raw_names for name in
                                   akas.get("rawNames", [])]  # Extract the rawNames list
            is_dr = any("dr" in name for name in flattened_raw_names)

            mobile_details = get_current_mobile_number_and_phone_number(obj["phoneNumbers"])
            current_address = get_current_address(obj["addresses"])

            first_file_object = {
                "npi": payload["npi"],
                "pSpecialization": payload.get("specialization", ""),
                "FirstName": obj["name"]["firstName"],
                "MiddleName": obj["name"]["middleName"],
                "LastName": obj["name"]["lastName"],
                "FullName": obj["fullName"],
                "DoB": obj["dob"],
                "Age": obj.get("age", "N/A"),
                "City": obj["locations"][0]["city"],
                "State": obj["locations"][0]["state"],
                "HasDr": 'XXX' if is_dr else '',
                "EmailAddress": convert_int_comma_separated([email["emailAddress"] for email in obj["emailAddresses"]]),
                "PhoneNo": get_phone_number(mobile_details),
                "FullAddress": current_address["fullAddress"] if current_address else "",
                "Cell": get_mobile_number(mobile_details),

            }
            second_file_object = {
                "pFirstName": payload["FirstName"],
                "pLastName": payload["LastName"],
                "pMiddleName": payload["MiddleName"],
                "pCity": payload.get("City", ""),
                "pState": payload.get("State", ""),
                "npi": payload["npi"],
                "pSpecialization": payload.get("specialization", ""),
                "FirstName": obj["name"]["firstName"],
                "MiddleName": obj["name"]["middleName"],
                "LastName": obj["name"]["lastName"],
                "FullName": obj["fullName"],
                "DoB": obj["dob"],
                "Age": obj.get("age", "N/A"),
                "City": obj["locations"][0]["city"],
                "State": obj["locations"][0]["state"],
                "HasDr": 'XXX' if is_dr else '',
                "EmailAddress": ' | '.join([email["emailAddress"] for email in obj["emailAddresses"]]),
                "PhoneNo": ' | '.join([mobile["phoneNumber"] for mobile in obj["phoneNumbers"] if
                                       mobile["phoneType"] == "LandLine/Services"]),
                "FullAddress": ' | '.join([address["fullAddress"] for address in obj["addresses"]])
            }

            for i, mobile_number in enumerate(
                    [mobile["phoneNumber"] for mobile in obj["phoneNumbers"] if mobile["phoneType"] == "Wireless"]):
                second_file_object[f"Cell{i + 1}"] = mobile_number

            file1_list.append(first_file_object)
            file2_list.append(second_file_object)

            if not match_found:
                not_matched_payload_data.append(create_empty_person_data(payload))

        except Exception as e:
            print(f"Exception for {payload['FirstName']},{payload['LastName']}: {e}")
            file1_list.append(create_empty_person_data(payload))
            file2_list.append(create_empty_person_data(payload))

    df1 = pd.DataFrame(file1_list)
    df2 = pd.DataFrame(file2_list)
    df_not_matched = pd.DataFrame(not_matched_payload_data)

    # Save the DataFrames to Excel files
    df1.to_excel(input_file_name.replace(".xlsx", "_output1.xlsx"), index=False)
    df2.to_excel(input_file_name.replace(".xlsx", "_output2.xlsx"), index=False)
    if not_matched_payload_data:
        df_not_matched.to_excel(input_file_name.replace(".xlsx", "_not_matched.xlsx"), index=False)
        print(
            f"Output files created: {input_file_name.replace('.xlsx', '_output1.xlsx')}, {input_file_name.replace('.xlsx', '_output2.xlsx')}, and {input_file_name.replace('.xlsx', '_not_matched.xlsx')}")
    else:
        print(
            f"Output files created: {input_file_name.replace('.xlsx', '_output1.xlsx')} and {input_file_name.replace('.xlsx', '_output2.xlsx')}")


if __name__ == "__main__":
    input_file_name = input("Enter the input file name: ")
    if not input_file_name.endswith(".xlsx"):
        input_file_name += ".xlsx"

    process_response_data(input_file_name)
