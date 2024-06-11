import numpy as np
import pandas as pd
import json
import argparse


def process_kp_json(kp_filename):
    with open(kp_filename) as json_file:
        kp_data = json.load(json_file)

    pd_datetime = pd.to_datetime(kp_data['datetime']).tz_localize(None)
    np_kp = np.array(kp_data['Kp'])
    df_kps = pd.DataFrame(data={'datetime': pd_datetime, 'Kp': np_kp})

    df_kps['kp_bin_no'] = (df_kps['Kp'] * 3).round(0).astype(int)
    df_kps['year'] = pd.DatetimeIndex(df_kps['datetime']).year
    df_kps['month'] = pd.DatetimeIndex(df_kps['datetime']).month
    df_kps['day'] = pd.DatetimeIndex(df_kps['datetime']).day
    df_kps['hour'] = pd.DatetimeIndex(df_kps['datetime']).hour

    return df_kps


def json2hdf(kp_filename, out_filename):
    df = process_kp_json(kp_filename)
    df = df.set_index('datetime')
    df.to_hdf(out_filename, key='df', mode='w')


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Converting kp-index data from JSON to CSV file with DataFrame')
    parser.add_argument('in_filename', type=str, help='The name of the JSON file to read')
    parser.add_argument('out_filename', type=str, help='The name of the CSV file to record the DataFrame')
    args = parser.parse_args()
    
    kp_filename = args.in_filename
    out_filename = args.out_filename

    json2hdf(kp_filename, out_filename)
