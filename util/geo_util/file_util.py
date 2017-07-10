import json
import csv


def open_json(file_path):
    with open(file_path) as data_file:
        return json.load(data_file)


def write_dict_as_json(file_path, output):
    with open(file_path, 'w') as file:
        json.dump(output, file)


def open_csv(file_path):
    with open(file_path, 'r', encoding="utf-8") as opt_file:
        reader = csv.reader(opt_file, delimiter=",")
        return list(reader)
