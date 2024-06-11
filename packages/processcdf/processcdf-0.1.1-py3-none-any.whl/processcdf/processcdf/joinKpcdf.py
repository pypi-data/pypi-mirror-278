import numpy as np
import pandas as pd
import argparse


def _read_kps_hdf(filename):
    df = pd.read_hdf(filename, 'df')
    return df


def _read_cdf_hdf(filename):
    df = pd.read_hdf(filename, 'df')
    return df


def _join_dfs(filename_kps, filename_cdfs):
    df_kps = _read_kps_hdf(filename_kps)
    df_cdfs = _read_cdf_hdf(filename_cdfs)

    df = pd.merge(df_kps, df_cdfs, how='inner', on=['year', 'month', 'day', 'hour'])

    return df


def _save2hdf(filename_kps, filename_cdfs, filename):
    df = _join_dfs(filename_kps, filename_cdfs)
    df.to_hdf(filename, key='df', mode='w')



def join2hdf():
    parser = argparse.ArgumentParser(
        description='Combining files with kp index data and CDF data into one new HDF file.')
    parser.add_argument('filename_kps', type=str, help='The filename with kp index values')
    parser.add_argument('filename_cdfs', type=str, help='The filename with the CDF files data')
    parser.add_argument('out_filename', type=str, help='The name of the HDF file to record the DataFrame')
    args = parser.parse_args()

    filename_kps = args.filename_kps
    filename_cdfs = args.filename_cdfs
    out_filename = args.out_filename

    _save2hdf(filename_kps, filename_cdfs, out_filename)
