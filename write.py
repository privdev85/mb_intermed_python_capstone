"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import transform_to_str, datetime_to_str



def transform_result_for_csv_writing(results):
    fieldkeys = ["time", "distance", "velocity", "_designation", "name", "diameter", "hazardous"]
    outlist = list()
    for approach in list(results):
        unpacked_dict = unpack_approach(approach)
        outlist.append([transform_to_str(unpacked_dict[fkey]) for fkey in fieldkeys])

    return outlist

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )

    outlist = transform_result_for_csv_writing(results)

    with open(filename, 'w') as f:
        write = csv.writer(f)
        write.writerow(fieldnames)
        write.writerows(outlist)

    return

def unpack_approach(approach):
    return {**approach.__dict__, **approach.__dict__['neo'].__dict__}

def get_dict_for_json_mapping():
    return {"datetime_utc":'time',
         "distance_au":'distance',
         "velocity_km_s":'velocity',
         "designation":'designation',
         "name":"name",
         "diameter_km":"diameter",
         "potentially_hazardous":"hazardous"
         }

def approach_vars():
    return ['datetime_utc','distance_au','velocity_km_s']



def transform_approaches_to_list_of_dicts(approaches,keymap_dict,approach_vars):
    resultlist=list()
    for approach in approaches:
        unpacked_approach = unpack_approach(approach)
        approachdict = {"neo":{}}
        for key,lookup_val in keymap_dict.items():
            if key in ['datetime_utc']:
                value = datetime_to_str(unpacked_approach[lookup_val])
            elif key in ['designation','name']:
                value = transform_to_str(unpacked_approach[lookup_val])
            elif key in ['distance_au','velocity_km_s','diameter_km']:
                value = float(unpacked_approach[lookup_val])
            elif key in ['potentially_hazardous']:
                value = bool(unpacked_approach[lookup_val])
            else:
                raise RuntimeError('unexpected_key')
            if key in approach_vars:
                approachdict[key]=value
            else:
                approachdict['neo'][key]=value
        resultlist.append(approachdict)
    return resultlist


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    resultlist = transform_approaches_to_list_of_dicts(results,get_dict_for_json_mapping(),approach_vars())
    with open(filename,'w') as file:
        json.dump(resultlist,file)
    return