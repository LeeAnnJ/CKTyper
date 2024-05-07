import csv
import json
import pickle
import xml.etree.ElementTree as ET

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
        if with_title: data = list(reader)
        else: data = list(reader)[1:] # Skip the first row
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

def read_XML(file):
    with open(file,'r',encoding='utf-8') as f:
        tree = ET.parse(f)
    return tree

def read_pickle(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    return data

def write_pickle(file,data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)
    return