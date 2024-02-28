import csv
import json

def load_json(json_file):
    with open(json_file,'r',errors='ignore') as jf:
        data = json.load(jf)
    return data

def load_text(file):
    with open(file, 'r') as f:
        text = f.read()
    return text

def read_csv(filename, with_title=False):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        # Skip the first row
        if not with_title: data = data[1:]
    return data

def write_json(file,data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)
    return

def write_csv(file,data,header:list|None):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        if header: writer.writerow(header)
        writer.writerows(data)
    return