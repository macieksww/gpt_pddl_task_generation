import re
import json
import os
from exceptions import AttributeErrorException, WrongPathException

def save_to_file(text, filepath):
    try:
        if os.path.isfile(filepath):
            with open(filepath, 'w+') as file:
                file.write(text)
        else:
            raise WrongPathException()
    except WrongPathException as e:
        for i in range(10):
            print("WRONG PATHEXC")
            print(e)

def save_lines_to_file(lines, filepath):
    with open(filepath, 'w+') as file:
        file.writelines(lines)

def str_to_json(text):
    pattern = r'{(\n.*)*}'
    plan_lines = []
    matches = re.search(pattern, text)
    if matches:
        try:
            json_like_str = text[matches.span()[0]:matches.span()[1]]
            return json.loads(json_like_str)
        except AttributeErrorException() as e:
            print(e)
            return
    else:
        return
        
def write_file(filepath, text, mode='wl'):
    try:
        match mode:
            # write
            case 'w':
                with open(filepath, 'w+') as file:
                    file.write(text)
            # writelines
            case 'wl':
                with open(filepath, 'w+') as file:
                    file.writelines(text)
    except FileNotFoundError as e:
        print('File doesnt exist')
          
def read_file(filepath, mode='rl'):
    try:
        match mode:
            # read
            case 'r':
                with open(filepath, 'r') as file:
                    file = file.read()
            # readlines
            case 'rl':
                with open(filepath, 'r') as file:
                    file = file.readlines()
    except FileNotFoundError as e:
        print('File doesnt exist')
    else:  
        return file