import os
import datetime
import json

files = os.listdir()

file_list = []
date_time_format = '%Y-%m-%d %H:%M:%S'
for file in files:
    path = os.path.abspath(file)
    size = os.path.getsize(file)
    created_at = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime(date_time_format)
    modified_at = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime(date_time_format)
    is_dir = os.path.isdir(file)

    file_dict = {
        'FileName': file,
        'Path': path,
        'Type': 'Dir' if is_dir else 'File',
        'Size in bytes': size,
        'Created at': created_at,
        'Modified at': modified_at
    }

    file_list.append(file_dict)

print(json.dumps(file_list, indent = 2))