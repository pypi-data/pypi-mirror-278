#%%
import yaml
import os
import zipfile
import googlemaps

def read_config(input_path = 'config/config.yaml'):
    '''
    Reads a yaml file and converts it to a dict.

    Parameters:
        - input_path: Path to the input yaml file

    Returns:
        - yaml_data: A dictionary of the yaml contents
    '''
    read = open(input_path, 'r')
    data = read.read()
    yaml_data = yaml.safe_load(data)
    return yaml_data


def extract_zip(zip_path):
    '''
    Extracts zipped folder contents to regular folder, deletes zipped folder after.

    Parameters:
        - zip_path: Path to the zipped folder

    Returns:
        - Extracted contents in regular folder
    '''
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        folder_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_dir = os.path.join(os.path.dirname(zip_path), folder_name)
        zip_ref.extractall(extract_dir)

    # Remove the zip file after extraction
    os.remove(zip_path)


def geocode_address(api_key, address):
    '''
    Returns latitude and longitude coordinates using the Google Maps API based on a provided address.

    Parameters:
        - api_key: Google Maps API Key
        - address: Address to obtain lat/long coordinates for.

    Returns:
        - latitude and longitude coordinates
    '''
    gmaps = googlemaps.Client(key=api_key)

    try:
        geocode_result = gmaps.geocode(address)

        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            lat, long = location['lat'], location['lng']
            return lat, long
        else:
            print('Unable to get lat/long from address')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None
    

def add_ordinal_suffix(number):
    '''
    Takes an interger and returns it as a string with proper ordinal suffix.
    For instance, 27 becomes 27th, 3 becomes 3rd, etc.

    Parameters:
        - number: Number to get suffix for

    Returns:
        - string as number + suffix
    '''
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

    return f'{number}{suffix}'