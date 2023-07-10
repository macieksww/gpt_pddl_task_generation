import re
import json
def save_to_file(text, filepath):
    with open(filepath, 'w+') as file:
        file.write(text)

def save_lines_to_file(lines, filepath):
    with open(filepath, 'w+') as file:
        file.writelines(lines)

def str_to_json(text):
    pattern = r'{(\n.*)*}'
    plan_lines = []
    matches = re.search(pattern, text)
    json_like_str = text[matches.span()[0]:matches.span()[1]]
    return json.loads(json_like_str)
