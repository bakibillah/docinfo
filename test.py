import json

# Open the JSON file
with open('Us.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)

# Now, 'data' contains the contents of the JSON file as a dictionary
print(data)
