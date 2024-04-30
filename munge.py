import csv
def identify_unneccessary_fields(data_set,list_of_unwanted_fields):
    for record in data_set.copy(): #iterate through shallow copy so changes can be made to the size of the actual object without raising an error
        for field,value in record.items():
            if field in list_of_unwanted_fields:
                record[field] = "---"
            '''
            if field == "the_geom":
                record[field] = "---"
            elif field == "City":
                record[field] = "---"
            elif field == "Suite":
                record[field] = "---"
            elif "Location" in field:
                record[field] = "---"
            '''    
    return data_set
def remove_unneccessary_fields(data_set):
    for record in data_set:
        for field,value in (record.copy()).items():
            if value == "---": #now remove all uneccessary fields
                del record[field]
    return data_set
def remove_commas(data_set,field):
    for record in data_set:
        record[field] = value
        if "," in value:
            record[field] = value.replace(",","")

def to_camelCase(string):
    if isinstance(string,str):
        return str.title(string)
def clean_up(all_data):
    for record in all_data:
        for field,value in (record.copy()).items():
            record[field] = to_camelCase(value)
    return all_data
def perform_munging_unique_to_dataset(all_data):
    ''' 
    'Cleans' the values in the 'BusinessType' fields
    '''
    for record in all_data:
        for field,value in (record.copy()).items():
            if field == "BusinessType":
                #criteria
                if value.startswith("880"):
                    record[field] = "Bed & Breakfast 1 to 5 rooms"
                elif value.startswith("4704"):
                    record[field] = "Traveler Accomodation"
                else:
                    record[field] = value[7:]#slice-out the # prefix                
    return(all_data)

def unique_values(data_set,field,separator=","):
    '''
    Takes two parameters: a dataset and a field within which the search will take place.
    Identifies and prints all UNIQUE values in that field
    '''
    unique_values = []
    for record in data_set:
        for key,value in record.items():
            if key == field:
                if value not in unique_values:
                    unique_values += [value]
    return unique_values

with open("data/hotelsMotels.csv","r") as file:
    all_data = list(csv.DictReader(file))
    all_data = clean_up(remove_unneccessary_fields(identify_unneccessary_fields(all_data,["the_geom","City","Suite","Location"])))
    #now perform some munging that is unique to the content of the dataset
    cleaned_data = perform_munging_unique_to_dataset(all_data) 

with open("data/hotelsMotels_clean.csv", "w") as output:
    headers = "" #first line
    for (index,key) in enumerate(list(all_data[1].keys())):
        if index == len(list(all_data[1].keys()))-1:
            headers += (str(key)+"\n")
        else:
            headers += (str(key)+",")
    output.write(headers)
    line = ""
    for row in all_data:##fix
        #create a list of all data for each field (of each row) that will dynamically change for each row
        data = list(row.values())
        for (index,value) in enumerate(data):
            if index == len(list(row.values()))-1:
                if value == '': #if there are any fields with an empty String for a value, set that value to "---" so empty values can be parsed correctly when writing to the CSV file
                    line += "---" + "\n"
                else:   
                    line += value + "\n"
            else:
                if value == '':
                    line += "---" + ","
                else:
                    line += value + ","
        output.write(line)
        line = ""