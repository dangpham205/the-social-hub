from datetime import datetime
import re, os
from pathlib import Path
def sqlachemy_obj_to_dict(obj):
    dictret = dict(obj.__dict__)
    dictret.pop('_sa_instance_state', None)
    dictret.pop('created_at', None)
    dictret.pop('updated_at', None)
    dictret.pop('deleted_at', None)
    return dictret

def clean_str_to_import(data):
    if type(data) is not str:
        data = str(data)
    data = data.strip()
    data = data.replace('\n', '. ')
    data = data.replace('"', "'")
    return data

def get_current_time_as_int() -> int:
    now = datetime.now()
    current_time = now.timestamp()
    return int(current_time)

def convert_datetime_to_timestamp(y, m, d, h=0, i=0 ,s=0) -> int:
    now = datetime(y, m, d, h, i , s)
    current_time = now.timestamp()
    return int(current_time)

def check_is_roman(subject):
    pattern = "M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"
    if subject:
        if re.fullmatch(pattern, subject):
            return True
        return False

def number_to_roman(number):
    list_map = {
        'XL': 40,
        'X': 10,
        'IX': 9,
        'V': 5,
        'IV': 4,
        'I': 1,
    }
    number = int(number)
    return_value = ''
    while number > 0:
        for roman, num_int in list_map.items():
            if number >= num_int:
                number = number - num_int
                return_value = return_value + roman
                break
    return return_value

def open_file_as_root_path(file_path):
    # root_path = os.path.dirname(__file__)
    path_root = Path(__file__).parents[2]
    abs_file_path = os.path.join(path_root, file_path)
    return open(abs_file_path, 'rb')

def write_to_json(file_path, content):
    path_root = Path(__file__).parents[2]
    abs_file_path = os.path.join(path_root, file_path)
    f = open(abs_file_path + '/output.json', "w")
    f.write(content)
    print(abs_file_path)