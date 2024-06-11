import numpy as np
import pandas as pd
import cdflib
import functools
import os, time
import argparse
import logging


H_MLAT = 2
H_KP = 1/3


def _get_round_hours(df):
    lst_h3step = []

    for epoch_hour in df['hour']:
        for hour in range(3, 25, 3):
            if epoch_hour < hour:
                if hour == 24:
                    lst_h3step.append(21)
                    break
                else:
                    lst_h3step.append(hour - 3)
                    break

    df['hour_3step'] = lst_h3step

    return df


@functools.cache
def _gen_lst_for_lat():
    mlats = [-90 + H_MLAT*i for i in range(91)]
    return mlats


def _get_lst_bin_mlat(series_mlat):
    mlats = _gen_lst_for_lat()

    lst_lat = []
    # получение списка бинов mlat
    for lat in series_mlat:
        for i in range(len(mlats)):
            if lat < mlats[i]:
                lst_lat.append(i - 1)
                break
            if lat == mlats[-1] and i == len(mlats) - 1:
                lst_lat.append(i - 1)
                break
    return lst_lat


def _read_cdf(dir, cdf_filename):
    cdf_file = cdflib.CDF(dir + '/' + cdf_filename)

    epochs = cdf_file.varget('Epoch')
    ltime = cdf_file.varget('SC_AACGM_LTIME')
    mlat = cdf_file.varget('SC_AACGM_LAT')

    df = pd.DataFrame()
    df['MLT'] = ltime
    df['MLAT'] = mlat
    df['mlt_bin_no'] = (df['MLT'] * 60 // 15).astype(int)

    lst_mlat = _get_lst_bin_mlat(df['MLAT'])
    series_mlat = pd.Series(lst_mlat)
    df = df.merge(series_mlat.rename('mlat_bin_no'), left_index=True, right_index=True)

    df['datetime'] = cdflib.cdfepoch.to_datetime(epochs)
    df['year'] = pd.DatetimeIndex(df['datetime']).year
    df['month'] = pd.DatetimeIndex(df['datetime']).month
    df['day'] = pd.DatetimeIndex(df['datetime']).day
    df['hour'] = pd.DatetimeIndex(df['datetime']).hour

    lst_for_ordering = ['datetime', 'MLT', 'mlt_bin_no', 'MLAT', 'mlat_bin_no', 'year', 'month', 'day', 'hour']
    df = df[lst_for_ordering]

    return df


def _merge_cdfs(dir):
    df = pd.DataFrame()

    for file in os.listdir(dir):
        new_df = _read_cdf(dir, file)
        df = pd.concat([df, new_df])
        logging.info(f'File "{file}" added to DataFrame')

    logging.info(f'All CDF files are merged')

    return df


def _save2hdf(dir, filename):
    df = _merge_cdfs(dir)
    df.to_hdf(filename, key='df', mode='w')
    logging.info(f'DataFrame saved to HDF!')


def merge_cdf():
    logging.basicConfig(level=logging.INFO, filename='mergecdf2hdf.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s')
    start = time.time()

    parser = argparse.ArgumentParser(description='Combining several CDF files from a directory into one DataFrame, saving the result in HDF')
    parser.add_argument('input_dir', type=str, help='A directory with CDF files to merge')
    parser.add_argument('out_filename', type=str, help='The name of the HDF file to record the DataFrame')
    args = parser.parse_args()

    dir = args.input_dir
    out_filename = args.out_filename
    _save2hdf(dir, out_filename)
    end = time.time()

    print((end - start)/60, 'min')
